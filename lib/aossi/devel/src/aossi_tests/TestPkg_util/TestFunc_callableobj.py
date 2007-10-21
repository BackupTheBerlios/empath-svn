# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import callableobj
from inspect import isfunction

class Test_callableobj(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable returns None'''
        self.assertTrue(callableobj(1) is None)
    # End def #}}}

    def testMethodFunc(self): #{{{
        '''Return object if a function or a method'''
        def _(): #{{{
            pass
        # End def #}}}
        for o in (_, self.setUp):
            self.assertTrue(callableobj(o) is o)
    # End def #}}}

    def testCallable(self): #{{{
        '''Callable object with __call__ method returns the method'''
        class _(object): #{{{
            def __call__(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        self.assertEqual(callableobj(t), t.__call__)
    # End def #}}}

    def testClass(self): #{{{
        '''Classes are callable objects too'''
        class _(object): #{{{
            pass
        # End class #}}}
        ret = callableobj(_)
        self.assertTrue(ret)
        self.assertTrue(isfunction(ret))
    # End def #}}}

    def testWrap(self): #{{{
        '''Any other objects get wrapped in a function'''
        _ = isinstance
        self.assertFalse(isfunction(_))
        ret = callableobj(_)
        self.assertTrue(ret)
        self.assertTrue(isfunction(ret))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

