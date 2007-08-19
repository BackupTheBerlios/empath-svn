# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.mappings import AnyKey 

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_no_count_nomatch(self): #{{{
        '''AnyKey without count option, no matches'''
        a = AnyKey(enumerate('abcde'))
        self.assertFalse(a(zip(xrange(20, 25), 'abcde')))
    # End def #}}}

    def test_no_count_match(self): #{{{
        '''AnyKey without count option, matches'''
        a = AnyKey(enumerate('abcde'))
        for i in xrange(1, 10):
            self.assertTrue(a(zip(range(0, i), range(0, i))))
    # End def #}}}

    def test_count_nomatch(self): #{{{
        '''AnyKey with count option, no matches'''
        a = AnyKey(enumerate('abcde'), count=4)
        self.assertFalse(a(zip((0, 1, 6, 7, 8), 'abcde')))
    # End def #}}}

    def test_count_match(self): #{{{
        '''AnyKey with count option, matches'''
        a = AnyKey(enumerate('abcde'), count=3)
        self.assertTrue(a(zip(range(3), range(3))))
        self.assertTrue(a(zip(range(5), range(5))))
    # End def #}}}

    def test_noself_noobj_nocount(self): #{{{
        '''No self, no obj, no count, returns True'''
        a = AnyKey()
        self.assertTrue(a({}))
    # End def #}}}

    def test_noself_obj_nocount(self): #{{{
        '''No self, obj, no count, returns True'''
        a = AnyKey()
        self.assertTrue(a(enumerate('abcde')))
    # End def #}}}

# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

