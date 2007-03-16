# Module: smanstal.tests
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.egg.tests import addtest as add_egg_test
from smanstal.tests import addtest, mksuite
from unittest import TextTestRunner
from pkg_resources import resource_filename, Requirement, cleanup_resources
import sys, os.path as op, os

req = Requirement.parse('smanstal')
from smanstal_tests.unit import egg

@add_egg_test((req, egg.__file__))
def suite(): #{{{
    cur = op.dirname(__file__)
    fs = resource_filename(req, 'smanstal_tests/unit/filesystem')
    dname = op.dirname(fs)
    os.chdir(dname)
    imp = ''
    if not fs.startswith(cur) and not op.isdir('fstests'):
        imp = 'fstests'
        os.rename('filesystem', imp) 
    sys.path = [dname] + sys.path
    if imp:
        fs = __import__(imp, level=0)
    else:
        import smanstal_tests.unit.filesystem as fs
    print fs.__file__

    @addtest(fs.__file__)
    def all_suite(): #{{{
        pass
    # End def #}}}

    return all_suite()
# End def #}}}

def run_suite(): #{{{
    TextTestRunner(verbosity=2).run(suite())
    cleanup_resources()
# End def #}}}

if __name__ == '__main__':
    run_suite()
