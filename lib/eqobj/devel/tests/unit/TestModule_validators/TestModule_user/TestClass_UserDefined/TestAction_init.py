# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.validators.user import UserDefined

class Test_init(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_callable_check(self): #{{{
        '''Can be initialized only with callables'''
        class A(object): pass
        c = [isinstance, lambda x: x, A]
        for t in c:
            a = UserDefined(t)
        for t in [1, 'a', 1.5]:
            try:
                a = UserDefined(t)
            except TypeError, err:
                self.assertEqual(str(err).strip(), "UserDefined objects can only accept callable objects")
            else:
                self.assertTrue(True)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

