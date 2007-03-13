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

class Test_getcallable(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNormalFunction(self): #{{{
        '''Return back normal functions and unbound methods'''
        _ = (lambda: None)
        ub_ = method(_, None, None)
        for f in (_, ub_):
            cw = CallableWrapper(f)
            ret = cw._getcallable()
            self.assertEqual(ret, f)
    # End def #}}}

    def testDeadReferences(self): #{{{
        '''If the reference dies, return None'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        cw = CallableWrapper(t.me, weak=True)
        del t
        self.assertTrue(cw._getcallable() is None)
    # End def #}}}

    def testMethod(self): #{{{
        '''Bound and instance methods'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t1, i_ = _.me, _()
        t2 = i_.me
        for f in (t1, t2):
            cw = CallableWrapper(f)
            ret = cw._getcallable()
            self.assertNotEqual(ret, f)
            self.assertEqual(ret, f.im_func)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

