# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import ishashable, isiterable

class BaseMappingSet(object): #{{{
    __slots__ = ('_dict',)
    #==============================
    # Common
    #==============================
    def __init__(self, iter=()): #{{{
        if self.__class__ == BaseMappingSet:
            raise NotImplementedError("BaseMappingSet is an abstract class")
        elif not isiterable(iter):
            raise TypeError("%s object is not iterable" %iter.__class__.__name__)
        mkval = self._mkvalfunc()
        mkkey = self._mkkeyfunc()
        self._dict = dict((mkkey(None, k, iter), mkval(None, k, iter)) for k in iter)
    # End def #}}}

    def __len__(self): #{{{
        return len(self._dict)
    # End def #}}}

    def __contains__(self, el): #{{{
        if not ishashable(el):
            return False
        return self._dict.__contains__(el)
    # End def #}}}

    def __eq__(self, obj): #{{{
        try:
            lobj = len(obj)
        except:
            return False
        if lobj != len(self):
            return False
        for el in obj:
            if el not in self:
                return False
        return True
    # End def #}}}

    def __ne__(self, obj): #{{{
        return not self.__eq__(obj)
    # End def #}}}

    def __nonzero__(self): #{{{
        return bool(self._dict)
    # End def #}}}

    def __str__(self): #{{{
        return str(tuple(self._dict.iterkeys()))
    # End def #}}}

    def __repr__(self): #{{{
        return ''.join([self.__class__.__name__, self.__str__()])
    # End def #}}}
    #==============================
    # Dict methods
    #==============================
    def __iter__(self): #{{{
        return self._dict.__iter__()
    # End def #}}}

    def __getitem__(self, key): #{{{
        return self._dict.__getitem__(key)
    # End def #}}}

    def get(self, key, d=None): #{{{
        return self._dict.get(key, d)
    # End def #}}}

    def keys(self): #{{{
        return self._dict.keys()
    # End def #}}}

    def iterkeys(self): #{{{
        return self._dict.iterkeys()
    # End def #}}}

    def values(self): #{{{
        return self._dict.values()
    # End def #}}}

    def itervalues(self): #{{{
        return self._dict.itervalues()
    # End def #}}}

    def items(self): #{{{
        return self._dict.items()
    # End def #}}}

    def iteritems(self): #{{{
        return self._dict.iteritems()
    # End def #}}}
    #==============================
    # Bitwise operators
    #==============================
    def __and__(self, iter): #{{{
        return self.new(el for el in iter if el in self)
    # End def #}}}
    def __or__(self, obj): #{{{
        def inter(): #{{{
            for el in self:
                yield el
            for el in obj:
                yield el
        # End def #}}}
        return self.new(el for el in inter())
    # End def #}}}
    def __sub__(self, obj): #{{{
        return self.new(el for el in self if el not in obj)
    # End def #}}}
    def __xor__(self, obj): #{{{
        def uncommon(): #{{{
            for el in self:
                if el not in obj:
                    yield el
            for el in obj:
                if el not in self:
                    yield el
        # End def #}}}
        return self.new(el for el in uncommon())
    # End def #}}}

    def __rand__(self, obj): #{{{
        return self.new(obj).__and__(self)
    # End def #}}}
    def __ror__(self, obj): #{{{
        return self.new(obj).__or__(self)
    # End def #}}}
    def __rsub__(self, obj): #{{{
        return self.new(obj).__sub__(self)
    # End def #}}}
    def __rxor__(self, obj): #{{{
        return self.new(obj).__xor__(self)
    # End def #}}}

    def union(self, s): #{{{
        return self | s
    # End def #}}}
    def intersection(self, s): #{{{
        return self & s
    # End def #}}}
    def difference(self, s): #{{{
        return self - s
    # End def #}}}
    def symmetric_difference(self, s): #{{{
        return self ^ s
    # End def #}}}

    #==============================
    # Public methods
    #==============================
    def issubset(self, s): #{{{
        if not self or s is self:
            return True
        try:
            lens = len(s)
        except:
            return False
        if len(self) > lens:
            return False
        for el in self:
            if el not in s:
                return False
        return True
    # End def #}}}

    def issuperset(self, s): #{{{
        if not s or s is self:
            return True
        try:
            lens = len(s)
        except:
            return False
        if len(self) < lens:
            return False
        for el in s:
            if el not in self:
                return False
        return True
    # End def #}}}

    def __copy__(self): #{{{
        return self.__class__(self)
    # End def #}}}

    def new(self, iter=()): #{{{
        return self.__class__(iter)
    # End def #}}}

