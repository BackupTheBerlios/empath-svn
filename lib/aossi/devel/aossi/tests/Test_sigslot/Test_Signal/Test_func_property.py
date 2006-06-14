# Module: aossi.tests.Test_sigslot.Test_Signal.Test_func_property
# File: Test_func_property.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import Signal
from aossi.signal import Signal
import inspect

def DummyFunction(): #{{{
    pass
# End def #}}}

class TestfuncProperty(unittest.TestCase): #{{{
    def setUp(self): #{{{
        self.s = Signal(DummyFunction)
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testIsProperty(self): #{{{
        '''func is a property'''
        of = self.s.__class__.func
        self.assert_(inspect.isdatadescriptor(of))
        self.assert_(isinstance(of, property))
    # End def #}}}

    def testReturnsOriginalFunction(self): #{{{
        '''func property returns the original function'''
        self.assertEqual(self.s.func.cid, id(DummyFunction))
    # End def #}}}

# End class #}}}

