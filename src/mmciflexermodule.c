/*
  Copyright (C) 2023 Morten Kjeldgaard
*/
#include <stdio.h>  // For definition of (FILE *)
#include <stdlib.h> // neede for abs()
#include "mmciflexer.h" // use token defs from here
#include "version.h"
#include <Python.h>

FILE *sneaky_fopen(const char *path, const char *mode);
int mmcif_get_token();
char *mmcif_get_string(void);
void mmcif_set_file(FILE *fp);
int mmcif_get_lineno(void);

FILE *fp;
int close_file = 1;
int debug = 0;

/*
  lexer_open_with_filename(): This functions opens the named file in
  regular C fashion. The file can be straight text or gzip compressed.
*/
static PyObject *lexer_open_with_filename(PyObject *self, PyObject *args)
{
  char *filename;

  if (!PyArg_ParseTuple(args, "s", &filename)) {
    return NULL;
  }

  fp = sneaky_fopen(filename, "r");
  if (!fp) {
    PyErr_SetString(PyExc_FileNotFoundError, "File not found");
    return NULL;
  }
  close_file = 1; /* Close file in C, manually */
  mmcif_set_file(fp);

  /* The value of the fp pointer is returned */
  return Py_BuildValue("i", fp);
}


/*
  lexer_open_with_df(): Pass an open file object from Python to C
  extension code.
*/
static PyObject *lexer_open_with_fd(PyObject *self, PyObject *args)
{
  PyObject *fileobj = NULL;

  if (!PyArg_ParseTuple(args, "O", &fileobj)) {
    return NULL;
  }

  /* From an open Python file object, get the file descriptor */
  int fd = PyObject_AsFileDescriptor(fileobj);
  if (fd < 0) {
    return NULL;
  }

  FILE* fp = fdopen(fd, "r");   /* lex expects a file pointer structure */
  close_file = 0; /* this file is closed in Python */

  mmcif_set_file(fp);

  /* The value of the fp pointer is returned */
  return Py_BuildValue("i", fp);
}


/*
  lexer_close_file(): close a file that has been opened by
  lexer_open_with_filename().
*/
static PyObject *lexer_close_file(PyObject *self)
{
  int status;
  if (close_file) { /* if the file is opened in Python, skip this */
    status = fclose(fp);
  } else {
    status = 0;
  }

  /* Upon successful completion 0 is returned.  Otherwise, EOF is returned */
  return Py_BuildValue("i", status);
}


