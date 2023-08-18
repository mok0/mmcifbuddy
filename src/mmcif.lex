/* -*- mode: text -*- */
%{
    /* Copyright (C) 2023 Morten Kjeldgaard */

#ifdef __APPLE__
/* Disable certain compiler warnings that come from the lex generated code */
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunreachable-code"
#pragma GCC diagnostic ignored "-Wsign-compare"
#pragma GCC diagnostic ignored "-Wunneeded-internal-declaration"
#endif

#include <ctype.h>
#include <string.h>
#include "mmciflexer.h"
char *shoveleft (char *str);
int strtrim (char *str, int length);

static int in_loop, in_save;

%}

%option never-interactive
%option prefix="mmcif"
%option noyywrap
%option nounput
%option yylineno

%x sSEMICOLON

comment			#.*\n
save_item               save__[^ \t\n]+
save_category           save_{1}([^_ \t\n]){1}[^ \t\n]+
save_                   ^save_
loop			^[:blank:]*loop_
ident			^[Dd][Aa][Tt][Aa]_[^ \t\n]+
name			_[^ \t\n]+
integer                 -?[0-9]+
float                   -?(([0-9]+)|([0-9]*\.[0-9]+)([eE][-+]?[0-9]+)?)
word           		[^ \t\n]+
single_quote            '[^'\n]*'
double_quote            \"[^"\n]*\"
semicolon		^;(.*\n)

%%

{ident}             {
                        in_loop = 0; in_save = 0;
                        return tID;  /* data_<pdbid> at start of file */
                    }

{comment}           {
                        strtrim(yytext, yyleng); /* strip trailing whitespace */
                        if(in_loop) {
                            /* uncertain if loop_ is always terminated by comment? */
                            in_loop = 0;
                            return tLOOP_END;
                        } else {
                        return tCOMMENT;
                        }
                    }

{name}              {
                        if(in_loop == 1)
                            {in_loop = 2;};  /* signal that name is found inside loop */
                        return tNAME;       /* e.g. _entity.id */
                    }

{loop}              {
                        in_loop = 1;
                        return tLOOP;
                    }

{save_item}         { in_save = 2;  return tSAVE_ITEM;  /* save__{word}+ */ }
{save_category}     { in_save = 1; return tSAVE_CATEGORY;  }
{save_}             { in_save = 0; return tSAVE_END;  }

{semicolon}         {
                        BEGIN(sSEMICOLON);   /* Enter semicolon state */
                        yytext[0] = ' ';     /* There is a leading semicolon in the first string */
                        shoveleft(yytext);   /* get rid of it */
                        int n = strlen(yytext);
                        yytext[n-1] = '\0';
                        return tDATALINE_BEGIN;
                    }

<sSEMICOLON>;\n     {
                        BEGIN(INITIAL);
                        strtrim(yytext, yyleng);
                        return tDATALINE_END;
                    }


<sSEMICOLON>.*\n    {
                        strtrim(yytext, yyleng);
                        return tDATALINE;
                    }


{double_quote}      {
                            if (yytext[0] == '\"') {  /* get rid of double quote characters */
                                yytext[0] = ' ';
                                shoveleft(yytext);
                                yytext[yyleng-2] = '\0';
                            }
                            return tDOUBLE_QUOTE;
                    }

{single_quote}      {
                            if (yytext[0] == '\'') {  /* get rid of single quote characters */
                                yytext[0] = ' ';
                                shoveleft(yytext);
                                yytext[yyleng-2] = '\0';
                            }
                            return tSINGLE_QUOTE;
                    }

{integer}           { return tINT;      /* integer token, returned as a string */   }

{float}             { return tFLOAT;    /* floating point token, returned as a string */ }

{word}              { return tDATA;     /* string token value */ }

[ \t\n]+					     /* ignore whitespace */

<<EOF>>             { return 0; }

%%

/*
   Set the yyin FILE pointer to the file to be lexed
*/
void mmcif_set_file(FILE *fp)
{
    yyin=fp;
}


/*
   Advance to and return next token value
*/

int mmcif_get_token()
{
    return yylex();
}

/*
   Return latest token string.
*/
char *mmcif_get_string(void)
{
    return yytext;
}

/*
   Get the current line number, maintained by the lexer
*/
int mmcif_get_lineno(void)
{
    return yylineno;
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


/*
  s t r t r i m
  Trim spaces and junk off the end of a character string
  mk 950404, 2023-08-01
*/

int strtrim (char *str, int length) {
    register char *s;

    s = str + length - 1;
    while (isspace(*--s) && s > str)  /* trim spaces off end */
        ;
    *++s = '\0';
    return s-str; // return new length
}
