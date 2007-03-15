# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.egg.tests import BaseUnitTest, addtest, mksuite
from pkg_resources import Requirement
import os.path as op

__req__ = Requirement.parse('smanstal')

temp_path = op.abspath(__file__)
if op.exists(temp_path):
    __file__ = temp_path
del temp_path

from smanstal.util.py import AutoProp
from types import MethodType as method

class Test_autoprop(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoName(self): #{{{
        '''If no name, don't create the property'''
        class Test(object): #{{{
            __metaclass__ = AutoProp
            def get_(self): #{{{
                return 42
            # End def #}}}
        # End class #}}}
        self.assertTrue(getattr(Test, 'get_', None))
        self.assertTrue(isinstance(Test.get_, method))
    # End def #}}}

    def testCreateGet(self): #{{{
        '''Create get property'''
        class Test(object): #{{{
            __metaclass__ = AutoProp
            def get_hello(self): #{{{
                return 42
            # End def #}}}
        # End class #}}}
        self.assertFalse(getattr(Test, 'get_hello', None))
        self.assertTrue(getattr(Test, 'hello', None))
        self.assertTrue(isinstance(Test.hello, property))
        t = Test()
        self.assertEqual(t.hello, 42)
        def tset(t): t.hello = 43
        def tdel(t): del t.hello
        msg = re.compile(r'can\'t set attribute')
        self.assertRaisesEx(AttributeError, tset, t, exc_pattern=msg)

        msg = re.compile(r'can\'t delete attribute')
        self.assertRaisesEx(AttributeError, tdel, t, exc_pattern=msg)
    # End def #}}}

    def testInvalidName(self): #{{{
        '''Tricky names don't get propertized'''
        class Test(object): #{{{
            __metaclass__ = AutoProp
            def getmello_hello(self): #{{{
                return 42
            # End def #}}}
        # End class #}}}
        self.assertTrue(getattr(Test, 'getmello_hello', None))
        self.assertTrue(isinstance(Test.getmello_hello, method))
    # End def #}}}

    def testStringFunc(self): #{{{
        '''String instead of expected function don't propertize'''
        class Test(object): #{{{
            __metaclass__ = AutoProp
            get_hello = 'NO PROPERTY'
            # End def #}}}
        # End class #}}}
        self.assertTrue(getattr(Test, 'get_hello', None))
        self.assertTrue(isinstance(Test.get_hello, basestring))
    # End def #}}}

    def testDocProperty(self): #{{{
        '''Doc property'''
        class Test(object): #{{{
            __metaclass__ = AutoProp
            doc_hello = 'NO PROPERTY'
            def get_hello(self): #{{{
                return 42
            # End def #}}}
        # End class #}}}
        self.assertFalse(getattr(Test, 'doc_hello', None))
        self.assertFalse(getattr(Test, 'get_hello', None))
        self.assertTrue(hasattr(Test, 'hello'))
        self.assertTrue(isinstance(Test.hello, property))
        self.assertEqual(Test().hello, 42)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

