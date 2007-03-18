# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.introspect import ispackage
from smanstal.types import introspect
from smanstal import types
import smanstal

class Test_ispackage(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testPackageModule(self): #{{{
        '''Package module returns True'''
        for p in (types, smanstal):
            self.assertTrue(ispackage(p))
    # End def #}}}

    def testNonPackageModule(self): #{{{
        '''Non-package module returns False'''
        self.assertFalse(ispackage(introspect))
    # End def #}}}

    def testPythonObject(self): #{{{
        '''Arbitrary python object returns False'''
        self.assertFalse(ispackage(1))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

