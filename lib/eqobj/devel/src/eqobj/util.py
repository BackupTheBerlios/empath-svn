# Module: eqobj.util
# File: util.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj

__all__ = ('AlwaysTrue', 'AlwaysFalse', 'EqObjOptions', 'EqObjWritableOptions')

class AlwaysTrue(EqObj): #{{{
    def __compare__(self, obj): #{{{
        return True
    # End def #}}}
# End class #}}}

class AlwaysFalse(EqObj): #{{{
    def __compare__(self, obj): #{{{
        return False
    # End def #}}}
# End class #}}}

class EqObjOptions(object): #{{{
    def __get__(self, inst, owner): #{{{
        self._options = inst._options
        return self
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
    def __setitem__(self, name, val): #{{{
        self._option[name] = val
    # End def #}}}
# End class #}}}
