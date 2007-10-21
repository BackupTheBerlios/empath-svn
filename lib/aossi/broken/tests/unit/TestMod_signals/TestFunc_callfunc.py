# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.signals import Signal
from aossi.core import callfunc
from aossi.cwrapper import CallableWrapper

class Test_callfunc(BaseUnitTest): #{{{
    def setUp(self): #{{{
        def sigfunc(): #{{{
            return 400
        # End def #}}}
        self.signal = Signal(sigfunc, weak=False)
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNormalFunction(self): #{{{
        '''Calls normal functions'''
        def test(): #{{{
            return 42
        # End def #}}}
        func = CallableWrapper(test)
        ret = callfunc(self.signal, func, None, False, None)
        self.assertEqual(ret, 42)
    # End def #}}}

    def testPassRet(self): #{{{
        '''Giving pass_ret = True sends the given return value as the only argument'''
        def test(ret): #{{{
            return 42 + ret
        # End def #}}}
        func = CallableWrapper(test)
        ret = callfunc(self.signal, func, None, True, 100)
        self.assertEqual(ret, 142)
    # End def #}}}

    def testMethodSignalFuncTarget(self): #{{{
        '''Go from a method to a normal function'''
        class _(object): #{{{
            def me(self, a): #{{{
                return 100
            # End def #}}}
        # End class #}}}
        def test(a): #{{{
            return a
        # End def #}}}
        t = _()
        sig = Signal(t.me)
        func = CallableWrapper(test)
        ret = callfunc(sig, func, None, False, None, 42)
        self.assertEqual(ret, 42)
        ret = callfunc(sig, func, None, False, None, t, 42)
        self.assertEqual(ret, 42)
    # End def #}}}

    def testMethodSignalMethodTarget(self): #{{{
        '''Go from a method to a method of the same class'''
        class _(object): #{{{
            def test1(self, a): #{{{
                return 100
            # End def #}}}
            def test2(self, a): #{{{
                return a
            # End def #}}}
            def test3(self, *args): #{{{
                return len(args)
            # End def #}}}
        # End class #}}}
        t = _()
        sig = Signal(t.test1)
        func = CallableWrapper(t.test2)
        func2 = CallableWrapper(t.test3)
        ret = callfunc(sig, func, None, False, None, 42)
        self.assertEqual(ret, 42)
        ret = callfunc(sig, func2, None, False, None, 42)
        self.assertEqual(ret, 1)
    # End def #}}}

    def testMethodSignalMethodTarget2(self): #{{{
        '''Go from a method to a method of a different class'''
        class c(object): #{{{
            def test1(self, a): #{{{
                return 100
            # End def #}}}
        # End class #}}}
        class cc(object): #{{{
            def test2(self, a): #{{{
                return a
            # End def #}}}
        # End class #}}}
        t, tt = c(), cc()
        sig = Signal(c.test1)
        func = CallableWrapper(cc.test2)
        ret = callfunc(sig, func, None, False, None, 42)
        self.assertEqual(ret, 42)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

