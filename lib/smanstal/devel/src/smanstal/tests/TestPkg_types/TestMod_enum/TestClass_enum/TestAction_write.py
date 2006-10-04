# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.types.enum import Enum

class Test_write(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSettingEnum(self): #{{{
        '''Setting a value to an enum is illegal'''
        name = 'red'
        msg = re.compile("Attribute '%s' is read-only" %name)
        test = Enum(red=1)
        self.assertRaisesEx(AttributeError, test.__setattr__, name, 2, exc_pattern=msg)
    # End def #}}}

    def testSetNonEnumVal(self): #{{{
        '''Setting any attribute is illegal'''
        name = 'boo'
        msg = re.compile("Attribute '%s' is read-only" %name)
        test = Enum(red=1)
        self.assertRaisesEx(AttributeError, test.__setattr__, name, 2, exc_pattern=msg)
    # End def #}}}

    def testDeleteEnumVal(self): #{{{
        '''Deleting an enum value is illegal'''
        name = 'red'
        msg = re.compile("Attribute '%s' is read-only" %name)
        test = Enum(red=1)
        self.assertRaisesEx(AttributeError, test.__delattr__, name, exc_pattern=msg)
    # End def #}}}

    def testDeleteNonEnumVal(self): #{{{
        '''Deleting any attribute is illegal'''
        name = 'boo'
        msg = re.compile("Attribute '%s' is read-only" %name)
        test = Enum(red=1)
        self.assertRaisesEx(AttributeError, test.__delattr__, name, exc_pattern=msg)
    # End def #}}}

# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

