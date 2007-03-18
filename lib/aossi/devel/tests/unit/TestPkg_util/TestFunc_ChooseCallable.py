# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import ChooseCallable, StopCascade, AmbiguousChoiceError

class Test_ChooseCallable(BaseUnitTest): #{{{
    def setUp(self): #{{{
        def mkfunc(i): #{{{
            l = lambda inp: i+inp > 10
            r = lambda inp: i+inp
            return (l, r)
        # End def #}}}
        self.choices = [mkfunc(i) for i in xrange(20)]
        self.origfunc = lambda i: i+400
        self.callfunc = lambda f, *a, **kw: f(*a, **kw)
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testFirstPolicy(self): #{{{
        '''Policy 'first' returns the first function that succeeds'''
        args = [0]
        ret = ChooseCallable(self.choices, 'first', self.origfunc, self.callfunc, *args)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0](*args), 11)
    # End def #}}}

    def testDefaultPolicy(self): #{{{
        '''Policy 'default' returns None'''
        args = [0]
        ret = ChooseCallable(self.choices, 'default', self.origfunc, self.callfunc, *args)
        self.assertTrue(ret is None)
    # End def #}}}

    def testLastPolicy(self): #{{{
        '''Policy 'last' returns the last function that succeeds'''
        args = [0]
        ret = ChooseCallable(self.choices, 'last', self.origfunc, self.callfunc, *args)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0](*args), 19)
    # End def #}}}

    def testCascadeOriginalFunc(self): #{{{
        '''Policy 'cascade' always returns the original function as first list element'''
        args = [0]
        ret = ChooseCallable(self.choices, 'cascade', self.origfunc, self.callfunc, *args)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(ret[0] is self.origfunc)
    # End def #}}}

    def testCascadePolicy(self): #{{{
        '''Policy 'cascade' returns all functions whose conditions succeeds'''
        args = [0]
        ret = ChooseCallable(self.choices, 'cascade', self.origfunc, self.callfunc, *args)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 10)
        for f, exp in zip(ret, [400] + range(11, 20)):
            self.assertEqual(f(*args), exp)
    # End def #}}}

    def testStopCascade(self): #{{{
        '''Any condition that raises a StopCascade stops cascade'''
        def modify(cond, f): #{{{
            if f(0) == 15:
                def cond(i): raise StopCascade()
            return (cond, f)
        # End def #}}}
        args = [0]
        choices = [modify(cond, f) for cond, f in self.choices]
        ret = ChooseCallable(choices, 'cascade', self.origfunc, self.callfunc, *args)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 5)
        for f, exp in zip(ret, [400] + range(11, 15)):
            self.assertEqual(f(*args), exp)
    # End def #}}}

    def testStopCascadeArg(self): #{{{
        '''If any argument passed to StopCascade, it will be bool casted and used as conditional value for that function'''
        def modify(cond, f, errval): #{{{
            if f(0) == 15:
                def cond(i): raise StopCascade(errval)
            return (cond, f)
        # End def #}}}
        args, origfunc, callfunc = [0], self.origfunc, self.callfunc
        for errval, elen, maxval in ((False, 5, 15), (True, 6, 16)):
            choices = [modify(cond, f, errval) for cond, f in self.choices]
            ret = ChooseCallable(choices, 'cascade', origfunc, callfunc, *args)
            self.assertTrue(ret)
            self.assertTrue(isinstance(ret, list))
            self.assertEqual(len(ret), elen)
            for f, exp in zip(ret, [400] + range(11, maxval)):
                self.assertEqual(f(*args), exp)
    # End def #}}}

    def testUnknownPolicy(self): #{{{
        '''If unknown policy and more than one conditional passes, raises AmbiguousChoiceError'''
        msg = re.compile(r'Found more than one selectable callable')
        fargs = [ChooseCallable, self.choices, None, self.origfunc, self.callfunc, 0]
        fkw = dict(exc_pattern=msg)
        self.assertRaisesEx(AmbiguousChoiceError, *fargs, **fkw)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

