# Module: aossi.cwrapper
# File: cwrapper.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('CallableWrapper', 'cid', 'num_static_args')
from warnings import warn
from types import MethodType as method
from inspect import getargspec, isfunction as _isf, ismethod as _ism
from aossi.misc import iscallable, methodtype, cref, ChoiceObject, \
    METHODTYPE_NOTMETHOD, METHODTYPE_UNBOUND, METHODTYPE_INSTANCE, METHODTYPE_CLASS

def cid(obj): #{{{
    if isinstance(obj, CallableWrapper) or isinstance(obj, ChoiceObject):
        return obj.cid
    return hash(obj)
# End def #}}}

def num_static_args(obj): #{{{
    if not iscallable(obj):
        return -1
    if _ism(obj):
        obj = obj.im_func
    if isinstance(obj, CallableWrapper):
        return obj._numargs
    if not _isf(obj):
        obj = obj.__call__
    argspec = getargspec(obj)
    l, d = len(argspec[0]), argspec[3]
    if d:
        l -= len(d)
    return l
# End def #}}}

class CallableWrapper(object): #{{{
    __slots__ = ('__weakref__', '_object', '_function', '_newcall', '_numargs', '_funcid')
    def __init__(self, obj, callback=None, **kwargs): #{{{
        if not iscallable(obj):
            raise TypeError('Argument must be a valid callable object')
        elif callback is not None and not callable(callback):
            raise TypeError('callback argument must be a callable object')

        self._object = None
        self._function = None
        self._newcall = self.call
        self._numargs = num_static_args(obj)
        isweak = bool(kwargs.get('weak', True))

        mtype = methodtype(obj)
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
        if o and len(args) == self._numargs - 1:
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
    
    # Properties #{{{
    numargs = property(lambda s: s._numargs)
    isdead = property(lambda s: s._isdead())
    callable = property(lambda s: s._getcallable())
    cid = property(lambda s: s._funcid)
    # End properties #}}}
# End class #}}}


