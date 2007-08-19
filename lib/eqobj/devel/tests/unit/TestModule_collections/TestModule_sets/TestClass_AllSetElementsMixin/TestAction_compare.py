# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.sets import AllSetElements

class Test_allkeys(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_unequal_lengths(self): #{{{
        '''Unequal lengths is always False'''
        a = AllSetElements(range(5))
        self.assertFalse(a(range(9)))
        self.assertFalse(a(range(3)))
    # End def #}}}

    def test_nomatch(self): #{{{
        '''No match'''
        a = AllSetElements(range(5))
        self.assertFalse(a((0, 1, 2, 9, 10)))
    # End def #}}}

    def test_match(self): #{{{
        '''Sets match'''
        a = AllSetElements(range(5))
        self.assertTrue(a(range(5)))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

