# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj, Invert

class Test_not(BaseUnitTest): #{{{
    def setUp(self): #{{{
        class LessThanTen(EqObj): #{{{
            def __compare__(self, obj): #{{{
                if not isinstance(obj, int):
                    return False
                return (obj < 10)
            # End def #}}}
        # End class #}}}
        self.lt = LessThanTen()
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testLTClass(self): #{{{
        '''Test LessThanTen class from setUp()'''
        lt = self.lt
        a, f = self.assertTrue, self.assertFalse
        for i in xrange(10):
            a(lt(i))
        for i in xrange(10, 20):
            f(lt(i))
    # End def #}}}

    def test_init(self): #{{{
        '''Invert should only allow objects that have a __eq__ method'''
        for val in (1, 1.5, self.lt):
            try:
                a = Invert
            except TypeError, err:
                msg = "Invert only supports objects that have a __eq__ method"
                self.assertEquals(str(err).strip(), msg)
            else:
                self.assertTrue(True)
    # End def #}}}

    def test_invert(self): #{{{
        '''Test invert'''
        lt = Invert(self.lt)
        a, f = self.assertTrue, self.assertFalse
        for i in xrange(10):
            f(lt(i))
        for i in xrange(10, 20):
            a(lt(i))
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

