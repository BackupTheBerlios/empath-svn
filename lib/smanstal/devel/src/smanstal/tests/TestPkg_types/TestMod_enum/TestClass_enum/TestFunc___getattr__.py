# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.enum import Enum

class Test_getattr(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testInEnum(self): #{{{
        '''Return attr stored in enum'''
        test = Enum(red=1, blue=2)
        self.assertEqual(test.red, 1)
        self.assertEqual(test.blue, 2)
        self.assertRaisesEx(AttributeError, test.__getattr__, 'wacky')
    # End def #}}}

    def testTransform(self): #{{{
        '''Transform values in enum'''
        def transform(k, v): #{{{
            if isinstance(v, int):
                return v + 1
            return v
        # End def #}}}
        test = Enum(red=1, blue=3)
        test.transformer_ = transform
        self.assertEqual(test.red, 2)
        self.assertEqual(test.blue, 4)
        self.assertEqual(test, 2)
        self.assertEqual(test, 4)
        self.assertNotEqual(test, 1)
        self.assertNotEqual(test, 3)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

