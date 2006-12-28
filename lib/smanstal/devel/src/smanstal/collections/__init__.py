# Module: smanstal.collections
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import ishashable, iscallable, ismapping, isclass
from smanstal.util.proxy import proxy  

__all__ = ('staticsequence', 'opair', 'unopair', 'multiset', 'bag', 'frozenmultiset', 'frozenbag')

#def staticsequence(name, pcls, **options): #{{{
#    n = options.get('n', 1)
#    h = options.get('hashable', True)
#    assert n >= 1, "cannot create custom tuple type with less than 1 element"
#    def wrap(func_name): #{{{
#        def wrapper(self, *args, **kwargs): #{{{
#            return getattr(self._pair, func_name)(*args, **kwargs)
#        # End def #}}}
#        wrapper.__name__ = func_name
#        return wrapper
#    # End def #}}}
#    class metapair(type): #{{{
#        def __new__(cls, classname, bases, clsdict): #{{{
#            l = clsdict
#            block = ('__init__', '__class__', '__doc__', '__getattribute__', '__new__', '__reduce__', 
#                    '__reduce_ex__', '__str__', '__repr__') + tuple(k for k in l.iterkeys() if k not in ('block', 'l'))
#            for n in [n for n in dir(pcls) if n not in block and iscallable(getattr(pcls, n))]:
#                l[n] = wrap(n)
#            return type.__new__(cls, classname, bases, clsdict)
#        # End def #}}}
#    # End class #}}}
#    class pair(object): #{{{
#        __metaclass__ = metapair
#        __slots__ = ('_pair',)
#        def __init__(self, *args): #{{{
#            if not args:
#                raise TypeError("'%s' object cannot be empty" %name)
#            if len(args) == 1 and n > 1:
#                args = args[0]
#            exec compile('args = (%s) = args' %', '.join('v%i' %i for i in xrange(n)), '<string>', 'exec') in locals()
#            p = pcls(args)
#            if h:
#                hash(p) # Throw error if not hashable
#            object.__setattr__(self, '_pair', p)
#        # End def #}}}

#        def __str__(self): #{{{
#            return str(tuple(self._pair))
#        # End def #}}}

#        def __repr__(self): #{{{
#            return ''.join([name, str(self)])
#        # End def #}}}

#        def __hash__(self): #{{{
#            return hash(self._pair)
#        # End def #}}}

#        def __setattr__(self, n, val): #{{{
#            raise AttributeError("'%s' object cannot set attribute '%s'" %(name, n))
#        # End def #}}}

#        def __delattr__(self, n): #{{{
#            raise AttributeError("'%s' object cannot delete attribute '%s'" %(name, n))
#        # End def #}}}

#        def __eq__(self, obj): #{{{
#            if not isinstance(obj, self.__class__):
#                obj = self.__class__(obj)
#            return self._pair == obj._pair
#        # End def #}}}

#        def __ne__(self, obj): #{{{
#            return not self.__eq__(obj)
#        # End def #}}}

#    # End class #}}}
#    pair.__name__ = name
#    return pair
## End def #}}}

def staticsequence(name, pcls, **options): #{{{
    n = options.get('n', 1)
    h = options.get('hashable', True)
    assert n >= 1, "cannot create static sequence type with less than 1 element"
    assert isclass(pcls), "cannot create static sequence from non-class"
    BaseSeq = proxy(pcls)
    class StaticSequence(BaseSeq): #{{{
        __slots__ = ()
        def __init__(self, *args): #{{{
            if not args:
                raise TypeError("'%s' object cannot be empty" %name)
            if len(args) == 1 and n > 1:
                args = args[0]
            exec compile('args = (%s) = args' %', '.join('v%i' %i for i in xrange(n)), '<string>', 'exec') in locals()
            super(StaticSequence, self).__init__(args)
            if h:
                hash(self) # Throw error if not hashable
        # End def #}}}

        def __repr__(self): #{{{
            return ' '.join([name, str(self)])
        # End def #}}}

        def __setattr__(self, n, val): #{{{
            raise AttributeError("'%s' object cannot set attribute '%s'" %(name, n))
        # End def #}}}

        def __delattr__(self, n): #{{{
            raise AttributeError("'%s' object cannot delete attribute '%s'" %(name, n))
        # End def #}}}

        def __eq__(self, obj): #{{{
            if not isinstance(obj, self.__class__):
                try:
                    obj = self.__class__(obj)
                except TypeError:
                    return False
            return super(StaticSequence, self).__eq__(obj)
        # End def #}}}

        def __ne__(self, obj): #{{{
            return not self.__eq__(obj)
        # End def #}}}
    # End class #}}}
    StaticSequence.__name__ = name
    return StaticSequence
# End def #}}}

opair = staticsequence('opair', tuple, n=2)

class baseunopair(tuple): #{{{
    __slots__ = ()
    def __eq__(self, o): #{{{
        try:
            val = (v1, v2) = o
        except:
            raise Exception(o)
        sup = super(baseunopair, self).__eq__
        return bool(sup(val) or sup(val[::-1]))
    # End def #}}}

    def __hash__(self): #{{{
        return hash((min(self), max(self)))
    # End def #}}}
# End class #}}}
unopair = staticsequence('unopair', baseunopair, n=2)

class basedisunopair(baseunopair): #{{{
    __slots__ = ()
    def __init__(self, *args): #{{{
        if len(args) == 1:
            args = args[0]
        if args:
            v1, v2 = args
            if v1 == v2:
                raise ValueError("Pairs must be of distinct values")
        super(basedisunopair, self).__init__(self, *args)
    # End def #}}}
# End class #}}}
disunopair = staticsequence('disunopair', basedisunopair, n=2)


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
