# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import iscallable, isiterable
from smanstal.types.callobj import quote

__all__ = ('iterquery',)

class iterquery(object): #{{{
    __slots__ = ('_vars',)
    def __init__(self, *args, **opts): #{{{
        largs = len(args)
        if largs not in (1, 2):
            raise TypeError('Expected either 1 or 2 arguments, got %i instead' %largs)
        itertype = opts.get('itertype', tuple)
        parent, q = quote(opts.get('parent', None)), None
        if largs == 2:
            q = args[0]
        else:
            q = lambda i: True
        q, aiter = self.init_query(q), None
        if largs == 2:
            aitre = args[1]
        else:
            aiter = args[0]
        self._vars = parent, itertype, itertype(el for el in aiter if q(el))
    # End def #}}}

    def init_query(self, f): #{{{
        if not iscallable(f):
            return (lambda i: i== f)
        else:
            return f
    # End def #}}}
    init_filter = init_query

    def __iter__(self): #{{{
        return iter(self._vars[-1])
    # End def #}}}

    def __getitem__(self, i): #{{{
        count = 0
        for el in self:
            if count == i:
                return el
            count += 1
        raise IndexError('iterquery index out of range')
    # End def #}}}

    def as(self, itertype): #{{{
        return itertype(self)
    # End def #}}}

    def apply(self, chains, funcname=None): #{{{
        if not isiterable(chains):
            raise TypeError("Argument is not iterable")
        init = self
        for filter in chains:
            comp = filter, (), {}
            comp, i = list(comp), 0
            if funcname:
                comp[i], i = funcname, i+1
                for el in filter:
                    comp[i], i = el, i+1
            else:
                if not isinstance(filter, basestring):
                    flen = len(filter)
                    if not flen:
                        raise TypeError("Function name expected in chain: none found")
                    for el in filter:
                        comp[i], i = el, i+1
            fname, args, kw = comp
            init = getattr(init, fname)(*args, **kw)
        return init
    # End def #}}}

    def filter(self, f): #{{{
        f = self.init_filter(f)
        newiter = (i for i in self if f(i))
        _, itertype, _iter = self._vars
        kw = dict(parent=self, itertype=itertype)
        return self.__class__(newiter, **kw)
    # End def #}}}

    def reduce(self, f, *init): #{{{
        if len(init) > 1:
            raise TypeError('reduce() expected at most 2 arguments (%i given)' %len(init))
        value = list(init)
        for val in self:
            if not value:
                value.append(val)
            else:
                value[0] = f(value[0], val)
        if not value:
            raise TypeError('reduce() of empty sequence with no initial value')
        return value[0]
    # End def #}}}

    def _anyall_func(self, args): #{{{
        f = None
        if not args:
            f = lambda v: bool(v)
        else:
            if len(args) > 1:
                raise TypeError('any() takes at most 1 argument (%i given)'  %len(args))
            f = func = args[0]
            if iscallable(func):
                f = lambda v: bool(func(v))
            else:
                raise TypeError("Compare function must be callable")
        return f
    # End def #}}}

    def any(self, *args): #{{{
        return True in self.each(self._anyall_func(args))
    # End def #}}}

    def all(self, *args): #{{{
        return False not in self.each(self._anyall_func(args))
    # End def #}}}

    def each(self, f): #{{{
        _, itertype, _iter = self._vars
        kw = dict(parent=self, itertype=itertype)
        return self.__class__((f(i) for i in self), **kw)
    # End def #}}}
    map = each

    parent = property(lambda s: s._vars[0]())
    itertype = property(lambda s: s._vars[1])
# End class #}}}
