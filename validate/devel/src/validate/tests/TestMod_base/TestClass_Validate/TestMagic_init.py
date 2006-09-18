# Module: validate.tests.TestMod_validate.TestClass_Validate.TestMagic_init
# File: TestMagic_init.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the validate project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.base import Validate

class TestInit(unittest.TestCase): #{{{
    def setUp(self): #{{{
        class v(Validate): pass
        self.v = v
    # End def #}}}

    def tearDown(self): #{{{
        del self.v
    # End def #}}}

    def testIsAbstract(self): #{{{
        '''Validate is an abstract class i.e. instantiation raises error'''
        try:
            Validate()
            self.assert_(False)
        except NotImplementedError, err:
            errstr = "Validate is an abstract class"
            e = str(err).strip()
            self.assertEqual(e, errstr)
        try:
            self.v(1)
        except:
            self.assert_(False)
        self.assert_(True)
    # End def #}}}

    def testStoreArg(self): #{{{
        '''Stores any arguments passed in'''
        def test_storage(*args): #{{{
            v = None
            try:
                v = self.v(*args)
            except:
                self.assert_(False)
            self.assert_(hasattr(v, '_stored'))
            self.assertEqual(v._stored, args)
            if args:
                self.assert_(v._stored)
                self.assert_(v._stored[0] is args[0])
        # End def #}}}
        test_storage()
        test_storage(1)
    # End def #}}}

    def testStoreMoreArgs(self): #{{{
        '''Storing more than one argument raises error'''
        def test_storage(*args): #{{{
            v = None
            try:
                v = self.v(*args)
                self.assert_(False)
            except NotImplementedError, err:
                errstr = "Passing more than one argument is not supported"
                s = str(err).strip()
                self.assertEqual(errstr, s)
        # End def #}}}
        input = [(1, 2, 3), ('a', 'b')]
        for i in input:
            test_storage(*i)
    # End def #}}}

    def testKeywordArgs(self): #{{{
        '''Only accepts expected keyword arguments'''
        def test_kwargs(**kw): #{{{
            expected = ('exact',)
            v = None
            try:
                v = self.v(**kw)
                self.assert_(False)
            except ValueError, err:
                errstr = "Unexpected arguments %s" %', '.join([kw for kw in kw.iterkeys() if kw not in expected])
                e = str(err).strip()
                self.assertEqual(errstr, e)
        # End def #}}}
        test_kwargs(hello=1)
        test_kwargs(hello=1, moo=2)
        test_kwargs(hello=1, blue=42, exact=True)
    # End def #}}}

    def testExpectedKeywordArgs(self): #{{{
        '''Passing in expected options saves as appropriate'''
        def test_kw_exact(exact): #{{{
            v = None
            try:
                v = self.v(exact=exact)
            except:
                self.assert_(False)
            self.assert_(hasattr(v, '_exact'))
            self.assertEqual(v._exact, bool(exact))
            self.assert_(isinstance(v._exact, bool))
        # End def #}}}
        input = [True, False, 123, None, {1:1}, [], [1, 2, 3]]
        for i in input:
            test_kw_exact(i)
    # End def #}}}
# End class #}}}

