# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.validators.type import ObjectType

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_init_check(self): #{{{
        '''init should accept any object'''
        test = [1, 'a', 1.5]
        for val in test:
            try:
                ObjectType(val)
            except:
                raise
                self.assertTrue(False)
        ObjectType(int)
#    # End def #}}}

    def test_all_subclass(self): #{{{
        '''Will do an OR comparison of an object against all subclasses of the initialized object'''
        class A(object): pass
        class B(A): pass
        class C(A): pass
        class D(B): pass
        class E(object): pass

        obj = ObjectType(B)
        self.assertEqual(obj, C)
        self.assertEqual(obj, D)
        self.assertNotEqual(obj, E)
    # End def #}}}

    def test_instances(self): #{{{
        '''Can validate on instances'''
        obj = ObjectType(basestring)
        self.assertEqual(obj, str)
        self.assertEqual(obj, 'Hello')
        self.assertEqual(obj, u'World')
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

