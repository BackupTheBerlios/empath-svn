# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement
import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite
import hotshot, hotshot.stats as hsstats, pstats

from aossi.core import BaseSignal
from aossi.signals import Signal, DefaultExtension, OnReturnExtension, StreamExtension, ChooseExtension, ReplaceExtension, AroundExtension 
from aossi.decorators import (signal, make_signal, DefaultDecoSignal, OnReturnDecoSignal, ReplaceDecoSignal, AroundDecoSignal, 
                StreamDecoSignal, CondDecoSignal, WhenDecoSignal, CascadeDecoSignal, 
                MatchTypeDecoSignal, MatchDecoSignal)
from aossi.deco import signal as oldsig
from dispatch import generic

#class Signal(OnReturnExtension, StreamExtension, ReplaceExtension, AroundExtension, BaseSignal): #{{{
#    __slots__ = ()
## End class #}}}

#class Signal(ChooseExtension, BaseSignal):
#    __slots__ = ()
## End class #}}}

#def signal(**kwargs): #{{{
#    sigext = [DefaultExtension]
#    decoext = [DefaultDecoSignal]
#    decoext = [OnReturnDecoSignal]
#    kwargs['sigext_'] = sigext
#    kwargs['decoext_'] = decoext
#    return make_signal(**kwargs)
## End def #}}}

class TestGeneralProfile(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.base_flist = [self.base_before]

        if not isinstance(self.basesignal_sig, BaseSignal):
            self.basesignal_sig = ss = BaseSignal(self.basesignal_sig, weak=False)
            ss.connect(before=[self.signal_before])
        if not isinstance(self.signal_sig, Signal):
            self.signal_sig = ss = Signal(self.signal_sig, weak=False)
            ss.connect(before=[self.signal_before])
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def stub(self, sig, res, f): #{{{
        for i in xrange(1000):
#            f(i)
            sig(res, f)
    # End def #}}}

    def base_before(self, l, f): #{{{
        f('aossi before')
    # End def #}}}

    def base_sig(self, l, f): #{{{
        for basefunc in self.base_flist:
            basefunc(l, f)
        f('AOSSI SIG%i' %len(l))
    # End def #}}}

    def basesignal_before(self, l, f): #{{{
        f('aossi before')
    # End def #}}}

    def basesignal_sig(self, l, f): #{{{
        f('AOSSI SIG%i' %len(l))
    # End def #}}}

    def signal_before(self, l, f): #{{{
        f('aossi before')
    # End def #}}}

    def signal_sig(self, l, f): #{{{
        f('AOSSI SIG%i' %len(l))
    # End def #}}}

    @oldsig()
    def old_sig(self, l, f): #{{{
        f('OLD SIG%i' %len(l))
    # End def #}}}

    @old_sig.before
    def old_before(self, l, f): #{{{
        f('old before')
    # End def #}}}

    @signal(weakcondf=False)
    def aossi_sig(self, l, f): #{{{
        f('AOSSI SIG%i' %len(l))
    # End def #}}}

    @aossi_sig.cond(lambda s, l, f: True)
    def aossi_before(self, l, f): #{{{
        f('aossi before')
    # End def #}}}

    @generic()
    def rd_sig(self, l, f): #{{{
        f('RD SIG%i' %len(l))
    # End def #}}}

    @rd_sig.when("True")
    def rd_before(self, l, f): #{{{
        f('rd before')
    # End def #}}}

    def profile_dispatch(self, pfname, pdname, prname, sig): #{{{
        res = []
        prof = hotshot.Profile(pfname)
        prof.runcall(self.stub, sig, res, res.append)
        prof.close()
        stats = hsstats.load(pfname)

        with file(pdname, 'wb') as f:
            stats.dump_stats(prname)
            stats = pstats.Stats(prname, stream=f)

            stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            stats.print_stats()
    # End def #}}}

    def testDispatch(self): #{{{
        pd = self.profile_dispatch
        pd('data/base.prof', 'data/base_results.txt', 'data/base_dump.prof', self.base_sig)
        pd('data/signal.prof', 'data/signal_results.txt', 'data/signal_dump.prof', self.signal_sig)
        pd('data/basesignal.prof', 'data/basesignal_results.txt', 'data/basesignal_dump.prof', self.basesignal_sig)
#        pd('data/old.prof', 'data/old_results.txt', 'data/old_dump.prof', self.old_sig)
        pd('data/aossi.prof', 'data/aossi_results.txt', 'data/aossi_dump.prof', self.aossi_sig)
#        pd('data/rd.prof', 'data/rd_results.txt', 'data/rd_dump.prof', self.rd_sig)
    # End def #}}}

#    def testDefault(self): #{{{
#        '''Simple profile'''
#        res = []
#        prof = hotshot.Profile('data/general.prof')
#        prof.runcall(self.stub, self.aososi_sig, res, res.append)
#        prof.close()
#        stats = hsstats.load('data/general.prof')

#        with file('data/results.txt', 'wb') as f:
#            stats.dump_stats('data/general2.prof')
#            stats = pstats.Stats('data/general2.prof', stream=f)

#            stats.strip_dirs()
#            stats.sort_stats('time', 'calls')
#            stats.print_stats()
#    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

