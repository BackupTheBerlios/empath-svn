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

class Test_call(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNormalFunction(self): #{{{
        '''Call normal functions'''
        class t(object): pass
        _ = lambda i: i+42
        cw = CallableWrapper(_)
        self.assertEqual(cw.call(0), _(0))
    # End def #}}}

    def testBoundInstanceMethods(self): #{{{
        '''Methods get class/instance sent'''
        class _(object): #{{{
            def me(self): #{{{
                return self is t
            # End def #}}}

            @classmethod
            def classme(cls): #{{{
                return cls is _
            # End def #}}}

            @staticmethod
            def ub(): #{{{
                return True
            # End def #}}}
        # End class #}}}
        t = _()
        b, i, ci, ub = _.classme, t.me, t.classme, t.ub
        for f in (b, i, ci, ub):
            cw = CallableWrapper(f)
            self.assertTrue(cw.call())
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

