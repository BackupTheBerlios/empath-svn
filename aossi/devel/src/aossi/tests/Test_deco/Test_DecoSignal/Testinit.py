# Module: aossi.tests.Test_deco.Test_DecoSignal.Testinit
# File: Testinit.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.deco import *

class Test__init__(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testInitializeVariables(self): #{{{
        '''Internal variables initialized'''
        @signal
        def testme():
            return 1
        s = testme.signal
        self.assert_(isinstance(getattr(s, '_settings', None), dict))
        self.assert_(isinstance(getattr(s, '_global_settings', None), dict))
        self.assert_(not s._settings)
        self.assert_(not s._global_settings)
    # End def #}}}
# End class #}}}

