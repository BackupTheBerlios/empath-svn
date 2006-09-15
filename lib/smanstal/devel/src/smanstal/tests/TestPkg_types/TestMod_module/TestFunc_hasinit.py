# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.module import hasinit
import os.path as op

class Test_hasinit(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonDirectory(self): #{{{
        '''Passing in non-directory fails'''
        msg = re.compile(r"'.*' is not a directory path string")
        self.assertRaisesEx(TypeError, hasinit, op.abspath(__file__), exc_pattern=msg)
    # End def #}}}

    def testNonString(self): #{{{
        '''Non-string argument fails'''
        msg = re.compile(r"'.*' is not a directory path string")
        self.assertRaisesEx(TypeError, hasinit, 1, exc_pattern=msg)
    # End def #}}}

    def testNonPackage(self): #{{{
        '''Passing in a non-python package directory return False'''
        a = op.abspath(__file__)
        d = op.dirname(a)
        dir = op.join(d, op.basename(a).split('.')[0])
        self.assertFalse(hasinit(dir))
    # End def #}}}

    def testPackage(self): #{{{
        '''Passing in a package directory return True'''
        a = op.abspath(__file__)
        dir = op.dirname(a)
        self.assertTrue(hasinit(dir))
    # End def #}}}
# End class #}}}

suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
