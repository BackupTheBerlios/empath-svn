# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite
from smanstal.types import absmodpath

import os.path as op

class Test_absmodpath(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonModule(self): #{{{
        '''Non-module argument fails'''
        msg = re.compile("Cannot determine module path of int object")
        self.assertRaisesEx(TypeError, absmodpath, 1, exc_pattern=msg)
    # End def #}}}

    def testDynamicModule(self): #{{{
        '''Dynamically creating a module object returns that objects name'''
        import new
        m = new.module('blublah')
        self.assertEqual(absmodpath(m), 'blublah')
    # End def #}}}

    def testInit(self): #{{{
        '''Passing in path to __init__.py[co]? does the right thing'''
        import smanstal.types.module as mod
        me = op.abspath(mod.__file__)
        dir = op.dirname(me)
        init = tuple(op.join(dir, '__init__.py%s' %c) for c in ('', 'c', 'o'))
        expected = 'smanstal.types'
        self.assertTrue(False not in (absmodpath(i) == expected for i in init))
    # End def #}}}

    def testNonPythonFile(self): #{{{
        '''Passing a valid but non-python file returns None'''
        f = op.abspath(__file__)
        name = op.basename(f).split('.')[0]
        d = op.dirname(f)
        path = op.join(d, name, 'file')
        self.assertTrue(not absmodpath(path))
    # End def #}}}

    def testNonPackage(self): #{{{
        '''Passing a non-package path returns None'''
        f = op.abspath(__file__)
        name = op.basename(f).split('.')[0]
        d = op.dirname(f)
        path = op.join(d, name)
        self.assertTrue(not absmodpath(path))
    # End def #}}}

    def testPythonFile(self): #{{{
        '''Passing a python file'''
        f = op.abspath(__file__)
        expected = 'smanstal.tests.TestMod_types.TestMod_module.TestFunc_absmodpath'
        self.assertEqual(absmodpath(f), expected)
    # End def #}}}

    def testPythonPackage(self): #{{{
        '''Passing a python package'''
        f = op.abspath(__file__)
        d = op.dirname(f)
        expected = 'smanstal.tests.TestMod_types.TestMod_module'
        self.assertEqual(absmodpath(d), expected)
    # End def #}}}
# End class #}}}

suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

