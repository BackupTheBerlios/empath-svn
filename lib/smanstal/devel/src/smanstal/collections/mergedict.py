# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import ismapping, isiterable

__all__ = ('MergeDictMixin', 'mergedict')

class MergeDictMixin(object): #{{{
    __slots__ = ()
    def __init__(self, *args, **kwargs): #{{{
        super(MergeDictMixin, self).__init__()
        self.merge(*args, **kwargs)
    # End def #}}}

    # To maintain internal consistency, setitem and delitem operations
    # will clear the merged items list
    def __setitem__(self, k, v): #{{{
        self.clearmerged()
        super(MergeDictMixin, self).__setitem__(k, v)
    # End def #}}}
    
    def __delitem__(self, k): #{{{
        self.clearmerged()
        super(MergeDictMixin, self).__delitem__(k)
    # End def #}}}

    def merge(self, *args, **kwargs): #{{{
        alldict = []
        for a in args:
            if not ismapping(a):
                a = [(k, v) for k, v in a]
            if a:
                alldict.append(a)
        if kwargs:
            alldict.append(kwargs)
        if not alldict:
            return
        for d in alldict:
            super(MergeDictMixin, self).update(d)
        sall = getattr(self, '_alldict', None)
        if sall is None:
            self._alldict = sall = []
        sall.extend(alldict)
    # End def #}}}

    update = merge

    def clear(self): #{{{
        self.clearmerged()
        super(MergeDictMixin, self).clear()
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
    # End properties #}}}
# End class #}}}

class mergedict(MergeDictMixin, dict): #{{{
    __slots__ = ('_alldict',)
# End class #}}}
