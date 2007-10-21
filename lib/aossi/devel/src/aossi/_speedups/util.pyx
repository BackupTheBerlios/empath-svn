# Module: aossi.util
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from weakref import ref

__all__ = ('callobj', 'cref', 'ChooseCallable', 'AmbiguousChoiceError', 'StopCascade', 'OrderedDictMixin')

class AmbiguousChoiceError(StandardError): pass
class StopCascade(Exception): pass

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
#    check = check + tuple('iter' + c for c in check)
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
# cref
# ==================================================================================
cdef class callobj: #{{{
    cdef object __weakref__
    def __init__(self): #{{{
        raise NotImplementedError("callobj is an abstract class")
    # End def #}}}

    def __call__(self): #{{{
        raise NotImplementedError("Please override the __call__ method")
    # End def #}}}
# End class #}}}

cdef class cref(callobj): #{{{
    cdef object _ref, _isweak
#    __slots__ = ('_ref', '_isweak')
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
    property isweak:
        def __get__(self): #{{{
            return self._isweak
        # End def #}}}
    property ref:
        def __get__(self): #{{{
            return self._ref
        # End def #}}}
#    isweak = property(lambda s: s._isweak)
#    ref = property(lambda s: s._ref)
    # End properties #}}}
# End class #}}}
# ==================================================================================
# ChooseCallable
# ==================================================================================
# choices: sequence of 2-tuples
#   - A function that computes whether or not its partner will be run
#   - A callable that runs if its partner evaluates to True
# policy: Default policies: default, cascade, first, last
# origfunc: The original callable that is wrapped
# callfunc: A callable that accepts three arguments:
#   - A callable to call
#   - Arguments passed to the given callable
#   - Keyword arguments passed to the given callable
cdef _cascade_chooser(callfunc, chooser, args, kwargs): #{{{
    cret = stop = False
    try:
        cret = callfunc(chooser, *args, **kwargs)
    except StopCascade, err:
        if err.args:
            cret = bool(err.args[0])
        stop = True
    return cret, stop
# End def #}}}

cdef _build_found(cascade, choices, policy, origfunc, callfunc, args, kwargs): #{{{
    found = []
    fapp = found.append
    if cascade:
        fapp(origfunc)
    for chooser, func in choices: #{{{
        cret = stop = False
        if cascade:
            cret, stop = _cascade_chooser(callfunc, chooser, args, kwargs)
        else:
            cret = callfunc(chooser, *args, **kwargs)
        if cret:
            fapp(func)
            if policy == 'first':
                return found
        if cascade and stop:
            break
    return found
    # End for #}}}
# End def #}}}

def ChooseCallable(choices, policy, origfunc, callfunc, *args, **kwargs): #{{{
    if policy == 'default':
        return None
    cascade = policy == 'cascade'
    found = _build_found(cascade, choices, policy, origfunc, callfunc, args, kwargs)
    if not found:
        return None
    elif policy == 'last':
        return found[-1:]
    elif cascade or len(found) == 1:
        return found
    raise AmbiguousChoiceError('Found more than one selectable callable')
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

cdef class _odm_itergetfunc: #{{{
    cdef object get, keys
    def __init__(self, od): #{{{
        self.get = od.get
        self.keys = _keymaster(od)
    # End def #}}}

    def __call__(self, index): #{{{
        key = self.keys[index]
        return self.get(key)
    # End def #}}}
# End class #}}}

cdef class _odm_iteritems: #{{{
    cdef object iter, iterget, i
    def __init__(self, od): #{{{
        self.iter = od.__iter__()
        self.iterget = od._itergetfunc()
        self.i = 0
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        i, key = self.i, self.iter.next()
        self.i = i + 1 
        return (key, self.iterget(i))
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
            skeys = _keymaster(self)
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
        return iter(_keymaster(self))
    # End def #}}}

    def __setitem__(self, key, val): #{{{
        super(OrderedDictMixin, self).__setitem__(key, val)
        if self._setitem_keycheck(key): 
            self._add_key(key)
    # End def #}}}

    def _add_key(self, key): #{{{
        _keymaster(self).append(key)
    # End def #}}}

    def _setitem_keycheck(self, key): #{{{
        return (key not in _keymaster(self))
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

    def clear(self): #{{{
        super(OrderedDictMixin, self).clear()
#        self._keys = []
        _keymaster.register(self)
    # End def #}}}

    def copy(self): #{{{
        return self.__copy__()
    # End def #}}}

    def items(self): #{{{
        return list(self.iteritems())
    # End def #}}}

    def keys(self): #{{{
        return list(_keymaster(self))
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

    def _itergetfunc(self): #{{{
        return _odm_itergetfunc(self)
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

    def _pop_removekey(self, key, *args, **kw): #{{{
        try:
            _keymaster(self).remove(key)
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
            key = _keymaster(self)[-1]
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
        return _keymaster(self).sort(cmp, key, reverse)
    # End def #}}}
# End class #}}}
