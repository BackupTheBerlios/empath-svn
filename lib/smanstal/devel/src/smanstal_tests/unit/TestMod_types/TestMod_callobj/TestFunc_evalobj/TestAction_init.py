# Module: anyall.tests.TestPkg_anyall.TestMod_callobj.TestFunc_evalobj.TestAction_init
# File: TestAction_init.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the anyall project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.callobj import *
from smanstal.types import callobj as mod_callobj
from smanstal.types.module import absmodpath

class Test_evalobj_init(BaseUnitTest): #{{{
    def testPassNonString(self): #{{{
        '''Cannot evaluate non-basestring'''
        msg = re.compile("Cannot evaluate int object")
        self.assertRaisesEx(TypeError, evalobj, 1, exc_pattern=msg)
    # End def #}}}

    def testCopyConstructor(self): #{{{
        '''Passing in an evalobj instance copies internal vars'''
        g = globals()
        l = locals()
        a = evalobj('1', g, l)
        b = evalobj(a)
        self.assertTrue(b._evalstr is a._evalstr)
        self.assertTrue(b._globals is a._globals)
        self.assertTrue(b._locals is a._locals)
    # End def #}}}

    def testNoGlobals(self): #{{{
        '''No globals passed in will get globals of module'''
        modpath = absmodpath(mod_callobj)
        a = evalobj('1')
        g = a._globals
        self.assertTrue('__file__' in g)
        self.assertEqual(g['__file__'], mod_callobj.__file__)
        self.assertEqual(absmodpath(g['__file__']), modpath)
    # End def #}}}

    def testNoLocals(self): #{{{
        '''No locals passed in will be set to globals'''
        g = {'hello': 'world'}
        a = evalobj('1', g)
        self.assertTrue(a._locals is g)
    # End def #}}}
    
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

