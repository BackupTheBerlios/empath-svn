# Module: smanstal.tests.TestPkg_types.TestMod_callobj.TestFunc_callobj.TestAction_init
# File: TestAction_init.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.callobj import callobj

class Test_callobj(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoInit(self): #{{{
        '''Must subclass to initialize'''
        msg = re.compile("callobj is an abstract class")
        self.assertRaisesEx(NotImplementedError, callobj, exc_pattern=msg)
    # End def #}}}

    def testSubClass(self): #{{{
        '''A subclass can init just fine'''
        class Test(callobj): #{{{
            def __init__(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        a = Test()
    # End def #}}}

    def testNoCall(self): #{{{
        '''Subclass must override __call__'''
        class Test(callobj): #{{{
            __name__ = 'Test'
            def __init__(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        a = Test()
        msg = re.compile("Please override the __call__ method")
        self.assertRaisesEx(NotImplementedError, a, exc_pattern=msg)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

