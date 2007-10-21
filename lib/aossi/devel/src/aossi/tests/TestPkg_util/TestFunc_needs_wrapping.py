# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.util import needs_wrapping

class Test_needs_wrapping(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonCallable(self): #{{{
        '''Non-callable is not a wrapped object'''
        self.assertFalse(needs_wrapping(1))
    # End def #}}}

    def testMethodFunc(self): #{{{
        '''Functions and methods are not wrapped'''
        def _(): #{{{
            pass
        # End def #}}}
        for o in (_, self.setUp):
            self.assertFalse(needs_wrapping(o))
    # End def #}}}

    def testCallableObjects(self): #{{{
        '''Objects with a __call__ method are not wrapped'''
        class _(object): #{{{
            def __call__(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        self.assertFalse(needs_wrapping(_()))
    # End def #}}}

    def testClass(self): #{{{
        '''Classes are callable objects too'''
        class _(object): #{{{
            pass
        # End class #}}}
        self.assertTrue(needs_wrapping(_))
    # End def #}}}

    def testNeedsWrapping(self): #{{{
        '''Any other object needs wrapping'''
        self.assertTrue(needs_wrapping(isinstance))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

