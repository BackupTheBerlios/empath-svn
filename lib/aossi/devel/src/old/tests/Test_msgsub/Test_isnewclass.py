# Module: aossi.tests.Test_msgsub.Test_isnewclass
# File: Test_isnewclass.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.msgsub import isnewclass

class Testisnewclass(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testPassNewClass(self): #{{{
        '''New style classes succeeds'''
        class A(object): pass
        self.assert_(isnewclass(A))
    # End def #}}}

    def testFailOldClass(self): #{{{
        '''Old style classes fails'''
        class A: pass
        self.assert_(not isnewclass(A))
    # End def #}}}

    def testFailNewClassInstance(self): #{{{
        '''New style class instances fails'''
        class A(object): pass
        self.assert_(not isnewclass(A()))
    # End def #}}}
# End class #}}}

