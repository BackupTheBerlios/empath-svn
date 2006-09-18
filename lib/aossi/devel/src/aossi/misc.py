# Module: aossi.misc
# File: misc.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('iscallable', 'methodtype', 'methodname', 'cref', 'isreadonly', 'ChooseCallable', 'ChoiceObject', 'AmbiguousChoiceError',
            'StopCascade', 'cargnames', 'cargdefstr', 'cargval', 'iswrapped', 'callableobj', 'cgetargspec', 'callable_wrapper',
            'METHODTYPE_NOTMETHOD', 'METHODTYPE_UNBOUND', 'METHODTYPE_CLASS', 'METHODTYPE_INSTANCE')
from aossi.impex import import_, CopyModuleImporter
_ab = import_(':aossi:__builtin__', importer=CopyModuleImporter(copy_prefix=':aossi:'))
property = _ab.property

from weakref import ref
from inspect import isfunction as _isf, ismethod as _ism, isbuiltin as _isb, \
        isclass, formatargspec, getargspec

METHODTYPE_NOTMETHOD = 0
METHODTYPE_UNBOUND = 1
METHODTYPE_CLASS = 2
METHODTYPE_INSTANCE = 3

class AmbiguousChoiceError(StandardError): pass
class StopCascade(Exception): pass

def cargnames(obj): #{{{
    obj = callableobj(obj)
    if not obj: return None
    fargnames, fvargs, fvkey, fdef = getargspec(obj)
    return fargnames, fvargs, fvkey
# End def #}}}

def cgetargspec(obj): #{{{
    len = _ab.len
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

def iswrapped(obj): #{{{
    if _ism(obj) or _isf(obj):
        return False
    elif hasattr(obj, '__call__') and _ism(obj.__call__):
        return False
    else:
        return True
# End def #}}}

def callableobj(obj): #{{{
    if not iscallable(obj):
        return None
    if _ism(obj) or _isf(obj):
        return obj
    elif hasattr(obj, '__call__') and _ism(obj.__call__):
        return obj.__call__
    else:
        obj = callable_wrapper(obj)
    return obj
# End def #}}}

def iscallable(obj): #{{{
    if isclass(obj):
        return False
    return _ab.callable(obj)
#    if not callable(obj):
#        return False
#    elif _ism(obj) or _isf(obj) or _isb(obj):
#        return True
#    elif isinstance(obj, type(str.__call__)):
#        return False
#    elif hasattr(obj, '__call__'):
#        return iscallable(obj.__call__)
#    return False
# End def #}}}

def callable_wrapper(func): #{{{
    if not _ab.callable(func):
        raise TypeError('Argument is not callable')
    def callwrapper(*args, **kwargs): #{{{
        return func(*args, **kwargs)
    # End def #}}}
    return callwrapper
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
    for i in _ab.dir(o):
        if _ab.getattr(o, i) == obj:
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

def isreadonly(obj, aname, attr): #{{{
    ret = False
    try:
        _ab.setattr(obj, aname, attr)
    except:
        ret = True
    return ret
# End def #}}}

def isiterable(obj): #{{{
    iobj = getattr(obj, '__iter__', None)
    return bool(iobj and not isclass(obj))
# End def #}}}

def ChooseCallable(choices, policy, origfunc, callfunc, *args, **kwargs): #{{{
    if policy == 'default':
        return None
    cascade = policy == 'cascade'
    def build_found(): #{{{
        def cascade_chooser(chooser, *args, **kwargs): #{{{
            cret = False
            stop = False
            try:
                cret = callfunc(chooser, *args, **kwargs)
            except StopCascade, err:
                if err.args:
                    cret = _ab.bool(err.args[0])
                stop = True
            return cret, stop
        # End def #}}}
        if cascade:
            yield origfunc
        for chooser, func in choices: #{{{
            cret = False
            stop = False
            if cascade:
                cret, stop = cascade_chooser(chooser, *args, **kwargs)
            else:
                cret = callfunc(chooser, *args, **kwargs)
            if cret:
                yield func
                if policy == 'first':
                    return 
            if cascade and stop:
                break
        # End for #}}}
    # End def #}}}
    found = [f for f in build_found()]
    if not found:
        return None
    elif policy == 'last':
        return found[-1:]
    elif cascade or _ab.len(found) == 1:
        return found
    raise AmbiguousChoiceError('Found more than one selectable callable')
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
