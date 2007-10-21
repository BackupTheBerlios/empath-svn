# Module: aossi.util
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('OrderedDictMixin',)

_join = '_'.join

# ==================================================================================
# introspect
# ==================================================================================
# Copied from stdlib types module
class _C:
    def _m(self): pass
def _f(): pass

ClassType = type(_C)
function = type(_f)
method = type(_C()._m)
bfunction = type(len)
bmethod = type([].append)

# Adapted from aossi.util.introspect
def isclass(obj): #{{{
    return isinstance(obj, ClassType) or hasattr(obj, '__bases__')
# End def #}}}

def iscallable(obj): #{{{
    return bool(isinstance(obj, (function, bfunction, method, bmethod)) or
                isclass(obj) or 
                hasattr(obj, '__call__'))
# End def #}}}

def _mkitername(name): #{{{
    return _join(['iter', name])
# End def #}}}

def ismapping(obj): #{{{
    if isinstance(obj, dict):
        return True
    check = ('items', 'keys', 'values')
    check = check + tuple(map(_mkitername, check))
    check = check + ('__getitem__',)

#    return False not in (iscallable(getattr(obj, n, None)) for n in check)
    ret = True
    for n in check:
        if not iscallable(getattr(obj, n, None)):
            ret = False
            break
    return ret
# End def #}}}

# ==================================================================================
# odict
# ==================================================================================
cdef class _odm_keymaster: #{{{
    cdef object keys
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

#cdef class _odm_itergetfunc: #{{{
#    cdef object get, keys
#    def __init__(self, od): #{{{
#        self.get = od.get
#        self.keys = _keymaster(od)
#    # End def #}}}

#    def __call__(self, index): #{{{
#        key = self.keys[index]
#        return self.get(key)
#    # End def #}}}
## End class #}}}

cdef class _odm_iteritems: #{{{
    cdef object iter, iterget, i, get, keys
    def __init__(self, od): #{{{
        self.iter = od.__iter__()
        self.iterget = od._indexvalue
        self.i = 0
        self.get = od.get
#        self.keys = _keymaster(od)
        self.keys = od._keys
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        i, key, get, keys = self.i, self.iter.next(), self.get, self.keys
        self.i = i + 1 
        return (key, self.iterget(i, get, keys))
    # End def #}}}
# End class #}}}

cdef class _odm_itervalues: #{{{
    cdef object iter
    def __init__(self, od): #{{{
        self.iter = od.iteritems()
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        k, v = self.iter.next()
        return v
    # End def #}}}
# End class #}}}

def _odm_str(item): #{{{
    k, v = item
    return '%s: %s' %(repr(k), repr(v))
# End def #}}}

cdef class OrderedDictMixin: #{{{
    # -------------------------------------------------
    # Helper methods
    # -------------------------------------------------
    def _add_key(self, key): #{{{
#        _keymaster(self).append(key)
        self._keys.append(key)
    # End def #}}}

    def _setitem_keycheck(self, key): #{{{
#        return (key not in _keymaster(self))
        return (key not in self._keys)
    # End def #}}}

    def _pop_removekey(self, key, *args, **kw): #{{{
        try:
#            _keymaster(self).remove(key)
            self._keys.remove(key)
        except ValueError:
            pass
    # End def #}}}

#    def _itergetfunc(self): #{{{
#        return _odm_itergetfunc(self)
#    # End def #}}}

    def _indexvalue(self, index, getfunc, keys): #{{{
        key = keys[index]
        return getfunc(key)
    # End def #}}}
    
    # -------------------------------------------------
    # Magic methods
    # -------------------------------------------------
    def __init__(self, *args, **kwargs): #{{{
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

    def __dealloc__(self): #{{{
        _keymaster.deregister(self)
    # End def #}}}

    def __eq__(self, other): #{{{
        if not isinstance(other, OrderedDictMixin): return False
        if super(OrderedDictMixin, self).__eq__(other):
#            skeys = _keymaster(self)
            skeys = self._keys
            skeys_len = len(skeys)
            if skeys_len != len(other):
                return False
            okeys = other.itervalues()
            for i from 0 <= i < skeys_len:
                try:
                    if skeys[i] != okeys.next():
                        return False
                except StopIteration:
                    return True
        return False
    # End def #}}}

    def __ne__(self, other): #{{{
        return not self.__eq__(other)
    # End def #}}}

    def __str__(self): #{{{
        o = '{%s}'
        t = ', '.join(map(_odm_str, self.iteritems()))
        return '{%s}' %t
    # End def #}}}
    
    def __iter__(self): #{{{
#        return iter(_keymaster(self))
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
#        _keymaster.register(self)
    # End def #}}}

    def copy(self): #{{{
        return self.__copy__()
    # End def #}}}

    def items(self): #{{{
        return list(self.iteritems())
    # End def #}}}

    def keys(self): #{{{
#        return list(_keymaster(self))
        return list(self._keys)
    # End def #}}}

    def values(self): #{{{
        return list(self.itervalues())
    # End def #}}}
    
    def iterkeys(self): #{{{
        return self.__iter__()
    # End def #}}}
    
    def itervalues(self): #{{{
        return _odm_itervalues(self)
    # End def #}}}

    def iteritems(self): #{{{
        return _odm_iteritems(self)
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
#            key = _keymaster(self)[-1]
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
            if ismapping(args):
                seq = args.iteritems()
            else:
                seq = iter(args)
            for k, v in seq:
                setitem(k, v)
        if kw:
            for k, v in kw.iteritems():
                setitem(k, v)
    # End def #}}}

    def sort(self, cmp=None, key=None, reverse=False): #{{{
#        return _keymaster(self).sort(cmp, key, reverse)
        return self._keys.sort(cmp, key, reverse)
    # End def #}}}

    def count(self, value): #{{{
#        return _keymaster(self).count(value)
        return self._keys.count(value)
    # End def #}}}

    def index(self, value, *args): #{{{
        return self._keys.index(value, *args)
    # End def #}}}

    def insert(key, item): #{{{
#        keys = _keymaster(self)
        keys = self._keys
        ikey, ival = item
        super(OrderedDictMixin, self).__setitem__(ikey, ival)
        ind = keys.index(key)
        keys.insert(ind, ikey)
    # End def #}}}

    def reverse(self): #{{{
#        _keymaster(self).reverse()
        self._keys.reverse()
    # End def #}}}

    # -------------------------------------------------
    # Properties
    # -------------------------------------------------
    property _keys:
        def __get__(self): #{{{
            return _keymaster(self)
        # End def #}}}
# End class #}}}
