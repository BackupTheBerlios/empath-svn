# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite


from eqobj.collections.sequences import AnyElement

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.c = AnyElement([1, 2, 3, 'a', 'b', 'c'])
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_method_counterror(self): #{{{
        '''Raise error if count option < 0'''
        a = AnyElement(count=-10)
        try:
            a == [1]
        except ValueError, err:
            msg = "count option must be >= 0: -10"
            self.assertEquals(str(err).strip(), msg)
    # End def #}}}

    def test_count_empties_havecount(self): #{{{
        '''If both sequences are empty and have a non-zero, non-None count option, return False'''
        a = AnyElement(count=3)
        self.assertFalse(a == [])
    # End def #}}}

    def test_count_empties_nocount(self): #{{{
        '''If both sequences are empty and have a zero count option, return True'''
        a = AnyElement(count=0)
        self.assertTrue(a == [])
    # End def #}}}

    def test_default_precmp(self): #{{{
        '''Default pre_cmp: If the len() of the smallest sequence < count return False'''
        class Test(AnyElement): #{{{
            def _cmp(self, val, count): #{{{
                raise NotImplementedError
            # End def #}}}
            def _post_cmp(self, val, count): #{{{
                raise NotImplementedError
            # End def #}}}
        # End class #}}}
        a = Test(self.c._initobj, count=20)
        try:
            self.assertFalse(a == range(10))
        except:
            self.assertTrue(False)
    # End def #}}}

    def test_default_cmp_nocount(self): #{{{
        '''Default cmp: If no count and there is a match, return True'''
        class Test(AnyElement): #{{{
            def _post_cmp(self, val, count): #{{{
                raise NotImplementedError
            # End def #}}}
        # End class #}}}
        a = Test(self.c._initobj)
        try:
            self.assertTrue(a == range(1, 10))
        except:
            self.assertTrue(False)
    # End def #}}}

    def test_default_cmp_count_exceed(self): #{{{
        '''Default cmp: If count and there are more matches than count, return False'''
        class Test(AnyElement): #{{{
            def _post_cmp(self, val, count): #{{{
                raise NotImplementedError
            # End def #}}}
        # End class #}}}
        a = Test(self.c._initobj, count=2)
        try:
            self.assertFalse(a == range(1, 10))
        except:
            self.assertTrue(False)
    # End def #}}}

    def test_default_post_cmp_nomatch(self): #{{{
        '''Default post_cmp: If there are not exactly count matches, return False'''
        try:
            a = AnyElement(self.c._initobj, count=5)
        except:
            self.assertTrue(False)
        self.assertFalse(a == range(1, 10))
    # End def #}}}
    
    def test_default_post_cmp_match(self): #{{{
        '''Default post_cmp: If there are exactly count matches, return False'''
        try:
            a = AnyElement(self.c._initobj, count=3)
        except:
            self.assertTrue(False)
        self.assertTrue(a == range(1, 10))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

