# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.util.script import cmd, InvalidDestinationError
from smanstal.types.module import rootpackage, absmodpath, pkgdir

import os.path as op, os
datadir = op.join(pkgdir(__file__), 'unit', 'data', 'util', 'shell', 'cmd')

class Test_callcommand(BaseUnitTest): #{{{
    def setUp(self): #{{{
        pass
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testSingleCall(self): #{{{
        '''Test absolute path to executable'''
        c = cmd('/bin/ls', datadir)
        res = ' '.join(c(buffer=False)).replace('\n', '')
        self.assertEqual(set(res.split(' ')), set(['a', 'ariel', 'b', 'c']))
    # End def #}}}

    def testEnv(self): #{{{
        '''Test finding binary within executable path'''
        c = cmd('ls', datadir)
        res = ' '.join(c(buffer=False)).replace('\n', '')
        self.assertEqual(set(res.split(' ')), set(['a', 'ariel', 'b', 'c']))
    # End def #}}}

    def testPipeTwoCommands(self): #{{{
        '''Create pipe between two commands'''
        p = cmd('ls', datadir) | cmd('grep', 'a')
        res = set(n for n in p().replace('\n', ' ').split(' ') if n)
        self.assertEqual(res, set(['a', 'ariel']))
    # End def #}}}

    def testPipeThreeCommands(self): #{{{
        '''Create pipes between three commands'''
        p = cmd('ls', datadir) | cmd('grep', 'ariel') | cmd('sed', '-e', 's/a/O/g')
        res = p().replace('\n', '')
        self.assertEqual(res, 'Oriel')
    # End def #}}}

    def testPipeFourCommands(self): #{{{
        '''Create pipes between four commands'''
        p = cmd('ls', datadir) | cmd('grep', 'a') | cmd('grep', 'ariel') | cmd('sed', '-e', 's/a/O/g')
        res = p().replace('\n', '')
        self.assertEqual(res, 'Oriel')
    # End def #}}}

    def testPipePipes(self): #{{{
        '''Is bad to try and pipe pipes'''
        p1 = cmd('ls', datadir) | cmd('grep', 'a')
        p2 = cmd('ls', datadir) | cmd('grep', 'ariel') | cmd('sed', '-e', 's/a/O/g')
        msg = re.compile('Cannot send data to an already established command pipe')
        self.assertRaisesEx(InvalidDestinationError, p1.__or__, p2, exc_pattern=msg)
    # End def #}}}

    def testPipeTwoNamedCommands(self): #{{{
        '''Create pipe between two named commands'''
        ls, grep = cmd.name('ls'), cmd.name('grep')
        p = ls(datadir) | grep('a')
        res = set(n for n in p().replace('\n', ' ').split(' ') if n)
        self.assertEqual(res, set(['a', 'ariel']))
    # End def #}}}

    def testPipeThreeNamedCommands(self): #{{{
        '''Create pipes between three named commands'''
        ls, grep, sed = cmd.name('ls'), cmd.name('grep'), cmd.name('sed')
        p = ls(datadir) | grep('ariel') | sed('-e', 's/a/O/g')
        res = p().replace('\n', '')
        self.assertEqual(res, 'Oriel')
    # End def #}}}

    def testPipeFourNamedCommands(self): #{{{
        '''Create pipes between four named commands'''
        ls, grep, sed = cmd.name('ls'), cmd.name('grep'), cmd.name('sed')
        p = ls(datadir) | grep('a') | grep('ariel') | sed('-e', 's/a/O/g')
        res = p().replace('\n', '')
        self.assertEqual(res, 'Oriel')
    # End def #}}}

# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

