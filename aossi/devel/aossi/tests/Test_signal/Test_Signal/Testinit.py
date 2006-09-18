# Module: aossi.tests.Test_sigslot.Test_Signal.Testinit
# File: Testinit.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import Signal, CallableWrapper
from aossi.signal import Signal
from aossi.cwrapper import CallableWrapper
from weakref import ref, ReferenceType as wrtype

def DummyFunction(): #{{{
    pass
# End def #}}}

class Test__init__(unittest.TestCase): #{{{
    def setUp(self): #{{{
        self.s = Signal(DummyFunction)
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testInvalidSignalObject(self): #{{{
        '''Non-callable argument is illegal'''
        try:
            a = Signal(1)
            self.assert_(False)
        except TypeError, err:
            self.assertEqual(str(err).strip(), "Argument must be callable.");
        except:
            self.assert_(False)
    # End def #}}}

    def test_origfuncInternalVariable(self): #{{{
        '''_func internal variable is properly initialized'''
        s = self.s
        f = getattr(s, '_func', None)

        # Test _origfunc
        self.assert_(f is not None)
        self.assert_(isinstance(f, CallableWrapper))
        self.assertEqual(f.cid, id(DummyFunction))
    # End def #}}}

    def test_beforefuncInternalVariable(self): #{{{
        '''_beforefunc internal variable is properly initialized'''
        s = self.s

        # Test _beforefunc
        self.assert_(hasattr(s, '_beforefunc'))
        self.assert_(isinstance(s._beforefunc, list))
        self.assert_(not s._beforefunc)
    # End def #}}}

    def test_afterfuncInternalVariable(self): #{{{
        '''_afterfunc internal variable is properly initialized'''
        s = self.s

        # Test _afterfunc
        self.assert_(hasattr(s, '_afterfunc'))
        self.assert_(isinstance(s._afterfunc, list))
        self.assert_(not s._afterfunc)
    # End def #}}}

    def test_aroundfuncInternalVariable(self): #{{{
        '''_aroundfunc internal variable is properly initialized'''
        s = self.s

        # Test _aroundfunc
        self.assert_(hasattr(s, '_aroundfunc'))
        self.assert_(isinstance(s._aroundfunc, list))
        self.assert_(not s._aroundfunc)
    # End def #}}}
# End class #}}}

