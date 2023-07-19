/*
  $Id: mmcif.lex,v 1.2 2000/08/17 23:14:20 mok Exp $
*/

%{
#include <string.h>

  char *shoveleft (char *str);
%}

%option noyywrap
%option nounput

comment			#.*\n
name			_[^ \t\n]+
loop			[Ll][Oo][Oo][Pp]_
data			[Dd][Aa][Tt][Aa]_[^ \t\n]+
free_value		[^ \t\n]+
single_quote_value	'[^'\n]*'
double_quote_value	\"[^"\n]*\"
semicolon_value		^;(.*\n[^;])*.*\n;

%%

{comment}					/* ignore */

{name} { return 1; }        /* _entity.id) */

{loop} { return 2; }        /* _loop */

{data} { return 3;}         /* data_<pdbid> at start of file */

{semicolon_value} { return 4; } /* eg. ;value\n;	 */

{double_quote_value} {
    if (yytext[0] == '\"') {  /* "value" */
        yytext[0] = ' ';
        shoveleft(yytext);
        int n = strlen(yytext);
        yytext[n-1] = '\0';
        }
    return 5;
}

{single_quote_value} {   /* 'value' */
if (yytext[0] == '\'') {
    yytext[0] = ' ';
    shoveleft(yytext);
    int n = strlen(yytext);
    yytext[n-1] = '\0';
    }
    return 6;
}

{free_value} { return 7; }  /* value */

[ \t\n]+					/* ignore */

%%


void mmcif_set_file(FILE *fp)
{
    yyin=fp;
}

int mmcif_get_token()
{
    return yylex();
}

char *mmcif_get_string(void)
{
    return yytext;
}

/*
   s h o v e l e f t
   Shove a string to the left.
   mok 2021-08-23.
*/
char *shoveleft (char *str)
{
  register char *t, *s;

  s = str;
  if (*s < 33) {
    t = s;
    while (*t) {
      *t = *(t+1);
      t++;
    }
  }
  else {
    s++;
  }
  return str;
}
