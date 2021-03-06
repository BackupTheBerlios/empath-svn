# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.validators.type import SubType

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_class_check(self): #{{{
        '''init checks if object is a class'''
        test = [1, 'a', 1.5]
        for val in test:
            try:
                SubType(val)
            except TypeError, err:
                self.assertEqual(str(err).strip(), 'SubType objects can only initialize on class objects')
            else:
                self.assertTrue(False)
        SubType(int)
    # End def #}}}

    def test_simple_compare(self): #{{{
        '''Simple checks'''
        class A(object): pass
        class B(A): pass
        class C(object): pass
        self.assertNotEqual(SubType(int), 42)
        self.assertEqual(SubType(int), int)
        self.assertEqual(SubType(A), A)
        self.assertNotEqual(SubType(B), A)
        self.assertEqual(SubType(A), B)
        self.assertNotEqual(SubType(C), A)
    # End def #}}}

    def test_compound_compare(self): #{{{
        '''Can do OR comparison on tuple of classes'''
        class A(int): pass
        class B(str): pass
        a = SubType((int, str))
        self.assertEqual(a, A)
        self.assertEqual(a, B)
        self.assertNotEqual(a, unicode)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

