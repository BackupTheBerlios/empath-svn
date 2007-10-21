# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import cargval

class Test_cargval(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable returns None'''
        self.assertTrue(cargval(1) is None)
    # End def #}}}

    def testReturnDefaults(self): #{{{
        '''Return default name/value mapping only'''
        def _(a, b, c=1, d=2, e=3): #{{{
            pass
        # End def #}}}
        ret = cargval(_)
        self.assertTrue(ret)
        self.assertTrue(isinstance(ret, dict))
        self.assertEqual(ret, {'c': 1, 'd': 2, 'e': 3})
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

