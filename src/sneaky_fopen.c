#include <stdio.h>
#include <zlib.h>

/*
  Use gzopen from zlib but masquerade as an ordinary
  stdio *FiLE pointer structure.
*/

FILE *sneaky_fopen(const char *path, const char *mode)
{
  gzFile zfp;

  /* try gzopen */
  zfp = gzopen(path, mode);
  if (zfp == NULL) {
    return NULL;
  }
  /* open file pointer */
  return funopen(zfp,
                 (int(*)(void*, char*,int))gzread,
                 (int(*)(void*,const char*,int))gzwrite,
                 (fpos_t(*)(void*,fpos_t,int))gzseek,
                 (int(*)(void*))gzclose);

}
