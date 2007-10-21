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

class Test_get_original(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testDead(self): #{{{
        '''Raise error if reference died'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        cw = CallableWrapper(t.me, weak=True)
        del t
        self.assertTrue(cw.isdead)
        msg = re.compile(r'Cannot retrieve original: dead reference')
        self.assertRaisesEx(ValueError, cw._get_original, exc_pattern=msg)
    # End def #}}}

    def testNormalFunction(self): #{{{
        '''Normal functions or unbound methods return _getcallable result'''
        _ = lambda: None
        ub = method(_, None, None)

        for f in (_, ub):
            cw = CallableWrapper(f)
            gcr = cw._getcallable()
            self.assertEqual(cw._get_original(), gcr)
    # End def #}}}

    def testBoundInstanceMethods(self): #{{{
        '''Bound or instance methods returns same'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        b, i = _.me, t.me
        for f in (b, i):
            cw = CallableWrapper(f)
            ret = cw._get_original()
            self.assertEqual(ret, f)
            self.assertTrue(ret.im_class is f.im_class)
            self.assertTrue(ret.im_self is f.im_self)
            self.assertTrue(ret.im_func is f.im_func)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

