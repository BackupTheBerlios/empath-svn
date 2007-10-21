# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.cwrapper import CallableWrapper
from warnings import simplefilter, resetwarnings

class Test_call(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testDeadReference(self): #{{{
        '''Dead wrapper issued a warning'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        cw = CallableWrapper(t.me, weak=True)
        simplefilter('error', RuntimeWarning)
        del t
        self.assertTrue(cw.isdead)
        msg = re.compile(r'Calling a dead wrapper')
        self.assertRaisesEx(RuntimeWarning, cw, exc_pattern=msg)
        resetwarnings()
    # End def #}}}

    def testDeadReferenceReturn(self): #{{{
        '''If dead wrapper, return None'''
        class _(object): #{{{
            def me(self): #{{{
                pass
            # End def #}}}
        # End class #}}}
        t = _()
        cw = CallableWrapper(t.me, weak=True)
        simplefilter('ignore', RuntimeWarning)
        del t
        self.assertTrue(cw.isdead)
        self.assertTrue(cw() is None)
        resetwarnings()
    # End def #}}}

    def testWrap(self): #{{{
        '''If wrapped, will call the wrap function'''
        def deco(f): #{{{
            def w(s): #{{{
                return 400
            # End def #}}}
            return w
        # End def #}}}
        _ = lambda: 100
        cw = CallableWrapper(_)
        self.assertEqual(cw(), 100)
        cw.wrap(deco)
        self.assertEqual(cw(), 400)
        cw.unwrap()
        self.assertEqual(cw(), 100)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

