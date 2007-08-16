# Module: eqobj.util
# File: util.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj

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
