# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj

class Test_boolcast(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class MyTrue(EqObj): #{{{
            def __compare__(self, s, obj): #{{{
                return 1
            # End def #}}}
        # End class #}}}

        class MyFalse(EqObj): #{{{
            def __compare__(self, s, obj): #{{{
                return 0
            # End def #}}}
        # End class #}}}

        self.t = MyTrue
        self.f = MyFalse

    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_nonzero_method(self): #{{{
        '''Nonzero method return'''
        t = self.t()
        f = self.f()
        self.assertEquals(t.__nonzero__(), 1)
        self.assertEquals(f.__nonzero__(), 0)
    # End def #}}}

    def test_workflow(self): #{{{
        '''Test expected usage of boolean casting'''
        class AlwaysTrue(EqObj): #{{{
            def __compare__(self, s, obj): #{{{
                return True
            # End def #}}}
        # End class #}}}

        for val in (1, 1.5, True, False, "a", None, "", [], {}, (), [1]):
            self.assertTrue(AlwaysTrue(val))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

