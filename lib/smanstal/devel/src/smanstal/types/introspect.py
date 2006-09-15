# Module: smanstal.types.introspect
# File: introspect.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from types import (FunctionType as function, BuiltinFunctionType as bfunction, 
        MethodType as method, BuiltinMethodType as bmethod, ModuleType, ClassType)
import inspect as i
import os.path as op

__all__ = ('ismodule', 'isfilemodule', 'ispackage', 'isfunction', 'ismethod', 'ismetaclass', 
            'isclass', 'isbaseobject', 'isimmutable', 'iscallable')

def isproperty(obj): #{{{
    return isinstance(obj, property)
# End def #}}}

def ismodule(obj): #{{{
    return isinstance(obj, ModuleType)
# End def #}}}
   
def isfilemodule(obj): #{{{
    try:
        assert ismodule(obj)
        assert op.isfile(getattr(obj, '__file__', ''))
    except AssertionError:
        return False
    return True
# End def #}}}

def ispackage(obj): #{{{
    try:
        assert isfilemodule(obj)
        assert hasattr(obj, '__path__')
    except AssertionError:
        return False
    return True
# End def #}}}

def isfunction(obj): #{{{
   return isinstance(obj, function) or isinstance(obj, bfunction)
# End def #}}}

def ismethod(obj): #{{{
   return isinstance(obj, method) or isinstance(obj, bmethod)
# End def #}}}

def ismetaclass(obj): #{{{
    return isclass(obj) and issubclass(obj, type)
# End def #}}}

def isclass(obj): #{{{
    return isinstance(obj, ClassType) or hasattr(obj, '__bases__')
# End def #}}}

def isbaseobject(obj): #{{{
    return (obj is object or obj is type)
# End def #}}}

def isimmutable(obj): #{{{
    try:
        hash(obj)
    except TypeError, err:
        if str(err).find('unhashable') >= 0:
            return False
    else:
        return True
# End def #}}}

def iscallable(obj): #{{{
    return hasattr(obj, '__call__')
# End def #}}}
