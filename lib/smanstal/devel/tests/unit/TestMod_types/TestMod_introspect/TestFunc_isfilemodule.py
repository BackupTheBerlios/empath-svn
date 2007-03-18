# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.introspect import isfilemodule
from types import ModuleType as module

class Test_isfilemodule(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testFileModule(self): #{{{
        '''Module created from a file returns True'''
        self.assertTrue(isfilemodule(re))
    # End def #}}}

    def testNonFileModule(self): #{{{
        '''Non-file module returns False'''
        mod = module('testmod')
        self.assertFalse(isfilemodule(mod))
    # End def #}}}

    def testPythonObject(self): #{{{
        '''Arbitrary python object returns False'''
        self.assertFalse(isfilemodule(1))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

