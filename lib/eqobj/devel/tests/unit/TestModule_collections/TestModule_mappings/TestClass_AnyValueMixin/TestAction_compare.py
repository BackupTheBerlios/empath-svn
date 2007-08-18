# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.mappings import AnyValue

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_noself_noobj_nocount(self): #{{{
        '''No self, no obj, no count, returns True'''
        a = AnyValue()
        self.assertEquals(a, {})
    # End def #}}}

    def test_noself_noobj_count(self): #{{{
        '''No self, no obj, count, returns False'''
        a = AnyValue(count=1)
        self.assertNotEquals(a, {})
    # End def #}}}

    def test_self_noobj_nocount(self): #{{{
        '''self, no obj, no count, returns False'''
        a = AnyValue({1: 'a'})
        self.assertNotEquals(a, {})
    # End def #}}}

    def test_self_noobj_count(self): #{{{
        '''self, no obj, count, returns False'''
        a = AnyValue({1: 'a'}, count=1)
        self.assertNotEquals(a, {})
    # End def #}}}

    def test_noself_obj_nocount(self): #{{{
        '''No self, obj, no count, returns True'''
        a = AnyValue()
        self.assertEquals(a, {'a': 1})
    # End def #}}}

    def test_noself_obj_count(self): #{{{
        '''No self, obj, count, returns False'''
        a = AnyValue(count=1)
        self.assertNotEquals(a, {'a': 1})
    # End def #}}}

    def test_self_obj_nocount_one(self): #{{{
        '''self, obj, nocount, 1 match, returns True'''
        a = AnyValue({'a': 1})
        self.assertEquals(a, {'a': 1})
    # End def #}}}

    def test_self_obj_nocount_diffkey(self): #{{{
        '''self, obj, nocount, no matching keys, returns False'''
        a = AnyValue({'a': 1})
        self.assertNotEquals(a, {'b': 1})
    # End def #}}}

    def test_self_obj_nocount_none(self): #{{{
        '''self, obj, nocount, no match, returns False'''
        a = AnyValue({'a': 1})
        self.assertNotEquals(a, {'a': 2})
    # End def #}}}

    def test_self_obj_nocount_many(self): #{{{
        '''self, obj, nocount, many matches, returns True'''
        a = AnyValue(enumerate('abcde'))
        val = 'abcde'
        for i in xrange(1, 5):
            self.assertEquals(a, enumerate(val[:i]))
    # End def #}}}

    def test_self_obj_ltcount(self): #{{{
        '''self, obj, < count matches, returns False'''
        a = AnyValue(enumerate('abcde'), count=5)
        self.assertNotEquals(a, enumerate('abc'))
    # End def #}}}

    def test_self_obj_gtcount(self): #{{{
        '''No self, obj, > count matches, returns True'''
        a = AnyValue(enumerate('abcde'), count=3)
        self.assertEquals(a, enumerate('abcde'))
    # End def #}}}

    def test_self_obj_eqcount(self): #{{{
        '''No self, obj, == count matches, returns True'''
        a = AnyValue(enumerate('abcde'), count=5)
        self.assertEquals(a, enumerate('abcde'))
    # End def #}}}

# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

