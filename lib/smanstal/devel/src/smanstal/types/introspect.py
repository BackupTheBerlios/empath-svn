# Module: smanstal.types.introspect
# File: introspect.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from types import (FunctionType as function, BuiltinFunctionType as bfunction, 
        MethodType as method, BuiltinMethodType as bmethod, ModuleType, ClassType,
        GeneratorType)
import inspect as i
import os.path as op
import re
_CompiledRegex = type(re.compile(''))

__all__ = ('ismodule', 'isfilemodule', 'ispackage', 'isfunction', 'isbfunction', 'ismethod',
            'isbmethod', 'isboundmethod', 'isunboundmethod', 'hasmagicname', 'ismagicname', 
            'ismetaclass', 'isclass', 'isobjclass', 'isobjinstance', 'isbaseobject', 
            'isimmutable', 'iscallable', 'isiterable', 'isgenerator', 'issequence', 'isindexable',
            'iscompiledregex', 'mro')

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

def isbfunction(obj): #{{{
    return isinstance(obj, bfunction)
# End def #}}}

def ismethod(obj): #{{{
   return isinstance(obj, method) or isinstance(obj, bmethod)
# End def #}}}

def isbmethod(obj): #{{{
   return isinstance(obj, bmethod)
# End def #}}}

def isboundmethod(obj): #{{{
    return ismethod(obj) and getattr(obj, 'im_self', None)
# End def #}}}

def isunboundmethod(obj): #{{{
    return ismethod(obj) and not getattr(obj, 'im_self', None)
# End def #}}}

def hasmagicname(obj): #{{{
    return ismagicname(getattr(obj, '__name__', ''))
# End def #}}}

def ismagicname(obj): #{{{
    return isinstance(obj, basestring) and obj.startswith('__') and obj.endswith('__')
# End def #}}}

def ismetaclass(obj): #{{{
    return isclass(obj) and issubclass(obj, type)
# End def #}}}

def isclass(obj): #{{{
    return isinstance(obj, ClassType) or hasattr(obj, '__bases__')
# End def #}}}

def isobjclass(obj): #{{{
    return isinstance(obj, object) and isinstance(obj, type) and isclass(obj)
# End def #}}}

def isobjinstance(objinst, objtype=None): #{{{
    if objtype:
        return isinstance(objinst, objtype)
    return not isobjclass(objinst)
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
    return isfunction(obj) or ismethod(obj) or isclass(obj) or hasattr(obj, '__call__')
# End def #}}}

def ismapping(obj): #{{{
    if isinstance(obj, dict):
        return True
    check = ('items', 'keys', 'values')
    check += tuple('iter' + c for c in check)
    check += ('__getitem__',)
    return False not in (iscallable(getattr(obj, n, None)) for n in check)
# End def #}}}

def isiterable(obj): #{{{
    return iscallable(getattr(obj, '__iter__', None))
# End def #}}}

def isgenerator(obj): #{{{
    return isiterable(obj) and isinstance(obj, GeneratorType)
# End def #}}}

def issequence(obj): #{{{
    return isiterable(obj) and iscallable(getattr(obj, '__getitem__', None))
# End def #}}}

isindexable = issequence

def iscompiledregex(obj): #{{{
    return isinstance(obj, _CompiledRegex)
# End def #}}}

def mro(cls): #{{{
    if isobjclass(cls):
        return cls.mro()
    def calc_mro(curcls): #{{{
        if curcls is cls:
            yield cls
        for b in curcls.__bases__:
            yield b
            for c in calc_mro(b):
                yield c
    # End def #}}}
    return [c for c in calc_mro(cls)]
# End def #}}}
