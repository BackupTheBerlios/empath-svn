# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.enum import Enum

class Test_eq(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSingleValue(self): #{{{
        '''Single value enum is equal'''
        test = Enum(red=42)
        self.assertEqual(test, 42)
        self.assertNotEqual(test, 1)
    # End def #}}}

    def testMultiValue(self): #{{{
        '''Multi value enum is equal'''
        names = 'abcdefghijklmn'
        valid = len(names) - 1
        d = dict(zip(names, range(valid + 1)))
        test = Enum(**d)
        from random import randint
        for i in xrange(valid+1):
            self.assertEqual(test, i)
        for i in xrange(20):
            self.assertNotEqual(test, randint(valid+2, 100+valid+2))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

