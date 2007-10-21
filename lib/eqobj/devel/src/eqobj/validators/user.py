# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj
from eqobj.util import iscallable

__all__ = ('UserDefined',)

class UserDefined(EqObj): #{{{
    __slots__ = ()
    def __init__(self, obj): #{{{
        if not iscallable(obj):
            raise TypeError("UserDefined objects can only accept callable objects")
        super(UserDefined, self).__init__(obj)
    # End def #}}}

    def __compare__(self, s, obj): #{{{
        return s(obj)
    # End def #}}}
# End class #}}}
