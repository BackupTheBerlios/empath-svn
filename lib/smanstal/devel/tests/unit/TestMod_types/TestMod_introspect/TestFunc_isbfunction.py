# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.introspect import isbfunction

class Test_isbfunction(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testPythonFunction(self): #{{{
        '''Pure python function returns False'''
        self.assertFalse(isbfunction(isbfunction))
    # End def #}}}

    def testBuiltinFunction(self): #{{{
        '''Built-in function returns True'''
        self.assertTrue(isbfunction(max))
    # End def #}}}

    def testMethod(self): #{{{
        '''Method returns False'''
        class Test(object): #{{{
            def test(self): pass
        # End class #}}}
        self.assertFalse(isbfunction(Test.test))
    # End def #}}}

    def testCallable(self): #{{{
        '''Arbitrary non-function callable returns False'''
        class Test(object): #{{{
            def __call__(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        for c in (Test, Test()):
            self.assertFalse(isbfunction(c))
    # End def #}}}

    def testPythonObject(self): #{{{
        '''Arbitrary object returns False'''
        self.assertFalse(isbfunction(1))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

