# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections.sets import MappingSet

class Test_xor(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.set = MappingSet([1, 2, 3])
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testReturnMappingSet(self): #{{{
        '''Return type is a MappingSet instance'''
        ret = self.set ^ [1, 2, 3]
        self.assertTrue(ret.__class__ is MappingSet)
    # End def #}}}

    def testEmptySet(self): #{{{
        '''Return empty set if no common elements'''
        ret = self.set ^ [1, 2, 3]
        self.assertFalse(ret)
    # End def #}}}

    def testUncommon(self): #{{{
        '''Return only uncommon elements'''
        ret = self.set ^ [1, 2, 5]
        self.assertEquals(ret, [3, 5])
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

