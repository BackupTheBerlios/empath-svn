# Module: aossi.tests.Test_deco.Test_signal
# File: Test_signal.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.deco import signal, DecoSignal
from aossi.cwrapper import CallableWrapper, cid
from inspect import isfunction, ismethod

class Testsignal(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def _basictest(self, s, ctype=isfunction): #{{{
        self.assert_(ctype(s))
        self.assert_(hasattr(s, 'signal'))
        self.assert_(hasattr(s, 'settings'))
        self.assert_(hasattr(s, 'global_settings'))
        self.assert_(hasattr(s, 'after'))
        self.assert_(hasattr(s, 'before'))
        self.assert_(hasattr(s, 'around'))
        self.assert_(hasattr(s, 'onreturn'))
        self.assert_(hasattr(s, 'cond'))
        self.assert_(hasattr(s, 'when'))
        self.assert_(hasattr(s, 'cascade'))
        self.assert_(isinstance(s.signal, DecoSignal))
        self.assertEqual(s(), 1)
    # End def #}}}

    def testReturnValue(self): #{{{
        '''Returns a properly decorated function'''
        def DummyFunction(): #{{{
            return 1
        # End def #}}}
        s = signal(DummyFunction)
        self._basictest(s)
    # End def #}}}

    def testFunctionDecorator(self): #{{{
        '''Decorating a function'''
        @signal
        def DummyFunction(): #{{{
            return 1
        # End def #}}}

        s = DummyFunction
        self._basictest(s)
    # End def #}}}

    def testMethodDecorator(self): #{{{
        '''Decorating a method'''
        class A(object): #{{{
            @signal
            def a(self): #{{{
                return 1
            # End def #}}}
        # End class #}}}

        s = A().a
        self._basictest(s, ismethod)
    # End def #}}}

    def testOneSignal(self): #{{{
        '''A callable can only be decorated once as a signal'''
        def testme():
            pass
        s1 = signal(testme)
        s2 = signal(s1)
        self.assert_(s1 is s2)
    # End def #}}}
# End class #}}}

