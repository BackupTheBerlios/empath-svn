# Module: validate.value
# File: value.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the validate project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from validate.base import Validate, Validate_And, Validate_Or, callobj

__all__ = ('ValidateValue', 'ValidateValue_Or', 'ValidateValue_And',
            'ValidateValueSequence', 'ValidateValueSequence_Or', 'ValidateValueSequence_And',
            'vv', 'vv_and', 'vv_or', 'vvseq', 'vvseq_and', 'vvseq_or',
            'vvmap', 'vvmap_and', 'vvmap_or')

class _BaseValidateValue(object): #{{{
    __slots__ = ()

    def __init__(self, *vobj, **options): #{{{
        if self.__class__ == _BaseValidateValue:
            raise NotImplementedError("_BaseValidateValue is an abstract class")
    # End def #}}}

    def __and__(self, obj): #{{{
        return ValidateValue_And(self, obj)
    # End def #}}}

    def __or__(self, obj): #{{{
        return ValidateValue_Or(self, obj)
    # End def #}}}
# End class #}}}

class ValidateValue_Or(_BaseValidateValue, Validate_Or): #{{{
    __slots__ = tuple()
    def __init__(self, *vobj, **options): #{{{
        super(ValidateValue_Or, self).__init__(*vobj, **options)
        Validate_Or.__init__(self, *vobj, **options)
    # End def #}}}
# End class #}}}

ValidateValue = ValidateValue_Or

class ValidateValue_And(_BaseValidateValue, Validate_And): #{{{
    __slots__ = tuple()
    def __init__(self, *vobj, **options): #{{{
        super(ValidateValue_And, self).__init__(*vobj, **options)
        Validate_And.__init__(self, *vobj, **options)
    # End def #}}}
# End class #}}}

class _BaseValidateValueSequence(object): #{{{
    __slots__ = ()
    def __init__(self, *vobj, **options): #{{{
        if self.__class__ == _BaseValidateValueSequence:
            raise NotImplementedError("_BaseValidateValueSequence is an abstract class")
        old_options = dict(options)
        shrink_type = shrink_target = bool(options.pop('shrink', False))
        shrink_type = bool(options.pop('shrink_type', shrink_type))
        shrink_target = bool(options.pop('shrink_target', shrink_target))
        if options.get('exact', False):
            shrink_type = shrink_target = False
        opt = dict(shrink_type=shrink_type, shrink_target=shrink_target)
        self._set_options(*opt.items())
        valid = self._valid_seq
        def check_vobj(vobj): #{{{
            for vo in vobj:
                v = valid(vo)
                if v:
                    try:
                        yield self.__class__(*v, **old_options)
                    except:
                        raise TypeError("Detected non-Validate instance, non-sequence argument")
                else:
                    yield vo
        # End def #}}}

        vobj = tuple(vo for vo in check_vobj(vobj))
        super(_BaseValidateValueSequence, self).__init__(*vobj, **options)
    # End def #}}}

    def __eq__(self, obj): #{{{
        try:
            olen = len(obj)
        except TypeError:
            return False
        opt = self.options
        slen = len(self._stored)
        vobj = self._stored
        if slen < olen and opt['shrink_target']:
            obj = obj[:slen]
        elif slen > olen and opt['shrink_type']:
            vobj = vobj[:olen]
        elif slen != olen:
            return False
        result = self._validate_single_result
        try:
            ret = self._validate_results(result(vobj[i], obj[i]) for i in xrange(olen))
        except:
            return False
        return ret
    # End def #}}}

    def _valid_seq(self, seq): #{{{
        if isinstance(seq, basestring):
            return None
        ret = []
        try:
            ret = [i for i in seq]
        except TypeError:
            return None
        return ret
    # End def #}}}

    def _validate(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateValueSequence, self)._validate(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-Validate instance, non-type, non-sequence argument")
    # End def #}}}

    def _validate_exact(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateValueSequence, self)._validate_exact(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-Validate instance, non-type, non-sequence argument")
    # End def #}}}
# End class #}}}

class ValidateValueSequence_Or(_BaseValidateValueSequence, ValidateValue_Or): #{{{
    __slots__ = tuple()
# End class #}}}

class ValidateValueSequence_And(_BaseValidateValueSequence, ValidateValue_And): #{{{
    __slots__ = tuple()
# End class #}}}

ValidateValueSequence = ValidateValueSequence_And

class _BaseValidateValueMapping(object): #{{{
    __slots__ = ()
    def __init__(self, *vobj, **options): #{{{
        if self.__class__ == _BaseValidateValueMapping:
            raise NotImplementedError("_BaseValidateValueMapping is an abstract class")
        old_options = dict(options)
        missingkw_type = missingkw_target = bool(options.pop('missingkw', False))
        missingkw_type = bool(options.pop('missingkw_type', missingkw_type))
        missingkw_target = bool(options.pop('missingkw_target', missingkw_target))
        if options.get('exact', False):
            missingkw_type = missingkw_target = False
        opt = dict(missingkw_type=missingkw_type, missingkw_target=missingkw_target)
        self._set_options(*opt.items())
        validmap = self._valid_map
        def check_vobj(vobj): #{{{
            if len(vobj) == 1:
                v = vobj[0]
                m = getattr(v, 'iteritems', None)
                if m:
                    vobj = m()
            try:
                for k, vo in vobj:
                    if validmap(vo):
                        yield k, self.__class__(vo, **old_options)
                    else:
                        yield k, vo
            except:
                raise TypeError("Detected non-ValidateValue instance, non-type, non-mapping argument")
        # End def #}}}

        vobj = tuple(vo for vo in check_vobj(vobj))
        super(_BaseValidateValueMapping, self).__init__(*vobj, **options)
    # End def #}}}

    def __eq__(self, obj): #{{{
        o_set = None
        try:
            obj = dict(obj)
            o_set = set(obj.keys())
        except TypeError:
            return False
        vobj = dict(self._stored)
        vo_set = set(vobj.keys())
        miss_vo = set(kw for kw in vo_set if kw not in o_set)
        miss_o = set(kw for kw in o_set if kw not in vo_set)
        common = vo_set & o_set
        opt = self.options
        if miss_vo and not opt['missingkw_type']:
            return False
        if miss_o and not opt['missingkw_target']:
            return False

        result = self._validate_single_result
        try:
            ret = self._validate_results(result(vobj[kw], obj[kw]) for kw in common)
        except:
            return False
        return ret
    # End def #}}}

    def _valid_map(self, vobj): #{{{
        try:
            dict(vobj)
        except (TypeError, ValueError):
            return False
        return True
    # End def #}}}

    def _validate(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateValueMapping, self)._validate(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-ValidateValue instance, non-type, non-mapping argument")
    # End def #}}}

    def _validate_exact(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateValueMapping, self)._validate_exact(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-ValidateValue instance, non-type, non-mapping argument")
    # End def #}}}
# End class #}}}

class ValidateValueMapping_Or(_BaseValidateValueMapping, ValidateValue_Or): #{{{
    __slots__ = tuple()
# End class #}}}

class ValidateValueMapping_And(_BaseValidateValueMapping, ValidateValue_And): #{{{
    __slots__ = tuple()
# End class #}}}

ValidateValueMapping = ValidateValueMapping_And

# Short name aliases
vv = vv_or = ValidateValue
vv_and = ValidateValue_And

vvseq = vvseq_and = ValidateValueSequence_And
vvseq_or = ValidateValueSequence_Or

vvmap = vvmap_and = ValidateValueMapping_And
vvmap_or = ValidateValueMapping_Or
