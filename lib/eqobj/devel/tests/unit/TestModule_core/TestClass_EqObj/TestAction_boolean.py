# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj, OrObj, AndObj, BooleanOperation

class Max10(EqObj): #{{{
    def __compare__(self, obj): #{{{
        return obj <= 10
    # End def #}}}
# End class #}}}

class Max20(EqObj): #{{{
    def __compare__(self, obj): #{{{
        return obj <= 20
    # End def #}}}
# End class #}}}

class Test_boolean(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.max10 = Max10()
        self.max20 = Max20()
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_or_return(self): #{{{
        '''Bitwise or returns an OrObj BooleanOperation object'''
        ret = self.max10 | self.max20
        self.assertTrue(isinstance(ret, BooleanOperation))
        self.assertTrue(isinstance(ret, OrObj))
    # End def #}}}

    def test_and_return(self): #{{{
        '''Bitwise and returns an AndObj BooleanOperation object'''
        ret = self.max10 & self.max20
        self.assertTrue(isinstance(ret, BooleanOperation))
        self.assertTrue(isinstance(ret, AndObj))
    # End def #}}}

    def test_bool_orop(self): #{{{
        '''OR operation works as expected'''
        obj = self.max10 | self.max20
        for i in xrange(21):
            self.assertTrue(obj(i))
        self.assertFalse(obj(21))
    # End def #}}}

    def test_bool_andop(self): #{{{
        '''AND operation works as expected'''
        obj = self.max10 & self.max20
        for i in xrange(11):
            self.assertTrue(obj(i))
        for i in xrange(11, 21):
            self.assertFalse(obj(i))
    # End def #}}}

    def test_use_boolfunc(self): #{{{
        '''Should be able to use a callable that returns a boolean when given a single value'''
        other = lambda o: o == 10
        obj = other & self.max20
        for i in xrange(10):
            self.assertFalse(obj(i))
        self.assertTrue(obj(10))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

