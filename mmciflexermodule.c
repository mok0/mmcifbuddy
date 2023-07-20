/*
  $Id: MMCIFlex.c,v 1.2 2000/08/17 23:14:18 mok Exp $
*/

#include <Python.h>

int mmcif_get_token();
char *mmcif_get_string(void);
void mmcif_set_file(FILE *fp);


FILE *fp;

static PyObject *MMCIFlex_open_file(PyObject *self, PyObject *args)
{
	char *filename;

	if (!PyArg_ParseTuple(args, "s", &filename))
		return NULL;
	fp = fopen(filename, "r");
	mmcif_set_file(fp);
	//Py_INCREF(Py_None);
	return Py_None;
}


static PyObject *MMCIFlex_close_file(PyObject *self, PyObject *args)
{
	/* verify no arguments */
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	fclose(fp);
        //	Py_INCREF(Py_None);
	return Py_None;
}


static PyObject *MMCIFlex_get_token(PyObject *self, PyObject *args)
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
    {"open_file", MMCIFlex_open_file, METH_VARARGS, "Open mmCIF file for reading"},
    {"close_file", MMCIFlex_close_file, METH_VARARGS, "Close mmCIF file"},
    {"get_token", MMCIFlex_get_token, METH_VARARGS, "Get token from mmCIF file"},
    {NULL, NULL, 0, NULL}  /* Sentinel */
  };


/* PyModuleDef struct holds information about your module itself. It
   is not an array of structures, but rather a single structure that’s
   used for module definition:
*/
static struct PyModuleDef mmciflexmodule = {
  PyModuleDef_HEAD_INIT,
  "mmciflex",
  "Python module to read tokens from an mmCIF file",
  -1,
  MMCIFMethods
};

/*
  When a Python program imports your module for the first time, it
  will call PyInit_mmciflex():
*/
PyMODINIT_FUNC PyInit_mmciflex()
{
  PyObject *module = PyModule_Create(&mmciflexmodule);

  /* Add int constant by name */
  PyModule_AddIntConstant(module, "NAME", 1);
  PyModule_AddIntConstant(module, "LOOP", 2);
  PyModule_AddIntConstant(module, "DATA", 3);
  PyModule_AddIntConstant(module, "SEMICOLONS", 4);
  PyModule_AddIntConstant(module, "DOUBLEQUOTED", 5);
  PyModule_AddIntConstant(module, "QUOTED", 6);
  PyModule_AddIntConstant(module, "SIMPLE", 7);

  return module;
}
