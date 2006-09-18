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

class TestValidateValueSequence_Or(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleValueValidation(self): #{{{
        '''Simple value validation'''
        v = ValidateValueSequence_Or(1, 2, 3)
        val = [1, 2, 3]
        self.assertEqual(v, val)
    # End def #}}}

    def testSubSequence(self): #{{{
        '''Validate a sequence containing a sequence'''
        v = ValidateValueSequence_Or(1, [3, 4, 5], 2)
        val = [1, [3, 4, 5], 2]
        self.assertEqual(v, val)
    # End def #}}}

    def testOrOperation(self): #{{{
        '''Just a single valid value validates'''
        v = ValidateValueSequence_Or(1, 2, 3)
        val = [1, 4, 5]
        self.assertEqual(v, val)
    # End def #}}}
# End class #}}}

