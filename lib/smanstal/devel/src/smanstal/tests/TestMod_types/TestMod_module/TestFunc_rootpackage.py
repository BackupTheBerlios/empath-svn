# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite
from smanstal.types.module import rootpackage
import os.path as op

class Test_rootpackage(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonModule(self): #{{{
        '''Passing a non-module is bad'''
        msg = re.compile(r"Cannot determine root package of int object '1'")
        self.assertRaisesEx(TypeError, rootpackage, 1, exc_pattern=msg)
    # End def #}}}

    def testPythonPackage(self): #{{{
        '''Python package returns root package'''
        import smanstal.types as st
        import smanstal
        self.assertTrue(rootpackage(st) is smanstal)
    # End def #}}}

    def testPythonModule(self): #{{{
        '''Python module returns root package'''
        from smanstal.types import module
        import smanstal
        self.assertTrue(rootpackage(module) is smanstal)
    # End def #}}}

    def testRootPackage(self): #{{{
        '''Root package returns itself'''
        import smanstal
        self.assertTrue(rootpackage(smanstal) is smanstal)
    # End def #}}}

    def testDynamicModule(self): #{{{
        '''Dynamic module returns itself'''
        import new
        m = new.module('boo')
        self.assertTrue(rootpackage(m) is m)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

