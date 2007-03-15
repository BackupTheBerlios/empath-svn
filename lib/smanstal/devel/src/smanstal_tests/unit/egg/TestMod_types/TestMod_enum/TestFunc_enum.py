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

from smanstal.types.enum import enum

class Test_enum(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNoEmptyEnums(self): #{{{
        '''No empty enums'''
        msg = re.compile("Empty enums are not supported")
        self.assertRaisesEx(AssertionError, enum, exc_pattern=msg)
    # End def #}}}

    def testNonStringName(self): #{{{
        '''Passing a non-string name is bad'''
        msg = re.compile("Non-string name detected: int")
        self.assertRaisesEx(TypeError, enum, [1], exc_pattern=msg)
    # End def #}}}

    def testNonInteger(self): #{{{
        '''Passing a non-integer value is bad'''
        msg = re.compile("Non-integer value detected: str")
        self.assertRaisesEx(TypeError, enum, [('red', 'red')], exc_pattern=msg)
    # End def #}}}

    def testIntLong(self): #{{{
        '''Any integer or long type is accepted for a value'''
        enum([('red',1), ('blue', 2)])
        enum([('red',1L), ('blue', 2L)])
        self.assertTrue(True)
    # End def #}}}

    def testStartValue(self): #{{{
        '''Can change default start value'''
        a = enum('abcdefg', start=10)
        self.assertEqual(set(a.values()), set(xrange(10, 17)))
    # End def #}}}

    def testManualValue(self): #{{{
        '''Explicitly setting a value will increment from there'''
        a = enum(['a', 'b', 'c', ('d', 100), 'e', 'f', 'g'])
        self.assertEquals(set(a.iteritems()), set([('a', 0), ('b', 1), ('c', 2), ('d', 100), ('e', 101), ('f', 102), ('g', 103)]))
    # End def #}}}

    def testHashable(self): #{{{
        '''Enums are hashable'''
        a = enum('abcdefg')
        self.assertTrue(hash(a))
    # End def #}}}

    def testReadOnly(self): #{{{
        '''Cannot write to enum'''
        a = enum('abcdefg')
        self.assertRaisesEx(AttributeError, setattr, a, 'a', 200)
        self.assertRaisesEx(AttributeError, setattr, a.n, 'a', 200)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__req__, __file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

