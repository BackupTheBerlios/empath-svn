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

    def _pre_cmp(self, self_obj, obj, count): #{{{
        raise NotImplementedError
    # End def #}}}

    def _cmp(self, val, count): #{{{
        raise NotImplementedError
    # End def #}}}

    def _post_cmp(self, val, count): #{{{
        raise NotImplementedError
    # End def #}}}

    def _cmp_loop(self, s, obj, target, options): #{{{
        raise NotImplementedError
    # End def #}}}
# End class #}}}

class EqAnyElement(EqSequence): #{{{
    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(EqAnyElement, self).__init__(obj)
    # End def #}}}

    def _check_options(self, opt, expected=()): #{{{
        expected = frozenset(['count']) | frozenset(expected)
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
        return opt
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

    def _cmp_loop(self, s, obj, target, options): #{{{
        if not s and not obj:
            return (isinstance(target, int) and not target)
        sb = {len(s): s, len(obj): obj}
        if len(sb) == 1:
            small, big, sblen = s, obj, ((sb.keys()[0],)*2)
        else:
            sblen = sorted(sb)
            small = sb.pop(sblen[0])
            big = sb.pop(sblen[1])
        pre = self._pre_cmp(s, obj, target)
        if pre is not None:
            return pre
        cmp_count, count = self._cmp, 0
        for i in xrange(sblen[0]):
            if small[i] == big[i]:
                count += 1
                ret = cmp_count(count, target)
                if ret is not None:
                    return ret
        return self._post_cmp(count , target)
    # End def #}}}

    def __compare__(self, obj, **override): #{{{
        options = dict(self._options)
        options.update(override)
        target = options.get('count', None)
        if target is not None:
            target = int(target)
            if target < 0:
                raise ValueError("count option must be >= 0: %i" %target)
        s = self._initobj
        return self._cmp_loop(s, obj, target, options)
    # End def #}}}

    options = EqObjOptions()
# End class #}}}

class AnyElement(EqAnyElement, EqObj): pass

class EqAllElements(EqAnyElement): #{{{
    def __init__(self, obj=(), **kwargs): #{{{
        kwargs.pop('count', None)
        super(EqAllElements, self).__init__(obj, **kwargs)
        self._options['count'] = len(self._initobj)
    # End def #}}}

    def _pre_cmp(self, self_obj, obj, count): #{{{
        if len(self_obj) != len(obj):
            return False
    # End def #}}}
# End class #}}}

class AllElements(EqAllElements, EqObj): pass

class TrimOption(object): #{{{
    def _check_options(self, opt, expected=()): #{{{
        expected = ('trim_head', 'trim_tail', 'trim') + expected
        optget = opt.get
        th = optget('trim_head', None)
        tt = optget('trim_tail', None)
        t = optget('trim', None)
        t = t if (th is None and tt is None) else bool(th and tt)
        opt['trim_head'] = th
        opt['trim_tail'] = tt
        opt['trim'] = t
        return super(TrimOption, self)._check_options(opt, expected)
    # End def #}}}

    def _trim_head(self, s, obj, options): #{{{
        compare = super(TrimOption, self)._cmp_loop
        obj_len, s_len = len(obj), len(s)
        min_end = obj_len - (obj_len - s_len)
        max_start = (obj_len - min_end)+1
        for i in xrange(max_start):
            if compare(s, obj[i:min_end+i], s_len, options):
                return (True, min_end+i)
        return (False, None)
    # End def #}}}

    def _cmp_loop(self, s, obj, target, options): #{{{
        cmp_loop = super(TrimOption, self)._cmp_loop
        obj_len, s_len = len(obj), len(s)
        opt = options.get
        th = opt('trim_head', None)
        tt = opt('trim_tail', None)
        t = opt('trim', None)
        if obj_len > s_len and (th or tt or t):
            if target < s_len:
                s_len = target
            ret, end = False, len(obj)
            if th:
                ret, end = self._trim_head(s, obj, options)
            else:
                ret, end = cmp_loop(s, obj[:s_len], s_len, options), s_len
            if tt:
                return ret
            else:
                return (end == obj_len)
        return cmp_loop(s, obj, target, options)
    # End def #}}}
# End class #}}}

class MissingOption(TrimOption): #{{{
    def _check_options(self, opt, expected=()): #{{{
        expected = ('missing_head', 'missing_tail', 'missing') + expected
        optget = opt.get
        th = optget('missing_head', None)
        tt = optget('missing_tail', None)
        t = optget('missing', None)
        t = t if (th is None and tt is None) else bool(th and tt)
        opt['missing_head'] = th
        opt['missing_tail'] = tt
        opt['missing'] = t
        return super(TrimOption, self)._check_options(opt, expected)
    # End def #}}}

    def _cmp_loop(self, s, obj, target, options): #{{{
        obj_len, s_len = len(obj), len(s)
        cmp_loop = super(MissingOption, self)._cmp_loop

        opt = options.pop
        trimopt = {}
        trimopt['trim_head'] = th = opt('missing_head', None)
        trimopt['trim_tail'] = tt = opt('missing_tail', None)
        trimopt['trim'] = t = opt('missing', None)
        if obj_len < s_len and (th or tt or t):
            return cmp_loop(obj, s, target, trimopt)
        return cmp_loop(s, obj, target, options)
    # End def #}}}
# End class #}}}
