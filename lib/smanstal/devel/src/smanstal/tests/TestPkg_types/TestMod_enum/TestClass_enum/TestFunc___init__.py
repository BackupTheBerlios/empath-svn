# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.enum import Enum

class Test_EnumInit(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoArgs(self): #{{{
        '''No init args raises error'''
        msg = re.compile("Cannot create empty enum")
        self.assertRaisesEx(ValueError, Enum, exc_pattern=msg)
    # End def #}}}

    def testStoreArgs(self): #{{{
        '''Any arguments passed in is stored'''
        expected = dict(red=1, blue=2)
        test = Enum(**expected)
        self.assertTrue(isinstance(getattr(test, '_enum', None), dict))
        self.assertEqual(test._enum, expected)
        self.assertTrue(test.enum_ is not test._enum)
        self.assertEqual(test.enum_, test._enum)
    # End def #}}}

    def testStoreTransformer(self): #{{{
        '''Passing in a func'''
        def transform(k, v): #{{{
            if isinstance(v, int):
                return v + 1
            return v
        # End def #}}}
        test = Enum(red=1, blue=2)
        test.transformer_ = transform
        self.assertTrue(test.transformer_ is transform)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

