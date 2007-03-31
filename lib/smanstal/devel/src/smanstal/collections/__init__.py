# Module: smanstal.collections
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import ishashable, iscallable, ismapping, isclass
from smanstal.collections.attrdict import *

__all__ = ('multiset', 'bag', 'frozenmultiset', 'frozenbag')

class multiset(dict): #{{{
    __slots__ = ()
    def __init__(self, init=None): #{{{
        super(multiset, self).__init__()
        if init:
            self.update(init)
    # End def #}}}

    def __str__(self): #{{{
        return super(multiset, self).__str__()
    # End def #}}}

    def __repr__(self): #{{{
        return '%s(%s)'%(self.__class__.__name__, super(multiset, self).__repr__())
    # End def #}}}

    # =======================
    # Dict methods
    # =======================
    def __eq__(self, o): #{{{
        if not isinstance(o, multiset):
            o = multiset(o)
        return super(multiset, self).__eq__(o)
    # End def #}}}

    def __ne__(self, o): #{{{
        return not self.__eq__(o)
    # End def #}}}

    def __setitem__(self, obj, val): #{{{
        val = int(val)
        if val == 0:
            self.__delitem__(obj)
        elif val < 0:
            raise ValueError("Negative element counts are invalid: %i" %val)
        else:
            super(multiset, self).__setitem__(obj, val)
    # End def #}}}

    def setdefault(self, obj, val=None): #{{{
        if val == None:
            val = 1
        cur = self.get(obj)
        if cur is None:
            cur = val
            self.__setitem__(obj, cur)
        return cur
    # End def #}}}

    def __iter__(self): #{{{
        for k, v in self.iteritems():
            count = v
            while count:
                yield k
                count -= 1
    # End def #}}}
    # =======================
    # Set methods
    # =======================
    def __and__(self, obj): #{{{
        def inter(self, obj): #{{{
            return ((el, min(count, obj[el])) for el, count in self.iteritems() if el in obj)
        # End def #}}}
        cls = self.__class__
        return cls(inter(self, cls(obj)))
    # End def #}}}

    def __or__(self, obj): #{{{
        def union(self, obj): #{{{
            for el, count in self.iteritems():
                if el in obj:
                    count = max(count, obj[el])
                yield el, count
            for el, count in obj.iteritems():
                if el not in self:
                    yield el, count
        # End def #}}}
        cls = self.__class__
        return cls(union(self, cls(obj)))
    # End def #}}}

    def __sub__(self, obj): #{{{
        return self.__class__((k, v) for k, v in self.iteritems() if k not in obj)
    # End def #}}}

    def __xor__(self, obj): #{{{
        def get_xor(self, obj): #{{{
            for el, c in self.iteritems():
                if el not in obj:
                    yield el, c
            for el, c in obj.iteritems():
                if el not in self:
                    yield el, c
        # End def #}}}
        cls = self.__class__
        return cls(get_xor(self, cls(obj)))
    # End def #}}}

    def __rand__(self, obj): #{{{
        return self.__and__(obj)
    # End def #}}}
    def __ror__(self, obj): #{{{
        return self.__or__(obj)
    # End def #}}}
    def __rsub__(self, obj): #{{{
        return self.__sub__(obj)
    # End def #}}}
    def __rxor__(self, obj): #{{{
        return self.__xor__(obj)
    # End def #}}}

    def __iand__(self, obj): #{{{
        a = self & obj
        self.clear()
        self.update(a)
    # End def #}}}

    def __ior__(self, obj): #{{{
        a = self | obj
        self.clear()
        self.update(a)
    # End def #}}}

    def __isub__(self, obj): #{{{
        a = self - obj
        self.clear()
        self.update(a)
    # End def #}}}

    def __ixor__(self, obj): #{{{
        a = self ^ obj
        self.clear()
        self.update(a)
    # End def #}}}

    def add(self, el): #{{{
        self[obj] = self.get(obj, 0) + 1
    # End def #}}}

    def difference(self, s): #{{{
        return self.__sub__(s)
    # End def #}}}

    def difference_update(self, s): #{{{
        return self.__isub__(s)
    # End def #}}}

    def intersection(self, s): #{{{
        return self.__and__(s)
    # End def #}}}

    def intersection_update(self, s): #{{{
        return self.__iand__(s)
    # End def #}}}

    def symmetric_difference(self, s): #{{{
        return self.__xor__(s)
    # End def #}}}

    def symmetric_difference_update(self, s): #{{{
        return self.__ixor__(s)
    # End def #}}}

    def union(self, s): #{{{
        return self.__or__(s)
    # End def #}}}

    def update(self, s): #{{{
        if ismapping(s):
            s = s.iteritems()
        def set_mapping(init): #{{{
            for item in init:
                try:
                    obj, count = item
                except (ValueError, TypeError):
                    obj, count = item, self.get(item, 0) + 1
                    cur = count
                else:
                    cur = self.get(obj, 1)
                try:
                    count = int(count)
                except (TypeError, ValueError):
                    count = cur
                else:
                    if not count:
                        self.pop(obj, 0)
                        continue
                    elif count < 0:
                        raise ValueError("Invalid count of %i for %s object" %(count, obj.__class__.__name__))
                yield obj, count
        # End def #}}}
        super(multiset, self).update(set_mapping(s))
    # End def #}}}

    def discard(self, obj): #{{{
        if obj not in self:
            return
        self.remove(obj)
    # End def #}}}
# End class #}}}

class _metafms(type): #{{{
    def __new__(cls, classname, bases, clsdict): #{{{
        def mk_noupdate(name): #{{{
            def noupdate(self, *args, **kwargs): #{{{
                raise TypeError("%s is immutable" %classname)
            # End def #}}}
            noupdate.__name__ = name
            return noupdate
        # End def #}}}
        noupdate_mag = ('setitem', 'delitem', 'iand', 'ior', 'isub', 'ixor')
        noupdate = ('setdefault', 'remove', 'pop', 'clear', 'discard', 'update', 'difference_update',
                    'intersection_update', 'symmetric_difference_update') + tuple('__%s__' %n for n in noupdate_mag)
        for name in noupdate:
            clsdict[name] = mk_noupdate(name)
        return type.__new__(cls, classname, bases, clsdict)
    # End def #}}}
# End class #}}}

class frozenmultiset(multiset): #{{{
    __metaclass__ = _metafms
    __slots__ = ()
    def __init__(self, init=None): #{{{
        super(frozenmultiset, self).__init__()
        if init:
            super(frozenmultiset, self).update(init)
    # End def #}}}

    def __hash__(self): #{{{
        return hash(frozenset(self.iteritems()))
    # End def #}}}
# End class #}}}
bag = multiset
frozenbag = frozenmultiset
