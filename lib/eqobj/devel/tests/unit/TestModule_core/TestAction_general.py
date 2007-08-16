# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from eqobj.core import EqObj

class TestGeneral(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def test_eqobj_eqerror(self): #{{{
        '''Using EqObj objects should always raise an error on any comparison'''
        def boolcast(): #{{{
            a = bool(EqObj())
        # End def #}}}
        def callobj(): #{{{
            t = EqObj()
            a = t()
        # End def #}}}
        def eqcmp(): #{{{
            t = EqObj()
            a = t.__eq__(1)
        # End def #}}}
        for f in (boolcast, callobj, eqcmp):
            check = False
            try:
                f()
            except NotImplementedError:
                check = True
            self.assertTrue(check)
    # End def #}}}

    #def test_experiment(self): #{{{
        #'''Experiment'''

        #class AlwaysTrue(EqObj): #{{{
            #pass
        ## End class #}}}
        #CTrue = AlwaysTrue()

        #a = bool(AlwaysTrue(1))
        #b = CTrue(1)
        #c = (CTrue == 1)
        #self.assertTrue(False not in (a, b, c))
    ## End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

