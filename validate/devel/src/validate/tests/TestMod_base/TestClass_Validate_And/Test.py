# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.base import Validate_And

class TestValidateAnd(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testMultipleArgs(self): #{{{
        '''BooleanValidate instances can accept multiple arguments'''
        try:
            Validate_And(1, 2, 3)
            self.assert_(True)
        except:
            self.assert_(False)
    # End def #}}}

    def testAllValidate(self): #{{{
        '''All validating input'''
        v = Validate_And(*tuple(1 for x in xrange(10)))
        self.assert_(v == 1)
    # End def #}}}

    def testSomeValidate(self): #{{{
        '''Few that validate overall returns False'''
        v = Validate_And(*tuple(x for x in xrange(10)))
        self.assert_(True not in (v == x for x in xrange(10)))
    # End def #}}}

    def testNoneValidate(self): #{{{
        '''No validation'''
        v = Validate_And(*tuple(x for x in xrange(10)))
        self.assertNotEqual(v, 12)
    # End def #}}}
# End class #}}}

