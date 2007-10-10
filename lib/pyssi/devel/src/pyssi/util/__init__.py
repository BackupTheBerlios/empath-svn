# Module: aossi.util
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the pyssi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from inspect import formatargspec, getargspec

# package imports
from pyssi.util.introspect import *
from pyssi.util.byteplay import (LOAD_CONST, LOAD_FAST, CALL_FUNCTION, 
                                 CALL_FUNCTION_VAR, CALL_FUNCTION_KW,
                                 CALL_FUNCTION_VAR_KW)

try:
    from pyssi._speedups.util import cref
except ImportError:
    from pyssi.util.callobj import quote as cref

# ==================================================================================
# Constants
# ==================================================================================

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

def bp_call_args(args, vargs, vkeys, defaults, callmethod=False): #{{{
    if callmethod:
        args = args[1:]
    num_pos = num_kw = 0
    have_vargs = have_vkeys = False
    ret = []
    rapp = ret.append
    for a in args:
#        if a in defaults:
#            rapp((LOAD_CONST, a))
#            rapp((LOAD_CONST, defaults[a]))
#            num_kw += 1
#        else:
        rapp((LOAD_FAST, a))
        num_pos += 1
    if vargs != None:
        rapp((LOAD_FAST, vargs))
        have_vargs = True
    if vkeys != None:
        rapp((LOAD_FAST, vkeys))
        have_vkeys = True
    cnum = (num_kw << 8) | (num_pos)
    if not have_vargs and not have_vkeys:
        rapp((CALL_FUNCTION, cnum))
    elif have_vargs and not have_vkeys:
        rapp((CALL_FUNCTION_VAR, cnum))
    elif not have_vargs and have_vkeys:
        rapp((CALL_FUNCTION_KW, cnum))
    else:
        rapp((CALL_FUNCTION_VAR_KW, cnum))
    return ret
# End def #}}}

def default_argvals(args, defaults): #{{{
    if not defaults:
        return 
    argdefs = args[len(defaults)*-1:]
    return tuple(defaults[a] for a in argdefs)
# End def #}}}
