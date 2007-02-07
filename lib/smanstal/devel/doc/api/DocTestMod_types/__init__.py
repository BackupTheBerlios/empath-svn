# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest
import os, os.path as op, doctest
from smanstal.tests import addtest, mkdocsuite

# Create doc suite function for this directory
suite = addtest(mkdocsuite(op.dirname(op.abspath(__file__)), recurse=True))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
