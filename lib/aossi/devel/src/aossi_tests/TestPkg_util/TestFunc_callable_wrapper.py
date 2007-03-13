# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.introspect import isfunction
from aossi.util import callable_wrapper

class Test_callable_wrapper(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callables raises error'''
        msg = re.compile(r'Argument is not callable')
        self.assertRaisesEx(TypeError, callable_wrapper, 1, exc_pattern=msg)
    # End def #}}}

    def testReturn(self): #{{{
        '''Returns a method'''
        class Class(object): #{{{
            def meth(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        def func(): #{{{
            pass
        # End def #}}}
        input = (Class, isinstance, Class.meth, func)
        for c in input:
            ret = callable_wrapper(c)
            self.assertTrue(isfunction(ret))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

