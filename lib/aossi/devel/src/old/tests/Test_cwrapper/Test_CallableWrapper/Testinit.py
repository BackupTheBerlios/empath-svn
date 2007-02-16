# Module: aossi.tests.Test_sigslot.Test_CallableWrapper.Testinit
# Module: Testinit.py
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
#from aossi.sigslot import CallableWrapper, cref
from aossi.cwrapper import CallableWrapper
from aossi.misc import cref
from weakref import ref, ReferenceType

def DummyFunction():
    pass

class DummyClass(object): #{{{
    def DummyMethod(self): #{{{
        pass
    # End def #}}}
# End class #}}}

class Test__init__(unittest.TestCase): #{{{
    def setUp(self): #{{{
        self.w = CallableWrapper(DummyFunction)
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Initializing with non-callable is illegal'''
        try:
            w = CallableWrapper(1)
            self.assert_(False)
        except TypeError, err:
            self.assertEqual(str(err).strip(), 'Argument must be a valid callable object')
        except:
            self.assert_(False)
    # End def #}}}

#    def testUnexpectedKeywordArguments(self): #{{{
#        '''Unexpected keyword arguments is illegal'''
#        try:
#            w = CallableWrapper(DummyFunction, hello=1)
#            self.assert_(False)
#        except ValueError, err:
#            self.assertEqual(str(err).strip(), 'valid keyword arguments are: hardwrap')
#        except:
#            self.assert_(False)
#    # End def #}}}

    def testNonMethodCallable(self): #{{{
        '''Initializing with non-method callable sets simple weakref'''
        self.assert_(self.w._object is None)
        self.assert_(isinstance(self.w._function, cref))
        self.assert_(self.w._function() is DummyFunction)
    # End def #}}}

    def testInstanceMethodCallable(self): #{{{
        '''Initializing with an instance method callable sets weakref on instance and stores method's internal function'''
        A = DummyClass
        a = A()
        w = CallableWrapper(a.DummyMethod)
        self.assert_(w._object is not None)
        self.assert_(isinstance(w._object, cref))
        self.assert_(w._object() is a)
        self.assert_(w._function is a.DummyMethod.im_func)
    # End def #}}}

    def testClassMethodCallable(self): #{{{
        '''Initializing with a class method callable sets weakref on class and stores method's internal function'''
        A = DummyClass
        w = CallableWrapper(A.DummyMethod)
        self.assert_(w._object is not None)
        self.assert_(isinstance(w._object, cref))
        self.assert_(w._object() is A)
        self.assert_(w._function is A.DummyMethod.im_func)
    # End def #}}}

    def testNonCallableCallback(self): #{{{
        '''Initializing with non-callable callaback is illegal'''
        try:
            w = CallableWrapper(DummyFunction, 1)
            self.assert_(False)
        except TypeError, err:
            self.assertEqual(str(err).strip(), 'callback argument must be a callable object')
        except:
            self.assert_(False)
    # End def #}}}

#    def testHardWrapInstanceMethod(self): #{{{
#        '''Setting hardwrap for instance method stores method name'''
#        A = DummyClass
#        a = A()
#        w = CallableWrapper(a.DummyMethod, hardwrap=True)
#        self.assertEqual(w._hardwrap, 'DummyMethod')
#    # End def #}}}

#    def testHardWrapClassMethod(self): #{{{
#        '''Setting hardwrap for class method stores method name'''
#        A = DummyClass
#        w = CallableWrapper(A.DummyMethod, hardwrap=True)
#        self.assertEqual(w._hardwrap, 'DummyMethod')
#    # End def #}}}

#    def testHardWrapNonMethod(self): #{{{
#        '''Setting hardwrap for non-method callable is ignored'''
#        w = CallableWrapper(DummyFunction, hardwrap=True)
#        self.assert_(w._hardwrap is None)
#    # End def #}}}

# End class #}}}

