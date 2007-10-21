# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# Note: this uses the same tests as for CallableWrapper._getcallable()
# but modified to use CallableWrapper._getref() instead.

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.cwrapper import CallableWrapper
from types import MethodType as method

class Test_getref(BaseUnitTest): #{{{
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
            ret = cw._getref()()
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
        self.assertTrue(cw._getref()() is None)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

