# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from operator import itemgetter

# package imports
from eqobj.core import EqObj, IsObj

__all__ = ('MappingMixin', 'Mapping')

class MappingMixin(object): #{{{
    __slots__ = ()

    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(MappingMixin, self).__init__(self._init_transform(obj))
    # End def #}}}

    def _init_transform(self, obj): #{{{
        obj = dict(obj)
        exact = self._options['exact']
        def mkv(o): #{{{
            if exact:
                return IsObj(o)
            return o
        # End def #}}}
        values, validators = {}, {}
        for k, v in obj.iteritems():
            k = mkv(k)
            if isinstance(k, EqObj):
                validators[k] = v
            else:
                values[k] = v
        return (values, validators)
    # End def #}}}

    def _trim_options(self, opt): #{{{
        optget = opt.get
        trim = bool(optget('trim', False))
        opt['trim'] = trim
        return opt
    # End def #}}}

    def _missing_options(self, opt): #{{{
        optget = opt.get
        missing = bool(optget('missing', False))
        opt['missing'] = missing
        return opt
    # End def #}}}

    def _check_options(self, opt, expected=()): #{{{
        options = ['trim', 'missing', 'exact']
        expected = frozenset(options) | frozenset(expected)
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
        opt['exact'] = bool(opt.get('exact', False))
        opt = self._trim_options(opt)
        opt = self._missing_options(opt)
        return opt
    # End def #}}}

    def __transform__(self, obj): #{{{
        return dict(obj)
    # End def #}}}

    def __compare__(self, s, obj): #{{{
        options = self._options
        t, m = itemgetter('trim', 'missing')(options)
        valuemap, validatemap = s
        nomatch, trim, missing = set(), set(), set()
        tadd, missadd = trim.add, missing.add
        trem, nmadd, nmrem = trim.discard, nomatch.add, nomatch.discard
        # trim, nomatch
        for ok in obj:
            if ok not in valuemap:
                tadd(ok)
            else:
                if valuemap[ok] != obj[ok]:
                    nmadd(ok)
        # missing
        for vk in valuemap:
            if vk not in obj:
                missadd(vk)
        if missing and not m:
            return False
        for ok in obj:
            if ok in valuemap:
                if valuemap[ok] != obj[ok]:
                    nmadd(ok)
        for ok in (trim | nomatch):
            for vk, vv in validatemap.iteritems():
                if vk == ok:
                    trem(ok)
                    ov = obj[ok]
                    if vv != ov:
                        nmadd(ok)
                    else:
                        nmrem(ok)
        if nomatch or (trim and not t):
            return False
        return True
    # End def #}}}
# End class #}}}

class Mapping(MappingMixin, EqObj): #{{{
    __slots__ = ('_options',)
# End class #}}}
