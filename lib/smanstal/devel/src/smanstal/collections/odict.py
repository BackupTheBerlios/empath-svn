# Module: smanstal.collections.odict
# File: odict.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from smanstal.types.introspect import ismapping

__all__ = ('OrderedDictMixin', 'odict')

class OrderedDictMixin(object): #{{{
    __slots__ = ()
    def __init__(self, *args, **kwargs): #{{{
        self._keys = []
        super(OrderedDictMixin, self).__init__()
        arglen = len(args)
        if arglen == 1:
            if isinstance(args[0], dict):
                self.update(args[0])
            else:
                for k, v in args[0]:
                    self.__setitem__(k, v)
            self.update(kwargs)
        elif arglen == 0:
            self.update(kwargs)
        else:
            self.update(*args, **kwargs)
    # End def #}}}

#    def _keyval(self, key): #{{{
#        return key
#    # End def #}}}

    def __eq__(self, other): #{{{
        if not isinstance(other, OrderedDictMixin): return False
        if super(OrderedDictMixin, self).__eq__(other):
            return self._keys == other._keys
        return False
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
            self._keys.append(key)
    # End def #}}}

    def _setitem_keycheck(self, key): #{{{
        return key not in self._keys
    # End def #}}}

    def __delitem__(self, key): #{{{
        super(OrderedDictMixin, self).__delitem__(key)
        self._pop_removekey(key)
    # End def #}}}

    def __copy__(self): #{{{
        od = odict()
        od.update(self)
        return od
    # End def #}}}

    def clear(self): #{{{
        super(OrderedDictMixin, self).clear()
        self._keys = []
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

    def _itergetfunc(self): #{{{
        get = self.get
        def func(key, index): #{{{
            return get(key)
        # End def #}}}
        return func
    # End def #}}}
    
    def iteritems(self): #{{{
        iterget = self._itergetfunc()
        i = 0
        for key in self: 
            yield (key, iterget(key, i))
            i += 1
    # End def #}}}

    def fromkeys(self, seq, value=None): #{{{
        od = odict()
        for k in seq:
            od[k] = value
        return od
    # End def #}}}

    def _pop_removekey(self, key, *args, **kw): #{{{
        try:
            self._keys.remove(key)
        except ValueError:
            pass
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
        if key not in self._keys: self._keys.append(key)
        return super(OrderedDictMixin, self).setdefault(key, *args, **opt)
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
# End class #}}}

class odict(OrderedDictMixin, dict): #{{{
    __slots__ = ('_keys',)
# End class #}}}
