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

class Test_eq(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoLength(self): #{{{
        '''Passing object with no length returns false'''
        a = MappingSet([1, 2, 3])
        self.assertNotEquals(a, 1)
    # End def #}}}

    def testDifferentLengths(self): #{{{
        '''Different length sequence returns False'''
        a = MappingSet([1, 2, 3])
        self.assertNotEquals(a, range(4))
        self.assertNotEquals(a, range(2))
    # End def #}}}

    def testDifferentContents(self): #{{{
        '''Same length but different contents returns False'''
        a = MappingSet([1, 2, 3])
        self.assertNotEquals(a, range(17, 20))
        self.assertNotEquals(a, [1, 2, 4])
    # End def #}}}

    def testSame(self): #{{{
        '''Same length and same contents returns True'''
        a = MappingSet([1, 2, 3])
        self.assertEquals(a, [1, 2, 3])
        self.assertEquals(a, (1, 2, 3))
        self.assertEquals(a, dict((i, i) for i in range(1, 4)))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

