# Module: smanstal.collections.odict
# File: odict.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from smanstal.types.introspect import ismapping

__all__ = ('OrderedDictMixin', 'odict')

class _odm_keymaster: #{{{
    __slots__ = ('keys',)
    def __init__(self): #{{{
        self.keys = dict()
    # End def #}}}

    def __call__(self, od): #{{{
        return self.keys[id(od)]
    # End def #}}}

    def register(self, od): #{{{
        self.keys[id(od)] = []
    # End def #}}}

    def deregister(self, od): #{{{
        self.keys.pop(id(od), None)
    # End def #}}}
# End class #}}}

_keymaster = _odm_keymaster()

class OrderedDictMixin(object): #{{{
    __slots__ = ()
    # -------------------------------------------------
    # Helper methods
    # -------------------------------------------------
    def _add_key(self, key): #{{{
        self._keys.append(key)
    # End def #}}}

    def _setitem_keycheck(self, key): #{{{
        return key not in self._keys
    # End def #}}}

    def _itergetfunc(self): #{{{
        get = self.get
        keys = self._keys
        def func(index): #{{{
            key = keys[index]
            return get(key)
        # End def #}}}
        return func
    # End def #}}}

    def _indexvalue(self, index, getfunc, keys): #{{{
        key = keys[index]
        return getfunc(key)
    # End def #}}}
    
    def _pop_removekey(self, key, *args, **kw): #{{{
        try:
            self._keys.remove(key)
        except ValueError:
            pass
    # End def #}}}

    # -------------------------------------------------
    # Magic methods
    # -------------------------------------------------
    def __init__(self, *args, **kwargs): #{{{
#        self._keys = []
        _keymaster.register(self)
        super(OrderedDictMixin, self).__init__()
        if not args and not kwargs:
            return
        arglen = len(args)
        if arglen == 1:
            self.update(args[0], **kwargs)
        elif arglen == 0:
            self.update(kwargs)
        else:
            self.update(*args, **kwargs)
    # End def #}}}

    def __del__(self): #{{{
        _keymaster.deregister(self)
    # End def #}}}

    def __eq__(self, other): #{{{
        if not isinstance(other, OrderedDictMixin): return False
        if super(OrderedDictMixin, self).__eq__(other):
            return self._keys == other._keys
        return False
    # End def #}}}

    def __ne__(self, other): #{{{
        return not self.__eq__(other)
    # End def #}}}

    def __str__(self): #{{{
        o = '{%s}'
        t = ', '.join('%s: %s' %(repr(k), repr(v)) for k, v in self.iteritems())
        return '{%s}' %t
    # End def #}}}
    
    def __iter__(self): #{{{
        return iter(self._keys)
    # End def #}}}

    def __setitem__(self, key, val): #{{{
        super(OrderedDictMixin, self).__setitem__(key, val)
        if self._setitem_keycheck(key): 
            self._add_key(key)
    # End def #}}}

    def __delitem__(self, key): #{{{
        super(OrderedDictMixin, self).__delitem__(key)
        self._pop_removekey(key)
    # End def #}}}

    def __copy__(self): #{{{
        od = self.__class__()
        od.update(self)
        return od
    # End def #}}}

    # -------------------------------------------------
    # Public interface
    # -------------------------------------------------
    def clear(self): #{{{
        super(OrderedDictMixin, self).clear()
        self._keys[:] = []
#        self._keys = []
#        _keymaster.register(self)
    # End def #}}}

    def copy(self): #{{{
        return self.__copy__()
    # End def #}}}

    def items(self): #{{{
        return list(self.iteritems())
    # End def #}}}

    def keys(self): #{{{
        return list(self._keys)
    # End def #}}}

    def values(self): #{{{
        return [v for v in self.itervalues()]
    # End def #}}}
    
    def iterkeys(self): #{{{
        return self.__iter__()
    # End def #}}}
    
    def itervalues(self): #{{{
        return (v for k, v in self.iteritems())
    # End def #}}}

    def iteritems(self): #{{{
#        iterget = self._itergetfunc()
        get = self.get
        keys = self._keys
        iterget = self._indexvalue
        i = 0
        for key in self: 
            yield (key, iterget(i, get, keys))
            i += 1
    # End def #}}}

    def fromkeys(self, seq, value=None): #{{{
        od = odict()
        for k in seq:
            od[k] = value
        return od
    # End def #}}}

    def pop(self, key, *args, **kw): #{{{
        ret = super(OrderedDictMixin, self).pop(key, *args, **kw)
        self._pop_removekey(key, *args, **kw)
        return ret
    # End def #}}}

    def popitem(self): #{{{
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)
    # End def #}}}

    def setdefault(self, key, *args, **opt): #{{{
        ret = super(OrderedDictMixin, self).setdefault(key, *args, **opt)
        if self._setitem_keycheck(key): 
            self._add_key(key)
        return ret
    # End def #}}}

    def update(self, *args, **kw): #{{{
        new = {}
        setitem = self.__setitem__
        if args:
            largs = len(args)
            if largs > 1:
                raise TypeError('odict expected at most 1 arguments, got %i' %largs)
            args = args[0]
            seq = args.iteritems() if ismapping(args) else iter(args)
            for k, v in seq:
                setitem(k, v)
        if kw:
            for k, v in kw.iteritems():
                setitem(k, v)
    # End def #}}}

    def sort(self, cmp=None, key=None, reverse=False): #{{{
        return self._keys.sort(cmp, key, reverse)
    # End def #}}}

    def count(self, value): #{{{
        return self._keys.count(value)
    # End def #}}}

    def index(self, value, *args): #{{{
        return self._keys.index(value, *args)
    # End def #}}}

    def insert(key, item): #{{{
        keys = self._keys
        ikey, ival = item
        super(OrderedDictMixin, self).__setitem__(ikey, ival)
        ind = keys.index(key)
        keys.insert(ind, ikey)
    # End def #}}}

    def reverse(self): #{{{
        self._keys.reverse()
    # End def #}}}

    _keys = property(lambda s: _keymaster(s))
# End class #}}}

class odict(OrderedDictMixin, dict): #{{{
    __slots__ = ()
# End class #}}}
