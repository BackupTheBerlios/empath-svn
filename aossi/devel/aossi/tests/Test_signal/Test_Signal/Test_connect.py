# Module: aossi.tests.Test_sigslot.Test_Signal.Test_connect
# File: Test_connect.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import CallableWrapper, Signal, cid
from aossi.signal import Signal
from aossi.cwrapper import CallableWrapper, cid

def DummyFunction(a): #{{{
    return a
# End def #}}}

class Testconnect(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testUnexpectedArgs(self): #{{{
        '''Passing in unexpected keyword arguments illegal'''
        s = Signal(DummyFunction)
        try:
            s.connect(hello=1)
            self.assert_(False)
        except ValueError, err:
            self.assertEqual(str(err).strip(), 'valid keyword arguments are: before, around, onreturn, choose, weak, weakcondf')
    # End def #}}}

    def testNonFunction(self): #{{{
        '''Passing in a non-function argument is illegal'''
        check = ('after_slots', 'before', 'around')
        for arg in check: #{{{
            res = False
            s = Signal(DummyFunction)
            try:
                if arg == 'after_slots':
                    s.connect(1)
                else:
                    s.connect(**{arg: [1]})
            except TypeError, err:
                msg = 'Detected non-callable element of %s sequence' %arg
                res = str(err).strip() == msg
                if not res:
                    raise Exception(str(err) + ' ::: ' + msg)
            self.assert_(res)
        # End for #}}}
    # End def #}}}

    def testFirstAdd(self): #{{{
        '''Add brand new function'''
        check = ('after_slots', 'before')
        def test_add(a): #{{{
            pass
        # End def #}}}
        taid = id(test_add)
        for arg in check: #{{{
            res = False
            s = Signal(DummyFunction)
            l = None
            if arg == 'after_slots':
                s.connect(test_add)
                l = s._afterfunc
            else:
                s.connect(**{arg: [test_add]})
                l = eval('s._%sfunc' %arg)
            self.assertEqual(len(l), 1)
            self.assertEqual(l[0].cid, taid)
        # End for #}}}
    # End def #}}}

    def testExistingAdd(self): #{{{
        '''Add existing function'''
        check = ('after_slots', 'before')
        def a(a): #{{{
            pass
        # End def #}}}
        def b(a): #{{{
            pass
        # End def #}}}
        bid = id(b)
        for arg in check: #{{{
            res = False
            s = Signal(DummyFunction)
            l = None
            if arg == 'after_slots':
                s.connect(a, b)
                s.connect(b)
                l = s._afterfunc
            else:
                s.connect(**{arg: [a, b]})
                s.connect(**{arg: [b]})
                l = eval('s._%sfunc' %arg)
            self.assertEqual(len(l), 2)
            self.assertEqual(l[1].cid, bid)
        # End for #}}}
    # End def #}}}

    def testAddSameToDifferentSlots(self): #{{{
        '''Adding the same function to different slot allowed'''
        def a(): #{{{
            pass
        # End def #}}}
        aid = id(a)
        s = Signal(DummyFunction)
        s.connect(a, before=[a])
        self.assertEqual(len(s._afterfunc), 1)
        self.assertEqual(len(s._beforefunc), 1)

        self.assertEqual(s._afterfunc[0].cid, aid)
        self.assertEqual(s._beforefunc[0].cid, aid)
    # End def #}}}

    def testAddInstanceMethod(self): #{{{
        '''Connecting an instance method'''
        class A(object): #{{{
            def test(self): #{{{
                return self.__class__.__name__
            # End def #}}}
        # End class #}}}
        class B(object): #{{{
            def test(self): #{{{
                return self.__class__.__name__
            # End def #}}}
        # End class #}}}
        a = A()
        b = B()
        s = Signal(a.test)
        s.connect(b.test)
        self.assert_(True)
    # End def #}}}

    def testExistingInstanceMethod(self): #{{{
        '''Does not add already existing instance method'''
        class A(object): #{{{
            def test(self): #{{{
                return self.__class__.__name__
            # End def #}}}
        # End class #}}}
        class B(object): #{{{
            def test(self): #{{{
                return self.__class__.__name__
            # End def #}}}
        # End class #}}}
        a = A()
        b = B()
        s = Signal(a.test)
        s.connect(b.test)
        s.connect(b.test)
        s.connect(b.test)
        s.connect(b.test)
        s.connect(b.test)
        self.assertEqual(len(s._afterfunc), 1)
        self.assertEqual(cid(s._afterfunc[0]), cid(b.test))
    # End def #}}}

    def testDerefInstanceMethod(self): #{{{
        '''Dereferencing a connected instance method cleans the appropriate list'''
        class A(object): #{{{
            def test(self): #{{{
                return self.__class__.__name__
            # End def #}}}
        # End class #}}}
        class B(object): #{{{
            def test(self): #{{{
                return self.__class__.__name__
            # End def #}}}
        # End class #}}}
        a = A()
        b = B()
        s = Signal(a.test)
        s.connect(b.test)
        s.connect(b.test)
        self.assertEqual(len(s._afterfunc), 1)
        self.assertEqual(cid(s._afterfunc[0]), cid(b.test))

        del b
        self.assertEqual(len(s._afterfunc), 0)
    # End def #}}}

    def testChangeChooser(self): #{{{
        '''After connecting a chooser and its callable, change the chooser'''
        def DummyNew(a): #{{{
            return 'hello %s' %str(a)        
        # End def #}}}
        def choose1(a): #{{{
            return True
        # End def #}}}
        def choose2(a): #{{{
            return False
        # End def #}}}
        s = Signal(DummyFunction)
        s.connect(choose=[(choose1, DummyNew)])
        s.connect(choose=[(choose2, DummyNew)])
        self.assertEqual(len(s._choosefunc), 1)
        self.assertEqual(s._choosefunc[0].choosefunc.cid, cid(choose2))
        ret = s('world')
        self.assertEqual(ret, 'world')
    # End def #}}}
# End class #}}}

