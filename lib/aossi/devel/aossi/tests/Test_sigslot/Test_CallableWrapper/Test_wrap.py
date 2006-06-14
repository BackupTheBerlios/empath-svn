# Module: aossi.tests.Test_sigslot.Test_CallableWrapper.Test_wrap
# File: Test_wrap.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import CallableWrapper, iscallable, num_static_args
from aossi.cwrapper import CallableWrapper, num_static_args
from aossi.misc import iscallable
from types import MethodType as method

def DummyReplacement(f): #{{{
    def newcall(self, *args, **kwargs): #{{{
        ret = f(*args, **kwargs)
        return "HELLO: %s :WORLD" %str(ret)
    # End def #}}}
    return newcall
# End def #}}}

def DummyFunction(a, b): #{{{
    return "MEMEMEME"
# End def #}}}

class Testwrap(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonMethodWrap(self): #{{{
        '''Wrapping a non-method callable'''
        w = CallableWrapper(DummyFunction)
        w.wrap(DummyReplacement)
        self.assertEqual(w(1, 2), "HELLO: %s :WORLD" %DummyFunction(1, 2))
    # End def #}}}

    def testClassMethodWrap(self): #{{{
        '''Wrapping class method'''
        class A(object):
            def helloworld(self, a, b):
                return 'hello world'

        w = CallableWrapper(A.helloworld)
        w.wrap(DummyReplacement)
        A.helloworld = method(w, None, A)
    
        z = CallableWrapper(A.helloworld)
        z.wrap(DummyReplacement)
        A.helloworld = method(z, None, A)

        a = A()
        self.assertEqual(a.helloworld(1, 2), 'HELLO: HELLO: hello world :WORLD :WORLD')
    # End def #}}}

    def testInstanceMethodWrap(self): #{{{
        '''Wrapping instance method'''
        class A(object):
            def helloworld(self, a, b):
                return 'hello world'

        a = A()
        w = CallableWrapper(a.helloworld)
        w.wrap(DummyReplacement)
        a.helloworld = method(w, a, A)
    
        z = CallableWrapper(a.helloworld)
        z.wrap(DummyReplacement)
        a.helloworld = method(z, a, A)

        self.assertEqual(a.helloworld(1, 2), 'HELLO: HELLO: hello world :WORLD :WORLD')
        self.assertEqual(A().helloworld(1, 2), 'hello world')
     # End def #}}}

    def testUnWrap(self): #{{{
        '''Unwrap'''
        class A(object):
            def helloworld(self, a, b):
                return 'hello world'

        a = A()
        w = CallableWrapper(a.helloworld)
        w.wrap(DummyReplacement)
        a.helloworld = method(w, a, A)
    
        self.assertEqual(a.helloworld(1, 2), 'HELLO: hello world :WORLD')
        self.assertEqual(A().helloworld(1, 2), 'hello world')
        w.unwrap()
        self.assertEqual(A().helloworld(1, 2), a.helloworld(1, 2))
    # End def #}}}
# End class #}}}

