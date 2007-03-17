# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.multivalue import MultiValue

class Test_MultiValueInit(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoArgs(self): #{{{
        '''No init args raises error'''
        msg = re.compile("Cannot create empty mval")
        self.assertRaisesEx(ValueError, MultiValue, exc_pattern=msg)
    # End def #}}}

    def testStoreArgs(self): #{{{
        '''Any arguments passed in is stored'''
        expected = dict(red=1, blue=2)
        test = MultiValue(**expected)
        self.assertTrue(isinstance(getattr(test, '_mval', None), dict))
        self.assertEqual(test._mval, expected)
        self.assertTrue(test.p.mval is not test._mval)
        self.assertEqual(test.p.mval, test._mval)
    # End def #}}}

    def testStoreTransformer(self): #{{{
        '''Passing in a func'''
        def transform(k, v): #{{{
            if isinstance(v, int):
                return v + 1
            return v
        # End def #}}}
        test = MultiValue(red=1, blue=2)
        test.p.transformer = transform
        self.assertTrue(test._tfunc is transform)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

