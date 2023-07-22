/*
  $Id: MMCIFlexer.c,v 1.2 2000/08/17 23:14:18 mok Exp $
*/
#include "mmciflexer.h" // use token defs from here
#include <Python.h>

int mmcif_get_token();
char *mmcif_get_string(void);
void mmcif_set_file(FILE *fp);

FILE *fp;

static PyObject *MMCIFlexer_open_file(PyObject *self, PyObject *args)
{
  
  PyObject *file = NULL;

 /*   To pass a Python file object instead of a file name use this */
  if (!PyArg_ParseTuple(args, "O", &file)) {
        return NULL;
  }

  int fd =  PyObject_AsFileDescriptor(file);
  if (fd < 0) {
    return NULL;
  }

  fp = fdopen(fd, "r");
  mmcif_set_file(fp);

  return Py_None;
}


static PyObject *MMCIFlexer_close_file(PyObject *self)
{
  fclose(fp);
  return Py_None;
}


static PyObject *MMCIFlexer_get_token(PyObject *self)
{
  int flag;
  char *value="";

  /* get token number */
  flag = mmcif_get_token();

  /* if flag==0 we are EOF */
  if(flag) {
    value = mmcif_get_string();
  }

  /* return the (tokennumber, string) tuple */
  return Py_BuildValue("(is)", flag, value);
}

/*
  The PyMethodDef struct holds information about the methods in the
  module.
*/
static PyMethodDef MMCIFMethods[]=
  {
    {"open_file", MMCIFlexer_open_file, METH_VARARGS, "Open mmCIF file for reading"},
    {"close_file", (PyCFunction)MMCIFlexer_close_file, METH_NOARGS, "Close mmCIF file"},
    {"get_token", (PyCFunction)MMCIFlexer_get_token, METH_NOARGS, "Get next token from mmCIF file"},
    {NULL, NULL, 0, NULL}  /* Sentinel */
  };


/* PyModuleDef struct holds information about your module itself. It
   is not an array of structures, but rather a single structure that’s
   used for module definition:
*/
static struct PyModuleDef _mmciflexermodule = {
  PyModuleDef_HEAD_INIT,
  "_mmciflexer",
  "Python module to read tokens from an mmCIF file",
  -1,
  MMCIFMethods
};

/*
  When a Python program imports your module for the first time, it
  will call PyInit_mmciflexer():
*/
PyMODINIT_FUNC PyInit__mmciflexer()
{
  PyObject *module = PyModule_Create(&_mmciflexermodule);

  /* Add int constant by name */
  PyModule_AddIntConstant(module, "tNAME", tNAME);
  PyModule_AddIntConstant(module, "tLOOP", tLOOP);
  PyModule_AddIntConstant(module, "tDATA", tDATA);
  PyModule_AddIntConstant(module, "tSEMICOLON", tSEMICOLON );
  PyModule_AddIntConstant(module, "tDOUBLE_QUOTE", tDOUBLE_QUOTE);
  PyModule_AddIntConstant(module, "tSINGLE_QUOTE", tSINGLE_QUOTE);
  PyModule_AddIntConstant(module, "tVALUE", tVALUE);
  PyModule_AddIntConstant(module, "tDATALINE_BEGIN", tDATALINE_BEGIN);
  PyModule_AddIntConstant(module, "tDATALINE", tDATALINE);
  PyModule_AddIntConstant(module, "tEND", tEND);
  PyModule_AddIntConstant(module, "tCOMMENT", tCOMMENT);

  return module;
}
