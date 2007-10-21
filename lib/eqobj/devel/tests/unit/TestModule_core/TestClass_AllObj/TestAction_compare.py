# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import AllObj
from eqobj.validators.type import InstanceType as itype

class Test_compare(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_single(self): #{{{
        '''Single compare'''
        a = AllObj(itype(int))
        self.assertEqual(a, 1)
        self.assertNotEqual(a, '1')
    # End def #}}}

    def test_multi(self): #{{{
        '''Multi compare'''
        a = AllObj(*map(itype, [bool, int]))
        self.assertNotEqual(a, 1)
        self.assertEqual(a, True)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

