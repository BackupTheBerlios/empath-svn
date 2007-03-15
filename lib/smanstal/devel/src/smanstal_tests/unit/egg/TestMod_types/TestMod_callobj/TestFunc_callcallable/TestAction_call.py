# Module: anyall.tests.TestPkg_anyall.TestMod_callobj.TestFunc_callcallable.TestAction_call
# File: TestAction_call.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the anyall project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.egg.tests import BaseUnitTest, addtest, mksuite
from pkg_resources import Requirement
import os.path as op

__req__ = Requirement.parse('smanstal')

temp_path = op.abspath(__file__)
if op.exists(temp_path):
    __file__ = temp_path
del temp_path

from smanstal.types.callobj import q, callcallable

class Test_callcallable_call(BaseUnitTest): #{{{
    def testCall(self): #{{{
        '''Call callcallable'''
        def testme(*args, **kwargs): #{{{
            return len(args), len(kwargs)
        # End def #}}}

        a = callcallable(testme, 1, 2, q(testme), testme=q(testme), blue=1)
        self.assertEqual(a(), (3, 2))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

