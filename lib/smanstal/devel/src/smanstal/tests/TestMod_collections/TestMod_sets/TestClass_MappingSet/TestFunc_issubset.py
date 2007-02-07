# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections.sets import MappingSet

class Test_issubset(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.set = MappingSet(xrange(10))
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoLength(self): #{{{
        '''Argument with no length returns False'''
        nol = (i for i in xrange(10))
        self.assertFalse(self.set.issubset(nol))
    # End def #}}}
    def testUncommon(self): #{{{
        '''Set has uncommon elements returns False'''
        nol = range(1, 11)
        self.assertFalse(self.set.issubset(nol))
    # End def #}}}

    def testBigger(self): #{{{
        '''If set is bigger, return False'''
        o = range(9)
        self.assertFalse(self.set.issubset(o))
    # End def #}}}

    def testSame(self): #{{{
        '''Set is a subset of itself'''
        self.assertTrue(self.set.issubset(self.set))
    # End def #}}}

    def testSmaller(self): #{{{
        '''Smaller set with all elements'''
        self.assertTrue(self.set.issubset(range(20)))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

