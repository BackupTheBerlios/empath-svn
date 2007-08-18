# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.sequences import *

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class TestAll(ExtrapolateOption, AllElements): #{{{
            pass
        # End class #}}}
        class TestAny(ExtrapolateOption, AnyElement): #{{{
            pass
        # End class #}}}
        self.cls_any = TestAny
        self.cls_all = TestAll
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_ex_any(self): #{{{
        '''Extrapolate on an AnyElement object'''
        a = self.cls_any([3, 4, 5], extrapolate=True)
        self.assertEqual(a, [3, 4, 5, 6, 7])
    # End def #}}}

    def test_ex_all(self): #{{{
        '''Extrapolate on an AllElements object'''
        a = self.cls_all([3, 4, 5], extrapolate=True)
        self.assertNotEqual(a, [3, 4, 5, 6, 7])
    # End def #}}}

    def test_ex_all_success(self): #{{{
        '''Extrapolate on an AllElements object that matches'''
        a = self.cls_all([3, 4, 5], extrapolate=True)
        self.assertNotEqual(a, [3, 4, 5, 5, 5])
    # End def #}}}

    def test_ex_all_fail_oneoff(self): #{{{
        '''Extrapolate on an AllElements object that does not match by one'''
        a = self.cls_all([3, 4, 5], extrapolate=True)
        self.assertNotEqual(a, [3, 4, 5, 5, 6])
    # End def #}}}

    def test_ex_any_count(self): #{{{
        '''Extrapolate on AnyElement with a specified count'''
        cls_any = self.cls_any
        for i in xrange(3, 6):
            a = cls_any([3, 4, 5], extrapolate=True, count=i)
            self.assertEqual(a, [3, 4, 5, 5, 5, 6, 7, 8])

        a = cls_any([3, 4, 5], extrapolate=True, count=6)
        self.assertNotEqual(a, [3, 4, 5, 5, 5, 6, 7, 8])
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

