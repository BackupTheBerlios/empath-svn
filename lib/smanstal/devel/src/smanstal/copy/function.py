# Module: smanstal.copy.function
# File: function.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from types import FunctionType as function, MethodType as method

__all__ = ('copyfunction', 'copymethod')

# ===================================================
# copyfunction
# ===================================================
def copyfunction(func, name = None):
    if isinstance(func, function) or isinstance(func, method):
        if not name:
            name = func.func_name
        tempfunc = function(func.func_code, func.func_globals, name, func.func_defaults, func.func_closure)
        tempfunc.func_doc = None
        return tempfunc
    names = tuple(o.__class__.__name__ for o in (func, name))
    raise TypeError("Cannot copy function = %s with name = %s" %names)
# ===================================================
# copymethod
# ===================================================
def copymethod(meth, name = None):
    if isinstance(meth, method):
        if not name:
            name = meth.func_name
        tempmeth = copyfunction(meth, name)
        return method(tempmeth, None)
    names = tuple(o.__class__.__name__ for o in (meth, name))
    raise TypeError("Cannot copy method = %s with name = %s" %names)
