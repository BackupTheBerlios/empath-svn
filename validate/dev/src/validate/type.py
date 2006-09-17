# Module: validate.type
# File: type.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the validate project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from validate.base import Validate, Validate_And, Validate_Or, callobj, ReturnBoolean, valTrue
from types import ClassType

__all__ = ('ValidateType', 'ValidateType_Or', 'ValidateType_And', 
            'ValidateTypeSequence', 'ValidateTypeSequence_Or', 'ValidateTypeSequence_And',
            'ValidateTypeMapping', 'ValidateTypeMapping_Or', 'ValidateTypeMapping_And',
            'vt', 'vt_and', 'vt_or', 'vtseq', 'vtseq_and', 'vtseq_or',
            'vtmap', 'vtmap_and', 'vtmap_or')

def _istype(obj): #{{{
    return (isinstance(obj, type) or isinstance(obj, ClassType) or 
                hasattr(obj, '__bases__'))
# End def #}}}

class _BaseValidateType(object): #{{{
    __slots__ = ()

    def __init__(self, *vobj, **options): #{{{
        if self.__class__ == _BaseValidateType:
            raise NotImplementedError("_BaseValidateType is an abstract class")
        valid = self._valid_vobj
        if [vo for vo in vobj if not valid(vo)]:
            raise TypeError("Detected non-ValidateType instance, non-type argument")
        super(_BaseValidateType, self).__init__(*vobj, **options)
    # End def #}}}

    def __and__(self, obj): #{{{
        return ValidateType_And(self, obj)
    # End def #}}}

    def __or__(self, obj): #{{{
        return ValidateType_Or(self, obj)
    # End def #}}}

    def _valid_vobj(self, vobj): #{{{
        return _istype(vobj) or self._isvalidatetype(vobj) or isinstance(vobj, callobj)
    # End def #}}}

    def _isvalidatetype(self, obj): #{{{
        return isinstance(obj, _BaseValidateType) or isinstance(obj, ReturnBoolean)
    # End def #}}}

    def _validate(self, vobj, obj): #{{{
        if not self._valid_vobj(vobj):
            raise TypeError("Detected non-ValidateType instance, non-type argument")
        elif self._isvalidatetype(vobj):
            return vobj == obj
        return isinstance(obj, vobj)
    # End def #}}}

    def _validate_exact(self, vobj, obj): #{{{
        if not self._valid_vobj(vobj):
            raise TypeError("Detected non-ValidateType instance, non-type argument")
        elif self._isvalidatetype(vobj):
            return vobj == obj
        return obj.__class__ == vobj
    # End def #}}}
# End class #}}}

class ValidateType_Or(_BaseValidateType, Validate_Or): #{{{
    __slots__ = ()
# End class #}}}

ValidateType = ValidateType_Or

class ValidateType_And(_BaseValidateType, Validate_And): #{{{
    __slots__ = ()
# End class #}}}

