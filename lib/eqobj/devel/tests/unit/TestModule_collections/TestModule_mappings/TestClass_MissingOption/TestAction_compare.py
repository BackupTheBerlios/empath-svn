# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.mappings import AllKeys, MissingOption

class TestMissing(MissingOption, AllKeys): pass

class Test_missingoption(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_missing(self): #{{{
        '''Missing expected keys'''
        a = TestMissing(enumerate('abcde'), missing=True)
        self.assertTrue(a(zip((0, 2, 4), range(3))))
    # End def #}}}

    def test_nomissing(self): #{{{
        '''No missing'''
        a = TestMissing(enumerate('abcde'))
        self.assertFalse(a(zip((0, 2, 4), range(3))))
    # End def #}}}

    def test_falsemissing(self): #{{{
        '''missing == False'''
        a = TestMissing(enumerate('abcde'), missing=False)
        self.assertFalse(a(zip((0, 2, 4), range(3))))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

