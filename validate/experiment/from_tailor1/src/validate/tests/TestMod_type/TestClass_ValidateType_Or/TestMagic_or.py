# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.type import ValidateType_Or, ValidateType_And

class TestOr(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testReturnVTInst(self): #{{{
        '''Returns ValidateType_Or instance'''
        v1 = ValidateType_Or(int)
        v2 = ValidateType_Or(str)
        v = v1 | v2
        self.assert_(isinstance(v, ValidateType_Or))
    # End def #}}}
# End class #}}}

