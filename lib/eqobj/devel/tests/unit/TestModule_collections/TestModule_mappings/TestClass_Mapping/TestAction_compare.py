# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.mappings import Mapping
from eqobj.validators.type import InstanceType as itype

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_simple(self): #{{{
        '''Simple, obvious usage'''
        template = dict(enumerate('abcd'))
        val = dict(template)
        a = Mapping(template)
        self.assertEqual(a, val)
    # End def #}}}

    def test_matchkey(self): #{{{
        '''Simple validation with eqobj keys'''
        template = {itype(int): 1}
        a = Mapping(template)
        self.assertEqual(a, {1:1})
        self.assertEqual(a, {42:1})
        self.assertNotEqual(a, {'1':1})
        self.assertNotEqual(a, {1:2})
    # End def #}}}

    def test_multimatch(self): #{{{
        '''Multi key type match'''
        template = {itype(int): 1, 1: 'hello'}
        val1 = {242: 1, 1: 'hello'}
        val2 = {242: 1, 1: 'hello', 2: 1}
        bad = {242: 1, 1: 'world'}
        a = Mapping(template)
        self.assertEqual(a, val1)
        self.assertEqual(a, val2)
        self.assertNotEqual(a, bad)
    # End def #}}}

    def test_trim(self): #{{{
        '''Trim unknown keys in other'''
        template = {1:1}
        val = {1:1, 2:2}
        a = Mapping(template, trim=True)
        self.assertEqual(a, val)

        a = Mapping(template)
        self.assertNotEqual(a, val)
    # End def #}}}

    def test_missing(self): #{{{
        '''Other does not contain keys in self'''
        template = {1:1, 2:2}
        val = {1:1}
        a = Mapping(template, missing=True)
        self.assertEqual(a, val)

        a = Mapping(template)
        self.assertNotEqual(a, val)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

