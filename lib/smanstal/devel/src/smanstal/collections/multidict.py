# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from smanstal.types.introspect import ismapping

__all__ = ('MultiDictMixin', 'multidict')

class MultiDictMixin(object): #{{{
    __slots__ = ()
    def __init__(self, *args, **kwargs): #{{{
        super(MultiDictMixin, self).__init__()
        arglen = len(args)
        if arglen == 1:
            if isinstance(args[0], dict):
                self.update(args[0])
            else:
                setitem = self.__setitem__
                for k, v in args[0]:
                    setitem(k, v)
            self.update(kwargs)
        elif arglen == 0:
            self.update(kwargs)
        else:
            self.update(*args, **kwargs)
    # End def #}}}

    def __setitem__(self, key, val): #{{{
        setdefault = super(MultiDictMixin, self).setdefault
        setdefault(key, []).append(val)
    # End def #}}}

    def __getitem__(self, key): #{{{
        v = super(MultiDictMixin, self).__getitem__(key)
        return list(v)
    # End def #}}}

    def __copy__(self): #{{{
        return self.__class__(self)
    # End def #}}}

    def copy(self): #{{{
        return self.__copy__()
    # End def #}}}

    def items(self): #{{{
        return list(self.iteritems())
    # End def #}}}

    def values(self): #{{{
        return list(self.itervalues())
    # End def #}}}
    
    def iterkeys(self): #{{{
        return self.__iter__()
    # End def #}}}
    
    def itervalues(self): #{{{
        return (v for k, v in self.iteritems())
    # End def #}}}
    
    def iteritems(self): #{{{
        supiter = super(MultiDictMixin, self).iteritems()
        return ((k, v) for k, vlist in supiter for v in vlist)
    # End def #}}}

    def fromkeys(self, seq, value=None): #{{{
        md = self.__class__()
        for k in seq:
            md[k] = value
        return md
    # End def #}}}
    
    # 1 arg: normal dict pop
    # 2 arg: normal dict pop
    # 3 arg: key, index, default pop
    def pop(self, *args, **kw): #{{{
        lenargs = len(args)
        if lenargs > 3:
            raise TypeError('pop expected at most 3 arguments, got %i' %lenargs)
        pop = super(MultiDictMixin, self).pop
        k = i = d = ()
        if not lenargs:
            return pop()
        elif lenargs < 3:
            k = (args[0],)
            d = (args[1],) if lenargs == 2 else d
            temp = kw.get('index', None)
            i = (temp,) if temp is not None else i
        else:
            k, i, d = tuple((a,) for a in args) 
        key = k[0]
        if key not in self:
            if not d:
                raise KeyError(key)
            return d[0]
        if i:
            supget = super(MultiDictMixin, self).__getitem__
            vlist = supget(key)
            try:
                ret = vlist.pop(int(i[0]))
            except:
                if not d:
                    raise
                ret = d[0]
            return ret
        else:
            return pop(key, *d)
    # End def #}}}

    # 1 arg: normal dict get
    # 2 arg: normal dict get
    # 3 arg: key, index, default get
    def get(self, *args, **kw): #{{{
        lenargs = len(args)
        if not lenargs or lenargs > 3:
            raise TypeError('get expected at between 1 and 3 arguments, got %i' %lenargs)
        get = super(MultiDictMixin, self).get
        k = i = d = None
        if lenargs < 3:
            i = int(kw.get('index', 0))
            k, d = (args[0], [None]) if lenargs == 1 else (args[0], [args[1]])
        else:
            k, i, d = args
        return get(k, d)[i]
    # End def #}}}

    def getall(self, key, *d): #{{{
        len_d = len(d)
        if len_d > 1:
            raise TypeError('getall expected 1 or 2 arguments, got %i' %len_d)
        d = [] if not d else d[0]
        get = super(MultiDictMixin, self).get
        ret = list(get(key, []))
        return d if not ret else ret
    # End def #}}}

    # 1 arg: normal dict setdefault
    # 2 arg: normal dict setdefault
    # 3 arg: key, index, default setdefault
    def setdefault(self, *args, **opt): #{{{
        setm = bool(opt.get('setmissing', False))
        lenargs = len(args)
        if not lenargs or lenargs > 3:
            raise TypeError('setdefault expected between 1 and 3 arguments, got %i' %lenargs)
        setdefault = super(MultiDictMixin, self).setdefault
        ret = None
        if lenargs < 3:
            args = (args[0], [None]) if lenargs == 1 else (args[0], [args[1]])
            ret = setdefault(*args)
        else:
            k, i, d = args
            ret = setdefault(k, [])
            curlen = len(ret)
            if i < 0:
                i = curlen - i
            if i >= curlen:
                if not setm and i > curlen:
                    raise IndexError("setmissing == False: can only set for index == %i" %curlen)
                diff = (i - curlen) + 1
                ret.extend([d]*diff)
            else:
                ret[i] = d
        return list(ret)
    # End def #}}}

    def update(self, *args, **kw): #{{{
        new = {}
        setitem = self.__setitem__
        if args:
            largs = len(args)
            if largs > 1:
                cname = self.__class__.__name__
                raise TypeError('%s expected at most 1 arguments, got %i' %(cname, largs))
            args = args[0]
            seq = args.iteritems() if ismapping(args) else iter(args)
            for k, v in seq:
                setitem(k, v)
        if kw:
            for k, v in kw.iteritems():
                setitem(k, v)
    # End def #}}}

    def add(self, key, val): #{{{
        self.__setitem__(key, val)
    # End def #}}}

    def replace(self, key, vals): #{{{
        vals = list(vals)
        self.pop(key)
        add = self.add
        for v in vals:
            add(key, v)
    # End def #}}}

    def change(self, key, index, val): #{{{
        if key not in self:
            raise KeyError(key)
        get = super(MultiDictMixin, self).get
        vals = get(key)
        vals[index] = val
    # End def #}}}
# End class #}}}

class multidict(MultiDictMixin, dict): #{{{
    __slots__ = ()
# End class #}}}
