# Module: smanstal.tests.TestPkg_types.TestMod_mdict.TestClass_mdict
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
from smanstal.tests import addtest, mksuite

# Create suite function for this package
suite = addtest(__file__)(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