class _BaseValidateTypeSequence(object): #{{{
    __slots__ = ()

    def __init__(self, *vobj, **options): #{{{
        if self.__class__ is _BaseValidateTypeSequence:
            raise NotImplementedError("_BaseValidateTypeSequence is an abstract class")
        old_options = dict(options)
        shallow = bool(options.get('shallow', False))
        shrink_type = shrink_target = bool(options.pop('shrink', False))
        shrink_type = bool(options.pop('shrink_type', shrink_type))
        shrink_target = bool(options.pop('shrink_target', shrink_target))
        if options.get('exact', False):
            shrink_type = shrink_target = False
        opt = dict(shrink_type=shrink_type, shrink_target=shrink_target)
        self._set_options(*opt.items())
        valid = self._valid_vobj
        def check_vobj(vobj): #{{{
            for vo in vobj:
                if not valid(vo):
                    if isinstance(vo, basestring):
                        raise TypeError("Detected non-ValidateType instance, non-type, non-sequence argument")
                    try:
                        if shallow:
                            tuple(vel for vel in vo)
                            yield self.__class__(**old_options)
                        else:
                            yield self.__class__(*tuple(vel for vel in check_vobj(vo)), **old_options)
                    except:
                        raise TypeError("Detected non-ValidateType instance, non-type, non-sequence argument")
                else:
                    yield vo
        # End def #}}}

        vobj = tuple(vo for vo in check_vobj(vobj))
        super(_BaseValidateTypeSequence, self).__init__(*vobj, **options)
    # End def #}}}

    def __eq__(self, obj): #{{{
        # Count a string as an atom
        if isinstance(obj, basestring):
            return False
        try:
            olen = len(obj[:])
        except TypeError:
            return False
        vobj = self._stored
        if not vobj and self._shallow:
            return True
        slen = len(vobj)
        opt = self.options
        if slen < olen and opt['shrink_target']:
            obj = obj[:slen]
            olen = slen
        elif slen > olen and opt['shrink_type']:
            vobj = vobj[:olen]
        elif slen != olen:
            return False
        elif not vobj:
            return True
        result = self._validate_single_result
        try:
            ret = self._validate_results(result(vobj[i], obj[i]) for i in xrange(olen))
        except:
            return False
        return ret
    # End def #}}}

    def _validate(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateTypeSequence, self)._validate(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-ValidateType instance, non-type, non-sequence argument")
    # End def #}}}

    def _validate_exact(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateTypeSequence, self)._validate_exact(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-ValidateType instance, non-type, non-sequence argument")
    # End def #}}}
# End class #}}}

class ValidateTypeSequence_Or(_BaseValidateTypeSequence, ValidateType_Or): #{{{
    __slots__ = ()
# End class #}}}

class ValidateTypeSequence_And(_BaseValidateTypeSequence, ValidateType_And): #{{{
    __slots__ = ()
# End class #}}}

ValidateTypeSequence = ValidateTypeSequence_And

class _BaseValidateTypeMapping(object): #{{{
    __slots__ = ()

    def __init__(self, *vobj, **options): #{{{
        if self.__class__ is _BaseValidateTypeMapping:
            raise NotImplementedError("_BaseValidateTypeMapping is an abstract class")
        old_options = dict(options)
        shallow = bool(options.get('shallow', False))
        missingkw_type = missingkw_target = bool(options.pop('missingkw', False))
        missingkw_type = bool(options.pop('missingkw_type', missingkw_type))
        missingkw_target = bool(options.pop('missingkw_target', missingkw_target))
        if options.get('exact', False):
            missingkw_type = missingkw_target = False
        opt = dict(missingkw_type=missingkw_type, missingkw_target=missingkw_target)
        self._set_options(*opt.items())
        valid = self._valid_vobj
        validseq = self._valid_seq
        def check_vobj(vobj): #{{{
            if len(vobj) == 1:
                v = vobj[0]
                m = getattr(v, 'iteritems', None)
                if m:
                    vobj = tuple(m())
            try:
                for k, vo in vobj:
                    if validseq(vo, True):
                        if shallow:
                            vo = self.__class__(**old_options)
                        else:
                            vo = self.__class__(*vo, **old_options)
                        yield k, vo
                    elif valid(vo, True):
                        yield k, vo
                    else:
                        gen = getattr(vo, 'items', vo)
                        if gen is not vo:
                            gen = gen()
                        tup = tuple(i for i in check_vobj(gen))
                        if shallow:
                            vo = self.__class__(**old_options)
                        else:
                            vo = self.__class__(*tup, **old_options)
                        yield k, vo
            except:
                raise TypeError("Detected non-ValidateType instance, non-type, non-mapping argument")
        # End def #}}}

        vobj = tuple(vo for vo in check_vobj(vobj))
        super(_BaseValidateTypeMapping, self).__init__(*vobj, **options)
    # End def #}}}

    def __eq__(self, obj): #{{{
        o_set = None
        try:
            obj = dict(obj)
            o_set = set(obj.keys())
        except TypeError, err:
            return False
        vobj = dict(self._stored)
        if not vobj:
            return self._shallow or not bool(o_set)
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

    def _valid_seq(self, vobj, init=False): #{{{
        if isinstance(vobj, basestring):
            return False
        k, v = None, None
        try:
            if init:
                return True in (self._valid_vobj(v) for k, v in vobj)
            k, v = vobj
        except (TypeError, ValueError):
            return False
        return self._valid_vobj(v, init)
    # End def #}}}

    def _valid_vobj(self, vobj, init=False): #{{{
        return super(_BaseValidateTypeMapping, self)._valid_vobj(vobj) or self._valid_seq(vobj, init)
    # End def #}}}

    def _validate(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateTypeMapping, self)._validate(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-ValidateType instance, non-type, non-mapping argument")
    # End def #}}}

    def _validate_exact(self, vobj, obj): #{{{
        try:
            return super(_BaseValidateTypeMapping, self)._validate_exact(vobj, obj)
        except TypeError:
            raise TypeError("Detected non-ValidateType instance, non-type, non-mapping argument")
    # End def #}}}
# End class #}}}

class ValidateTypeMapping_Or(_BaseValidateTypeMapping, ValidateType_Or): #{{{
    __slots__ = ()
# End class #}}}

class ValidateTypeMapping_And(_BaseValidateTypeMapping, ValidateType_And): #{{{
    __slots__ = ()
# End class #}}}

ValidateTypeMapping = ValidateTypeMapping_And

# Short name aliases
vt = vt_or = ValidateType
vt_and = ValidateType_And

vtseq = vtseq_and = ValidateTypeSequence_And
vtseq_or = ValidateTypeSequence_Or

vtmap = vtmap_and = ValidateTypeMapping_And
vtmap_or = ValidateTypeMapping_Or
