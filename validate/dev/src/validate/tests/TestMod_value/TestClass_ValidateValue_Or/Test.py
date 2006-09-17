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

class TestValidateValue_Or(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleValueValidation(self): #{{{
        '''Simple value validation'''
        v = ValidateValue(1, 2, 3)
        for val in xrange(1, 4):
            self.assertEqual(v, val)
        for val in xrange(4, 10):
            self.assertNotEqual(v, val)
    # End def #}}}

    def testMixedValues(self): #{{{
        '''Mixing up Validate instances works'''
        vt = ValidateType(int, str)
        v = ValidateValue(1, 'hello') & vt
        input = [(1, True), ('hello', True), (1L, False), (u'hello', False), (vt, False)]
        for i, ret in input:
            self.assertEqual(v == i, ret)
    # End def #}}}
# End class #}}}

