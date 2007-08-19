# Module: eqobj.util
# File: util.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj

__all__ = ('AlwaysTrue', 'AlwaysFalse', 'EqObjOptions', 'EqObjWritableOptions', 'MaxCount')

class AlwaysTrue(EqObj): #{{{
    def __compare__(self, s, obj): #{{{
        return True
    # End def #}}}
# End class #}}}

class AlwaysFalse(EqObj): #{{{
    def __compare__(self, s, obj): #{{{
        return False
    # End def #}}}
# End class #}}}

class EqObjOptions(object): #{{{
    __slots__ = ('_options',)
    def __init__(self, inst=None): #{{{
        if inst:
            self._options = inst._options
    # End def #}}}

    def __get__(self, inst, owner): #{{{
        return self.__class__(inst)
    # End def #}}}

    def __getattr__(self, name): #{{{
        try:
            return self._options[name]
        except KeyError:
            raise AttributeError("%s object has no attribute '%s'" %(self.__class__.__name__, name))
    # End def #}}}

    def __getitem__(self, name): #{{{
        return self._options[name]
    # End def #}}}
# End class #}}}

class EqObjWritableOptions(EqObjOptions): #{{{
    __slots__ = ()
    def __setitem__(self, name, val): #{{{
        self._option[name] = val
    # End def #}}}

    def __setattr__(self, name, val): #{{{
        self._option[name] = val
    # End def #}}}
# End class #}}}

class MaxCountType(object): #{{{
    __slots__ = ()
# End class #}}}

MaxCount = MaxCountType()

