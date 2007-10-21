# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.validators.type import InstanceType

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
                InstanceType(val)
            except TypeError, err:
                self.assertEqual(str(err).strip(), 'InstanceType objects can only initialize on class objects')
            else:
                self.assertTrue(False)
        InstanceType(int)
    # End def #}}}

    def test_simple_compare(self): #{{{
        '''Simple checks'''
        self.assertEqual(InstanceType(int), 42)
        self.assertNotEqual(InstanceType(int), '42')
        self.assertEqual(InstanceType(basestring), 'a')
        self.assertEqual(InstanceType(str), 'a')
        self.assertEqual(InstanceType(unicode), u'a')
        self.assertNotEqual(InstanceType(unicode), 'a')
        self.assertNotEqual(InstanceType(str), u'a')
    # End def #}}}

    def test_compound_compare(self): #{{{
        '''Can do OR comparison on tuple of classes'''
        a = InstanceType((int, str))
        self.assertEqual(a, 1)
        self.assertEqual(a, 'a')
        self.assertNotEqual(a, u'a')
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

