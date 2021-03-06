# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj

class UnitTestTemplate(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class AlwaysTrue(EqObj): #{{{
            def __compare__(self, s, obj): #{{{
                return True
            # End def #}}}
        # End class #}}}
        self.t = AlwaysTrue()
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_workflow_left(self): #{{{
        '''Test expected usage of EqObj callables: EqObj on left side'''
        t = self.t
        for val in (1, 1.5, True, False, "a", None, "", [], {}, (), [1]):
            self.assertEquals(t, val)
    # End def #}}}

    def test_workflow_right(self): #{{{
        '''Test expected usage of EqObj callables: EqObj on right side'''
        t = self.t
        for val in (1, 1.5, True, False, "a", None, "", [], {}, (), [1]):
            self.assertEquals(val, t)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

