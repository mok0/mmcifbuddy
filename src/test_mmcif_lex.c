/*#include "mmcifparser.c"*/
#include <stdio.h>

int mmcif_get_token();
char *mmcif_get_string(void);
void mmcif_set_file(FILE *fp);


int main(void)
{
  int flag=1;
  char *return_type_name[] = {"ZERO","tNAME","tLOOP","tDATA","tSEMICOLON",
                            "tDOUBLE_QUOTE", "tSINGLE_QUOTE","tVALUE",
                            "tDATALINE_BEGIN", "tDATALINE", "tEND", "tCOMMENT"};



  mmcif_set_file(stdin);

  while(flag) {
    flag = mmcif_get_token();
    if(!flag) {
      return 0;
    }
    printf("%d %s ", flag, return_type_name[flag]);
    printf("%s\n", mmcif_get_string());
  }
  return 1;
}
