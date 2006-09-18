# Module: aossi.tests.Test_msgsub.Test_examples
# File: Test_examples.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.msgsub import *
from aossi.msgsub import _siglist as sldict

class Testexamples(unittest.TestCase): #{{{
    def setUp(self): #{{{
        def test(a):
            if not hasattr(a.args, 'alist'):
                a.args.alist = []
            a.args.alist.append('test')
        def test2(a):
            if not hasattr(a.args, 'alist'):
                a.args.alist = []
            a.args.alist.append('test2')
        def test3(a):
            if not hasattr(a.args, 'alist'):
                a.args.alist = []
            a.args.alist.append('test3')
        self.test = test
        self.test2 = test2
        self.test3 = test3
    # End def #}}}

    def tearDown(self): #{{{
        sldict.clear()
        self.test = None
        self.test2 = None
        self.test3 = None
    # End def #}}}

    def testSubscribeExample(self): #{{{
        '''subscribe example'''
        subscribe('test', self.test)
        self.assertEqual(len(sldict), 1)
        self.assertEqual(sldict.keys()[0], 'test')
    # End def #}}}

    def testSimpleCancelExample(self): #{{{
        '''simple cancel example'''
        subscribe('test', self.test)
        subscribe('test2', self.test)
        subscribe('test3', self.test)
        self.assertEqual(len(sldict), 3)

        cancel('test')
        self.assertEqual(len(sldict), 2)
        keys = set(sldict.keys())
        e = set(['test2', 'test3'])
        self.assertEqual(keys, e)

        cancel('test3', Message, Arguments)
        self.assertEqual(len(sldict), 1)
        keys = set(sldict.keys())
        e = set(['test2'])
        self.assertEqual(keys, e)

        sldict.clear()
        subscribe('test', self.test)
        subscribe('test2', self.test)
        subscribe('test3', self.test)
        self.assertEqual(len(sldict), 3)

        cancel()
        self.assertEqual(len(sldict), 0)
    # End def #}}}

    def testMediumCancelExample(self): #{{{
        '''medium cancel example'''
        class M2(Message): pass
        class A2(Arguments): pass
        test = subscribe('test', self.test)
        test2 = subscribe('test2', self.test, M2, A2)
        subscribe('test', self.test, M2, A2)

        subscribe('test', self.test2)
        subscribe('test', self.test2, M2, A2)
        subscribe('test2', self.test2, M2, A2)
        subscribe('test', self.test3)
        subscribe('test', self.test3, M2, A2)
        subscribe('test2', self.test3, M2, A2)
        self.assertEqual(len(sldict), 2)
        ret = publish('test')
        self.assert_(hasattr(ret.args, 'alist'))
        self.assertEqual(ret.args.alist, ['test', 'test2', 'test3'])

        cancel('test', Message, Arguments, self.test2)
        ret = publish('test')
        self.assert_(hasattr(ret.args, 'alist'))
        self.assertEqual(ret.args.alist, ['test', 'test3'])

        ret = publish('test', M2, A2)
        self.assert_(hasattr(ret.args, 'alist'))
        self.assertEqual(ret.args.alist, ['test', 'test2', 'test3'])

        cancel('test', M2, A2, self.test3)
        ret = publish('test', M2, A2)
        self.assert_(hasattr(ret.args, 'alist'))
        self.assertEqual(ret.args.alist, ['test', 'test2'])

        cancel('test2', M2, A2, keep_signal=True)
        ret = publish('test2', M2, A2)
        self.assert_(hasattr(ret.args, 'alist'))
        self.assertEqual(ret.args.alist, ['test'])
    # End def #}}}
# End class #}}}

