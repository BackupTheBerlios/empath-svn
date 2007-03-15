# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.egg.tests import BaseUnitTest, addtest, mksuite
from pkg_resources import Requirement
import os.path as op

__req__ = Requirement.parse('smanstal')

temp_path = op.abspath(__file__)
if op.exists(temp_path):
    __file__ = temp_path
del temp_path

from smanstal.collections.sets import MappingSet

class Test_issuperset(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.set = MappingSet(xrange(10))
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoLength(self): #{{{
        '''Argument with no length returns False'''
        nol = (i for i in xrange(10))
        self.assertFalse(self.set.issuperset(nol))
    # End def #}}}
    def testUncommon(self): #{{{
        '''Other has uncommon elements returns False'''
        nol = range(1, 11)
        self.assertFalse(self.set.issuperset(nol))
    # End def #}}}

    def testBigger(self): #{{{
        '''If other is bigger, return False'''
        o = range(11)
        self.assertFalse(self.set.issuperset(o))
    # End def #}}}

    def testSame(self): #{{{
        '''Set is a superset of itself'''
        self.assertTrue(self.set.issuperset(self.set))
    # End def #}}}

    def testSmaller(self): #{{{
        '''Smaller other with all elements'''
        self.assertTrue(self.set.issuperset(range(9)))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

