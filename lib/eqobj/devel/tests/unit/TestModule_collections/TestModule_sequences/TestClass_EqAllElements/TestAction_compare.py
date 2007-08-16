# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.sequences import AllElements

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_count_option(self): #{{{
        '''count option is always the length of _initobj'''
        v = range(10)
        a = AllElements(v)
        self.assertEqual(a.options.count, 10)
    # End def #}}}

    def test_pre_cmp(self): #{{{
        '''If the lengths of self and the other object is not the same, return False'''
        class Test(AllElements): #{{{
            def _cmp(self, val, count): #{{{
                raise NotImplementedError
            # End def #}}}
            def _post_cmp(self, val, count): #{{{
                raise NotImplementedError
            # End def #}}}
        # End class #}}}
        v = range(10)
        a = Test(range(20))
        try:
            self.assertFalse(a == v)
        except:
            self.assertTrue(False)
    # End def #}}}

    def test_compare_same(self): #{{{
        '''Sequences are the same'''
        a = AllElements(range(5))
        self.assertEqual(a, range(5))
    # End def #}}}

    def test_compare_diff(self): #{{{
        '''Sequences are different'''
        a = AllElements(range(5))
        self.assertNotEqual(a, range(5, 10))
    # End def #}}}

    def test_compare_diff_start_same(self): #{{{
        '''Sequences are different but start with same element'''
        a = AllElements(range(5))
        self.assertNotEqual(a, range(0, 10, 2))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

