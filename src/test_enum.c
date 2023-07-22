#include <stdio.h>
#include "mmciflexer.h"

int main() {

  printf("tNAME = %d\n",(int) tNAME);
  printf("tLOOP = %d\n",(int) tLOOP);
  printf("tDATA = %d\n",(int) tDATA);
  printf("tSEMICOLON = %d\n",(int) tSEMICOLON);
  printf("tDOULBE_QUOTE = %d\n",(int) tDOUBLE_QUOTE);
  printf("tSINGLE_QUOTE = %d\n",(int) tSINGLE_QUOTE);
  printf("tVALUE = %d\n",(int) tVALUE);
  printf("tDATALINE_BEGIN = %d\n",(int) tDATALINE_BEGIN);
  printf("tDATALINE = %d\n",(int) tDATALINE);
  printf("tEND = %d\n",(int) tEND);
  printf("tHASH = %d\n",(int) tHASH);

}