/*
  lexer_get_token(): Get the next token from the stream, as
  given by the flex function mmcif_get_token().
*/
static PyObject *lexer_get_token(PyObject *self)
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

  if (debug) {
    int lineno = mmcif_get_lineno();
    printf("[%d/%d] %s\n", lineno, flag, value);
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
  lexer_set_debug_mode(): sets the debug variable enabling
  debugging output.
*/
static PyObject *lexer_set_debug_mode(PyObject *self, PyObject *args)
{
  int value;

  if (!PyArg_ParseTuple(args, "i", &value)) {
    return NULL;
  }

  debug = abs(value);
  printf("Setting debug mode to %d\n", debug);
  return Py_BuildValue("i", value);
}


/*
  The PyMethodDef struct holds information about the methods in the
  module, this is the interface of the above functions with Python.
*/
static PyMethodDef MMCIFMethods[]=
  {
    {"fopen", lexer_open_with_filename, METH_VARARGS, "Open mmCIF file for reading"},
    {"open", lexer_open_with_fd, METH_VARARGS, "Pass an open Python file descriptor for reading to module"},
    {"set_debug_mode", lexer_set_debug_mode, METH_VARARGS, "Set debug mode on (1) or off (0)"},
    {"fclose", (PyCFunction)lexer_close_file, METH_NOARGS, "Close mmCIF file"},
    {"get_token", (PyCFunction)lexer_get_token, METH_NOARGS, "Get next token from mmCIF file"},
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

  /*
    Add lexer constants by name, some of these are never returned by
    parser but eaten in this module
  */
  PyModule_AddIntConstant(module, "tEND_OF_FILE", tEND_OF_FILE);
  PyModule_AddIntConstant(module, "tNAME", tNAME);
  PyModule_AddIntConstant(module, "tLOOP", tLOOP);
  PyModule_AddIntConstant(module, "tLOOP_END", tLOOP_END);
  PyModule_AddIntConstant(module, "tID", tID);
  PyModule_AddIntConstant(module, "tSEMICOLON", tSEMICOLON );
  PyModule_AddIntConstant(module, "tDOUBLE_QUOTE", tDOUBLE_QUOTE);
  PyModule_AddIntConstant(module, "tSINGLE_QUOTE", tSINGLE_QUOTE);
  PyModule_AddIntConstant(module, "tDATA", tDATA);
  PyModule_AddIntConstant(module, "tDATALINE_BEGIN", tDATALINE_BEGIN);
  PyModule_AddIntConstant(module, "tDATALINE", tDATALINE);
  PyModule_AddIntConstant(module, "tDATALINE_END", tDATALINE_END);
  PyModule_AddIntConstant(module, "tCOMMENT", tCOMMENT);
  PyModule_AddIntConstant(module, "tINT", tINT);
  PyModule_AddIntConstant(module, "tFLOAT", tFLOAT);
  PyModule_AddIntConstant(module, "tSAVE_CATEGORY", tSAVE_CATEGORY);
  PyModule_AddIntConstant(module, "tSAVE_ITEM", tSAVE_ITEM);
  PyModule_AddIntConstant(module, "tSAVE_END", tSAVE_END);

  /* These compile time constants are from version.h (autogenerated) */
#ifdef GIT_COMMIT
  PyModule_AddObjectRef(module, "GIT_COMMIT", PyUnicode_FromString(GIT_COMMIT));
#endif
#ifdef GIT_BRANCH
  PyModule_AddObjectRef(module, "GIT_BRANCH", PyUnicode_FromString(GIT_BRANCH));
#endif
#ifdef COMPILE_TIME
  PyModule_AddObjectRef(module, "COMPILE_TIME", PyUnicode_FromString(COMPILE_TIME));
#endif
#ifdef VERSION
  PyModule_AddObjectRef(module, "VERSION", PyUnicode_FromString(VERSION));
#endif

  /* Add a list of token type names */
  PyObject* names = PyTuple_New(18);
  PyTuple_SetItem(names, (Py_ssize_t)tEND_OF_FILE, PyUnicode_FromString("tEND_OF_FILE"));
  PyTuple_SetItem(names, (Py_ssize_t)tNAME, PyUnicode_FromString("tNAME"));
  PyTuple_SetItem(names, (Py_ssize_t)tLOOP, PyUnicode_FromString("tLOOP"));
  PyTuple_SetItem(names, (Py_ssize_t)tLOOP_END, PyUnicode_FromString("tLOOP_END"));
  PyTuple_SetItem(names, (Py_ssize_t)tID, PyUnicode_FromString("tID"));
  PyTuple_SetItem(names, (Py_ssize_t)tSEMICOLON, PyUnicode_FromString("tSEMICOLON"));
  PyTuple_SetItem(names, (Py_ssize_t)tDOUBLE_QUOTE, PyUnicode_FromString("tDOUBLE_QUOTE"));
  PyTuple_SetItem(names, (Py_ssize_t)tSINGLE_QUOTE, PyUnicode_FromString("tSINGLE_QUOTE"));
  PyTuple_SetItem(names, (Py_ssize_t)tDATA, PyUnicode_FromString("tDATA"));
  PyTuple_SetItem(names, (Py_ssize_t)tDATALINE_BEGIN, PyUnicode_FromString("tDATALINE_BEGIN"));
  PyTuple_SetItem(names, (Py_ssize_t)tDATALINE, PyUnicode_FromString("tDATALINE"));
  PyTuple_SetItem(names, (Py_ssize_t)tDATALINE_END, PyUnicode_FromString("tDATALINE_END"));
  PyTuple_SetItem(names, (Py_ssize_t)tCOMMENT, PyUnicode_FromString("tCOMMENT"));
  PyTuple_SetItem(names, (Py_ssize_t)tINT, PyUnicode_FromString("tINT"));
  PyTuple_SetItem(names, (Py_ssize_t)tFLOAT, PyUnicode_FromString("tFLOAT"));
  PyTuple_SetItem(names, (Py_ssize_t)tSAVE_CATEGORY, PyUnicode_FromString("tSAVE_CATEGORY"));
  PyTuple_SetItem(names, (Py_ssize_t)tSAVE_ITEM, PyUnicode_FromString("tSAVE_ITEM"));
  PyTuple_SetItem(names, (Py_ssize_t)tSAVE_END, PyUnicode_FromString("tSAVE_END"));

  PyModule_AddObjectRef(module, "token_type_names", names);
  Py_DECREF(names);

  return module;
}
