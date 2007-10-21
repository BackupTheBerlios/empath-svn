# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

class UnitTestTemplate(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def ga_time(self): #{{{
        pass
    # End def #}}}

    def testDefault(self): #{{{
        '''Simple profile'''
        res = []
        prof = hotshot.Profile('data/experiment.prof')
        prof.runcall(self.stub, self.sig, res, res.append)
        prof.close()
        stats = hsstats.load('data/experiment.prof')

        with file('data/results-experiment.txt', 'wb') as f:
            stats.dump_stats('data/experiment2.prof')
            stats = pstats.Stats('data/experiment2.prof', stream=f)

            stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            stats.print_stats()
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

