# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.collections.mappings import AllKeys

class Test_allkeys(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_unequal_lengths(self): #{{{
        '''Unequal lengths is always False'''
        a = AllKeys(enumerate('abcde'))
        self.assertFalse(a(enumerate('abcdefghi')))
        self.assertFalse(a(enumerate('abc')))
    # End def #}}}

    def test_nomatch(self): #{{{
        '''No match'''
        a = AllKeys(enumerate('abcde'))
        self.assertFalse(a(zip((0, 1, 2, 9, 10), 'abcde')))
    # End def #}}}

    def test_match(self): #{{{
        '''Mappings match'''
        a = AllKeys(enumerate('abcde'))
        self.assertTrue(a(enumerate('abcde')))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

