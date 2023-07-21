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
  char *filename;

  if (!PyArg_ParseTuple(args, "s", &filename))
    return NULL;
  fp = fopen(filename, "r");
  mmcif_set_file(fp);
  //Py_INCREF(Py_None);

   /* return the fp integer */
  return Py_BuildValue("i", fp);

  //return Py_None;
}


static PyObject *MMCIFlexer_close_file(PyObject *self, PyObject *args)
{
  /* verify no arguments */
  if (!PyArg_ParseTuple(args, ""))
    return NULL;
  fclose(fp);
  //	Py_INCREF(Py_None);
  return Py_None;
}


static PyObject *MMCIFlexer_get_token(PyObject *self, PyObject *args)
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
    {"close_file", MMCIFlexer_close_file, METH_VARARGS, "Close mmCIF file"},
    {"get_token", MMCIFlexer_get_token, METH_VARARGS, "Get token from mmCIF file"},
    {NULL, NULL, 0, NULL}  /* Sentinel */
  };


/* PyModuleDef struct holds information about your module itself. It
   is not an array of structures, but rather a single structure that’s
   used for module definition:
*/
static struct PyModuleDef mmciflexermodule = {
  PyModuleDef_HEAD_INIT,
  "mmciflexer",
  "Python module to read tokens from an mmCIF file",
  -1,
  MMCIFMethods
};

/*
  When a Python program imports your module for the first time, it
  will call PyInit_mmciflexer():
*/
PyMODINIT_FUNC PyInit_mmciflexer()
{
  PyObject *module = PyModule_Create(&mmciflexermodule);

  /* Add int constant by name */
  PyModule_AddIntConstant(module, "NAME", tNAME);
  PyModule_AddIntConstant(module, "LOOP", tLOOP);
  PyModule_AddIntConstant(module, "DATA", tDATA);
  PyModule_AddIntConstant(module, "SEMICOLON", tSEMICOLON );
  PyModule_AddIntConstant(module, "DOUBLE_QUOTE", tDOUBLE_QUOTE);
  PyModule_AddIntConstant(module, "SINGLE_QUOTE", tSINGLE_QUOTE);
  PyModule_AddIntConstant(module, "VALUE", tVALUE);
  PyModule_AddIntConstant(module, "DATALINE", tDATALINE);
  PyModule_AddIntConstant(module, "COMMENT", tHASH);

  return module;
}
