# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite
from smanstal.types.module import parent

class Test_parent(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonModule(self): #{{{
        '''Non-module raises error'''
        msg = re.compile('Cannot import parent module of int object')
        self.assertRaisesEx(TypeError, parent, 1, exc_pattern=msg)
    # End def #}}}

    def testRootPackage(self): #{{{
        '''Root package returns itself'''
        self.assertTrue(parent(unittest) is unittest)
    # End def #}}}

    def testDynamicModule(self): #{{{
        '''Dynamic module returns itself'''
        import new
        m = new.module('booby')
        self.assertTrue(parent(m) is m)
    # End def #}}}

    def testPackage(self): #{{{
        '''Package returns parent'''
        import xml.sax as xs
        import xml
        self.assertTrue(parent(xs) is xml)
    # End def #}}}

    def testModule(self): #{{{
        '''Module returns parent'''
        import xml.sax as xs
        import xml
        self.assertTrue(parent(xs) is xml)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

