/*#include "mmcifparser.c"*/
#include <stdio.h>

int mmcif_get_token();
char *mmcif_get_string(void);
void mmcif_set_file(FILE *fp);


int main()
{
  int flag=1;

  mmcif_set_file(stdin);

  while(flag)
    {
      flag = mmcif_get_token();
      if(!flag)
	{
	  return 0;
	}
      printf("%d ", flag);
      printf("%s\n", mmcif_get_string());
    }
    return 1;
}
