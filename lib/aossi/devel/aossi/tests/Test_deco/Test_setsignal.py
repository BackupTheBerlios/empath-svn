# Module: aossi.tests.Test_deco.Test_setsignal
# Module: Test_setsignal.py
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.deco import *
from inspect import isfunction, ismethod

class Testsetsignal(unittest.TestCase): #{{{
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
        self.assert_(isinstance(s.signal, DecoSignal))
        self.assertEqual(s(), 1)
    # End def #}}}

    def testSetsGlobalSettings(self): #{{{
        '''Sets any global settings properly'''
        def testme():
            return 1
        kw = {'globals': locals(), 'weak': True, 'weakcondf': False}
        s = setsignal(**kw)(testme)
        self._basictest(s)
        self.assertEqual(s.signal._global_settings, kw)
    # End def #}}}
# End class #}}}

