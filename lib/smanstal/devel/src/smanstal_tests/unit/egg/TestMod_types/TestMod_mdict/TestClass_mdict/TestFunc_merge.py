# Module: smanstal.tests.TestPkg_types.TestMod_mdict.TestClass_mdict.TestFunc_merge
# File: TestFunc_merge.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.egg.tests import BaseUnitTest, addtest, mksuite
from pkg_resources import Requirement
import os.path as op

__req__ = Requirement.parse('smanstal')

temp_path = op.abspath(__file__)
if op.exists(temp_path):
    __file__ = temp_path
del temp_path

from smanstal.types.mdict import mdict

class Test_merge(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNormalArgs(self): #{{{
        '''Normal dict args'''
        test = mdict()
        self.assertTrue(isinstance(test.merged, tuple))
        self.assertFalse(test.merged)

        # Single dict
        a = {'1':1}
        test.merge(a)
        self.assertEqual(len(test), 1)
        self.assertEqual(test.items()[0], a.items()[0])
        self.assertEqual(test.merged, tuple([a]))
        test.clear()

        # Sequence
        seq1 = 'abcdefghijk'
        a = zip(seq1, range(len(seq1)))
        expected = dict(a)
        test.merge(a)
        self.assertEqual(len(test.merged), 1)
        self.assertEqual(test, expected)
        self.assertEqual(test.merged[0], expected)
        test.clear()

        # kwargs
        test.merge(**expected)
        self.assertEqual(len(test.merged), 1)
        self.assertEqual(test, expected)
        self.assertEqual(test.merged[0], expected)
        test.clear()
    # End def #}}}

    def testMixedArgs(self): #{{{
        '''Mixed args'''
        test = mdict()

        # Mix only args
        a1 = {'1':1}
        seq1 = 'abcdefghijk'
        a2 = zip(seq1, range(len(seq1)))
        a3 = zip(range(10), range(10))
        a4 = {'hello': 'world'}
        a5 = {'nice': 'you', 'how': 'doody'}
        test.merge(a1, a2, a3, a4, a5)

        self.assertEqual(len(test.merged), 5)
        count = 0
        m = test.merged
        expected = dict()
        while count < 5:
            a = dict(eval('a%i' %(count+1)))
            self.assertEqual(m[count], a)
            expected.update(a)
            count += 1
        self.assertEqual(test, expected)
    # End def #}}}

    def testKWOverrides(self): #{{{
        '''kwargs overrides values'''
        a = {'hello': 'world'}
        b = {'boo': 'ya'}
        override = {'hello': 'MY world'}
        expected = dict(a)
        expected.update(b)
        expected.update(**override)
        test = mdict(a, b, **override)
        self.assertEqual(test.merged[-1], override)
        self.assertEqual(test, expected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

