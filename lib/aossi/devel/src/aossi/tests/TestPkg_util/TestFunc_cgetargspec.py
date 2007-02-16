# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import cgetargspec

class Test_cgetargspec(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable returns None'''
        self.assertTrue(cgetargspec(1) is None)
    # End def #}}}

    def testNoDefaults(self): #{{{
        '''No defaults returns empty dict'''
        def _(a, b): #{{{
            pass
        # End def #}}}
        ret = cgetargspec(_)
        self.assertTrue(ret)
        self.assertEqual(len(ret), 4)
        self.assertTrue(isinstance(ret[3], dict))
        self.assertFalse(ret[3])
    # End def #}}}

    def testDefaultDict(self): #{{{
        '''Returns default name/value pair in dictionary map'''
        def _(a, b=1): #{{{
            pass
        # End def #}}}
        ret = cgetargspec(_)
        self.assertTrue(ret)
        self.assertTrue(len(ret), 4)
        self.assertTrue(isinstance(ret[3], dict))
        self.assertEqual(ret[3], {'b': 1})
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

