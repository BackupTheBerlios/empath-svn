# Module: aossi.misc
# File: misc.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('iscallable', 'methodtype', 'methodname', 'cref', 'ChooseCallable', 'ChoiceObject', 'AmbiguousChoiceError',
            'cargnames', 'cargdefstr', 'cargval', 'callableobj', 'cgetargspec',
            'METHODTYPE_NOTMETHOD', 'METHODTYPE_UNBOUND', 'METHODTYPE_CLASS', 'METHODTYPE_INSTANCE')
from weakref import ref
from inspect import isfunction as _isf, ismethod as _ism, formatargspec, getargspec

METHODTYPE_NOTMETHOD = 0
METHODTYPE_UNBOUND = 1
METHODTYPE_CLASS = 2
METHODTYPE_INSTANCE = 3

class AmbiguousChoiceError(StandardError): pass

def cargnames(obj): #{{{
    obj = callableobj(obj)
    if not obj: return None
    fargnames, fvargs, fvkey, fdef = getargspec(obj)
    return fargnames, fvargs, fvkey
# End def #}}}

def cgetargspec(obj): #{{{
    obj = callableobj(obj)
    if not obj: return None
    fargnames, fvargs, fvkey, fdef = getargspec(obj)
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
    if not obj: return None
    fargnames, fvargs, fvkey, fdef = getargspec(obj)
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

def callableobj(obj): #{{{
    if not iscallable(obj):
        return None
    if not _ism(obj) and not _isf(obj):
        obj = obj.__call__
    return obj
# End def #}}}

def iscallable(obj): #{{{
    if not callable(obj):
        return False
    elif _ism(obj) or _isf(obj):
        return True
    elif isinstance(obj, type(str.__call__)):
        return False
    elif hasattr(obj, '__call__'):
        return iscallable(obj.__call__)
    return False
# End def #}}}

def methodtype(obj): #{{{
    if not _ism(obj):
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

class cref(object): #{{{
    __slots__ = ('_ref', '_isweak', '__weakref__')
    def __init__(self, obj, callback=None, **kwargs): #{{{
        weak = bool(kwargs.get('weak', True))
        self._ref = obj
        self._isweak = weak
        if weak:
            self._ref = ref(obj, callback)
    # End def #}}}

    def __call__(self): #{{{
        if self._isweak:
            return self._ref()
        return self._ref
    # End def #}}}

    # Properties #{{{
    isweak = property(lambda s: s._isweak)
    ref = property(lambda s: s._ref)
    # End properties #}}}
# End class #}}}

def ChooseCallable(choices, policy, *args, **kwargs): #{{{
    found = []
    for chooser, func in choices: #{{{
        if chooser(*args, **kwargs):
            if policy == 'first':
                return func
            found.append(func)
    if found:
        flen = len(found)
        if policy == 'last':
            return found[-1]
        elif flen == 1:
            return found[0]
        elif flen > 1:
            if policy == 'default':
                return None
        raise AmbiguousChoiceError('Found more than one selectable callable')
    return None
    # End for #}}}
# End def #}}}

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