#    def _subgraph(self, iter=()): #{{{
#        return self.__class__(iter)
#    # End def #}}}

    def subset(self, iter=()): #{{{
        def check(): #{{{
            for el in iter:
                if el not in self:
                    raise ValueError("Value '%s' is not an member of this graph" %str(el))
                yield el
        # End def #}}}
        return self.new(check())
    # End def #}}}

    def superset(self, iter=()): #{{{
        g = self.__copy__()
        g.update(iter)
        return g
    # End def #}}}

    #==============================
    # Private methods
    #==============================
    def _mkkeyfunc(self): #{{{
        return lambda s, k, o: k
    # End def #}}}

    def _mkvalfunc(self): #{{{
        return lambda s, k, o: k
    # End def #}}}

    def _generate_hash(self): #{{{
        result = 0
        for elt in self:
            result ^= hash(elt)
        return result
    # End def #}}}
# End class #}}}

class FrozenMappingSet(BaseMappingSet): #{{{
    __slots__ = ('_hashcode',)
    #==============================
    # Common
    #==============================
    def __init__(self, iter=()): #{{{
        self._hashcode = None
        super(FrozenMappingSet, self).__init__(iter)
    # End def #}}}
    def __hash__(self): #{{{
        r = self._hashcode
        if r is None:
            self._hashcode = r = self._generate_hash()
        return r
    # End def #}}}
# End class #}}}

class MappingSet(BaseMappingSet): #{{{
    __slots__ = ()
    #==============================
    # Dict methods
    #==============================
    def pop(self, *args): #{{{
        if not args:
            return self.popitem()
        else:
            v = args[0]
            try:
                return v, self._dict.pop(*args)
            except:
                raise Exception(args, self._dict.keys())
    # End def #}}}

    def popitem(self): #{{{
        return self._dict.popitem()
    # End def #}}}

    def clear(self): #{{{
        pop = self.pop
        while self:
            pop()
#        return self._dict.clear()
    # End def #}}}
    #==============================
    # Bitwise operators
    #==============================
    def __iand__(self, obj): #{{{
        uncommon = self ^ obj
        pop = self.pop
        for el in uncommon:
            pop(el, None)
        return self
    # End def #}}}
    def __ior__(self, obj): #{{{
        mkval = self._mkvalfunc()
        mkkey = self._mkkeyfunc()
        self._dict.update((mkkey(self, k, obj), mkval(self, k, obj)) for k in obj)
        return self
    # End def #}}}
    def __isub__(self, obj): #{{{
        pop = self.pop
        for el in (self & obj):
            pop(el)
        return self
    # End def #}}}
    def __ixor__(self, obj): #{{{
        n = self.new
        add = n(obj) - n(self)
        self -= obj
        self |= add
        return self
    # End def #}}}

    def update(self, s): #{{{
        self.__ior__(s)
    # End def #}}}
    def intersection_update(self, s): #{{{
        self.__iand__(s)
    # End def #}}}
    def difference_update(self, s): #{{{
        self.__isub__(s)
    # End def #}}}
    def symmetric_difference_update(self, s): #{{{
        self.__ixor__(s)
    # End def #}}}
    #==============================
    # Set methods
    #==============================
    def add(self, obj): #{{{
        if obj in self:
            return
#        mkval = self._mkvalfunc()
        self |= [obj]
#        self._dict[obj] = mkval(self, obj, None)
    # End def #}}}

    def remove(self, el): #{{{
        self.pop(el)
    # End def #}}}

    def discard(self, el): #{{{
        if el not in self:
            return
        self.pop(el)
    # End def #}}}
# End class #}}}
