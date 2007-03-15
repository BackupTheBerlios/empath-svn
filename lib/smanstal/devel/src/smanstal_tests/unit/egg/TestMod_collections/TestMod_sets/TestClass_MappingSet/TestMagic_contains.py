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

class Test_contains(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testUsage(self): #{{{
        '''Test usage: BaseMappingSet.__contains__'''
        a = MappingSet()
        test = [1, 'a', 'hello', 2.2, a, (1, 2, 3), [1, 2, 3]]
        for el in test:
            self.assertFalse(el in a)

        a = MappingSet([1, 3, 4])
        for el in test:
            if isinstance(el, int):
                self.assertTrue(el in a)
            else:
                self.assertFalse(el in a)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

