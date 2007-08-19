# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.sets import AnySetElement 

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_no_count_nomatch(self): #{{{
        '''AnySetElement without count option, no matches'''
        a = AnySetElement(range(5))
        self.assertFalse(a(xrange(20, 25)))
    # End def #}}}

    def test_no_count_match(self): #{{{
        '''AnySetElement without count option, matches'''
        a = AnySetElement(range(5))
        for i in xrange(1, 10):
            self.assertTrue(a(range(0, i)))
    # End def #}}}

    def test_count_nomatch(self): #{{{
        '''AnySetElement with count option, no matches'''
        a = AnySetElement(range(5), count=4)
        self.assertFalse(a((0, 1, 6, 7, 8)))
    # End def #}}}

    def test_count_match(self): #{{{
        '''AnySetElement with count option, matches'''
        a = AnySetElement(range(5), count=3)
        self.assertTrue(a(range(3)))
        self.assertTrue(a(range(5)))
    # End def #}}}

# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

