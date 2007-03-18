# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.introspect import isstaticmethod

class Test_isstaticmethod(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class Test(object): #{{{
            def test(self): pass
            @classmethod
            def class_(cls): pass
            @staticmethod
            def static(): pass
            a=1
        # End class #}}}
        self.testcls = Test
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testMethod(self): #{{{
        '''Only class method returns True'''
        Test = self.testcls
        for m in ('test', 'class_', 'a'):
            self.assertFalse(isstaticmethod(Test, m))
        self.assertTrue(isstaticmethod(Test, 'static'))
    # End def #}}}

    def testNonClassObject(self): #{{{
        '''Non-class 'cls' argument raises error'''
        regex = re.compile('int object is not a class')
        self.assertRaisesEx(TypeError, isstaticmethod, 1, 'a', exc_pattern=regex)
    # End def #}}}

    def testNonStringObject(self): #{{{
        '''Non-string 'attr' argument raises error'''
        regex = re.compile(r'getattr[(][)][:] attribute name must be string')
        self.assertRaisesEx(TypeError, isstaticmethod, self.testcls, 1, exc_pattern=regex)
    # End def #}}}

    def testNonAttribute(self): #{{{
        ''''attr' attribute not a member of 'cls' raises error'''
        Test = self.testcls
        regex = re.compile('type object \'%s\' has no attribute \'who\'' %Test.__name__)
        self.assertRaisesEx(AttributeError, isstaticmethod, Test, 'who', exc_pattern=regex)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

