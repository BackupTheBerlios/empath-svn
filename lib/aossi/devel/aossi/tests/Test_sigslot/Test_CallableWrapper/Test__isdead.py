# Module: aossi.tests.Test_sigslot.Test_CallableWrapper.Test__isdead
# File: Test__isdead.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.cwrapper import CallableWrapper

class DummyClass(object): #{{{
    def DummyMethod(self): #{{{
        return 'DummyMethod'
    # End def #}}}
# End class #}}}

class Test_isdead(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testRemoveInstance(self): #{{{
        '''Deleting an instance makes for a dead CallableWrapper'''
        A = DummyClass
        a = A()
        w = CallableWrapper(a.DummyMethod)
        del a
        self.assert_(w._isdead())
    # End def #}}}

    def testRemoveNonMethodCallable(self): #{{{
        '''Deleting a non-method callable makes for a dead CallableWrapper'''
        def DummyFunction(): #{{{
            return 'DummyFunction'
        # End def #}}}

        w = CallableWrapper(DummyFunction)
        del DummyFunction
        self.assert_(w._isdead())
    # End def #}}}
# End class #}}}

