# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.type import ValidateTypeSequence

class TestValidateTypeSequence_And(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleSequenceType(self): #{{{
        '''Simple type validation on sequence'''
        v = ValidateTypeSequence(str, int)
        val = ['hello', 2]
        self.assertEqual(val, v)
    # End def #}}}

    def testShallowOption(self): #{{{
        '''Specifying shallow will not dig into sub-sequences'''
        v = ValidateTypeSequence(str, list, shallow=True)
        val = ['hello', ['world', 1, 2]]
        self.assertEqual(v, val)
    # End def #}}}

    def testShallowEmpty(self): #{{{
        '''An empty and shallow type sequence validates against any sequence'''
        v = ValidateTypeSequence(shallow=True)
        val = ['hello', ['world', 1, 2]]
        self.assertEqual(v, val)
        self.assertNotEqual(v, 1)
        self.assertNotEqual(v, 'hello')
        self.assertEqual(v, [])
    # End def #}}}

    def testNonShallowEmpty(self): #{{{
        '''An empty but non-shallow type sequence validates only against an empty sequence'''
        v = ValidateTypeSequence()
        val = ['hello', ['world', 1, 2]]
        self.assertNotEqual(v, val)
        self.assertEqual(v, [])
    # End def #}}}

    def testNonSequenceValue(self): #{{{
        '''Trying to validate a non-sequence will return False'''
        v = ValidateTypeSequence(str, int)
        val = 1
        self.assertNotEqual(val, v)
    # End def #}}}

    def testBadArg(self): #{{{
        '''Passing a bad argument raises error'''
        try:
            ValidateTypeSequence(str, 1)
            self.assert_(False)
        except TypeError, err:
            errstr = "Detected non-ValidateType instance, non-type, non-sequence argument"
            e = str(err).strip()
            self.assertEqual(errstr, e)
    # End def #}}}

    def testStringIsBadArg(self): #{{{
        '''Passing a string raises error'''
        try:
            ValidateTypeSequence('hello')
            self.assert_(False)
        except TypeError, err:
            errstr = "Detected non-ValidateType instance, non-type, non-sequence argument"
            e = str(err).strip()
            self.assertEqual(errstr, e)
    # End def #}}}

    def testSubSequence(self): #{{{
        '''Can validate on an element being a proper type sequence'''
        sub = [int, int, int]
        s = [str, long, sub, str]
        v = ValidateTypeSequence(*tuple(s), **dict(exact=True))
        val = ['hello', 99999L, [1, 2, 3], 'world']
        self.assertEqual(v, val)
    # End def #}}}

    def testBadSequence(self): #{{{
        '''Bad sequence does not validate'''
        sub = [int, int, int]
        s = [str, long, sub, str]
        v = ValidateTypeSequence(*tuple(s), **dict(exact=True))
        val = [2, '99999L', ['no', 'w', 'n'], 1]
        self.assertNotEqual(v, val)
    # End def #}}}

    def testSingleGoodValue(self): #{{{
        '''With even just one non-validating value, the whole sequence does not validate'''
        sub = [int, int, int]
        s = [str, long, sub, str]
        v = ValidateTypeSequence(*tuple(s), **dict(exact=True))
        val = ['hello', 99999L, [2, 1, 'w'], 'world']
        self.assertNotEqual(v, val)
    # End def #}}}
# End class #}}}

