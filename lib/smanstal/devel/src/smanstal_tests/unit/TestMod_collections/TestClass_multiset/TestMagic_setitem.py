# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections import multiset

class Test_setitem(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSetZero(self): #{{{
        '''Setting to zero deletes'''
        a = multiset((10, 20, 30))
        a[10] = 0
        expected = set({20:1, 30:1}.items())
        self.assertEqual(set(a.items()), expected)
    # End def #}}}

    def testBadNegative(self): #{{{
        '''Cannot set negative values'''
        a = multiset([20])
        msg = re.compile("Negative element counts are invalid: -100")
        self.assertRaisesEx(ValueError, a.__setitem__, 20, -100, exc_pattern=msg)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

