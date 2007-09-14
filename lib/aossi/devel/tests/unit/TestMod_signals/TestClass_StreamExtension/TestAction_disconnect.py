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

class Test_disconnect(BaseUnitTest): #{{{
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

    def testDisconnectAll(self): #{{{
        '''Can disconnect everything properly'''
        signal = self.signal
        signal.disconnect()
        self.assertFalse(signal.connected)
        self.assertFalse(True in (bool(l) for l in signal._funclist.itervalues()))
    # End def #}}}

    def testDisconnectAllStream_implicit(self): #{{{
        '''Can implicitly disconnect all stream functions'''
        signal = self.signal
        slot = signal.slot
        signal.disconnect(after=[])
        signal.disconnect(stream=[], streamin=[])
        self.assertFalse(signal.connected)
        self.assertFalse([f for f in slot('stream')])
        self.assertFalse([f for f in slot('streamin')])
        self.assertFalse([f for f in slot('after')])
    # End def #}}}

    def testDisconnectAllStream_explicit(self): #{{{
        '''Can explicitly disconnect all stream functions'''
        signal = self.signal
        slot = signal.slot
        signal.disconnect(stream=[], streamin=[], deleteall=True)
        self.assertTrue(signal.connected)
        self.assertFalse([f for f in slot('stream')])
        self.assertFalse([f for f in slot('streamin')])
        self.assertTrue([f for f in slot('after')])
    # End def #}}}

    def testDisconnectFunction(self): #{{{
        '''Disconnect a specific function'''
        signal = self.signal
        slot = signal.slot
        func = slot('stream').next()
        signal.disconnect(stream=[func])
        self.assertFalse([f for f in slot('stream')])
        self.assertTrue(signal.connected)

        def stream(l): #{{{
            l.append('stream')
            return 1
        # End def #}}}
        signal.connect(stream=[stream])
        self.assertTrue([f for f in slot('stream')])
        signal.disconnect(stream=[stream])
        self.assertFalse([f for f in slot('stream')])
    # End def #}}}

    def testDisconnectMethod(self): #{{{
        '''Disconnect a specific method'''
        class Test(object):
            def test(self): pass
            def stream(self): pass
        test = Test()
        signal = StreamSignal(test.test)
        signal.connect(stream=[test.stream])
        self.assertTrue(signal.connected)
        signal.disconnect(stream=[test.stream])
        self.assertFalse(signal.connected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

