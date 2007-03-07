# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from smanstal.types.introspect import ismapping, isclass, mro

__all__ = ('attrdict',)

class attrdict(dict): #{{{
    __slots__ = ('_obj',)
    def __init__(self, obj): #{{{
        self._obj = obj
        super(attrdict, self).__init__()
    # End def #}}}

    def shallowkeys(self): #{{{
        obj = self._obj
        def get_slots(obj): #{{{
            for cls in reversed(mro(obj)):
                for k, v in cls.__dict__.iteritems():
                    if k == '__slots__':
                        for k in v:
                            yield k
        # End def #}}}
        is_cls = isclass(obj)
        cls = obj if is_cls else obj.__class__
        names = set(cls.__dict__.iterkeys())
        if not is_cls:
            slots = getattr(cls, '__slots__', ())
            names.update(n for n in get_slots(cls))
            if not slots:
                names.update(obj.__dict__.iterkeys())
        return (n for n in names if hasattr(obj, n))
    # End def #}}}

    def shallowitems(self): #{{{
        getitem = self.__getitem__
        return ((n, getitem(n)) for n in self.shallowkeys())
    # End def #}}}

    def shallowvalues(self): #{{{
        return (v for k, v in self.shallowitems())
    # End def #}}}

    def __copy__(self): #{{{
        return self.copy()
    # End def #}}}

    def __cmp__(self, other): #{{{
        return self.copy().__cmp__(other.copy())
    # End def #}}}

    def __str__(self): #{{{
        ret = '{%s}'
        mid = ', '.join('%s: %s' %(repr(k), repr(v)) for k, v in self.iteritems())
        return ret %mid
    # End def #}}}

    def __len__(self): #{{{
        return len(self.items())
    # End def #}}}

    def __getitem__(self, k): #{{{
        try:
            return getattr(self._obj, k)
        except AttributeError:
            raise KeyError(k)
    # End def #}}}

    def __setitem__(self, k, v): #{{{
        setattr(self._obj, k, v)
    # End def #}}}

    def __delitem__(self, k): #{{{
        if k in self.shallowkeys():
            delattr(self._obj, k)
    # End def #}}}

    def __iter__(self): #{{{
        obj = self._obj
        def get_clsnames(obj): #{{{
            for cls in reversed(mro(obj)):
                for k, v in cls.__dict__.iteritems():
                    yield k
                    if k == '__slots__':
                        for k in v:
                            yield k
        # End def #}}}
        is_cls = isclass(obj)
        cls = obj if is_cls else obj.__class__
        names = set(k for k in get_clsnames(cls))
        if not is_cls:
            slots = getattr(cls, '__slots__', ())
            if not slots:
                names.update(obj.__dict__.iterkeys())
        return (n for n in names if hasattr(obj, n))
    # End def #}}}

    def __contains__(self, k): #{{{
        return hasattr(self._obj, k)
    # End def #}}}

    def iteritems(self): #{{{
        obj = self._obj
        return ((n, getattr(obj, n)) for n in self)
    # End def #}}}

    def iterkeys(self): #{{{
        return iter(self)
    # End def #}}}

    def itervalues(self): #{{{
        return (v for k, v in self.iteritems())
    # End def #}}}

    def items(self): #{{{
        return list(self.iteritems())
    # End def #}}}

    def keys(self): #{{{
        return list(self.iterkeys())
    # End def #}}}

    def values(self): #{{{
        return list(self.itervalues())
    # End def #}}}

    def setdefault(self, k, *d): #{{{
        ld = len(d)
        if ld > 1:
            raise TypeError('setdefault expected at most 2 arguments, got %i' %ld+1)
        if k in self:
            return self[k]
        else:
            if d:
                d = d[0]
            else:
                d = None
            self[k] = d
            return d
    # End def #}}}

    def update(self, m, **kw): #{{{
        imap, obj = m, self._obj
        if isinstance(m, dict):
            imap = dict.iteritems()
        for k, v in imap:
            setattr(obj, k, v)
        for k, v in kw.iteritems():
            setattr(obj, k, v)
    # End def #}}}

    def pop(self, k, *d): #{{{
        ld, obj = len(d), self._obj
        delitem = self.__delitem__
        if ld > 1:
            raise TypeError('pop expected at most 2 arguments, got %i' %ld+1)
        ret = None
        if k in self:
            ret = self[k]
            delitem(k)
        elif d:
            ret = d[0]
        return ret
    # End def #}}}

    def popitem(self): #{{{
        ret = None
        for k in self.shallowkeys():
            ret = (k, self[k])
            break
        self.pop(ret[0])
        return ret
    # End def #}}}

    def has_key(self, k): #{{{
        return k in self
    # End def #}}}

    def get(self, k, *d): #{{{
        ld, obj = len(d), self._obj
        if ld > 1:
            raise TypeError('get expected at most 2 arguments, got %i' %ld+1)
        ret = None
        if k in self:
            ret = self[k]
        elif d:
            ret = d[0]
        return ret
    # End def #}}}

    def clear(self): #{{{
        popitem = self.popitem
        for k in list(self.shallowkeys()):
            popitem()
    # End def #}}}

    def copy(self): #{{{
        return dict((k, v) for k, v in self.iteritems())
    # End def #}}}

    def fromkeys(self, ad, *d): #{{{
        ld, obj = len(d), self._obj
        ret = None
        if ld > 1:
            raise TypeError('fromkeys expected at most 2 arguments, got %i' %ld+1)
        if d:
            ret = d[0]
        return dict((k, ret) for k in self)
    # End def #}}}
# End class #}}}


