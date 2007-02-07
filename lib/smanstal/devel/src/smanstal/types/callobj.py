# Module: smanstal.types.callobj
# File: callobj.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the callobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from weakref import ref
from smanstal.types.introspect import iscallable

__all__ = ('callobj','quote', 'q', 'callcallable', 'evalobj')

class callobj(object): #{{{
    __slots__ = ('__weakref__',)
    def __init__(self): #{{{
        raise NotImplementedError("callobj is an abstract class")
    # End def #}}}

    def __call__(self): #{{{
        raise NotImplementedError("Please override the __call__ method")
    # End def #}}}
# End class #}}}

class quote(callobj): #{{{
    __slots__ = ('_ref', '_isweak')
    def __init__(self, obj, callback=None, **kwargs): #{{{
        weak = bool(kwargs.get('weak', True))
        auto = bool(kwargs.get('auto', True))
        self._ref = obj
        self._isweak = weak
        if weak:
            try:
                self._ref = ref(obj, callback)
            except TypeError:
                if not auto:
                    raise
                self._isweak = False
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

q = quote

class callcallable(callobj): #{{{
    __slots__ = ('_args', '_kwargs', '_callable')
    def __init__(self, c, *args, **kwargs): #{{{
        if not iscallable(c):
            raise TypeError("%s object is not callable" %c.__class__.__name__)
        mc = self._make_callobj
        self._args = tuple(mc(a) for a in args)
        self._kwargs = dict((k, mc(v)) for k, v in kwargs.iteritems())
        self._callable = c
    # End def #}}}

    def _make_callobj(self, obj): #{{{
        if isinstance(obj, callobj):
            return obj
        return q(obj)
    # End def #}}}

    def __call__(self): #{{{
        c = self._callable
        if isinstance(c, callobj):
            c = c()
        args = tuple(a() for a in self._args) 
        kwargs = dict((k, v()) for k, v in self._kwargs.iteritems())
        try:
            return c(*args, **kwargs)
        except:
            raise
            raise Exception(kwargs)
    # End def #}}}

    # Properties #{{{
    args = property(lambda s: s._args)
    kwargs = property(lambda s: dict(s._kwargs))
    callable = property(lambda s: s._callable)
    # End properties #}}}
# End class #}}}

class evalobj(callobj): #{{{
    __slots__ = ('_globals', '_locals', '_evalstr')
    def __init__(self, s, glob=None, loc=None): #{{{
        if isinstance(s, evalobj):
            s, glob, loc = s._evalstr, s._globals, s._locals
        elif not isinstance(s, basestring):
            raise TypeError('Cannot evaluate %s object' %s.__class__.__name__)
        self._evalstr = s
        if glob is None:
            glob = globals()
        if loc is None:
            loc = glob
        self._globals = glob
        self._locals = loc
    # End def #}}}

    def __call__(self, glob=None, loc=None): #{{{
        if glob is None:
            glob = self._globals
        if loc is None:
            loc = self._locals
        return eval(self._evalstr, glob, loc)
    # End def #}}}

    # Properties #{{{
    evalstr = property(lambda s: s._evalstr)
    # End properties #}}}
# End class #}}}

