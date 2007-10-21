# Module: aossi.util
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from aossi.util.introspect import *
from aossi.util.callobj import quote as cref
from inspect import formatargspec, getargspec

try:
    from aossi._speedups.util import ChooseCallable, AmbiguousChoiceError, StopCascade
except ImportError:
    from aossi.util._util import ChooseCallable, AmbiguousChoiceError, StopCascade

__all__ = ('property_', 'deprecated', 'cref', 'ChooseCallable', 'ChoiceObject', 
            'AmbiguousChoiceError', 'StopCascade', 'needs_wrapping', 'callableobj', 'callable_wrapper',
            'cargnames', 'cgetargspec', 'cargdefstr', 'cargval', 'methodtype', 'methodname',
            'METHODTYPE_NOTMETHOD', 'METHODTYPE_UNBOUND', 'METHODTYPE_CLASS', 'METHODTYPE_INSTANCE',
            'isclassmethod', 'isstaticmethod')

_isf, _ism, _isb = isfunction, ismethod, isbuiltin
# ==================================================================================
# Constants
# ==================================================================================
METHODTYPE_NOTMETHOD = 0
METHODTYPE_UNBOUND = 1
METHODTYPE_CLASS = 2
METHODTYPE_INSTANCE = 3

# ==================================================================================
# Exceptions
# ==================================================================================
# Based on the following recipe:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/205183
def property_(func): #{{{
    vals = dict((k, v) for k,v in func().iteritems() 
            if k in ('fdel', 'fset', 'fget', 'doc'))
    return property(**vals)
# End def #}}}

# Make it easier to deprecate functionality
def deprecated(msg, stacklevel=2): #{{{
    from warnings import warn
    warn(msg, DeprecationWarning, stacklevel=stacklevel)
# End def #}}}

# Does the same checks that callableobj does and
# decides if an object is wrapped based on those checks
def needs_wrapping(obj): #{{{
    if not iscallable(obj):
        return False
    elif _ism(obj) or _isf(obj) or isclass(obj):
#    elif any(f(obj) for f in (_ism, _isf, isclassmethod, isstaticmethod)):
        return False
    elif hasattr(obj, '__call__') and _ism(obj.__call__):
        return False
    else:
        return True
# End def #}}}

def callableobj(obj): #{{{
    if not iscallable(obj):
        return None
    if _ism(obj) or _isf(obj) or isclass(obj):
#    if any(f(obj) for f in (_ism, _isf, isclassmethod, isstaticmethod)):
        return obj
    elif hasattr(obj, '__call__') and _ism(obj.__call__):
        return obj.__call__
    else:
        obj = callable_wrapper(obj)
    return obj
# End def #}}}

def callable_wrapper(func): #{{{
    if not iscallable(func):
        raise TypeError('Argument is not callable')
    def callwrapper(*args, **kwargs): #{{{
        return func(*args, **kwargs)
    # End def #}}}
    return callwrapper
# End def #}}}

def cargnames(obj): #{{{
    obj = callableobj(obj)
    isc = isclass(obj)
    if not obj: return None
    elif isc:
        obj = obj.__init__
        obj = callable_wrapper(obj) if needs_wrapping(obj) else obj
    fargnames, fvargs, fvkey, fdef = getargspec(obj)
    if isc and fargnames:
        fargnames = fargnames[1:]
    return fargnames, fvargs, fvkey
# End def #}}}

def cgetargspec(obj): #{{{
    obj = callableobj(obj)
    isc = isclass(obj)
    if not obj: return None
    elif isc:
        obj = obj.__init__
        obj = callable_wrapper(obj) if needs_wrapping(obj) else obj
    fargnames, fvargs, fvkey, fdef = getargspec(obj)
    if isc and fargnames:
        fargnames = fargnames[1:]
    if not fdef:
        return fargnames, fvargs, fvkey, {}
    numargs = len(fargnames)
    numdef = len(fdef)
    diff = numargs - numdef
    admatch = fargnames[diff:]
    return fargnames, fvargs, fvkey, dict(zip(admatch, fdef))
# End def #}}}

def cargdefstr(obj): #{{{
    obj = callableobj(obj)
    isc = isclass(obj)
    if not obj: return None
    elif isc:
        obj = obj.__init__
        obj = callable_wrapper(obj) if needs_wrapping(obj) else obj
    fargnames, fvargs, fvkey, fdef = getargspec(obj)
    if isc and fargnames:
        fargnames = fargnames[1:]
    argstr = formatargspec(fargnames, fvargs, fvkey, fdef)[1:-1]
    other = []
    if fvargs:
        other.append(''.join(['*', fvargs]))
    if fvkey:
        other.append(''.join(['**', fvkey]))
    callstr = ', '.join(fargnames + other)
    return argstr, callstr
# End def #}}}

def cargval(obj): #{{{
    ret = cgetargspec(obj)
    if not ret:
        return None
    else:
        return ret[-1]
# End def #}}}

def methodtype(obj): #{{{
    if not ismethod(obj):
        return METHODTYPE_NOTMETHOD
    elif obj.im_self is None:
        if obj.im_class is None:
            return METHODTYPE_UNBOUND
        return METHODTYPE_CLASS
    else:
        return METHODTYPE_INSTANCE
# End def #}}}

def methodname(obj): #{{{
    o = None
    mt = methodtype(obj)
    if mt == METHODTYPE_CLASS:
        o = obj.im_class
    elif mt == METHODTYPE_INSTANCE:
        o = obj.im_self
    else:
        return
    for i in dir(o):
        if getattr(o, i) == obj:
            return i
# End def #}}}

# Assumes choosefunc and func are CallableWrapper objects
class ChoiceObject(object): #{{{
    __slots__ = ('_choosefunc', '_func')
    def __init__(self, choosefunc, func): #{{{
        self._choosefunc = choosefunc
        self._func = func
    # End def #}}}

    # Properties #{{{
    choosefunc = property(lambda s: s._choosefunc)
    callable = property(lambda s: s._func)
    cid = property(lambda s: s._func.cid)
    isdead = property(lambda s: s._func.isdead or s._choosefunc.isdead)
    # End properties #}}}
# End class #}}}
