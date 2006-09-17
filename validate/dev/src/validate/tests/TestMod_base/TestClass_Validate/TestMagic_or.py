# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.base import Validate, BooleanValidate, Validate_Or

class TestOr(unittest.TestCase): #{{{
    def setUp(self): #{{{
        class v(Validate): pass
        self.v = v
    # End def #}}}

    def tearDown(self): #{{{
        del self.v
    # End def #}}}

    def testOrInstance(self): #{{{
        '''Bit-wise or for two Validate instances returns Validate_Or instance'''
        v1 = self.v(1)
        v2 = self.v(1)
        self.assert_(v1 is not v2)
        v = v1 | v2
        self.assert_(isinstance(v, BooleanValidate))
        self.assert_(isinstance(v, Validate_Or))
        self.assertEqual(v.stored, (v1, v2))
    # End def #}}}

    def testOrOperation(self): #{{{
        '''Oring two Validate instances returns valid Validate_Or instance'''
        v1 = self.v(1)
        v2 = self.v(1)

        v = v1 | v2
        self.assertEqual(v, 1)

        v1 = self.v(1)
        v2 = self.v(2)
        v = v1 | v2
        self.assertEqual(v, 1)
        self.assertEqual(v, 2)

        self.assertNotEqual(v, 'hello')
    # End def #}}}
# End class #}}}

