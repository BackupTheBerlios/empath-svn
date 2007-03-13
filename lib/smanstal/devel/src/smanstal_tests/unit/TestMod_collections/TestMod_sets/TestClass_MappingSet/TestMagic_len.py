# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections.sets import MappingSet

class Test_len(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoArgs(self): #{{{
        '''Passing no arguments is valid'''
        a = MappingSet()
    # End def #}}}

    def testInternalDictLen(self): #{{{
        '''Returns length of internal dict'''
        a = MappingSet()
        self.assertEquals(len(a), len(a._dict))
        self.assertEquals(len(a), 0)
        a = MappingSet(range(10))
        self.assertEquals(len(a), len(a._dict))
        self.assertEquals(len(a), 10)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

