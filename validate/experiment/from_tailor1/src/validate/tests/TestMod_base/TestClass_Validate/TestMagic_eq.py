# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from validate.base import Validate

class TestEq(unittest.TestCase): #{{{
    def setUp(self): #{{{
        class v(Validate): pass
        self.v = v
    # End def #}}}

    def tearDown(self): #{{{
        del self.v
    # End def #}}}

    def testValues(self): #{{{
        '''Simple value tester'''
        def test_values(v, res, *vobj, **kw): #{{{
            if not vobj:
                vobj = (100,)
            vobj = self.v(*vobj, **kw)
            e = vobj.__eq__(v)
            self.assert_(isinstance(e, bool))
            self.assertEqual(e, res)
        # End def #}}}
        input = [(1, False), ('abc', False), (100, True),
                    (14, True, self.v(14)), ('hello', True, 'h' + 'ello')]
        for i in input:
            test_values(*i)
        input = [('hello', False, 'h' + 'ello')]
        for i in input:
            test_values(*i, **dict(exact=True))
    # End def #}}}
# End class #}}}

