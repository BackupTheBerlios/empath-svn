# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.core import BaseSignal
from aossi.signals import AroundExtension

class AroundSignal(AroundExtension, BaseSignal): #{{{
    __slots__ = ()
# End class #}}}

class Test_wrap(BaseUnitTest): #{{{
    def setUp(self): #{{{
        def sig(l): #{{{
            l.append('signal')
            return l
        # End def #}}}

        def wrap(func): #{{{
            def ar(self, l): #{{{
                l.append('around: before')
                func(l)
                l.append('around: after')
                return l
            # End def #}}}
            return ar
        # End def #}}}
        self.signal = signal = AroundSignal(sig, weak=False)
        signal.connect(around=[wrap])
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSimpleWrap(self): #{{{
        '''Around callable works as expected'''
        l = []
        ret = self.signal(l)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(ret is l)
        self.assertEqual(ret, ['around: before', 'signal', 'around: after'])
    # End def #}}}

    def testConnectedFunctions(self): #{{{
        '''Functions are correctly connected'''
        signal = self.signal
        slot = signal.slot
        self.assertEqual(len(list(slot('around'))), 1)
        self.assertTrue(signal.connected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

