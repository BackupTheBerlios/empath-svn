# Module: smanstal.types.mdict
# File: mdict.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import ismapping, isiterable

__all__ = ('mdict',)

class mdict(dict): #{{{
    __slots__ = ('_alldict',)
    def __init__(self, *args, **kwargs): #{{{
        super(mdict, self).__init__()
        self.merge(*args, **kwargs)
    # End def #}}}

    def merge(self, *args, **kwargs): #{{{
        alldict = []
        for a in args:
            if not ismapping(a):
                a = dict(a)
            alldict.append(a)
        if kwargs:
            alldict.append(kwargs)
        if not alldict:
            return
        for d in alldict:
            super(mdict, self).update(d)
        sall = getattr(self, '_alldict', None)
        if sall is None:
            self._alldict = sall = []
        sall.extend(alldict)
    # End def #}}}

    update = merge

    def clear(self): #{{{
        self.clearmerged()
        super(mdict, self).clear()
    # End def #}}}

    def clearmerged(self): #{{{
        cur = getattr(self, '_alldict', None)
        if cur is None:
            return
        delattr(self, '_alldict')
        return cur
    # End def #}}}

    def remerge(self): #{{{
        cur = self.clearmerged()
        self.clear()
        self.merge(*cur)
    # End def #}}}

    def itermitems(self): #{{{
        alldict = getattr(self, '_alldict', [])
        return (i for d in alldict for i in d.iteritems())
    # End def #}}}

    def itermkeys(self): #{{{
        return (k for k, v in self.itermitems())
    # End def #}}}

    def itermvalues(self): #{{{
        return (v for k, v in self.itermitems())
    # End def #}}}

    def mitems(self): #{{{
        return [i for i in self.itermitems()]
    # End def #}}}

    def mkeys(self): #{{{
        return [k for k, v in self.itermitems()]
    # End def #}}}

    def mvalues(self): #{{{
        return [v for k, v in self.itermitems()]
    # End def #}}}

    # Properties #{{{
    merged = property(lambda s: tuple(getattr(s, '_alldict', [])), None, lambda s: s.clearmerged())
    # End properties #}}}
# End class #}}}

class mlist(list): #{{{
    __slots__ = ('_alllist',)
    def __init__(self, *iterables): #{{{
        super(mlist, self).__init__()
        self.merge(*iterables)
    # End def #}}}

    def merge(self, *iterables): #{{{
        if not iterables:
            return
        for l in iterables:
            super(mlist, self).extend(l)
        sall = getattr(self, '_alldict', None)
        if sall is None:
            self._alllist = sall = []
        sall.extend(el for el in iterables)
    # End def #}}}

    update = merge

    def clear(self): #{{{
        self.clearmerged()
        while self:
            self.pop()
    # End def #}}}

    def clearmerged(self): #{{{
        cur = getattr(self, '_alllist', None)
        if cur is None:
            return
        delattr(self, '_alllist')
        return cur
    # End def #}}}

    def remerge(self): #{{{
        cur = self.clearmerged()
        self.clear()
        self.merge(*cur)
    # End def #}}}

    # Properties #{{{
    merged = property(lambda s: tuple(getattr(s, '_alllist', [])), None, lambda s: s.clearmerged())
    # End properties #}}}
# End class #}}}
