# Module: unit.TestMod_types.TestMod_introspect.TestFunc_isproperty
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.introspect import isproperty

class Test_isproperty(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonProperty(self): #{{{
        '''Non-property argument returns False'''
        self.assertFalse(isproperty(1))
    # End def #}}}

    def testProperty(self): #{{{
        '''Property argument returns True'''
        self.assertTrue(isproperty(property(lambda s: 1)))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

