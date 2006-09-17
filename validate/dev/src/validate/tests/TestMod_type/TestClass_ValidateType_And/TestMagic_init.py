# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.type import ValidateType_Or, ValidateType_And, _BaseValidateType
from validate.base import Validate

class TestInit(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoinstBase(self): #{{{
        '''Instantiating base class raises error'''
        try:
            _BaseValidateType()
            self.assert_(False)
        except NotImplementedError, err:
            strerr = "_BaseValidateType is an abstract class"
            e = str(err).strip()
            self.assertEqual(strerr, e)
    # End def #}}}

    def testNonType(self): #{{{
        '''Passing in a non-type, non-ValidateType instance raises error'''
        try:
            ValidateType_And('hello')
            self.assert_(False)
        except TypeError, err:
            errstr = "Detected non-ValidateType instance, non-type argument"
            e = str(err).strip()
            self.assertEqual(errstr, e)
    # End def #}}}

    def testType(self): #{{{
        '''Passing in a type'''
        try:
            ValidateType_And(str)
        except:
            self.assert_(False)
        self.assert_(True)
    # End def #}}}

    def testValidateType(self): #{{{
        '''Passing in a _BaseValidateType instance'''
        v1 = ValidateType_Or(int)
        v2 = ValidateType_And(str)
        try:
            ValidateType_Or(v1, v2)
        except:
            self.assert_(False)
        self.assert_(True)
    # End def #}}}

    def testIsValidate(self): #{{{
        '''ValidateType is an instance of Validate'''
        v1 = ValidateType_And(int)
        self.assert_(isinstance(v1, Validate))
    # End def #}}}
# End class #}}}

