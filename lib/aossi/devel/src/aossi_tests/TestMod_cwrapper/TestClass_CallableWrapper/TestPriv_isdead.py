# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.cwrapper import CallableWrapper
from aossi.util import cref

class Test_isdead(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testReferences(self): #{{{
        '''Live reference (functions always alive)'''
        t1 = lambda: None
        class t2(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t3 = t2()
        cw = None
        for f in (t1, t2.me, t3.me):
            cw = CallableWrapper(f, weak=True)
            self.assertEqual(cw._isdead(), False)
        del t3, f
        self.assertTrue(cw._isdead())
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

