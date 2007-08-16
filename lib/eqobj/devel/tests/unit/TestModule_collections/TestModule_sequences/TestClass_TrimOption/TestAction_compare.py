# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.sequences import TrimOption, AllElements

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class Test(TrimOption, AllElements): #{{{
            pass
        # End class #}}}
        self.cls = Test
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_th_nott_fail(self): #{{{
        '''Trimming head but not tail matches but still have tail returns False'''
        a = self.cls([3, 4, 5], trim_head=True)
        self.assertNotEqual(a, [0, 1, 2, 3, 4, 5, 6, 7])
    # End def #}}}

    def test_th_nott_success(self): #{{{
        '''Trimming head but have no more tail returns True'''
        a = self.cls([3, 4, 5], trim_head=True)
        self.assertEqual(a, [0, 1, 2, 3, 4, 5])
    # End def }}}

    def test_tt_noth_fail(self): #{{{
        '''Trimming only tail but no match at beginning returns False'''
        a = self.cls([3, 4, 5], trim_tail=True)
        self.assertNotEqual(a, [0, 1, 2, 3, 4, 5, 6, 7])
    # End def #}}}

    def test_tt_noth_success(self): #{{{
        '''Trimming only tail but match at beginning returns True'''
        a = self.cls([3, 4, 5], trim_tail=True)
        self.assertEqual(a, [3, 4, 5, 6, 7, 8, 9, 10])
    # End def #}}}

    def test_tt_th(self): #{{{
        '''Trim via explicit options returns True on match'''
        a = self.cls([3, 4, 5], trim_tail=True, trim_head=True)
        self.assertEqual(a, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

