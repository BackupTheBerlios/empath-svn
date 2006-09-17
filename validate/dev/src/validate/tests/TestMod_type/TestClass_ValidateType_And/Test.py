# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.type import ValidateType, ValidateType_And

class TestValidateType(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleTest(self): #{{{
        '''Simple type validation'''
        v = ValidateType_And(int)
        self.assertEqual(v, 1)
    # End def #}}}

    def testSimpleExactTest(self): #{{{
        '''Simple exact type validation'''
        v = ValidateType_And(str, exact=True)
        self.assertEqual(v, 'hello')

        v = ValidateType_And(basestring, exact=True)
        self.assertNotEqual(v, 'hello')

        v = v(basestring, exact=False)
        self.assertEqual(v, 'hello')
    # End def #}}}

    def testValidateMulti(self): #{{{
        '''Put together multiple ValidateType instances'''
        v = ValidateType_And(basestring, str)
        self.assertEqual(v, 'hello')
        self.assertNotEqual(v, u'hello')

        self.assertNotEqual(u'hello', v)
        self.assertEqual('hello', v)

        self.assertNotEqual(v, 1)
        self.assertNotEqual(v, 1.23)
        self.assertNotEqual(v, ValidateType)
    # End def #}}}
# End class #}}}

