# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.value import ValidateValueMapping_Or

class TestValidateValueMapping_Or(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleMappingType(self): #{{{
        '''Simple value validation on mapping'''
        v = ValidateValueMapping_Or(*dict(hello=1, world=2).items())
        val = dict(hello=1, world=2)
        self.assertEqual(val, v)
    # End def #}}}

    def testNonMappingValue(self): #{{{
        '''Trying to validate a non-mapping will return False'''
        v = ValidateValueMapping_Or(dict(hello=1))
        val = 1
        self.assertNotEqual(val, v)
    # End def #}}}

    def testSubMapping(self): #{{{
        '''Can validate on an element being a proper value mapping'''
        sub = {'sub1': 1, 'sub2': 2}
        s = {'s1': 'hello', 's2': 99999L, 's3': sub, 's4': 'world'}
        v = ValidateValueMapping_Or(s)
        val_sub = {'sub1': 1, 'sub2': 2}
        val = {'s1': 'hello', 's2': 99999L, 's3': val_sub, 's4': 'world'}
        self.assertEqual(v, val)
    # End def #}}}

    def testSubMapAsSequence(self): #{{{
        '''A submapping can be represented as a sequence of 2-tuples'''
        sub = {'sub1': 1, 'sub2': 2}
        s = {'s1': 'hello', 's2': 99999L, 's3': sub, 's4': 'world'}
        v = ValidateValueMapping_Or(s)
        val_sub = {'sub1': 1, 'sub2': 2}
        val = {'s1': 'hello', 's2': 99999L, 's3': val_sub.items(), 's4': 'world'}
        self.assertEqual(v, val)
    # End def #}}}

    def testBadMapping(self): #{{{
        '''Bad mapping does not validate'''
        sub = {'sub1': int, 'sub2': int}
        s = {'s1': str, 's2': long, 's3': sub, 's4': str}
        v = ValidateValueMapping_Or(s)
        val_sub = {'sub1': 'a', 'sub2': 'b'}
        val = {'s1': 1, 's2': '99999L', 's3': val_sub, 's4': 2}
        self.assertNotEqual(v, val)
    # End def #}}}

    def testSingleGoodValue(self): #{{{
        '''With even just one validating value, the whole mapping still validates'''
        sub = {'sub1': 1, 'sub2': 2}
        s = {'s1': 'hello', 's2': 99999L, 's3': sub, 's4': 'world'}
        v = ValidateValueMapping_Or(s)
        val_sub = {'sub1': 1, 'sub2': '2'}
        val = {'s1': 'hello', 's2': 99999L, 's3': val_sub, 's4': 'world'}
        self.assertEqual(v, val)
    # End def #}}}
# End class #}}}

