# Module: aossi.tests.Test_msgsub.Test__cleanlist
# File: Test__cleanlist.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.msgsub import _siglist as sldict, _cleanlist as clfunc

class Test_cleanlist(unittest.TestCase): #{{{
    def setUp(self): #{{{
        class Valid(object):
            valid = True
        class Invalid(object):
            valid = False
        self.Valid = Valid
        self.Invalid = Invalid

        adv = {2: Valid()}
        mdv = {1: adv}
        sldict['valid'] = mdv

        adiv = {4: Invalid()}
        mdiv = {3: adiv}
        sldict['invalid'] = mdiv
    # End def #}}}

    def tearDown(self): #{{{
        sldict.clear()
        self.Valid = None
        self.Invalid = None
    # End def #}}}

    def testGet(self): #{{{
        '''Retrieving signals works properly'''
        self.Invalid.valid = True
        expected = ['valid', 'invalid']
        count = 0
        for index, msg, allargs, arg, signal in clfunc():
            count += 1
            self.assert_(index in expected)
            if index == 'valid':
                self.assertEqual(msg, 1)
                self.assertEqual(arg, 2)
                self.assert_(isinstance(signal, self.Valid))
            else:
                self.assertEqual(msg, 3)
                self.assertEqual(arg, 4)
                self.assert_(isinstance(signal, self.Invalid))
        self.assertEqual(count, 2)
        self.assertEqual(len(sldict), 2)
    # End def #}}}

    def testGetValidOnly(self): #{{{
        '''Retrieve only valid signals and remove invalid signals'''
        count = 0
        self.assertEqual(len(sldict), 2)
        for index, msg, allargs, arg, signal in clfunc():
            count += 1
            self.assertEqual(index, 'valid')
            self.assertEqual(msg, 1)
            self.assertEqual(arg, 2)
            self.assert_(isinstance(signal, self.Valid))
        self.assertEqual(count, 1)
        self.assertEqual(len(sldict), 1)
        self.assert_(sldict.keys()[0] == 'valid')
    # End def #}}}

    def testAllInvalid(self): #{{{
        '''Calling function on completely invalid signals clears everything'''
        self.Valid.valid = False
        count = 0
        self.assertEqual(len(sldict), 2)
        for index, msg, allargs, arg, signal in clfunc():
            count += 1
        self.assertEqual(count, 0)
        self.assertEqual(len(sldict), 0)
    # End def #}}}

    def testInvalidateValid(self): #{{{
        '''Setting found signal to None removes it'''
        count = 0
        self.assertEqual(len(sldict), 2)
        for index, msg, allargs, arg, signal in clfunc():
            count += 1
            allargs[arg] = None
        self.assertEqual(count, 1)
        self.assertEqual(len(sldict), 0)
    # End def #}}}
# End class #}}}

