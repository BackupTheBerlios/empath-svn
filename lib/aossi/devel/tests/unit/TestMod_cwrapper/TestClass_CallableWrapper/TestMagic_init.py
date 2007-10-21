# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.cwrapper import CallableWrapper, cid
from aossi.util import (cref, METHODTYPE_CLASS, METHODTYPE_INSTANCE,
        METHODTYPE_UNBOUND, METHODTYPE_NOTMETHOD)
from types import MethodType as method

class Test_init(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable raises error'''
        msg = re.compile(r'Argument must be a valid callable object')
        self.assertRaisesEx(TypeError, CallableWrapper, 1, exc_pattern=msg)
    # End def #}}}

    def testCallbackArg(self): #{{{
        '''Callback argument must be one of None, callable'''
        msg = re.compile(r'callback argument must be a callable object')
        self.assertRaisesEx(TypeError, CallableWrapper, max, 1, exc_pattern=msg)
    # End def #}}}

    def testWeakKWArg(self): #{{{
        '''Weak keyword arg'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        o = _()
        cw = CallableWrapper(o.me, weak=True)
        self.assertTrue(cw._object.isweak)
    # End def #}}}

    def testNumArgs(self): #{{{
        '''_numargs and _maxargs gets set properly'''
        t = lambda a, b, c=1, d=2: None
        cw = CallableWrapper(t)
        self.assertEqual(cw._numargs, 2)
        self.assertEqual(cw._maxargs, 4)
    # End def #}}}

    def testClassMethod(self): #{{{
        '''Class method gets class soft reference and function hard reference'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        cw = CallableWrapper(_.me)
        self.assertTrue(cw._object)
        self.assertTrue(isinstance(cw._object, cref))
        self.assertEqual(cw._object(), _)
        self.assertEqual(cw._function, _.me.im_func)
        self.assertEqual(cw._methodtype, METHODTYPE_CLASS)
    # End def #}}}

    def testInstanceMethod(self): #{{{
        '''Instance method gets instance soft reference and function hard reference'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        cw = CallableWrapper(t.me)
        self.assertTrue(cw._object)
        self.assertTrue(isinstance(cw._object, cref))
        self.assertEqual(cw._object(), t)
        self.assertEqual(cw._function, _.me.im_func)
        self.assertEqual(cw._function, t.me.im_func)
        self.assertEqual(cw._methodtype, METHODTYPE_INSTANCE)
    # End def #}}}

    def testNormalFunction(self): #{{{
        '''Normal functions and unbound methods'''
        def _(): #{{{
            pass
        # End def #}}}
        funcs = ((_, METHODTYPE_NOTMETHOD), (method(_, None, None), METHODTYPE_UNBOUND))
        for f, mt in funcs:
            cw = CallableWrapper(f)
            self.assertTrue(cw._object is None)
            self.assertTrue(cw._function)
            self.assertTrue(isinstance(cw._function, cref))
            self.assertEqual(cw._function(), f)
            self.assertEqual(cw._methodtype, mt)
    # End def #}}}

    def testFuncID(self): #{{{
        '''Gets function id of original callable'''
        _ = lambda: None
        exp = cid(_)
        cw = CallableWrapper(_)
        self.assertEqual(cw._funcid, exp)
    # End def #}}}

    def testClass(self): #{{{
        '''Classes are valid callables'''
        class Test(object): pass
        cw = CallableWrapper(Test)
        self.assertEqual((cw.numargs, cw.maxargs), (0, None))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

