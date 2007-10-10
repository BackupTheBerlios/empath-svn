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

from pyssi.core import Signal

def base_before(l): #{{{
    l.append('BASE_BEFORE')
# End def #}}}

def base_signal(l): #{{{
    l.append('BASE_SIGNAL')
    return l
# End def #}}}

def base_after(l): #{{{
    l.append('BASE_AFTER')
# End def #}}}

def base(l): #{{{
    base_before(l)
    ret = base_signal(l)
    base_after(l)
    return ret
# End def #}}}

def signal_signal(l): #{{{
    l.append('SIGNAL')
    return l
# End def #}}}

def signal_before(l): #{{{
    l.append('BEFORE')
# End def #}}}

def signal_after(ret, l): #{{{
    l.append('AFTER')
# End def #}}}

signal = Signal(signal_signal)
signal.connect('before', dict(before=[signal_before]))
signal.connect('after', dict(after=[signal_after]))

class TestGeneralProfile(BaseUnitTest): #{{{
    def stub(self, sig, *args): #{{{
        for i in xrange(1000):
            sig(*args)
    # End def #}}}

    def profile_dispatch(self, pfname, pdname, prname, sig): #{{{
        res = []
        prof = hotshot.Profile(pfname)
        prof.runcall(self.stub, sig, res)
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
        pd('data/base.prof', 'data/base_results.txt', 'data/base_dump.prof', base)
        pd('data/signal.prof', 'data/signal_results.txt', 'data/signal_dump.prof', signal)
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

