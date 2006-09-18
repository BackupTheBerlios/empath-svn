# Module: validate.validate
# File: validate.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the validate project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from weakref import ref

__all__ = ('Validate',)

class Validate(object): #{{{
    __slots__ = ('_exact', '_stored', '_options', '__weakref__')
    def __init__(self, *vobj, **options): #{{{
        if self.__class__ is Validate:
            raise NotImplementedError("Validate is an abstract class")
        vlen = len(vobj)
        mvlen = bool(options.pop('multiple_args', False))
        if not mvlen and vlen > 1:
            raise NotImplementedError("Passing more than one argument is not supported")
        expected = ('exact',)
        unexpected = tuple(kw for kw in options if kw not in expected)
        if unexpected:
            raise ValueError("Unexpected arguments %s" %', '.join(unexpected))
        self._exact = bool(options.pop('exact', False))
        self._stored = vobj
        self._set_options(*options.items())
    # End def #}}}

    def __call__(self, *vobj, **options): #{{{
        return self.__class__(*vobj, **options)
    # End def #}}}

    def __and__(self, vobj): #{{{
        return Validate_And(self, vobj)
    # End def #}}}

    def __or__(self, vobj): #{{{
        return Validate_Or(self, vobj)
    # End def #}}}

    def __eq__(self, obj): #{{{
        result = self._validate_single_result
        return self._validate_results(result(vobj, obj) for vobj in self._stored)
    # End def #}}}

    def _validate_single_result(self, vobj, obj): #{{{
        if isinstance(vobj, callobj):
            vobj = vobj()
        valf = self._validate
        if self._exact:
            valf = self._validate_exact
        return valf(vobj, obj)
    # End def #}}}

    def _validate_results(self, results): #{{{
        for r in results:
            return r
        return False
    # End def #}}}

    def _validate(self, vobj, obj): #{{{
        return vobj == obj
    # End def #}}}

    def _validate_exact(self, vobj, obj): #{{{
        return vobj is obj
    # End def #}}}

    def _set_options(self, *args): #{{{
        t = tuple((k, v) for k, v in args)
        self._options = getattr(self, '_options', tuple()) + t
    # End def #}}}

    def _get_option(self, name, d=None): #{{{
        for k, v in self._options:
            if k == name:
                return v
        return d
    # End def #}}}

    # Properties #{{{
    exact = property(lambda s: s._exact)
    stored = property(lambda s: s._stored)
    options = property(lambda s: dict(s._options)) 
    # End properties #}}}
# End class #}}}

class BooleanValidate(Validate): #{{{
    __slots__ = tuple()
    def __init__(self, *vobj, **options): #{{{
        new_opt = dict(options)
        new_opt.update(multiple_args=True)
        super(BooleanValidate, self).__init__(*vobj, **new_opt)
    # End def #}}}
# End class #}}}

class Validate_And(BooleanValidate): #{{{
    __slots__ = tuple()
    def _validate_results(self, results): #{{{
        if False in results:
            return False
        return True
    # End def #}}}
# End class #}}}

class Validate_Or(BooleanValidate): #{{{
    __slots__ = tuple()
    def _validate_results(self, results): #{{{
        if True in results:
            return True
        return False
    # End def #}}}
# End class #}}}

class callobj(object): #{{{
    __slots__ = tuple(['__weakref__'])
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
        ret = c(*args, **kwargs)
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
        self._evalstr = s
        if not glob:
            glob = globals()
        if not loc:
            loc = glob
        self._globals = glob
        self._locals = loc
    # End def #}}}

    def __call__(self, glob=None, loc=None): #{{{
        if not glob:
            glob = self._globals
        elif not loc:
            loc = glob
        if not loc:
            loc = self._locals
        return eval(self._evalstr, glob, loc)
    # End def #}}}

    # Properties #{{{
    evalstr = property()
    # End properties #}}}
# End class #}}}
