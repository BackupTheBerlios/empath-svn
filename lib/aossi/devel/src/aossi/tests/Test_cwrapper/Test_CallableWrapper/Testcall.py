# Module: aossi.tests.Test_sigslot.Test_CallableWrapper.Testcall
# File: Testcall.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import CallableWrapper
from aossi.cwrapper import CallableWrapper

def DummyFunction(a): #{{{
    return 'DummyFunction'
# End def #}}}

class DummyClass(object): #{{{
    def DummyMethod(self, a): #{{{
        return 'DummyMethod'
    # End def #}}}
# End class #}}}

class Test__call__(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testInstanceMethod(self): #{{{
        '''Calls instance method correctly'''
        A = DummyClass
        a = A()
        w = CallableWrapper(a.DummyMethod)
        self.assertEqual(w(a), a.DummyMethod(a))
    # End def #}}}

    def testClassMethod(self): #{{{
        '''Calls class method correctly'''
        class C(object):
            def c(self):
                pass
        A = DummyClass
        a = A()
        w = CallableWrapper(A.DummyMethod)
        self.assertEqual(w(a, a), a.DummyMethod(a))
    # End def #}}}

    def testNonMethodCallable(self): #{{{
        '''Calls non-method callable correctly'''
        w = CallableWrapper(DummyFunction)
        self.assertEqual(w(1), DummyFunction(1))
    # End def #}}}
    
    def testDeadWrapper(self): #{{{
        '''Calling a dead wrapper generates a warning'''
        A = DummyClass
        a = A()
        w = CallableWrapper(a.DummyMethod)
        del a
        self.assert_(w._isdead())
    # End def #}}}
# End class #}}}

