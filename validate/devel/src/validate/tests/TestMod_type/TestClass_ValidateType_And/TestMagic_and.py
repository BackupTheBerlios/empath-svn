# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.type import ValidateType_Or, ValidateType_And

class TestAnd(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testReturnVTInst(self): #{{{
        '''Returns ValidateType_And instance'''
        v1 = ValidateType_And(int)
        v2 = ValidateType_And(str)
        v = v1 & v2
        self.assert_(isinstance(v, ValidateType_And))
    # End def #}}}
# End class #}}}

