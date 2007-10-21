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

from aossi.decorators import signal

class TestGeneralProfile(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def stub(self, sig, res, f): #{{{
        for i in xrange(1000):
#            f(i)
            sig(res, f)
    # End def #}}}

    @signal()
    def sig(self, l, f): #{{{
        f('SIG%i' %len(l))
    # End def #}}}

    @sig.before
    def before(self, l, f): #{{{
        f('before')
    # End def #}}}

    def testDefault(self): #{{{
        '''Simple profile'''
        res = []
        prof = hotshot.Profile('data/general.prof')
        prof.runcall(self.stub, self.sig, res, res.append)
        prof.close()
        stats = hsstats.load('data/general.prof')

        with file('data/results.txt', 'wb') as f:
            stats.dump_stats('data/general2.prof')
            stats = pstats.Stats('data/general2.prof', stream=f)

            stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            stats.print_stats()
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

