# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections.sets import BaseMappingSet, MappingSet

class Test_init(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoInitBase(self): #{{{
        '''No direct instantiation of BaseMappingSet'''
        msg = re.compile("BaseMappingSet is an abstract class")
        self.assertRaisesEx(NotImplementedError, BaseMappingSet, (), exc_pattern=msg)
    # End def #}}}

    def testInitDict(self): #{{{
        '''Intializes internal dict'''
        a = MappingSet([1, 2, 3])
        expected = {1:1, 2:2, 3:3}
        self.assertEquals(a._dict, expected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

