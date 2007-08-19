# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj
from eqobj.collections.sets import AllSetElementsMixin, TrimOption

class TestTrim(TrimOption, AllSetElementsMixin, EqObj): pass

class Test_trimoption(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_trim(self): #{{{
        '''Trims unknown keys'''
        a = TestTrim(range(5), trim=True)
        self.assertTrue(a(range(10)))
    # End def #}}}

    def test_notrim(self): #{{{
        '''No trim'''
        a = TestTrim(range(5))
        self.assertFalse(a(range(10)))
    # End def #}}}

    def test_falsetrim(self): #{{{
        '''Trim == False'''
        a = TestTrim(range(5), trim=False)
        self.assertFalse(a(range(10)))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

