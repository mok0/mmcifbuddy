#define WANT_RETURN_TYPES
#include "mmciflexer.h"
#include <stdio.h>

char *return_type_name[] = {"tEND_OF_FILE","tNAME","tLOOP", "tLOOP_END", 
                            "tID","tSEMICOLON", "tDOUBLE_QUOTE", "tSINGLE_QUOTE", "tDATA",
                            "tDATALINE_BEGIN", "tDATALINE", "tDATALINE_END", "tCOMMENT",
                            "tINT", "tFLOAT"};

int mmcif_get_token();
char *mmcif_get_string(void);
void mmcif_set_file(FILE *fp);


int main(void)
{
  int flag=1;
 
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
