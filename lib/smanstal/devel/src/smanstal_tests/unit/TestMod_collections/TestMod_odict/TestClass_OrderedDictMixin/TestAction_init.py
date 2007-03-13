# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections.odict import odict
from string import ascii_lowercase

class Testinit(BaseUnitTest): #{{{

    def setUp(self): #{{{
        self.mkinput = lambda input: ((v, k) for k, v in enumerate(input))
        self.d1 = ascii_lowercase[:13]
        self.d2 = ascii_lowercase[13:]
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testCreateVars(self): #{{{
        '''Init creates '_keys' empty list private variable'''
        od = odict()
        self.assertTrue(hasattr(od, '_keys'))
        self.assertTrue(isinstance(od._keys, list))
        self.assertEqual(len(od._keys), 0)
    # End def #}}}

    def testEmptyDict(self): #{{{
        '''Create an empty dict'''
        od = odict()
        self.assertFalse(od)
        self.assertEqual(len(od), 0)
        self.assertEqual(len(list(dict.__iter__(od))), 0)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

