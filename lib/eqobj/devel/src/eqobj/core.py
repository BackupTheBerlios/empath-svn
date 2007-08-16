# Module: eqobj.core
# File: core.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('EqObj', 'Invert')

_obj_getattr = object.__getattribute__

class EqObj(object): #{{{
    __slots__ = ('_initobj',)

    def __init__(self, obj=None): #{{{
        self._initobj = obj
    # End def #}}}

    def __transform__(self, obj): #{{{
        return obj
    # End def #}}}

    def __compare__(self, obj): #{{{
        raise NotImplementedError
    # End def #}}}

    def __call__(self, *args): #{{{
        obj = self._initobj
        if len(args) > 1:
            raise TypeError("EqObj callables only accepts one argument")
        if args:
            obj = args[0]
        return self.__eq__(obj)
    # End def #}}}

    def __eq__(self, obj): #{{{
        obj = self.__transform__(obj)
        return self.__compare__(obj)
    # End def #}}}

    def __ne__(self, obj): #{{{
        return not self.__eq__
    # End def #}}}

    def __invert__(self): #{{{
        return Invert(self)
    # End def #}}}

    def __nonzero__(self): #{{{
        return self()
    # End def #}}}
# End class #}}}

class Invert(EqObj): #{{{
    def __getattribute__(self, name): #{{{
        if name in ('__init__', '__eq__'):
            return _obj_getattr(self, name)
        return getattr(self._initobj, name)
    # End def #}}}

    def __init__(self, obj): #{{{
        if not hasattr(obj, '__eq__'):
            raise TypeError("Invert only supports objects that have a __eq__ method")
        super(Invert, self).__init__(obj)
    # End def #}}}

    def __eq__(self, obj): #{{{
        return not self._initobj.__eq__(obj)
    # End def #}}}
# End class #}}}
