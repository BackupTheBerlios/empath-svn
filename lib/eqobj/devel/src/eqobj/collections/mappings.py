# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj
from eqobj.util import EqObjOptions, MaxCount

__all__ = ('MappingMixin', 'AnyKeyMixin', 'AnyKey', 'AllKeysMixin', 'AllKeys', 'MappingOptionMixin', 
            'TrimOption', 'MissingOption')

class MappingMixin(object): #{{{
    __slots__ = ()
    def __init__(self, obj=(), **kwargs): #{{{
        self._options = self._check_options(kwargs)
        super(MappingMixin, self).__init__(self.__transform__(obj))
    # End def #}}}

    def _check_options(self, opt, expected=()): #{{{
        expected = frozenset(['count']) | frozenset(expected)
        got = frozenset(opt)
        if not expected.issuperset(got):
            raise TypeError("Detected unknown keyword arguments: %s" %", ".join(got - expected))
        return opt
    # End def #}}}

    def __transform__(self, obj): #{{{
        return dict(obj)
    # End def #}}}

    def _cmp(self, s, obj, val, target, options): #{{{
        raise NotImplementedError
    # End def #}}}

    def _cmp_map(self, s, obj, target, options): #{{{
        raise NotImplementedError
    # End def #}}}

    def __compare__(self, s, obj, **override): #{{{
        options = dict(self._options)
        options.update(override)
        target = options.get('count', None)
        if target is not None and target != MaxCount:
            target = int(target)
            if target < 0:
                raise ValueError("count option must be >= 0: %i" %target)
        return self._cmp_map(s, obj, target, options)
    # End def #}}}
# End class #}}}

class AnyKeyMixin(MappingMixin): #{{{
    __slots__ = ()
    def _cmp(self, s, obj, val, target, options): #{{{
        if target is None:
            return bool(val) or not s
        elif target == MaxCount:
            return val == len(s)
        else:
            return val >= target
    # End def #}}}

    def _cmp_map(self, s, obj, target, options): #{{{
        c_len = 0
        for el in s:
            if el in obj:
                c_len += 1
        return self._cmp(s, obj, c_len, target, options)
    # End def #}}}
# End class #}}}

class AnyKey(AnyKeyMixin, EqObj): #{{{
    __slots__ = ('_options',)
# End class #}}}

class AllKeysMixin(AnyKeyMixin): #{{{
    __slots__ = ()
    def __init__(self, obj=(), **kwargs): #{{{
        kwargs.pop('count', None)
        super(AllKeysMixin, self).__init__(obj, **kwargs)
        self._options['count'] = MaxCount
    # End def #}}}

    def _cmp(self, s, obj, val, target, options): #{{{
        if len(s) != len(obj):
            return False
        return super(AllKeysMixin, self)._cmp(s, obj, val, target, options)
    # End def #}}}
# End class #}}}

class AllKeys(AllKeysMixin, EqObj): #{{{
    __slots__ = ('_options',)
# End class #}}}

class AnyValueMixin(MappingMixin): #{{{
    __slots__ = ()
    def _pre_cmp(self, s, obj, common, target, options): #{{{
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

    def _cmp_map(self, s, obj, target, options): #{{{
        common = [el for el in s if el in obj]
        if target == MaxCount:
            target = len(common)
        ret = self._pre_cmp(s, obj, common, target, options)
        if ret is not None:
            return ret
        cmp_count = self._cmp
        count = 0
        for el in common:
            if s[el] == obj[el]:
                count += 1
                ret = cmp_count(s, obj, count, target, options)
                if ret is not None:
                    return ret
        return self._post_cmp(s, obj, count, target, options)
    # End def #}}}
# End class #}}}

class AnyValue(AnyValueMixin, EqObj): pass

class AllValuesMixin(AnyValueMixin): #{{{
    __slots__ = ()
    def __init__(self, obj=(), **kwargs): #{{{
        kwargs.pop('count', None)
        super(AllValuesMixin, self).__init__(obj, **kwargs)
        self._options['count'] = MaxCount
    # End def #}}}

    def _pre_cmp(self, s, obj, common, target, options): #{{{
        if len(s) != len(obj):
            return False
    # End def #}}}
# End class #}}}

class AllValues(AllValuesMixin, EqObj): pass

class MappingOptionMixin(object): #{{{
    __slots__ = ()
    def __init__(self, *args, **kwargs): #{{{
        if not isinstance(self, MappingMixin):
            raise TypeError("MappingOptionMixin can only be used with MappingMixin objects")
        super(MappingOptionMixin, self).__init__(*args, **kwargs)
    # End def #}}}

    def _rmfunc(self, obj): #{{{
        return obj.pop
    # End def #}}}
# End class #}}}

class TrimOption(MappingOptionMixin): #{{{
    __slots__ = ()
    def _check_options(self, opt, expected=()): #{{{
        expected = ('trim',) + tuple(expected)
        return super(TrimOption, self)._check_options(opt, expected)
    # End def #}}}

    def _cmp_map(self, s, obj, target, options): #{{{
        trim = bool(options.get('trim', False))
        if trim:
            unknown = [el for el in obj if el not in s]
            objpop = self._rmfunc(obj)
            for el in unknown:
                objpop(el) 
        return super(TrimOption, self)._cmp_map(s, obj, target, options)
    # End def #}}}
# End class #}}}

class MissingOption(MappingOptionMixin): #{{{
    __slots__ = ()
    def _check_options(self, opt, expected=()): #{{{
        expected = ('missing',) + tuple(expected)
        return super(MissingOption, self)._check_options(opt, expected)
    # End def #}}}

    def _cmp_map(self, s, obj, target, options): #{{{
        missing = bool(options.get('missing', False))
        if missing:
            missing = [el for el in s if el not in obj]
            spop = self._rmfunc(s)
            for el in missing:
                spop(el) 
        return super(MissingOption, self)._cmp_map(s, obj, target, options)
    # End def #}}}
# End class #}}}
