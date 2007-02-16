# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import methodname
from types import MethodType as method

class Test_methodname(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonInstClass(self): #{{{
        '''Non-method instance/class objects returns None'''
        nonmeth = lambda s: None
        unbound = method(nonmeth, None, None)
        for nm in (nonmeth, unbound):
            self.assertTrue(methodname(nm) is None)
    # End def #}}}

    def testInstClass(self): #{{{
        '''Retrieve method name from instance or class'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        for meth in (_.me, _().me):
            ret = methodname(meth)
            self.assertEqual(ret, 'me')
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

