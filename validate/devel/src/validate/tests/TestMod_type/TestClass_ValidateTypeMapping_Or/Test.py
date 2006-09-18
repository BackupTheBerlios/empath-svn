# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.type import ValidateTypeMapping_Or

class TestValidateTypeMapping_Or(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleMappingType(self): #{{{
        '''Simple type validation on mapping'''
        v = ValidateTypeMapping_Or(*dict(hello=int, world=int).items())
        val = dict(hello=1, world=2)
        self.assertEqual(val, v)
    # End def #}}}

    def testNonMappingValue(self): #{{{
        '''Trying to validate a non-mapping will return False'''
        v = ValidateTypeMapping_Or(dict(hello=int))
        val = 1
        self.assertNotEqual(val, v)
    # End def #}}}

    def testBadArg(self): #{{{
        '''Passing a bad argument raises error'''
        try:
            ValidateTypeMapping_Or(str)
            self.assert_(False)
        except TypeError, err:
            errstr = "Detected non-ValidateType instance, non-type, non-mapping argument"
            e = str(err).strip()
            self.assertEqual(errstr, e)
    # End def #}}}

    def testSubMapping(self): #{{{
        '''Can validate on an element being a proper type mapping'''
        sub = {'sub1': int, 'sub2': int}
        s = {'s1': str, 's2': long, 's3': sub, 's4': str}
        v = ValidateTypeMapping_Or(s, **dict(exact=True))
        val_sub = {'sub1': 1, 'sub2': 2}
        val = {'s1': 'hello', 's2': 99999L, 's3': val_sub, 's4': 'world'}
        self.assertEqual(v, val)
    # End def #}}}

    def testBadMapping(self): #{{{
        '''Bad mapping does not validate'''
        sub = {'sub1': int, 'sub2': int}
        s = {'s1': str, 's2': long, 's3': sub, 's4': str}
        v = ValidateTypeMapping_Or(s, **dict(exact=True))
        val_sub = {'sub1': 'a', 'sub2': 'b'}
        val = {'s1': 1, 's2': '99999L', 's3': val_sub, 's4': 2}
        self.assertNotEqual(v, val)
    # End def #}}}

    def testSingleBadValue(self): #{{{
        '''With even just one non-validating value, the whole mapping will still validate'''
        sub = {'sub1': int, 'sub2': int}
        s = {'s1': str, 's2': long, 's3': sub, 's4': str}
        v = ValidateTypeMapping_Or(s, **dict(exact=True))
        val_sub = {'sub1': 1, 'sub2': '2'}
        val = {'s1': 'hello', 's2': 99999L, 's3': val_sub, 's4': 'world'}
        self.assertEqual(v, val)
    # End def #}}}
# End class #}}}

