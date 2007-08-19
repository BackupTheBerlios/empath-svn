# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

class CollectionMixin(object): #{{{
    __slots__ = ()
    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(CollectionMixin, self).__init__(self.__transform__(obj))
    # End def #}}}

    def _check_options(self, opt, expected=()): #{{{
        expected = frozenset(['count']) | frozenset(expected)
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
        return opt
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

    def __transform__(self, obj): #{{{
        return tuple(obj)
    # End def #}}}

    def __compare__(self, s, obj, **override): #{{{
        options = dict(self._options)
        options.update(override)
        target = options.get('count', None)
        if target is not None and target != MaxCount:
            target = int(target)
            if target < 0:
                raise ValueError("count option must be >= 0: %i" %target)
        return self._cmp_loop(s, obj, target, options)
    # End def #}}}
# End class #}}}

