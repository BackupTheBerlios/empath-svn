# Module: aossi.tests.Test_sigslot.Test_CallableWrapper.Test__getcallable
# File: Test__getcallable.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import CallableWrapper
from aossi.cwrapper import CallableWrapper


def DummyFunction(): #{{{
    return 'DummyFunction'
# End def #}}}

class DummyClass(object): #{{{
    def DummyMethod(self): #{{{
        return 'DummyMethod'
    # End def #}}}
# End class #}}}

class Test_getcallable(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testMethodInstance(self): #{{{
        '''Instance method callable's im_func returned'''
        A = DummyClass
        a = A()
        w = CallableWrapper(a.DummyMethod)
        self.assert_(w._getcallable() is a.DummyMethod.im_func)
    # End def #}}}

    def testClassInstance(self): #{{{
        '''Class method callable's im_func returned'''
        A = DummyClass
        w = CallableWrapper(A.DummyMethod)
        self.assert_(w._getcallable() is A.DummyMethod.im_func)
    # End def #}}}

    def testNonExistantInstance(self): #{{{
        '''No longer existing instance returns None '''
        A = DummyClass
        a = A()
        w = CallableWrapper(a.DummyMethod)
        del a
        self.assert_(w._getcallable() is None)
    # End def #}}}

    def testNonMethodCallable(self): #{{{
        '''Non-method callable returns actual callable'''
        w = CallableWrapper(DummyFunction)
        self.assert_(w._getcallable() is DummyFunction)
    # End def #}}}

# End class #}}}

