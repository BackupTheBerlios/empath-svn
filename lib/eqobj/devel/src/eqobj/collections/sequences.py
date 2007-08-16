# Module: eqobj.collections.sequences
# File: sequences.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj
from eqobj.util import EqObjOptions

__all__ = ('EqAnyElement', 'AnyElement', 'EqAllElements', 'AllElements')

class EqSequence(object): #{{{
    def __init__(self, obj=()): #{{{
        super(EqSequence, self).__init__(self.__transform__(obj))
    # End def #}}}

    def __transform__(self, obj): #{{{
        return tuple(obj)
    # End def #}}}

# End class #}}}

class EqAnyElement(EqSequence): #{{{
    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(EqAnyElement, self).__init__(obj)
    # End def #}}}

    def _check_options(self, opt, expected=()): #{{{
        expected = frozenset(['count']) | expected
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
    # End def #}}}

    def _pre_cmp(self, self_obj, obj, count): #{{{
        if min([len(o) for o in (self_obj, obj)]) < count:
            return False
    # End def #}}}

    def _cmp(self, val, count): #{{{
        if count is None and val > 0:
            return True
        elif val > count:
            return False
    # End def #}}}

    def _post_cmp(self, val, count): #{{{
        return val == count
    # End def #}}}

    def __compare__(self, obj): #{{{
        opt = self._options.get
        count_opt = opt('count', None)
        if count_opt is not None:
            count_opt = int(count_opt)
            if count_opt < 0:
                raise ValueError("count option must be >= 0: %i" %count_opt)
        count = 0
        s = self._initobj
        if not s and not obj:
            return (isinstance(count_opt, int) and not count_opt)
        sb = {len(s): s, len(obj): obj}
        if len(sb) == 1:
            small, big, sblen = s, obj, ((sb.keys()[0],)*2)
        else:
            sblen = sorted(sb)
            small = sb.pop(sblen[0])
            big = sb.pop(sblen[1])
        pre = self._pre_cmp(s, obj, count_opt)
        if pre is not None:
            return pre
        cmp_count = self._cmp
        for i in xrange(sblen[0]):
            if small[i] == big[i]:
                count += 1
                ret = cmp_count(count, count_opt)
                if ret is not None:
                    return ret
        return self._post_cmp(count , count_opt)
    # End def #}}}

    options = EqObjOptions()
# End class #}}}

class AnyElement(EqAnyElement, EqObj): pass

class EqAllElements(EqAnyElement): #{{{
    def __init__(self, obj=()): #{{{
        super(EqAllElements, self).__init__(obj)
        self._options['count'] = len(self._initobj)
    # End def #}}}

    def _pre_cmp(self, self_obj, obj, count): #{{{
        if len(self_obj) != len(obj):
            return False
    # End def #}}}
# End class #}}}

class AllElements(EqAllElements, EqObj): pass
