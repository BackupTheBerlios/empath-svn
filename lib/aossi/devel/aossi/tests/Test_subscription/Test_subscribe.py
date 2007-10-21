# Module: aossi.tests.Test_subscription.Test_subscribe
# File: Test_subscribe.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.subscription import subscribe, _siglist

def dummy(a, var):
    var.append(a + 1)
    return var

def dummy2(a, var):
    var.append(a + 2)

class Testsubscribe(unittest.TestCase): #{{{
    def setUp(self): #{{{
        while _siglist:
            _siglist.pop()
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoneIssue(self): #{{{
        '''Trying to subscribe None issue is illegal'''
        try:
            subscribe(None, dummy)
            self.assert_(False)
        except TypeError, err:
            e = str(err).strip()
            self.assertEqual(e, 'issue can not be None')
        except Exception, err:
            raise err.__class__(err)
    # End def #}}}

    def testTargetUncallable(self): #{{{
        '''Passing in a non-callable target is illegal'''
        try:
            subscribe('noncallable target', 1)
            self.assert_(False)
        except TypeError, err:
            e = str(err).strip()
            self.assertEqual(e, 'target must be callable')
    # End def #}}}

    def testUnexpectedType(self): #{{{
        '''Trying to subscribe an unknown type is illegal'''
        try:
            subscribe('stranger', dummy, ftype='wacky')
            self.assert_(False)
        except ValueError, err:
            e = str(err).strip()
            self.assertEqual(e, 'detected unexpected type argument; must be one of the following: after, before, around, onreturn, choose')
    # End def #}}}

    def testNoChooseFunc(self): #{{{
        '''choose type must have an accompanying choosefunc'''
        subscribe('stranger', dummy)
        try:
            subscribe('stranger', dummy2, ftype='choose')
            self.assert_(False)
        except ValueError, err:
            e = str(err).strip()
            self.assertEqual(e, "an ftype of 'choose' must be accompanied with an appropriate 'choosefunc'")
    # End def #}}}

    def testNonCallableChooseFunc(self): #{{{
        '''Passing in a non-callable choosefunc is illegal'''
        subscribe('stranger', dummy)
        try:
            subscribe('stranger', dummy2, ftype='choose', choosefunc=1)
            self.assert_(False)
        except TypeError, err:
            e = str(err).strip()
            self.assertEqual(e, 'choosefunc argument must be callable')
    # End def #}}}

    def testWrapNonIssue(self): #{{{
        '''Attempting to wrap an unsubscribed issue raises an error'''
        def me():
            pass
        try:
            subscribe('not exist', me, ftype='after')
            self.assert_(False)
        except TypeError, err:
            e = str(err).strip()
            self.assertEqual(e, 'Please subscribe an issue first.')
        except Exception, err:
            e = str(err).strip()
            raise err.__class__(e)
    # End def #}}}

    def testFirstSubscription(self): #{{{
        '''Adding the first subscription'''
        self.assertEqual(len(_siglist), 0)
        subscribe('/first', dummy)
        self.assertEqual(len(_siglist), 1)
        self.assert_(True)
    # End def #}}}

    def testSubscribeAfter(self): #{{{
        '''Subscribing after types'''
        self.assertEqual(len(_siglist), 0)
        subscribe('after', dummy)
        self.assertEqual(len(_siglist), 1)
        subscribe('after', dummy2)
        self.assertEqual(len(_siglist), 1)
        io, signal = _siglist[0]
        var = []
        signal(0, var)
        self.assertEqual(var, [1, 2])
    # End def #}}}

    def testSubscribeBefore(self): #{{{
        '''Subscribing before types'''
        self.assertEqual(len(_siglist), 0)
        subscribe('before', dummy)
        self.assertEqual(len(_siglist), 1)
        subscribe('before', dummy2, ftype='before')
        self.assertEqual(len(_siglist), 1)
        io, signal = _siglist[0]
        var = []
        signal(0, var)
        self.assertEqual(var, [2, 1])
    # End def #}}}

    def testSubscribeOnReturn(self): #{{{
        '''Subscribing onreturn types'''
        def dummyr(ret):
            ret.append(42)

        self.assertEqual(len(_siglist), 0)
        subscribe('onreturn', dummy)
        self.assertEqual(len(_siglist), 1)
        subscribe('onreturn', dummyr, ftype='onreturn')
        self.assertEqual(len(_siglist), 1)
        io, signal = _siglist[0]
        var = []
        signal(0, var)
        self.assertEqual(var, [1, 42])
    # End def #}}}

    def testSubscribeChoose(self): #{{{
        '''Subscribing choose types'''
        def rep(a, var):
            var.append(a + 100)
            return var
        def crep(a, var):
            return True

        self.assertEqual(len(_siglist), 0)
        subscribe('choose', dummy)
        self.assertEqual(len(_siglist), 1)
        subscribe('choose', rep, 'choose', crep)
        self.assertEqual(len(_siglist), 1)
        io, signal = _siglist[0]
        var = []
        signal(0, var)
        self.assertEqual(var, [100])
    # End def #}}}

    def testSubscribeAround(self): #{{{
        '''Subscribing around types'''
        def wrapper(func):
            def newcall(self, a, var):
                var.append(a + 200)
                ret = func(a, var)
                ret.append(a + 300)
                return ret
            return newcall

        self.assertEqual(len(_siglist), 0)
        subscribe('around', dummy)
        self.assertEqual(len(_siglist), 1)
        subscribe('around', wrapper, 'around')
        self.assertEqual(len(_siglist), 1)
        io, signal = _siglist[0]
        var = []
        signal(0, var)
        self.assertEqual(var, [200, 1, 300])
    # End def #}}}
# End class #}}}

