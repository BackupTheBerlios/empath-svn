# Module: aossi.tests.Test_subscription.Test_publish
# File: Test_publish.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.subscription import publish, _siglist, subscribe
from warnings import filterwarnings, resetwarnings

def dummy(a, var):
    var.append(a + 1)
    return var

def dummy2(a, var):
    var.append(a + 2)

class Testpublish(unittest.TestCase): #{{{
    def setUp(self): #{{{
        while _siglist:
            _siglist.pop()
        filterwarnings('error')
    # End def #}}}

    def tearDown(self): #{{{
        resetwarnings()
    # End def #}}}

    def testPublishUnsubscribed(self): #{{{
        '''Publishing to an unsubscribed issue sends a warning'''
        try:
            publish('something', 1, 2, 3)
            self.assert_(False)
        except RuntimeWarning, err:
            e = str(err).strip()
            self.assertEqual(e, 'Publishing to unsubscribed issue')
    # End def #}}}

    def testPublish(self): #{{{
        '''Publish sends to the correct issue'''
        def dummy3(a, var):
            var.append(a + 3)
        subscribe('first', dummy)
        subscribe('first', dummy2)

        subscribe('second', dummy)
        subscribe('second', dummy3)
        self.assertEqual(len(_siglist), 2)
        var = []
        publish('first', 0, var)
        self.assertEqual(var, [1, 2])

        var = []
        publish('second', 2, var)
        self.assertEqual(var, [3, 5])
    # End def #}}}
# End class #}}}

