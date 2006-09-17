# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.value import *
from validate.base import *
from validate.type import *

class TestValidateValueSequence(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleValueValidation(self): #{{{
        '''Simple sequence value validation'''
        v = ValidateValueSequence(1, 2, 3)
        val = [1, 2, 3]
        self.assertEqual(v, val)
    # End def #}}}

    def testSubSequence(self): #{{{
        '''Validate a sequence containing a sequence'''
        v = ValidateValueSequence(1, [3, 4, 5], 2)
        val = [1, [3, 4, 5], 2]
        self.assertEqual(v, val)
    # End def #}}}

    def testAndOperation(self): #{{{
        '''Even just one non-validating value will cause validation failure'''
        v = ValidateValueSequence(1, [3, 4, 5], 2)
        val = [1, [3, 4, 'hello'], 2]
        self.assertNotEqual(v, val)
    # End def #}}}
# End class #}}}

