# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.cwrapper import CallableWrapper

class Test_unwrap(BaseUnitTest): #{{{
    def setUp(self): #{{{
        def deco(f): #{{{
            def w(s, a1, a2): #{{{
                if not isinstance(a1, basestring):
                    return False
                return f(a1, a2)
            # End def #}}}
            return w
        # End def #}}}
        self.deco = deco
        self.func = isinstance
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testUnwrap(self): #{{{
        '''Unwrapping returns to default call state'''
        cw = CallableWrapper(self.func)
        cw.wrap(self.deco)
        cw.unwrap()
        self.assertEqual(cw._newcall, cw.call)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

