# Module: aossi.cwrapper
# File: cwrapper.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('CallableWrapper', 'cid', 'num_static_args')

from aossi.impex import import_, CopyModuleImporter
#__builtins__.update(import_(':aossi:__builtin__', attr=True, importer=CopyModuleImporter(copy_prefix=':aossi:')))
#globals().update(__builtins__)
_ab = import_(':aossi:__builtin__', importer=CopyModuleImporter(copy_prefix=':aossi:'))
property = _ab.property

from warnings import warn
from types import MethodType as method
from inspect import getargspec, isfunction as _isf, ismethod as _ism, isbuiltin as _isb, isclass
from aossi.misc import (iscallable, iswrapped, methodtype, cref, ChoiceObject, callableobj,
        METHODTYPE_NOTMETHOD, METHODTYPE_UNBOUND, METHODTYPE_INSTANCE, METHODTYPE_CLASS)

def cid(obj): #{{{
    isinstance = _ab.isinstance
    if isinstance(obj, CallableWrapper) or isinstance(obj, ChoiceObject):
        return obj.cid
    return _ab.hash(obj)
# End def #}}}

def num_static_args(obj): #{{{
    if not iscallable(obj):
        return -1, None
    if _ism(obj):
        obj = obj.im_func
    if _ab.isinstance(obj, CallableWrapper):
        return obj._numargs, obj._maxargs
    if not _isf(obj):
        obj = obj.__call__
    argspec = getargspec(obj)
    l, d = _ab.len(argspec[0]), argspec[3]
    max = l
    if argspec[1]:
        max = None
    if d:
        l -= _ab.len(d)
    return l, max
# End def #}}}

class CallableWrapper(object): #{{{
    __slots__ = ('__weakref__', '_object', '_function', '_newcall', '_numargs', '_maxargs', '_funcid', 
                    '__name__', '_methodtype')
    def __init__(self, obj, callback=None, **kwargs): #{{{
        self.__name__ = _ab.getattr(obj, '__name__', 'Unnamed Callable')
        isw = iswrapped(obj)
        obj = callableobj(obj)
        if not obj:
            raise TypeError('Argument must be a valid callable object')
        elif callback is not None and not callable(callback):
            raise TypeError('callback argument must be a callable object')

        self._object = None
        self._function = None
        self._newcall = self.call
        self._numargs, self._maxargs = num_static_args(obj)
        isweak = _ab.bool(kwargs.get('weak', True))
        if isw:
            isweak = False

        mtype = methodtype(obj)
#        self._methodtype = mtype
        if mtype not in (METHODTYPE_NOTMETHOD, METHODTYPE_UNBOUND):
            o = obj.im_class
            if mtype == METHODTYPE_INSTANCE:
                o = obj.im_self
            self._object = cref(o, callback, weak=isweak)
            self._function = obj.im_func
        else:
            self._function = cref(obj, callback, weak=isweak)
        self._funcid = cid(obj)
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        if self._isdead():
            warn('Calling a dead wrapper', RuntimeWarning, stacklevel=2)
            return
        elif self._newcall:
            return self._newcall(*args, **kwargs)

        return self.call(*args, **kwargs)
    # End def #}}}

    def call(self, *args, **kwargs): #{{{
        f = self._getcallable()
        # If being called directly as a method instance and
        # no args got passed in i.e. no self reference,
        # add the object reference.
        o = self._object
        largs = _ab.len(args)
        withself_numargs = self._numargs - 1
        sendself = self._maxargs is not None and largs >= withself_numargs and largs <= self._maxargs - 1 
        sendself = sendself or (self._maxargs is None and largs >= withself_numargs)
        if o and sendself:
            return f(o(), *args, **kwargs)
        else:
            return f(*args, **kwargs)
    # End def #}}}

    def unwrap(self): #{{{
        self._newcall = self.call
    # End def #}}}

    def wrap(self, func): #{{{
        if not iscallable(func):
            raise TypeError('Argument must be a valid callable object')
        newfunc = func(self._newcall)
        if not iscallable(newfunc):
            raise TypeError('Return value of wrapping callable must be a valid callable object')
        if not _ism(newfunc):
            newfunc = method(newfunc, self, self.__class__)
        self._newcall = newfunc
    # End def #}}}

    def _isdead(self): #{{{
        return self._getcallable() is None
    # End def #}}}

    def _getcallable(self): #{{{
        if self._object is None:
            return self._function()
        elif self._object() is None:
            return None
        return self._function
    # End def #}}}

    def _get_original(self): #{{{
        if self.isdead:
            raise ValueError("Cannot retrieve original: dead reference")
        im_self = None
        im_class = None
        cwo = self._object
        if cwo:
            obj = cwo()
            if isclass(obj):
                im_class = obj
            else:
                im_self = obj
                im_class = obj.__class__
        if im_self or im_class:
            return method(self.callable, im_self, im_class)
        return self.callable
    # End def #}}}

    def _get_ismethod(self): #{{{
        if self.isdead:
            raise ValueError("Cannot determine callable type: dead reference")
        return bool(self._object)
    # End def #}}}
    
    # Properties #{{{
    numargs = property(lambda s: s._numargs)
    maxargs = property(lambda s: s._maxargs)
    isdead = property(lambda s: s._isdead())
    callable = property(lambda s: s._getcallable())
    cid = property(lambda s: s._funcid)
    original = property(lambda s: s._get_original())
    ismethod = property(lambda s: s._get_ismethod())
#    methodtype = property(lambda s: s._methodtype)
    # End properties #}}}
# End class #}}}


