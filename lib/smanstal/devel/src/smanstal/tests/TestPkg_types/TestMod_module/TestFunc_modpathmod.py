# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite
from smanstal.types.module import modpathmod

class Test_modpathmod(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testBadArg(self): #{{{
        '''Non-None, non-basestring raises error'''
        msg = re.compile(r"Cannot retrieve module from int object")
        self.assertRaisesEx(TypeError, modpathmod, 1, exc_pattern=msg)
    # End def #}}}

    def testNone(self): #{{{
        '''Passing None returns None'''
        self.assertTrue(not modpathmod(None))
        self.assertTrue(not modpathmod(''))
    # End def #}}}

    def testNonPathStr(self): #{{{
        '''Passing non-python module path raises error'''
        msg = re.compile(r"'/usr/lib/python2.4/inspect.py' is not a valid python module path")
        self.assertRaisesEx(ValueError, modpathmod, '/usr/lib/python2.4/inspect.py', exc_pattern=msg)
    # End def #}}}

    def testRootPackage(self): #{{{
        '''Import root package'''
        import smanstal
        self.assertTrue(modpathmod('smanstal') is smanstal)
    # End def #}}}

    def testPackagePath(self): #{{{
        '''Import sub-package'''
        import smanstal.types as st
        self.assertTrue(modpathmod('smanstal.types') is st)
    # End def #}}}

    def testModulePath(self): #{{{
        '''Import sub-module'''
        from smanstal.types import module
        self.assertTrue(modpathmod('smanstal.types.module') is module)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

