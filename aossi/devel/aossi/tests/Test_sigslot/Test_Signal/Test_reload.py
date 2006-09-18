# Module: aossi.tests.Test_sigslot.Test_Signal.Test_reload
# File: Test_reload.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import Signal, AmbiguousChoiceError
from aossi.signal import Signal
from aossi.misc import AmbiguousChoiceError
from warnings import warn

def DummyFunction(var): #{{{
    var.append('DUMMY')
    return 1
# End def #}}}

class Testreload(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleAfter(self): #{{{
        '''Callable connected after runs after'''
        def runafter(var): #{{{
            var.append('AFTER')
        # End def #}}}
        var = []
        s = Signal(DummyFunction)
        s.connect(runafter)
        ret = s(var)
        self.assertEqual(var, ['DUMMY', 'AFTER'])
        self.assertEqual(ret, 1)
    # End def #}}}

    def testSimpleBefore(self): #{{{
        '''Callable connected before runs before'''
        def runbefore(var): #{{{
            var.append('BEFORE')
        # End def #}}}
        var = []
        s = Signal(DummyFunction)
        s.connect(before=[runbefore])
        ret = s(var)
        self.assertEqual(var, ['BEFORE', 'DUMMY'])
        self.assertEqual(ret, 1)
    # End def #}}}

    def testSimpleAround(self): #{{{
        '''Callable connected around runs around'''
        def wrap_around(func): #{{{
            def runaround(s, var):
                var.append('AROUND FIRST')
                ret = func(var)
                var.append('AROUND LAST')
                return ret
            return runaround
        # End def #}}}
        var = []
        s = Signal(DummyFunction)
        s.connect(around=[wrap_around])
        ret = s(var)
        self.assertEqual(var, ['AROUND FIRST', 'DUMMY', 'AROUND LAST'])
        self.assertEqual(ret, 1)
    # End def #}}}

    def testSimpleReturn(self): #{{{
        '''Callable connected return runs return'''
        var = []
        def onreturn(ret): #{{{
            var.append(('RETURN', ret))
        # End def #}}}
        s = Signal(DummyFunction)
        s.connect(onreturn=[onreturn])
        ret = s(var)
        self.assertEqual(var, ['DUMMY', ('RETURN', 1)])
        self.assertEqual(ret, 1)
    # End def #}}}

    def testSimpleChooser(self): #{{{
        '''Pushing in an always true chooser runs it instead'''
        var = []
        def DummyNew(var): #{{{
            var.append('NEW')
            return 2
        # End def #}}}
        def choosenew(var):
            return True
        s = Signal(DummyFunction)
        s.connect(choose=[(choosenew, DummyNew)])
        ret = s(var)
        self.assertEqual(ret, 2)
        self.assertEqual(var, ['NEW'])
    # End def #}}}

    def testSimpleFirstChooser(self): #{{{
        '''Choose first acceptable choice'''
        var = []
        def DummyNew1(var): #{{{
            var.append('NEW1')
            return 1
        # End def #}}}
        def DummyNew2(var): #{{{
            var.append('NEW2')
            return 2
        # End def #}}}
        def choose1(var):
            return True
        def choose2(var):
            return True
        s = Signal(DummyFunction)
        c = [(choose1, DummyNew1), (choose2, DummyNew2)]
        s.connect(choose=c)
        s.chooserpolicy = 'first'
        ret = s(var)
        self.assertEqual(ret, 1)
        self.assertEqual(var, ['NEW1'])
    # End def #}}}

    def testSimpleLastChooser(self): #{{{
        '''Choose last acceptable choice'''
        var = []
        def DummyNew1(var): #{{{
            var.append('NEW1')
            return 1
        # End def #}}}
        def DummyNew2(var): #{{{
            var.append('NEW2')
            return 2
        # End def #}}}
        def choose1(var):
            return True
        def choose2(var):
            return True
        s = Signal(DummyFunction)
        c = [(choose1, DummyNew1), (choose2, DummyNew2)]
        s.connect(choose=c)
        s.chooserpolicy = 'last'
        ret = s(var)
        self.assertEqual(ret, 2)
        self.assertEqual(var, ['NEW2'])
    # End def #}}}

    def testSimpleDefaultChooser(self): #{{{
        '''If can't decide, choose original callable'''
        var = []
        def DummyNew1(var): #{{{
            var.append('NEW1')
            return 1
        # End def #}}}
        def DummyNew2(var): #{{{
            var.append('NEW2')
            return 2
        # End def #}}}
        def choose1(var):
            return True
        def choose2(var):
            return True
        s = Signal(DummyFunction)
        c = [(choose1, DummyNew1), (choose2, DummyNew2)]
        s.connect(choose=c)
        s.chooserpolicy = 'default'
        ret = s(var)
        self.assertEqual(ret, 1)
        self.assertEqual(var, ['DUMMY'])
    # End def #}}}

    def testSimpleAmbiguousChooser(self): #{{{
        '''Default or unknown policy generates error on ambiguity'''
        var = []
        def DummyNew1(var): #{{{
            var.append('NEW1')
            return 1
        # End def #}}}
        def DummyNew2(var): #{{{
            var.append('NEW2')
            return 2
        # End def #}}}
        def choose1(var):
            return True
        def choose2(var):
            return True
        s = Signal(DummyFunction)
        c = [(choose1, DummyNew1), (choose2, DummyNew2)]
        s.connect(choose=c)
        s.chooserpolicy = None
        try:
            ret = s(var)
            self.assert_(False)
        except AmbiguousChoiceError, err:
            self.assertEqual(str(err).strip(), 'Found more than one selectable callable')
        except:
            self.assert_(False)
    # End def #}}}
# End class #}}}

