# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj
from eqobj.collections.sequences import *

class CheckObjectType(EqObj): #{{{
    def __transform__(self, obj): #{{{
        def check(t):
            return isinstance(obj, t)
        return check
    # End def #}}}

    def __compare__(self, obj): #{{{
        return obj(self._initobj)
    # End def #}}}
# End class #}}}

class Test_general(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.cstr = CheckObjectType(basestring)
        self.cint = CheckObjectType(int)
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_eqobj_list(self): #{{{
        '''Simple isinstance eqobj'''
        a = [self.cstr, self.cint]
        b = CheckObjectType(list) & AllElements(a)
        self.assertEquals(b, ['a', 1])
        self.assertNotEquals(b, [1, 'a'])
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

