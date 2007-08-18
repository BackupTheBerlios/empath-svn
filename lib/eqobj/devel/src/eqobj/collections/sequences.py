# Module: eqobj.collections.sequences
# File: sequences.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj
from eqobj.util import EqObjOptions, MaxCount

__all__ = ('MaxCount', 'AnyElementMixin', 'AnyElement', 'AllElementsMixin', 'AllElements', 
            'ExtrapolateOption')

class SequenceMixin(object): #{{{
    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(SequenceMixin, self).__init__(self.__transform__(obj))
    # End def #}}}

    def _check_options(self, opt, expected=()): #{{{
        expected = frozenset(['count']) | frozenset(expected)
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
        return opt
    # End def #}}}

    def __transform__(self, obj): #{{{
        return tuple(obj)
    # End def #}}}

    def _pre_cmp(self, s, obj, target, options): #{{{
        raise NotImplementedError
    # End def #}}}

    def _cmp(self, s, obj, val, target, options): #{{{
        raise NotImplementedError
    # End def #}}}

    def _post_cmp(self, s, obj, val, target, options): #{{{
        raise NotImplementedError
    # End def #}}}

    def _cmp_loop(self, s, obj, target, options): #{{{
        raise NotImplementedError
    # End def #}}}
# End class #}}}

class AnyElementMixin(SequenceMixin): #{{{
    def _pre_cmp(self, s, obj, target, options): #{{{
        if not s:
            return not target
        elif isinstance(target, int) and len(s) < target:
            return False
    # End def #}}}

    def _cmp(self, s, obj, val, target, options): #{{{
        if target is None and val > 0:
            return True
        elif val >= target:
            return True
    # End def #}}}

    def _post_cmp(self, s, obj, val, target, options): #{{{
        if target is None:
            return bool(val)
        return val == target
    # End def #}}}

    def _cmp_loop(self, s, obj, target, options): #{{{
        s_len, o_len = len(s), len(obj)
        small_len, big_len = sorted((s_len, o_len))
        if target == MaxCount:
            target = s_len
        pre = self._pre_cmp(s, obj, target, options)
        if pre is not None:
            return pre
        cmp_count, count = self._cmp, 0
        for i in xrange(small_len):
            if s[i] == obj[i]:
                count += 1
                ret = cmp_count(s, obj, count, target, options)
                if ret is not None:
                    return ret
        return self._post_cmp(s, obj, count, target, options)
    # End def #}}}

    def __compare__(self, obj, **override): #{{{
        options = dict(self._options)
        options.update(override)
        target = options.get('count', None)
        if target is not None and target != MaxCount:
            target = int(target)
            if target < 0:
                raise ValueError("count option must be >= 0: %i" %target)
        s = self._initobj
        return self._cmp_loop(s, obj, target, options)
    # End def #}}}

    options = EqObjOptions()
# End class #}}}

class AnyElement(AnyElementMixin, EqObj): pass

class AllElementsMixin(AnyElementMixin): #{{{
    def __init__(self, obj=(), **kwargs): #{{{
        kwargs.pop('count', None)
        super(AllElementsMixin, self).__init__(obj, **kwargs)
        self._options['count'] = MaxCount
    # End def #}}}

    def _pre_cmp(self, s, obj, target, options): #{{{
        if len(s) != len(obj):
            return False
    # End def #}}}
# End class #}}}

class AllElements(AllElementsMixin, EqObj): pass

class SequenceOptionMixin(object): #{{{
    def __init__(self, *args, **kwargs): #{{{
        if not isinstance(self, SequenceMixin):
            raise TypeError("SequenceOptionMixin can only be used with SequenceMixin objects")
        super(SequenceOptionMixin, self).__init__(*args, **kwargs)
    # End def #}}}
# End class #}}}

class TrimOption(SequenceOptionMixin): #{{{
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
            if target == MaxCount:
                target = s_len
            elif target < s_len:
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
        if isinstance(self, ExtrapolateOption):
            trimopt['extrapolate'] = False
        if obj_len < s_len and (th or tt or t):
            return cmp_loop(obj, s, target, trimopt)
        return cmp_loop(s, obj, target, options)
    # End def #}}}
# End class #}}}

class ExtrapolateOption(SequenceOptionMixin): #{{{
    def _check_options(self, opt, expected=()): #{{{
        expected = ('extrapolate',) + expected
        return super(ExtrapolateOption, self)._check_options(opt, expected)
    # End def #}}}

    def _cmp_loop(self, s, obj, target, options): #{{{
        cmp_loop = super(ExtrapolateOption, self)._cmp_loop
        obj_len, s_len = len(obj), len(s)
        ex = bool(options.get('extrapolate', False))
        if ex and s_len < obj_len:
            if isinstance(target, int):
                if target < s_len:
                    s_len = target
            ret, end = False, len(obj)
            ret = cmp_loop(s, obj[:s_len], s_len, options)
            if ret and s:
                t = target
                if target is None:
                    return True
                elif target == MaxCount:
                    t = s_len
                cmp_count = self._cmp
                last = s[-1]
                ret = self._pre_cmp(s, obj, s_len, options)
                if ret is not None:
                    return ret
                count = s_len
                for i in xrange(s_len, obj_len):
                    if last == obj[i]:
                        count += 1
                        if target == MaxCount:
                            t = count
                        ret = cmp_count(s, obj, count, t, options)
                        if ret is not None:
                            return ret
                return self._post_cmp(s, obj, count, t, options)
            return ret
        return cmp_loop(s, obj, target, options)
    # End def #}}}
# End class #}}}
