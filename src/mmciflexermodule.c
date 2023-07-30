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

  if (!PyArg_ParseTuple(args, "s", &filename)) {
      return NULL;
  }

  fp = fopen(filename, "r");
  if (!fp) {
     PyErr_SetString(PyExc_FileNotFoundError, "File not found");
    return NULL;
  }
  
  mmcif_set_file(fp);

  /* The value of the fp pointer is returned */
  return Py_BuildValue("i", fp);
}


static PyObject *MMCIFlexer_close_file(PyObject *self)
{
  int status = fclose(fp);
  /* Upon successful completion 0 is returned.  Otherwise, EOF is returned */
  return Py_BuildValue("i", status);
}


static PyObject *MMCIFlexer_get_token(PyObject *self)
{
  int flag;
  char *value="";
  int ii;
  double dd;

  /* get token number */
  flag = mmcif_get_token();

  /* if flag==0 we are EOF, if not get the string */
  if(flag) {
    value = mmcif_get_string();
  }
 
 /* Treat doublequote and singlequote items as normal data */
  if (flag == tDOUBLE_QUOTE || flag == tSINGLE_QUOTE) {
    flag = tDATA;
  }

  /* In this switch statement, we return (flag, value) tuples to caller */
  switch (flag)
  {
      case tINT:
        /* special case for tINT data types, return tDATA token */
        ii = strtol(value, NULL, 10);
        return Py_BuildValue("(il)", tDATA, ii);

      case tFLOAT:
      /* special case for tFLOAT data types, return tDATA token */  
        dd = strtod(value, NULL);
        return Py_BuildValue("(id)", tDATA, dd);
  
      default:
        /* all other data types are returned as string values  */
        return Py_BuildValue("(is)", flag, value);

  }

/* We never come here */

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
  PyModule_AddIntConstant(module, "tLOOP_END", tLOOP_END);
  PyModule_AddIntConstant(module, "tID", tID);
  PyModule_AddIntConstant(module, "tSEMICOLON", tSEMICOLON ); 
  /*
  PyModule_AddIntConstant(module, "tDOUBLE_QUOTE", tDOUBLE_QUOTE);
  PyModule_AddIntConstant(module, "tSINGLE_QUOTE", tSINGLE_QUOTE); 
  */
  PyModule_AddIntConstant(module, "tDATA", tDATA);
  PyModule_AddIntConstant(module, "tDATALINE_BEGIN", tDATALINE_BEGIN);
  PyModule_AddIntConstant(module, "tDATALINE", tDATALINE);
  PyModule_AddIntConstant(module, "tDATALINE_END", tDATALINE_END);
  PyModule_AddIntConstant(module, "tCOMMENT", tCOMMENT);

  return module;
}
