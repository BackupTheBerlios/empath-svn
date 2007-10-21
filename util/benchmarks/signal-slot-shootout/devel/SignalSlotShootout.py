# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the signal-slot-shootout project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import with_statement
import os, os.path as op
from copy import deepcopy
import unittest, re
#from smanstal.tests import BaseUnitTest, addtest, mksuite
import hotshot, hotshot.stats as hsstats, pstats

from pyssi.core import Signal, signal as decosig
import dispatch
import louie

from aossi.core import BaseSignal
from aossi.signals import Signal as AossiSignal
from aossi.decorators import signal as aossi_signal

def base_before(l): #{{{
    l.append('BASE_BEFORE')
# End def #}}}

def base_signal(l): #{{{
    l.append('BASE_SIGNAL')
    return l
# End def #}}}

# pyssi after slots gets the return value of the signal
def base_after(l, *args): #{{{
    l.append('BASE_AFTER')
# End def #}}}

def run_base(l): #{{{
    base_before(l)
    ret = base_signal(l)
    base_after(l)
    return ret
# End def #}}}

#class TestGeneralProfile(BaseUnitTest):
class SignalSlotShootout(unittest.TestCase): #{{{

    def initBeforeAfter(self): #{{{
        run_signal = Signal(base_signal)
        run_signal.connect_before(dict(before=[base_before]))
        run_signal.connect_after(dict(after=[base_after]))

        run_deco = decosig(overload=False)(base_signal)
        run_deco.before(base_before)
        run_deco.after(base_after)

        run_rule = dispatch.generic()(lambda l: l)
        run_rule.when('True')(base_signal)
        run_rule.before('True')(base_before)
        run_rule.after('True')(base_after)

        louie.connect(base_before, 'before_after', base_signal)
        louie.connect(base_signal, 'before_after', base_signal)
        louie.connect(base_after, 'before_after', base_signal)

        def run_louie(l): #{{{
            ret = louie.send('before_after', base_signal, l)
            return ret[1][1]
        # End def #}}}

        run_aossi_basesignal = BaseSignal(base_signal)
        run_aossi_basesignal.connect(before=[base_before])
        run_aossi_basesignal.connect(after=[base_after])

        run_aossi_signal = AossiSignal(base_signal)
        run_aossi_signal.connect(before=[base_before])
        run_aossi_signal.connect(after=[base_after])

        run_aossi_deco = aossi_signal()(base_signal)
        run_aossi_deco.before(base_before)
        run_aossi_deco.after(base_after)

        ba = {'base': run_base,
              'signal': run_signal,
              'deco': run_deco,
              'rule': run_rule,
              'louie': run_louie,
              'aossi_basesignal': run_aossi_basesignal,
              'aossi_signal': run_aossi_signal,
              'aossi_deco': run_aossi_deco}
        dpath = op.join('data', 'before_after')
        if not op.exists(dpath):
            os.makedirs(dpath, 0700)
        return ba
    # End def #}}}

    def killBeforeAfter(self): #{{{
        louie.disconnect(base_before, 'before_after', base_signal)
        louie.disconnect(base_signal, 'before_after', base_signal)
        louie.disconnect(base_after, 'before_after', base_signal)
    # End def #}}}

    def setUp(self): #{{{
        self.tests = {'before_after': self.initBeforeAfter()}
    # End def #}}}

    def tearDown(self): #{{{
        self.killBeforeAfter()
        del self.tests
    # End def #}}}

    def stub(self, sig): #{{{
        for i in xrange(1000):
            sig([])
    # End def #}}}

    def profile_dispatch(self, pfname, pdname, prname, sig): #{{{
        res = []
        prof = hotshot.Profile(pfname)
        prof.runcall(self.stub, sig)
        prof.close()
        stats = hsstats.load(pfname)

        with file(pdname, 'wb') as f:
            stats.dump_stats(prname)
            stats = pstats.Stats(prname, stream=f)

            stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            stats.print_stats()
    # End def #}}}

    def testBeforeAfter(self): #{{{
        pd = self.profile_dispatch
        ba_tests = self.tests['before_after']
        for name, sig in ba_tests.iteritems():
            strdict = dict(name=name)
            pd('data/before_after/%(name)s.prof' %strdict, 
               'data/before_after/%(name)s_results.txt' %strdict, 
               'data/before_after/%(name)s_dump.prof' %strdict, sig)
    # End def #}}}
# End class #}}}

# Create suite function for this module
#suite = addtest(mksuite(__file__))
def suite(): #{{{
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(SignalSlotShootout))
    return s
# End def #}}}

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

