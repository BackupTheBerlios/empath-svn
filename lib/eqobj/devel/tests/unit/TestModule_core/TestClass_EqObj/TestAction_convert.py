# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj

class Test_convert(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class make_string(EqObj): #{{{
            def __transform__(self, obj): #{{{
                return str(obj).lower()
            # End def #}}}
            def __compare__(self, s, obj): #{{{
                return self._initobj == obj
            # End def #}}}
        # End class #}}}
        self.ms = make_string
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_convert_method(self): #{{{
        '''__transform__ method gets called'''
        a = self.ms("hello")
        for val in (1, 1.5, [], {}, (), "me", None, "", (1,)):
            self.assertFalse(a(val))
        for val in ("hello", "HELLO", "hElLo"):
            self.assertTrue(a(val))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

