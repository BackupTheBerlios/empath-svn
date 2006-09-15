# Module: smanstal.copy.function
# File: function.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from types import FunctionType as function, MethodType as method
from aossi.deco import signal_settings
from validate.base import valTrue
from validate.type import vt

__all__ = ('copyfunction', 'copymethod')

# ===================================================
# copyfunction
# ===================================================
@signal_settings(policy='first')
def copyfunction(func, name = None):
    names = tuple(o.__class__.__name__ for o in (func, name))
    raise TypeError("Cannot copy function = %s with name = %s" %names)
   
@copyfunction.match_value(vt(function, method), None)
def _cf_noname(func, name = None):
   return copyfunction(func, func.func_name)
   
@copyfunction.match_type(vt(function, method), basestring)
def _cf_docopy(func, name = None):
   tempfunc = function(func.func_code, func.func_globals, name, func.func_defaults, func.func_closure)
   tempfunc.func_doc = None
   return tempfunc
   
# ===================================================
# copymethod
# ===================================================
@signal_settings(policy='first')
def copymethod(meth, name = None):
    names = tuple(o.__class__.__name__ for o in (meth, name))
    raise TypeError("Cannot copy method = %s with name = %s" %names)
   
@copymethod.match_value(vt(method), None)
def _cm_noname(meth, name = None):
   return copymethod(meth, meth.func_name)

@copymethod.match_type(method, basestring)
def _cm_docopy(meth, name = None):
   tempmeth = copyfunction(meth, name)
   return method(tempmeth, None)
