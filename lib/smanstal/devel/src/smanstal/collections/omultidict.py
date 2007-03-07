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

    def __iter__(self): #{{{
        return iter(k for k, i in self._keys)
    # End def #}}}

    def _add_key(self, key): #{{{
        ind = self.getlen(key)
        key = (key, ind-1)
        super(omultidict, self)._add_key(key)
    # End def #}}}

    def _setitem_keycheck(self, key): #{{{
        # Allow addition to internal key list even if key already
        # exists
        return True
    # End def #}}}

    def _itergetfunc(self): #{{{
        keys = self._keys
        get = self.get
        def func(index): #{{{
            key, ind = keys[index]
            return get(key, index=ind)
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
