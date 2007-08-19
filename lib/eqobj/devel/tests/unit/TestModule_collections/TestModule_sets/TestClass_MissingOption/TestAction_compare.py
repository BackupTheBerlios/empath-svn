# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.sets import AllSetElements, MissingOption

class TestMissing(MissingOption, AllSetElements): pass

class Test_missingoption(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_missing(self): #{{{
        '''Missing expected keys'''
        a = TestMissing(range(5), missing=True)
        self.assertTrue(a((0, 2, 4)))
    # End def #}}}

    def test_nomissing(self): #{{{
        '''No missing'''
        a = TestMissing(range(5))
        self.assertFalse(a((0, 2, 4)))
    # End def #}}}

    def test_falsemissing(self): #{{{
        '''missing == False'''
        a = TestMissing(range(5), missing=False)
        self.assertFalse(a((0, 2, 4)))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

