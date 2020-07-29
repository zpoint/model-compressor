/* check your system path, sometimes it's <Python.h> */
#if defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)
    #include <Python.h>
#elif __APPLE__
    #include <Python/Python.h>
#else
    #include <Python.h>
#endif

#define PY_SSIZE_T_CLEAN
#include "compressor.hpp"

static PyMethodDef MyMethods[] = {
    {"compress_boolean", compress_boolean, METH_VARARGS, "compress boolean value"},
    {"compress_unicode", compress_unicode, METH_VARARGS, "compress boolean value"},
    {"compress_integer", compress_integer, METH_VARARGS, "compress boolean value"},
    {"compress_datetime", compress_datetime, METH_VARARGS, "compress boolean value"},
    {"compress_uuid", compress_uuid, METH_VARARGS, "compress boolean value"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initmodel_compressor(void)
{
    PyObject *m;

    m = Py_InitModule("model_compressor", MyMethods);
    if (m == NULL)
        return;
}
