# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import cargnames

class Test_cargnames(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable object returns None'''
        self.assertTrue(cargnames(1) is None)
    # End def #}}}

    def testCallable(self): #{{{
        '''Callable returns argument names'''
        def _(a, b, c, d=1, *args, **kw): #{{{
            pass
        # End def #}}}
        ret = cargnames(_)
        expected = (['a', 'b', 'c', 'd'], 'args', 'kw')
        self.assertTrue(ret)
        self.assertEqual(ret, expected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

