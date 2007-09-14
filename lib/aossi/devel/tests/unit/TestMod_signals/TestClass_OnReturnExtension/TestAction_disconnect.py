# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from aossi.core import BaseSignal
from aossi.signals import OnReturnExtension

class OnReturnSignal(OnReturnExtension, BaseSignal): #{{{
    __slots__ = ()
# End class #}}}

class Test_disconnect(BaseUnitTest): #{{{
    def setUp(self): #{{{
        def sig(l): #{{{
            l.append('signal')
            return l
        # End def #}}}

        def onret(l): #{{{
            l.append('onreturn')
            return 1
        # End def #}}}
        self.signal = signal = OnReturnSignal(sig, weak=False)
        signal.connect(onreturn=[onret])
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testDisconnectAll(self): #{{{
        '''Can disconnect everything properly'''
        signal = self.signal
        signal.disconnect()
        self.assertFalse(signal.connected)
    # End def #}}}

    def testDisconnectAllOnReturn_implicit(self): #{{{
        '''Can implicitly disconnect all onreturn functions'''
        signal = self.signal
        signal.disconnect(onreturn=[])
        self.assertFalse(signal.connected)
    # End def #}}}

    def testDisconnectAllOnReturn_explicit(self): #{{{
        '''Can explicitly disconnect all onreturn functions'''
        signal = self.signal
        signal.disconnect(onreturn=[], deleteall=True)
        self.assertFalse(signal.connected)
    # End def #}}}

    def testDisconnectFunction(self): #{{{
        '''Disconnect a specific function'''
        signal = self.signal
        func = list(signal.slot('onreturn'))[0]
        signal.disconnect(onreturn=[func])
        self.assertFalse(signal.connected)

        def onret(l): #{{{
            l.append('onreturn')
            return 1
        # End def #}}}
        signal.connect(onreturn=[onret])
        self.assertTrue(signal.connected)
        signal.disconnect(onreturn=[onret])
        self.assertFalse(signal.connected)
    # End def #}}}

    def testDisconnectMethod(self): #{{{
        '''Disconnect a specific method'''
        class Test(object):
            def test(self): pass
            def onret(self): pass
        test = Test()
        signal = OnReturnSignal(test.test)
        signal.connect(onreturn=[test.onret])
        self.assertTrue(signal.connected)
        signal.disconnect(onreturn=[test.onret])
        self.assertFalse(signal.connected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

