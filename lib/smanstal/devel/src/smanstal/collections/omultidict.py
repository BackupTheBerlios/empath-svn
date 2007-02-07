# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.collections.odict import OrderedDictMixin
from smanstal.collections.multidict import MultiDictMixin

__all__ = ('omultidict',)

class omultidict(OrderedDictMixin, MultiDictMixin, dict): #{{{
    __slots__ = ('_keys',)
    def __str__(self): #{{{
        o = 'omultidict([%s])'
        t = ', '.join('(%s, %s)' %(repr(k), repr(v)) for k, v in self.iteritems())
        return o %t
    # End def #}}}

    def _setitem_keycheck(self, key): #{{{
        # Allow addition to internal key list even if key already
        # exists
        return True
    # End def #}}}

    def _itergetfunc(self): #{{{
        getall = self.getall
        count = list.count
        keys = self._keys
        def func(key, index): #{{{
            ind = count(keys[:index], key)
            try:
                return getall(key)[ind]
            except:
                raise Exception(key, index, ind, getall(key), keys)
        # End def #}}}
        return func
    # End def #}}}

    def _pop_removekey(self, key, *args, **kw): #{{{
        remove = self._keys.remove
        while 1:
            try:
                remove(key)
            except ValueError:
                break
    # End def #}}}
# End class #}}}
