# Module: eqobj.collections.sequences
# File: sequences.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from math import ceil
from operator import itemgetter

# package imports
from eqobj.core import EqObj, IsObj

__all__ = ('SequenceMixin', 'Sequence')

class SequenceMixin(object): #{{{
    __slots__ = ()

    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(SequenceMixin, self).__init__(self._init_transform(obj))
    # End def #}}}

    def _init_transform(self, obj): #{{{
        exact = self._options['exact']
        def mkv(o): #{{{
            if exact:
                return IsObj(o)
            return o
        # End def #}}}
        return tuple(mkv(o) for o in obj)
    # End def #}}}

    def _trim_options(self, opt): #{{{
        optget = opt.get
        strim = (ltrim, rtrim) = optget('ltrim', None), optget('rtrim', None)
        trim = optget('trim', None)
        if trim and all(v is None for v in strim):
            ltrim = rtrim = trim = True
        else:
            ltrim, rtrim = map(bool, strim)
            trim = bool(trim)
        opt.update(trim=trim, ltrim=ltrim, rtrim=rtrim)
        return opt
    # End def #}}}

    def _missing_options(self, opt): #{{{
        optget = opt.get
        smissing = (lmissing, rmissing) = optget('lmissing', None), optget('rmissing', None)
        missing = optget('missing', None)
        if missing and all(v is None for v in smissing):
            lmissing = rmissing = missing = True
        else:
            lmissing, rmissing = map(bool, smissing)
            missing = bool(missing)
        opt.update(missing=missing, lmissing=lmissing, rmissing=rmissing)
        return opt
    # End def #}}}

    def _repeat_options(self, opt): #{{{
        for name in ('repeat', 'pad'):
            option = opt.get(name, False)
            if not isinstance(option, (int, slice, bool)):
                raise TypeError('%s keyword: Expected one of int, slice, boolean object, got %s instead' %(name, option.__class__.__name__))
            elif not isinstance(option, bool) and isinstance(option, int) and option <= 0:
                opt[name] = 1
            else:
                opt[name] = option
        return opt
    # End def #}}}

    def _check_options(self, opt, expected=()): #{{{
        options = ['trim', 'ltrim', 'rtrim', 'missing', 'lmissing', 'rmissing', 'repeat', 'pad', 'exact']
        expected = frozenset(options) | frozenset(expected)
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
        opt['exact'] = bool(opt.get('exact', False))
        opt = self._trim_options(opt)
        opt = self._missing_options(opt)
        opt = self._repeat_options(opt)
        return opt
    # End def #}}}

    def __transform__(self, obj): #{{{
        return tuple(obj)
    # End def #}}}

    def _unequal_lengths(self, big, small, options): #{{{
        ltrim, rtrim, repeat = options
        blen, slen = map(len, [big, small])
        if blen != slen and not any([ltrim, rtrim]) and repeat is False:
            return big, small, False
        if slen and repeat:
            if isinstance(repeat, bool):
                repeat = int(ceil(float(blen) / slen))
                small = (small * repeat)[:blen]
            elif isinstance(repeat, slice):
                frag = small[repeat]
                if frag:
                    gap = blen - slen
                    repeat = int(ceil(float(gap) / len(frag)))
                    small = (small + (frag * repeat))[:blen]
            else:
                small = small * repeat
        return big, small, True
    # End def #}}}

    def _cmp_loop(self, small, big, options): #{{{
        ltrim, rtrim, repeat = options
        slen, blen = map(len, [small, big])
        maxstart = (blen - slen) if ltrim else 0
        lastind = slen-1
        ret = None
        for i in xrange(0, maxstart+1):
            for sind, bind in enumerate(xrange(i, slen+i)):
                lastind = bind
                if small[sind] != big[bind]:
                    break
            else:
                ret = True
                break
            ret = False
        return (ret and (rtrim or (lastind+1) == blen))
    # End def #}}}

    def __compare__(self, s, obj): #{{{
        options = self._options
        names = ['ltrim', 'rtrim', 'lmissing', 'rmissing', 'repeat', 'pad']
        ltrim, rtrim, lmissing, rmissing, repeat, pad = itemgetter(*names)(options)
        slen, olen = map(len, [s, obj])
        big = small = opt = None
        if olen < slen:
            small, big, opt = obj, s, (lmissing, rmissing, pad)
        else:
            small, big, opt = s, obj, (ltrim, rtrim, repeat)
        if olen != slen:
            big, small, res = self._unequal_lengths(big, small, opt)
            if not res:
                return False
        return self._cmp_loop(small, big, opt)
    # End def #}}}
# End class #}}}

class Sequence(SequenceMixin, EqObj): #{{{
    __slots__ = ('_options',)
# End class #}}}
