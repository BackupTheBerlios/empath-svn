# Module: eqobj.core
# File: core.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('EqObj',)

class EqObj(object): #{{{
    __slots__ = ('_EqObj__initobj',)

    def __init__(self, obj=None): #{{{
        self.__initobj = obj
    # End def #}}}

    def __transform__(self, obj): #{{{
        return obj
    # End def #}}}

    def __compare__(self, obj): #{{{
        raise NotImplementedError
    # End def #}}}

    def __call__(self, *args): #{{{
        obj = self.__initobj
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
        return not(self.__eq__)
    # End def #}}}

    def __nonzero__(self): #{{{
        return self()
    # End def #}}}
# End class #}}}
