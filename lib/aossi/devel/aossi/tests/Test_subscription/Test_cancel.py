# Module: aossi.tests.Test_subscription.Test_cancel
# File: Test_cancel.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.subscription import subscribe, cancel, _siglist

def dummy(a, var):
    var.append(a + 1)
    return var

def dummy2(a, var):
    var.append(a + 2)

class Testcancel(unittest.TestCase): #{{{
    def setUp(self): #{{{
        while _siglist:
            _siglist.pop()
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testCancelAll(self): #{{{
        '''Cancel all subscriptions'''
        s = 'cancel all'
        self.assertEqual(len(_siglist), 0)
        subscribe(s, dummy)
        subscribe(s, dummy2)
        self.assertEqual(len(_siglist), 1)
        cancel()
        self.assertEqual(len(_siglist), 0)
    # End def #}}}

    def testCancelOne(self): #{{{
        '''Cancel a single subscription'''
        s = 'cancel one'
        self.assertEqual(len(_siglist), 0)
        subscribe(s, dummy)
        subscribe(s, dummy2)
        self.assertEqual(len(_siglist), 1)
        cancel(s)
        self.assertEqual(len(_siglist), 0)
    # End def #}}}

    def testCancelOneOfMany(self): #{{{
        '''Cancel a single subscription from many'''
        self.assertEqual(len(_siglist), 0)
        for s in xrange(5):
            subscribe(s, dummy)
        subscribe('special', dummy)
        for s in xrange(6, 10):
            subscribe(s, dummy)
        self.assertEqual(len(_siglist), 10)
        cancel('special')
        self.assertEqual(len(_siglist), 9)
        for io, signal in _siglist:
            self.assertNotEqual(io, 'special')
    # End def #}}}
# End class #}}}

