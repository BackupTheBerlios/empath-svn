# Module: anyall.tests.TestPkg_anyall.TestMod_callobj.TestFunc_callable.TestAction_init
# File: TestAction_init.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the anyall project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.egg.tests import BaseUnitTest, addtest, mksuite
from pkg_resources import Requirement
import os.path as op

__req__ = Requirement.parse('smanstal')

temp_path = op.abspath(__file__)
if op.exists(temp_path):
    __file__ = temp_path
del temp_path

from smanstal.types.callobj import callcallable, q, callobj

class Test_callcallable_init(BaseUnitTest): #{{{
    def testPassNonCallable(self): #{{{
        '''Non-callable is bad'''
        msg = re.compile("int object is not callable")
        self.assertRaisesEx(TypeError, callcallable, 1, exc_pattern=msg)
    # End def #}}}
    
    def testSetInternalVars(self): #{{{
        '''Internal vars get set'''
        a = callcallable(int)
        self.assertEqual(getattr(a, '_args'), tuple())
        self.assertEqual(getattr(a, '_kwargs'), dict())
        self.assertEqual(getattr(a, '_callable'), int)
    # End def #}}}

    def testArgsTransform(self): #{{{
        '''All args and keyword args are transformed into callobj objects'''
        def testme(*args, **kwargs): #{{{
            return len(args), len(kwargs)
        # End def #}}}

        a = callcallable(testme, 1, 2, q(testme), testme=q(testme), blue=1)
        self.assertEqual(len(a._args), 3)
        self.assertEqual(len(a._kwargs), 2)
        for arg in a._args:
            self.assertTrue(isinstance(arg, callobj))
        for k, v in a._kwargs.iteritems():
            self.assertTrue(isinstance(v, callobj))
            self.assertTrue(k in ('testme', 'blue'))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

