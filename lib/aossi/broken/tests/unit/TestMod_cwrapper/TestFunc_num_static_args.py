# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.cwrapper import num_static_args as nsa

class Test_num_static_args(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable returns (-1, None)'''
        self.assertEqual(nsa(1), (-1, None))
    # End def #}}}

    def testClass(self): #{{{
        '''Class objects are valid callables'''
        class _(object): 
            def __init__(self):
                pass
        self.assertEqual(nsa(_), (0, 0))
    # End def #}}}

    def testNonCallableObject(self): #{{{
        '''Object with non-method __call__'''
        class _(object): 
            __call__ = 1
        self.assertEqual(nsa(_()), (-1, None))
    # End def #}}}

    def testCallableWrapper(self): #{{{
        '''TODO - Passing a CallableWrapper object returns relevant attributes'''
        pass
    # End def #}}}

    def testVarArgs(self): #{{{
        '''Function with variable args'''
        t = lambda *a: None
        self.assertEqual(nsa(t), (0, None))
        t = lambda a, b, *c: None
        self.assertEqual(nsa(t), (2, None))
    # End def #}}}

    def testNoDefaults(self): #{{{
        '''Function with no default values'''
        t = lambda a, b, c: None
        self.assertEqual(nsa(t), (3, 3))
    # End def #}}}

    def testDefaults(self): #{{{
        '''Function with default values'''
        t = lambda a, b, c=1, d=2: None
        self.assertEqual(nsa(t), (2, 4))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

