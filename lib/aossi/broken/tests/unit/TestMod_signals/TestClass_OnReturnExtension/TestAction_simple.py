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

class Test_simple(BaseUnitTest): #{{{
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

    def testFunctionality(self): #{{{
        '''onreturn callable works as expected'''
        l = []
        ret = self.signal(l)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(ret is l)
        self.assertEqual(ret, ['signal', 'onreturn'])
    # End def #}}}

    def testConnectedFunctions(self): #{{{
        '''Functions are correctly connected'''
        signal = self.signal
        self.assertEqual(len(list(signal.slot('onreturn'))), 1)
        self.assertTrue(signal.connected)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

