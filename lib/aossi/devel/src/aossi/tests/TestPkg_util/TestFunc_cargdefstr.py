# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import cargdefstr

class Test_cargdefstr(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable returns None'''
        self.assertTrue(cargdefstr(1) is None)
    # End def #}}}

    def testReturn(self): #{{{
        '''Return a 2-tuple of str for arg definition and arg call'''
        def _(a, b, c=1, d=2, e=3, *args, **kwargs): #{{{
            pass
        # End def #}}}
        ret = cargdefstr(_)
        self.assertTrue(isinstance(ret, tuple))
        self.assertEqual(len(ret), 2)
        expected = ('a, b, c=1, d=2, e=3, *args, **kwargs',
                'a, b, c, d, e, *args, **kwargs')
        self.assertEqual(ret, expected)
    # End def #}}}

    def testNoArgs(self): #{{{
        '''No arguments returns 2-tuple of empty strings'''
        def _(): #{{{
            pass
        # End def #}}}
        self.assertEqual(cargdefstr(_), ('', ''))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

