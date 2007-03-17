# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.multivalue import MultiValue

class Test_getattr(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testInMultiValue(self): #{{{
        '''Return attr stored in enum'''
        test = MultiValue(red=1, blue=2)
        self.assertEqual(test.v.red, 1)
        self.assertEqual(test.v.blue, 2)
        self.assertRaisesEx(AttributeError, test.v.__getattribute__, 'wacky')
    # End def #}}}

    def testTransform(self): #{{{
        '''Transform values in enum'''
        def transform(k, v): #{{{
            if isinstance(v, int):
                return v + 1
            return v
        # End def #}}}
        test = MultiValue(red=1, blue=3)
        test.p.transformer = transform
        self.assertEqual(test.v.red, 2)
        self.assertEqual(test.v.blue, 4)
        self.assertEqual(test, 2)
        self.assertEqual(test, 4)
        self.assertNotEqual(test, 1)
        self.assertNotEqual(test, 3)
    # End def #}}}

    def testEqfunc(self): #{{{
        '''Function to test equality of two objects'''
        def eqfunc(s, o): #{{{
            return s.__class__ == o
        # End def #}}}
        test = MultiValue(red=1, white='hello')
        test.p.eqfunc = eqfunc
        self.assertNotEqual(test, 1)
        self.assertNotEqual(test, 'hello')
        self.assertEqual(test, int)
        self.assertEqual(test, str)

        test.p.eqfunc = test._mkeqfunc()

        self.assertEqual(test, 1)
        self.assertEqual(test, 'hello')
        self.assertNotEqual(test, int)
        self.assertNotEqual(test, str)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

