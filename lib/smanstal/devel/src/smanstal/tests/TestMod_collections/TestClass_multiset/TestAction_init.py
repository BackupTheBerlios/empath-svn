# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections import multiset

class Test_init(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testIter(self): #{{{
        '''Pass a hashable iter, sets count to one'''
        a = range(10)
        a = multiset(a)
        expected = [(i, 1) for i in a]
        self.assertEqual(a.items(), expected)
    # End def #}}}

    def testNothing(self): #{{{
        '''Pass nothing or empty sequence'''
        a = multiset()
        self.assertFalse(a)
        a = multiset([])
        self.assertFalse(a)
    # End def #}}}

    def testMultiset(self): #{{{
        '''Pass another multiset will copy it unconditionally'''
        a = multiset(range(10))
        b = multiset(a)
        expected = [(i, 1) for i in a]
        self.assertEqual(b.items(), expected)
    # End def #}}}

    def testGoodDict(self): #{{{
        '''Pass a dict with integer values'''
        test = {'hello': 20, 'world': 30}
        a = multiset(test)
        self.assertEqual(dict(a), test)
    # End def #}}}

    def testBadDict(self): #{{{
        '''Dict with non-integer values will set keys with count 1'''
        test = {'hello': 'world', 'william': 400}
        expected = {'hello': 1, 'william': 400}
        a = multiset(test)
        self.assertEqual(dict(a), expected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

