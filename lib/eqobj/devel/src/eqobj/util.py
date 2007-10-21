# Module: eqobj.util
# File: util.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from types import (FunctionType as function, BuiltinFunctionType as bfunction, 
        MethodType as method, BuiltinMethodType as bmethod, ClassType)

from eqobj.core import EqObj

__all__ = ('AlwaysTrue', 'AlwaysFalse', 'EqObjOptions', 'EqObjWritableOptions', 'MaxCount')

def isclass(obj): #{{{
    return isinstance(obj, ClassType) or hasattr(obj, '__bases__')
# End def #}}}

def isobjclass(obj): #{{{
    return isinstance(obj, object) and isinstance(obj, type) and isclass(obj)
# End def #}}}

def iscallable(obj): #{{{
    return bool(isinstance(obj, (function, bfunction, method, bmethod)) or
                isclass(obj) or 
                hasattr(obj, '__call__'))
# End def #}}}

def mro(cls): #{{{
    if isobjclass(cls):
        return cls.mro()
    def calc_mro(curcls): #{{{
        if curcls is cls:
            yield cls
        for b in curcls.__bases__:
            yield b
            for c in calc_mro(b):
                yield c
    # End def #}}}
    return [c for c in calc_mro(cls)]
# End def #}}}

class AlwaysBooleanType(EqObj): #{{{
    __slots__ = ()
# End class #}}}

class AlwaysTrueType(AlwaysBooleanType): #{{{
    __slots__ = ()
    def __compare__(self, s, obj): #{{{
        return True
    # End def #}}}
# End class #}}}

AlwaysTrue = AlwaysTrueType()

class AlwaysFalseType(AlwaysBooleanType): #{{{
    __slots__ = ()
    def __compare__(self, s, obj): #{{{
        return False
    # End def #}}}
# End class #}}}

AlwaysFalse = AlwaysFalseType()

