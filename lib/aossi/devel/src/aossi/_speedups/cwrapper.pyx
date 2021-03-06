# Module: aossi.cwrapper
# File: cwrapper.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from warnings import warn
from types import MethodType as method
from inspect import isfunction as _isf, ismethod as _ism, isclass

# package imports
from aossi.util import iscallable, needs_wrapping, cgetargspec, methodtype, cref, ChoiceObject, callableobj, \
        METHODTYPE_NOTMETHOD, METHODTYPE_UNBOUND, METHODTYPE_INSTANCE, METHODTYPE_CLASS

__all__ = ('cid', 'num_static_args', '_CallableWrapper')

def cid(obj): #{{{
    if isinstance(obj, _CallableWrapper) or isinstance(obj, ChoiceObject):
        return obj._funcid
    try:
        ret = hash(obj)
    except:
        obj = callableobj(obj)
        mtype = methodtype(obj)
        if mtype not in (METHODTYPE_NOTMETHOD, METHODTYPE_UNBOUND):
            obj = obj.im_func
        ret = hash(obj)
    return ret
# End def #}}}

# Returns 2-tuple:
#   - Number of mandatory arguments expected when calling the callable
#       - -1 == not a callable
#       - Any default values will reduce this number
#   - Maximum number of arguments expected, None == unlimited
# Assumes obj is either a function, a method, a CallableWrapper,
# or a callable with a __call__ method (not a method-wrapper)
def num_static_args(obj): #{{{
    if not iscallable(obj):
        return -1, None
    if _ism(obj):
        obj = obj.im_func
    if isinstance(obj, _CallableWrapper):
        return obj._numargs, obj._maxargs
    isc = isclass(obj)
    if not _isf(obj) and not isc:
        obj = obj.__call__
        if not _ism(obj):
            return -1, None
    argspec = cgetargspec(obj)
    l, d = len(argspec[0]), argspec[3]
    max = l
    if argspec[1]:
        max = None
    if d:
        l = l - len(d)
        if isc:
            l = l - 1
    return l, max
# End def #}}}

cdef class _CallableWrapper: #{{{
#class _CallableWrapper(object): #{{{
#    __slots__ = ('__weakref__', '_object', '_function', '_newcall', '_numargs', '_maxargs', '_funcid', 
#                    '__name__', '_methodtype')
    cdef public object __name__, _object, _function, _newcall, _numargs, _maxargs, _funcid, _methodtype

    def __init__(self, obj, callback=None, **kwargs): #{{{
        self.__name__ = getattr(obj, '__name__', 'UnnamedCallable')
        isw = needs_wrapping(obj)
        obj = callableobj(obj)
        if not obj:
            raise TypeError('Argument must be a valid callable object')
        elif callback is not None and not iscallable(callback):
            raise TypeError('callback argument must be a callable object')

        self._object = None
        self._function = None
        self._newcall = self.call
        self._numargs, self._maxargs = num_static_args(obj)
        isweak = bool(kwargs.get('weak', True))
        if isw:
            isweak = False

        mtype = methodtype(obj)
        self._methodtype = mtype
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
        nc = self._newcall
        if self._isdead():
            warn('Calling a dead wrapper', RuntimeWarning, stacklevel=2)
            return
        elif nc:
            return nc(*args, **kwargs)

        return self.call(*args, **kwargs)
    # End def #}}}

    def call(self, *args, **kwargs): #{{{
        f = self._getcallable()
        # If being called directly as a method instance and
        # no args got passed in i.e. no self reference,
        # add the object reference.
        o = self._object
        largs = len(args)
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

    # Wrapper functions will get passed the self reference
    # for the CallableWrapper object
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

    def _getref(self): #{{{
        sobj, sfun = self._object, self._function
        if sobj is None:
            return sfun
        return sobj
    # End def #}}}

    def _getcallable(self): #{{{
        sobj, sfun = self._object, self._function
        if sobj is None:
            return sfun()
        elif sobj() is None:
            return None
        return sfun
    # End def #}}}

    def _get_original(self): #{{{
        if self._isdead():
            raise ValueError("Cannot retrieve original: dead reference")
        im_self = None
        im_class = None
        cwo = self._object
        if cwo:
            obj = cwo()
            if isclass(obj):
                im_class = obj
            else:
                im_self, im_class = obj, obj.__class__
        gc_ret = self._getcallable()
        if im_self or im_class:
            return method(gc_ret, im_self, im_class)
        return gc_ret
    # End def #}}}

    def _get_ismethod(self): #{{{
        if self._isdead():
            raise ValueError("Cannot determine callable type: dead reference")
        return bool(self._object)
    # End def #}}}

    # Properties #{{{
    property numargs:
        def __get__(self): #{{{
            return self._numargs
        # End def #}}}
    property maxargs:
        def __get__(self): #{{{
            return self._maxargs
        # End def #}}}
    property isdead:
        def __get__(self): #{{{
            return self._isdead()
        # End def #}}}
    property isweak:
        def __get__(self): #{{{
            return self._getref().isweak
        # End def #}}}
    property callable:
        def __get__(self): #{{{
            return self._getcallable()
        # End def #}}}
    property cid:
        def __get__(self): #{{{
            return self._funcid
        # End def #}}}
    property original:
        def __get__(self): #{{{
            return self._get_original()
        # End def #}}}
    property ismethod:
        def __get__(self): #{{{
            return self._get_ismethod()
        # End def #}}}
    property methodtype:
        def __get__(self): #{{{
            return self._methodtype
        # End def #}}}
    # End properties #}}}
# End class #}}}


