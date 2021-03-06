# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.deco import *

class UnitTestTemplate(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testDefault(self): #{{{
        '''Always suceeds'''
        var = []

        @setsignal(globals=locals())
#        @signal
        def test(s, a):
            return 'Default'
        
        @test.when('a == 1')
        def replacement(s, a):
            return 'Replacement'

        class A(object):
            @test.when('var')
            def newtest(self, a):
                return 'newtest'

        @test.onreturn
        def helloworld(ret):
            if ret == 'Replacement':
                var.append(1)
        a = A()

        self.assertEqual(test(a, 42), 'Default')
        self.assertEqual(test(a, 1), 'Replacement')
        self.assertEqual(test(a, 2), 'newtest')
    # End def #}}}

    def testCascade(self): #{{{
        var = []

        @signal
        def test(a):
            a.append('first')

        @test.cascade('True', True)
        def test1(a):
            a.append('test1')

        @test.cascade('True')
        def test2(a):
            a.append('test2')

        @test.cascade('True')
        def test3(a):
            a.append('test3')

        test(var)
        expected = ['first', 'test1']
        self.assertEqual(var, expected)
    # End def #}}}
# End class #}}}

