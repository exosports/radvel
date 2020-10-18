# cimport the Cython declarations for numpy
from __future__ import absolute_import
cimport numpy as np
import numpy as np
import cython

# if you want to use the Numpy-C-API from Cython
# (not strictly necessary for this example, but good practice)
np.import_array()

cdef extern from "ecltr.c":
    double mandeltr(double t, double tc, double rprs, double inc,
                    double ars, double p, double flux)
    double mandelecl(double t, double te, double frat, double inc,
                     double ars, double p, double rprs, double flux)

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
def mandeltr_array(np.ndarray[DTYPE_t, ndim=1] t, double per, double tc,
                   double e, double om, double k, double flux, double ars,
		   double rprs, double inc):
    cdef int size, i
    size = t.shape[0]

    cdef np.ndarray[DTYPE_t, ndim=1] y = t.copy()
    for i in range(size):
        y[i] = mandeltr(t[i], tc, rprs, inc, ars, per, flux)

    return y

@cython.boundscheck(False)
def mandelecl_array(np.ndarray[DTYPE_t, ndim=1] t, double per, double te,
                    double e, double om, double k, double flux, double ars,
		    double rprs, double inc, double frat):
    cdef int size, i
    size = t.shape[0]

    cdef np.ndarray[DTYPE_t, ndim=1] y = t.copy()
    for i in range(size):
        y[i] = mandelecl(t[i], te, frat, inc, ars, per, rprs, flux)

    return y

