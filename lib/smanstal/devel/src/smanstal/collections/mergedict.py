# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import ismapping, isiterable

__all__ = ('MergeDictMixin', 'mergedict')

class _mdm_alldictmaster: #{{{
    __slots__ = ('alldict',)
    def __init__(self): #{{{
        self.alldict = dict()
    # End def #}}}

    def __call__(self, od): #{{{
        return self.alldict[id(od)]
    # End def #}}}

    def register(self, od): #{{{
        self.alldict[id(od)] = []
    # End def #}}}

    def deregister(self, od): #{{{
        self.alldict.pop(id(od), None)
    # End def #}}}
# End class #}}}

_alldictmaster = _mdm_alldictmaster()

class MergeDictMixin(object): #{{{
    __slots__ = ()
    def __init__(self, *args, **kwargs): #{{{
        _alldictmaster.register(self)
        super(MergeDictMixin, self).__init__()
        self.merge(*args, **kwargs)
    # End def #}}}

    def __del__(self): #{{{
        _alldictmaster.deregister(self)
    # End def #}}}

    # To maintain internal consistency, setitem and delitem operations
    # will clear the merged items list
    def __setitem__(self, k, v): #{{{
        self._clearmerged()
        super(MergeDictMixin, self).__setitem__(k, v)
    # End def #}}}
    
    def __delitem__(self, k): #{{{
        self._clearmerged()
        super(MergeDictMixin, self).__delitem__(k)
    # End def #}}}

    def merge(self, *args, **kwargs): #{{{
        alldict = []
        adapp = alldict.append
        for a in args:
            if not ismapping(a):
                a = [(k, v) for k, v in a]
            if a:
                adapp(a)
        if kwargs:
            adapp(kwargs)
        if not alldict:
            return
        update = super(MergeDictMixin, self).update
        for d in alldict:
            update(d)
        self._alldict.extend(alldict)
#        sall = getattr(self, '_alldict', None)
#        if sall is None:
#            self._alldict = sall = []
#        sall.extend(alldict)
    # End def #}}}

    update = merge

    def clear(self): #{{{
        self._clearmerged()
        super(MergeDictMixin, self).clear()
    # End def #}}}

    def _clearmerged(self): #{{{
        self._alldict[:] = []
    # End def #}}}

    def clearmerged(self): #{{{
        ret = list(self._alldict)
        self._clearmerged()
        return ret
#        cur = getattr(self, '_alldict', None)
#        if cur is None:
#            return
#        delattr(self, '_alldict')
#        return cur
    # End def #}}}

    def remerge(self): #{{{
        cur = self._clearmerged()
        self.clear()
        self.merge(*cur)
    # End def #}}}

    def itermitems(self): #{{{
        return (i for d in self.merged for i in d)
    # End def #}}}

    def itermkeys(self): #{{{
        return (k for k, v in self.itermitems())
    # End def #}}}

    def itermvalues(self): #{{{
        return (v for k, v in self.itermitems())
    # End def #}}}

    def mitems(self): #{{{
        return list(self.itermitems())
    # End def #}}}

    def mkeys(self): #{{{
        return list(self.itermkeys())
    # End def #}}}

    def mvalues(self): #{{{
        return list(self.itermvalues())
    # End def #}}}

    # Properties #{{{
    merged = property(lambda s: ([(k, v) for k, v in (d.iteritems() if ismapping(d) else d)] for d in getattr(s, '_alldict', [])), 
            None, lambda s: s.clearmerged())
    _alldict = property(lambda s: _alldictmaster(s))
    # End properties #}}}
# End class #}}}

class mergedict(MergeDictMixin, dict): #{{{
    __slots__ = ()
# End class #}}}
