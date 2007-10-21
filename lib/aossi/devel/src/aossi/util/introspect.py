# Module: aossi.util
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

#from aossi.impex import import_, CopyModuleImporter
#_ab = import_(':aossi:__builtin__', importer=CopyModuleImporter(copy_prefix=':aossi:'))

#from weakref import ref
from inspect import isfunction, ismethod, isbuiltin
from types import (FunctionType as function, BuiltinFunctionType as bfunction, 
        MethodType as method, BuiltinMethodType as bmethod, ClassType)

__all__ = ('isclass', 'iscallable', 'isiterable', 'ismapping',
            'isreadonly', 'isfunction', 'ismethod', 'isbuiltin',
            'isobjclass', 'mro')
# ==================================================================================
# Introspection functions
# ==================================================================================
def isclass(obj): #{{{
    return isinstance(obj, ClassType) or hasattr(obj, '__bases__')
# End def #}}}

def iscallable(obj): #{{{
    return bool(isinstance(obj, (function, bfunction, method, bmethod)) or
                isclass(obj) or 
                hasattr(obj, '__call__'))
# End def #}}}

def isiterable(obj): #{{{
    return isinstance(obj, basestring) or (not isclass(obj) and 
            iscallable(getattr(obj, '__iter__', None)))
# End def #}}}

def ismapping(obj): #{{{
    if isinstance(obj, dict):
        return True
    check = ('items', 'keys', 'values')
    check += tuple('iter' + c for c in check)
    check += ('__getitem__',)
    return False not in (iscallable(getattr(obj, n, None)) for n in check)
# End def #}}}

def isreadonly(obj, aname, attr): #{{{
    ret = False
    try:
        setattr(obj, aname, attr)
    except:
        ret = True
    return ret
# End def #}}}

def isobjclass(obj): #{{{
    return isinstance(obj, object) and isinstance(obj, type) and isclass(obj)
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
