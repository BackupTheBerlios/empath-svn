# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from aossi.misc import cargnames, cargdefstr, cargval

class UnitTestTemplate(unittest.TestCase): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testDefault(self): #{{{
        '''Always suceeds'''
        def a(hello, me, you=1, *what, **world):
            pass
        class A(object):
            def a(self):
                pass
        temp1 = cargnames(a)
        temp2 = cargnames(A.a)
        args = '%s ::: %s' %(str(temp1), str(temp2))
        raise Exception(args)
    # End def #}}}
# End class #}}}

