# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from operator import itemgetter

# package imports
from eqobj.core import EqObj

__all__ = ('SetMixin', 'Set')

class SetMixin(object): #{{{
    __slots__ = ()

    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(SetMixin, self).__init__(self._init_transform(obj))
    # End def #}}}

    def _init_transform(self, obj): #{{{
        values, validators = set(), set()
        v1up, v2up = values.add, validators.add
        for k in obj:
            if isinstance(k, EqObj):
                v2up(k)
            else:
                v1up(k)
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
        options = ['trim', 'missing']
        expected = frozenset(options) | frozenset(expected)
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
        opt = self._trim_options(opt)
        opt = self._missing_options(opt)
        return opt
    # End def #}}}

    def __transform__(self, obj): #{{{
        return set(obj)
    # End def #}}}

    def __compare__(self, s, obj): #{{{
        options = self._options
        t, m = itemgetter('trim', 'missing')(options)
        valueset, validateset = s
        trim = obj - valueset
        missing = valueset - obj
        tadd, trem, missadd = trim.add, trim.discard, missing.add
        if missing and not m:
            return False
        for ok in frozenset(trim):
            for vk in validateset:
                if vk == ok:
                    trem(ok)
        if trim and not t:
            return False
        return True
    # End def #}}}
# End class #}}}

class Set(SetMixin, EqObj): #{{{
    __slots__ = ('_options',)
# End class #}}}
