# Module: anyall.tests.TestPkg_anyall.TestMod_callobj.TestFunc_evalobj.TestAction_call
# File: TestAction_call.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the anyall project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.callobj import *

class Test_evalobj_call(BaseUnitTest): #{{{
    def testCall(self): #{{{
        '''Call evalobj'''
        a = evalobj('q(1)()')
        self.assertEqual(a(), 1)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

