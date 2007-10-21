# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.cwrapper import CallableWrapper

from types import MethodType as method

class Test_wrap(BaseUnitTest): #{{{
    def setUp(self): #{{{
        def deco(f): #{{{
            def w(s, a1, a2): #{{{
                if not isinstance(a1, basestring):
                    return False
                return f(a1, a2)
            # End def #}}}
            return w
        # End def #}}}
        self.deco = deco
        self.func = isinstance
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallableArg(self): #{{{
        '''Non-callable argument raises error'''
        cw = CallableWrapper(map)
        msg = re.compile(r'Argument must be a valid callable object')
        self.assertRaisesEx(TypeError, cw.wrap, 1, exc_pattern=msg)
    # End def #}}}

    def testNonCallableDeco(self): #{{{
        '''If return value of argument is not callable, raise error'''
        cw = CallableWrapper(isinstance)
        _ = lambda f: 1
        msg = re.compile(r'Return value of wrapping callable must be a valid callable object')
        self.assertRaisesEx(TypeError, cw.wrap, _, exc_pattern=msg)
    # End def #}}}

    def testMethodWrap(self): #{{{
        '''If return value of arg is not a method, makes it into a method'''
        cw = CallableWrapper(self.func)
        cw.wrap(self.deco)
        self.assertTrue(isinstance(cw._newcall, method))
    # End def #}}}

    def testWrap(self): #{{{
        '''Proper wrap functionality given proper input'''
        cw = CallableWrapper(self.func)
        cw.wrap(self.deco)
        self.assertTrue(cw._newcall('a', str))
        self.assertFalse(cw._newcall('a', unicode))
        self.assertTrue(cw._newcall(u'a', unicode))
        self.assertFalse(cw._newcall(1, int))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

