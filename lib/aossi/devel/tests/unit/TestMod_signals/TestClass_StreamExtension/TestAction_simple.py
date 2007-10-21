# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.core import BaseSignal
from aossi.signals import StreamExtension

class StreamSignal(StreamExtension, BaseSignal): #{{{
    __slots__ = ()
# End class #}}}

class Test_simple(BaseUnitTest): #{{{
    def setUp(self): #{{{
        def sig(l): #{{{
            l.append('signal')
            return l
        # End def #}}}

        def after(l): #{{{
            l.append('after')
        # End def #}}}

        def streamin(args, kwargs): #{{{
            args[0].append('streamin')
        # End def #}}}

        def stream(ret): #{{{
            ret.append('stream')
            return ret
        # End def #}}}
        self.signal = signal = StreamSignal(sig, weak=False)
        signal.connect(stream=[stream], streamin=[streamin], after=[after])
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testStreamFunctionality(self): #{{{
        '''stream and streamin callables works as expected'''
        l = []
        ret = self.signal(l)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(ret is l)
        self.assertEqual(ret, ['signal', 'streamin', 'stream', 'after'])
    # End def #}}}

    def testConnectedFunctions(self): #{{{
        '''Functions are correctly connected'''
        signal = self.signal
        slot = signal.slot
        self.assertEqual(len(list(slot('stream'))), 1)
        self.assertEqual(len(list(slot('streamin'))), 1)
        self.assertTrue(signal.connected)
        signal.disconnect(stream=list(slot('stream'))[:1])
        self.assertTrue(signal.connected)
        self.assertEqual(len(list(slot('stream'))), 0)
        self.assertEqual(len(list(slot('streamin'))), 1)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

