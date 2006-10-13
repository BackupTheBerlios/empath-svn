# Module: smanstal.types.introspect
# File: introspect.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import __builtin__
from types import (FunctionType as function, BuiltinFunctionType as bfunction, 
        MethodType as method, BuiltinMethodType as bmethod, ModuleType, ClassType,
        GeneratorType)
from weakref import ref
import inspect as i
import os.path as op
import re
_CompiledRegex = type(re.compile(''))

__all__ = ('ismodule', 'isfilemodule', 'ispackage', 'isfunction', 'isbfunction', 'ismethod',
            'isclassmethod', 'isbmethod', 'isboundmethod', 'isunboundmethod', 'hasmagicname', 
            'ismagicname', 'instanceclsname', 'ismetaclass', 'isclass', 'isobjclass', 'isobjinstance', 
            'isbaseobject', 'isimmutable', 'ishashable', 'iscallable', 'isiterable', 'isgenerator', 
            'issequence', 'isindexable', 'iscompiledregex', 'mro', 'isbasemetaclass', 'canweakref',
            'isbuiltin', 'numeric_methods')

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
   return isinstance(obj, function)
# End def #}}}

def isbfunction(obj): #{{{
    return isinstance(obj, bfunction)
# End def #}}}

def ismethod(obj): #{{{
   return isinstance(obj, method)
# End def #}}}

def isclassmethod(obj): #{{{
    return ismethod(obj) and isclass(getattr(obj, 'im_self', None))
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

def instanceclsname(obj): #{{{
    return obj.__class__.__name__
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

ishashable = isimmutable

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

def isbasemetaclass(bases, metacls): #{{{
    return not any(isinstance(b, metacls) for b in bases)
# End def #}}}

def canweakref(obj): #{{{
    try:
        r = ref(obj)
    except TypeError:
        return False
    else:
        return True
# End def #}}}

def isbuiltin(obj): #{{{
    if isbfunction(obj) or isbmethod(obj):
        return True
    if not isclass(obj):
        obj = obj.__class__
    return obj in __builtin__.__dict__.values()
# End def #}}}

def numeric_methods(): #{{{
    standard = [k for k, v in object.__dict__.iteritems() if iscallable(v)]
    numtype = (int, long, float, complex)
    num = set()
    for t in numtype:
        num |= set(k for k, v in t.__dict__.iteritems() if k not in standard and iscallable(v))
    num |= set(["__iadd__", "__isub__", "__imul__", "__idiv__", "__itruediv__", "__ifloordiv__", 
                "__imod__", "__ipow__", "__ilshift__", "__irshift__", "__iand__", "__ixor__", "__ior__",
                "__complex__", "__oct__", "__hex__"])
    remove = set(['__%s__' %n for n in ['getnewargs', 'setformat', 'getformat']] + ['conjugate'])
    num -= remove
    return num
# End def #}}}

def numeric_methods_proxysafe(): #{{{
    num_meth = numeric_methods()
    num_meth -= set('__%s__' %n for n in ['int', 'float', 'long', 'complex', 'oct', 'hex', 'index', 'coerce'])
    return num_meth
# End def #}}}
