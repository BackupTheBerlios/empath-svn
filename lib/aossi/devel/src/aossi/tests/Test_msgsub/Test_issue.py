# Module: aossi.tests.Test_msgsub.Test_issue
# File: Test_issue.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.msgsub import _siglist as sldict, issue

class Testissue(unittest.TestCase): #{{{
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

    def testGetIssue(self): #{{{
        '''Retrieve correct issue'''
        self.Invalid.valid = True
        ret = issue('valid', 1, 2)
        self.assert_(isinstance(ret, self.Valid))

        ret = issue('invalid', 3, 4)
        self.assert_(isinstance(ret, self.Invalid))
    # End def #}}}
# End class #}}}

