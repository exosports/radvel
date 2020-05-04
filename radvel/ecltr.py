import numpy as np
import radvel

# Try to import Ecl/Tr C functions
try:
    from . import _ecltr
    cext = True
except ImportError:
    print("WARNING: ECLTR: Unable to import C-based analytic\
           eclipse and transit light curve functions. Falling back\
           to slower Python implementation.")
    cext = False

def mandeltr(t, orbel, flux, ars, rprs, inc, use_c_funcs=cext):
    """
    Args:
        t (array of floats): times of light-curve observations
        orbel (array of floats): [per, tp, e, om, K]
        use_c_funcs (bool): (default: True) If True use the C
            functions. Else, use the Python functions.
    Returns:
        y: (array of floats): light-curve model
    """

    # unpack parameters
    per, tp, e, om, k = orbel

    tc = radvel.orbit.timeperi_to_timetrans(tp, per, e, om)

    if use_c_funcs:
        y = _ecltr.mandeltr_array(t, per, tc, e, om, k, flux, ars, rprs, inc)
    else:
        print("Python mandeltr() not yet implemented.")

    return y

def mandelecl(t, orbel, flux, ars, rprs, inc, frat, use_c_funcs=cext):
    """
    Args:
        t (array of floats): times of light-curve observations
        orbel (array of floats): [per, tp, e, om, K]
        use_c_funcs (bool): (default: True) If True use the C
            functions. Else, use the Python functions.
    Returns:
        y: (array of floats): light-curve model
    """

    # unpack parameters
    per, tp, e, om, k = orbel

    te = radvel.orbit.timeperi_to_timetrans(tp, per, e, om, secondary=True)

    if use_c_funcs:
        y = _ecltr.mandelecl_array(t, per, te, e, om, k, flux, ars, rprs, inc,
                                   frat)
    else:
        print("Python mandelecl() not yet implemented.")

    return y    
