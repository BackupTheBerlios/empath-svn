# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite


from eqobj.collections.sequences import Sequence

class Test_compare(BaseUnitTest): #{{{
#    def setUp(self): #{{{
#        self.c = AnyElement([1, 2, 3, 'a', 'b', 'c'])
#    # End def #}}}

#    def tearDown(self): #{{{
#        pass
#    # End def #}}}

    def test_simple(self): #{{{
        '''Simple compare'''
        a = Sequence(range(10))
        self.assertNotEqual(a, [1])
        self.assertNotEqual(a, [2])
        self.assertEqual(a, range(10))
    # End def #}}}

    def test_ltrim(self): #{{{
        '''Small self, left trim'''
        a = Sequence(range(10), ltrim=True)
        self.assertEqual(a, range(10))
        self.assertEqual(a, [100] + range(10))
    # End def #}}}

    def test_rtrim(self): #{{{
        '''Small self, right trim'''
        a = Sequence(range(10))
        self.assertNotEqual(a, range(10) + [100])

        a = Sequence(range(10), rtrim=True)
        self.assertEqual(a, range(10))
        self.assertEqual(a, range(10) + [100])
    # End def #}}}

    def test_trim(self): #{{{
        '''Small self, trim'''
        a = Sequence(range(10))
        self.assertNotEqual(a, [100] + range(10) + [100])

        a = Sequence(range(10), trim=True)
        self.assertEqual(a, range(10))
        self.assertEqual(a, [100] + range(10) + [100])
    # End def #}}}

    def test_lmissing(self): #{{{
        '''Big self, left missing'''
        a = Sequence(range(20), lmissing=True)
        self.assertEqual(a, range(20))
        self.assertEqual(a, range(10, 20))
    # End def #}}}

    def test_rmissing(self): #{{{
        '''Big self, right missing'''
        a = Sequence(range(20))
        self.assertNotEqual(a, range(10, 20))

        a = Sequence(range(20), rmissing=True)
        self.assertEqual(a, range(20))
        self.assertEqual(a, range(10))
    # End def #}}}

    def test_missing(self): #{{{
        '''Big self, missing'''
        a = Sequence(range(20))
        self.assertNotEqual(a, range(10, 15))

        a = Sequence(range(20), missing=True)
        self.assertEqual(a, range(20))
        self.assertEqual(a, range(10, 15))
    # End def #}}}

    def test_pad_int(self): #{{{
        '''Big self, pad integer'''
        a = Sequence(range(10)*2, pad=2)
        self.assertEqual(a, range(10))

        a = Sequence(range(10)*2, pad=1)
        self.assertNotEqual(a, range(10))

        a = Sequence(range(10)*2, pad=1, rmissing=True)
        self.assertEqual(a, range(10))
    # End def #}}}

    def test_pad_bool(self): #{{{
        '''Big self, pad bool'''
        a = Sequence(range(10)*2, pad=True)
        self.assertEqual(a, range(10))
    # End def #}}}

    def test_pad_slice(self): #{{{
        '''Big self, pad slice'''
        a = Sequence([1, 2] + ([3]*5), pad=slice(-1, None))
        self.assertEqual(a, [1, 2, 3])

        a = Sequence([1, 2] + ([3]*5), pad=slice(0, 0))
        self.assertNotEqual(a, [1, 2, 3])
    # End def #}}}

    def test_repeat_int(self): #{{{
        '''Small self, repeat integer'''
        a = Sequence(range(10), repeat=2)
        self.assertEqual(a, range(10)*2)

        a = Sequence(range(10), repeat=1)
        self.assertNotEqual(a, range(10)*2)

        a = Sequence(range(10), repeat=1, rtrim=True)
        self.assertEqual(a, range(10)*2)
    # End def #}}}

    def test_repeat_bool(self): #{{{
        '''Small self, repeat bool'''
        a = Sequence(range(10), repeat=True)
        self.assertEqual(a, range(10)*2)
    # End def #}}}

    def test_repeat_slice(self): #{{{
        '''Small self, repeat slice'''
        a = Sequence([1, 2, 3], repeat=slice(-1, None))
        self.assertEqual(a, [1, 2] + ([3]*5))

        a = Sequence([1, 2, 3], repeat=slice(0, 0))
        self.assertNotEqual(a, [1, 2] + ([3]*5))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

