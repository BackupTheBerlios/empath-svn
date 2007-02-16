# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import (methodtype, METHODTYPE_NOTMETHOD, 
        METHODTYPE_UNBOUND, METHODTYPE_CLASS, METHODTYPE_INSTANCE)
from smanstal.types.introspect import ismethod
from types import MethodType as method

class UnitTestTemplate(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonMethod(self): #{{{
        '''Non-method'''
        self.assertEqual(methodtype(2), METHODTYPE_NOTMETHOD)
    # End def #}}}

    def testUnboundMethod(self): #{{{
        '''Unbound method'''
        class A(object): pass
        def _(s): #{{{
            pass
        # End def #}}}
        _ = method(_, None, None)
        self.assertEqual(methodtype(_), METHODTYPE_UNBOUND)
    # End def #}}}

    def testClassMethod(self): #{{{
        '''Class methods'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        self.assertEqual(methodtype(_.me), METHODTYPE_CLASS)
    # End def #}}}

    def testInstanceMethod(self): #{{{
        '''Instance method'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        self.assertEqual(methodtype(_().me), METHODTYPE_INSTANCE)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

