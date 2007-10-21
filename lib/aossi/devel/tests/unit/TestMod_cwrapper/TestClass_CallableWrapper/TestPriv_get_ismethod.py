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

class Test_get_ismethod(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testDeadReference(self): #{{{
        '''Dead reference raises error'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        cw = CallableWrapper(t.me, weak=True)
        del t
        self.assertTrue(cw.isdead)
        msg = re.compile(r'Cannot determine callable type: dead reference')
        self.assertRaisesEx(ValueError, cw._get_ismethod, exc_pattern=msg)
    # End def #}}}

    def testBoundInstanceMethods(self): #{{{
        '''Bound or instance methods'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        for f in (_.me, t.me):
            cw = CallableWrapper(f)
            self.assertTrue(cw._get_ismethod())
    # End def #}}}

    def testNormalFunctions(self): #{{{
        '''Normal function or unbound method'''
        _ = lambda: None
        ub = method(_, None, None)
        for f in (_, ub):
            cw = CallableWrapper(f)
            self.assertFalse(cw._get_ismethod())
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

