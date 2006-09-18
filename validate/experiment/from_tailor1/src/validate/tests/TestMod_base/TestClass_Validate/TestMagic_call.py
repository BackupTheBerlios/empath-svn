# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.base import Validate

class TestCall(unittest.TestCase): #{{{
    def setUp(self): #{{{
        class v(Validate): pass
        self.v = v
    # End def #}}}

    def tearDown(self): #{{{
        del self.v
    # End def #}}}

    def testReturnsNewInstance(self): #{{{
        '''Calling a Validate instance returns a new Validate instance'''
        orig = self.v()
        new = orig()
        self.assert_(isinstance(new, Validate))
        self.assertEqual(new.__class__, orig.__class__)
        self.assert_(new is not orig)
    # End def #}}}
# End class #}}}

