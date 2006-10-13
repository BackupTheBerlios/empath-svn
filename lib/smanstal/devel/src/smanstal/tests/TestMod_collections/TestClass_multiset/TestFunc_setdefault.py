# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections import multiset

class Test_setdefault(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testDefault(self): #{{{
        '''Default set to 1'''
        a = multiset()
        res = a.setdefault('hello')
        self.assertEqual(dict(a), {'hello': 1})
        self.assertEqual(res, 1)
    # End def #}}}

    def testSetDefault(self): #{{{
        '''Set default properly'''
        a = multiset()
        res = a.setdefault('h', 200)
        self.assertEqual(dict(a), {'h': 200})
        self.assertEqual(res, 200)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

