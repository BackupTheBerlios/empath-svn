# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.mappings import AllValues

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_noself_noobj(self): #{{{
        '''No self, no obj, returns True'''
        a = AllValues()
        self.assertEquals(a, {})
    # End def #}}}

    def test_self_noobj(self): #{{{
        '''self, no obj, returns False'''
        a = AllValues({1: 'a'})
        self.assertNotEquals(a, {})
    # End def #}}}

    def test_noself_obj(self): #{{{
        '''No self, obj, returns False'''
        a = AllValues()
        self.assertNotEquals(a, {'a': 1})
    # End def #}}}

    def test_self_obj_gtobjlen(self): #{{{
        '''self, obj, len(obj) > self, returns False'''
        a = AllValues(enumerate('a'))
        self.assertNotEquals(a, enumerate('ab'))
    # End def #}}}

    def test_self_obj_ltobjlen(self): #{{{
        '''self, obj, len(obj) < self, returns False'''
        a = AllValues(enumerate('ab'))
        self.assertNotEquals(a, enumerate('a'))
    # End def #}}}

    def test_self_obj_eqobjlen_nomatch(self): #{{{
        '''self, obj, len(obj) == self, no matches,  returns False'''
        a = AllValues(enumerate('ab'))
        self.assertNotEquals(a, enumerate('cd'))
    # End def #}}}

    def test_self_obj_eqobjlen_somematch(self): #{{{
        '''self, obj, len(obj) == self, some matches,  returns False'''
        a = AllValues(enumerate('ab'))
        self.assertNotEquals(a, enumerate('bc'))
    # End def #}}}

    def test_self_obj_eqobjlen_allmatch(self): #{{{
        '''self, obj, len(obj) == self, all match,  returns True'''
        a = AllValues(enumerate('ab'))
        self.assertEquals(a, enumerate('ab'))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

