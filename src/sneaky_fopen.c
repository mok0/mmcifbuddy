#ifdef __linux
#define _GNU_SOURCE  /* Needed for fopencookie */
#endif

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

  /* Open file pointer, depending on implementation use
     different functions for macOS or Linux
   */

#ifdef __APPLE__
  /* funopen is only found on OpenBSD */
  return funopen(zfp,
                 (int(*)(void*, char*,int))gzread,
                 (int(*)(void*,const char*,int))gzwrite,
                 (fpos_t(*)(void*,fpos_t,int))gzseek,
                 (int(*)(void*))gzclose);
#else
  /* On Linux systems use fopencookie instead  */
  cookie_io_functions_t io;
  io.read = ( cookie_read_function_t *)gzread;
  io.write = (cookie_write_function_t *)gzwrite;
  io.seek = (cookie_seek_function_t *)gzseek;
  io.close = (cookie_close_function_t *)gzclose;
  return fopencookie(zfp, "r", io); // we only need to read
#endif

}
