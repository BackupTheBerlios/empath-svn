# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj

class Test_callable(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class AlwaysTrue(EqObj): #{{{
            def __compare__(self, obj): #{{{
                return True
            # End def #}}}
        # End class #}}}
        self.t = AlwaysTrue()
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_workflow(self): #{{{
        '''Test expected usage of EqObj callables'''
        t = self.t
        for val in (1, 1.5, True, False, "a", None, "", [], {}, (), [1]):
            self.assertTrue(t(val))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

