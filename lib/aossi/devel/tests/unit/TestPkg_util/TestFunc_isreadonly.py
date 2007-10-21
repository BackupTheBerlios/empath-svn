# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import isreadonly

class Test_isreadonly(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNormalObject(self): #{{{
        '''Normal objects are read-write'''
        class _(object): pass
        self.assertFalse(isreadonly(_, 'test', 42))
        self.assertFalse(isreadonly(_(), 'test', 42))
    # End def #}}}

    def testReadOnly(self): #{{{
        '''Read-only objects'''
        class _(object): #{{{
            __slots__ = ()
        # End class #}}}
        self.assertTrue(isreadonly(_(), 'test', 42))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

