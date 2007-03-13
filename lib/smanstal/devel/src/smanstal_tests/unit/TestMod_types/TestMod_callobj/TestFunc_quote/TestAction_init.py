# Module: anyall.tests.TestPkg_anyall.TestMod_callobj.TestFunc_quote.TestAction_init
# File: TestAction_init.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the anyall project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.callobj import quote
from weakref import ref

class Test_quote(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSetKeywords(self): #{{{
        '''Valid keywords get set properly'''
        a = quote(1, weak=False)
        self.assertTrue(a._isweak is False)
    # End def #}}}

    def testMakeWeakRef(self): #{{{
        '''Set weak reference'''
        class Test(object): pass
        t = Test()
        a = quote(t)
        self.assertTrue(isinstance(a._ref, ref))
        self.assertTrue(a._isweak is True)
    # End def #}}}

    def testAuto(self): #{{{
        '''If cannot set weak reference, automatically make a strong reference'''
        val = ''.join(['hello', 'world'])
        test = 'helloworld'
        self.assertTrue(test == val)
        self.assertFalse(test is val)
        a = quote(val)
        self.assertFalse(isinstance(a._ref, ref))
        self.assertTrue(a._isweak is False)
        self.assertTrue(a._ref is val)

        msg = re.compile("cannot create weak reference to 'str' object")
        self.assertRaisesEx(TypeError, quote, val, auto=False, exc_pattern=msg)
    # End def #}}}

# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

