# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the doctestdir project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
import os, os.path as op
import sys

# nose package imports
from nose.core import TestProgram
from nose.config import Config, all_config_files
from nose.plugins.base import Plugin
from nose.plugins.manager import DefaultPluginManager
from nose.plugins.doctests import Doctest

def _add_ext_dot(el): #{{{
    if not el.startswith('.'):
        el = ''.join(['.', el])
    return el
# End def #}}}
# =================================================
# hasinit
# =================================================
def hasinit(dir, source_first=True): #{{{
    source_first = (lambda seq: seq) if source_first else reversed
    if isinstance(dir, basestring) and op.isdir(dir):
        path1 = op.join(dir, '__init__.py')
        path2, path3 = path1 + 'c', path1 + 'o'
        for p in source_first((path1, path2, path3)):
            if op.isfile(p):
                return op.basename(p)
        return ''
#        return True in (op.isfile(p) for p in (path1, path2, path3))
    raise TypeError("'%s' is not a directory path string" %str(dir))
# End def #}}}

class DoctestDir(Doctest): #{{{
    """
    Activate doctestdir plugin to find and run doctests in non-package directories.
    """
    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)
        parser.add_option('--doctestdir-tests', action='store_true',
                          dest='doctest_tests',
                          default=env.get('NOSE_DOCTEST_TESTS'),
                          help="Also look for doctests in test modules. "
                          "Note that classes, methods and functions should "
                          "have either doctests or non-doctest tests, "
                          "not both. [NOSE_DOCTEST_TESTS]")
        parser.add_option('--doctestdir-extension', action="append",
                          dest="doctestExtension",
                          help="Also look for doctests in files with "
                          "this extension [NOSE_DOCTEST_EXTENSION]")
        parser.add_option('--doctestdir-recurse', action="store_true",
                          default=False,
                          dest="doctestdir_recurse",
                          help="Recurse through any directories found")
        # Set the default as a list, if given in env; otherwise
        # an additional value set on the command line will cause
        # an error.
        env_setting = env.get('NOSE_DOCTEST_EXTENSION')
        if env_setting is not None:
            parser.set_defaults(doctestExtension=tolist(env_setting))

    def configure(self, options, config):
        super(DoctestDir, self).configure(options, config)
        self.extension = [_add_ext_dot(el) for el in self.extension]
        abspath = op.abspath
        where = options.where
        if where == None:
            where = [os.getcwd()]
        self.where = set(abspath(p) for p in where)
        self.doctestdir_recurse = options.doctestdir_recurse

    def loadTestsFromDir(self, path): #{{{
        recurse = self.doctestdir_recurse
        loadfile = self.loadTestsFromFile
        pjoin = op.join
        where = self.where
        if not hasinit(path):
            for curdir, subdir, files in os.walk(path):
                if curdir not in where:
                    for f in files:
                        i = loadfile(pjoin(curdir, f))
                        if i != None:
                            for res in i:
                                if res:
                                    yield res
                if not recurse:
                    break
    # End def #}}}

# End class #}}}

class NosePluginManager(DefaultPluginManager): #{{{
    def loadPlugins(self): #{{{
        super(NosePluginManager, self).loadPlugins()
        self.addPlugin(DoctestDir())
    # End def #}}}
# End class #}}}

def run_nose(): #{{{
    argv = list(sys.argv)
    execpath = op.realpath(argv[0])
    testdir = op.abspath(op.dirname(execpath))
    if len(argv) == 1:
        argv.extend(['doc', 'unit'])
    os.chdir(testdir)
    env = os.environ
    cfg_files = all_config_files()
    config = Config(env=env, files=cfg_files, plugins=NosePluginManager())
    TestProgram(argv=argv, env=env, config=config)
# End def #}}}

if __name__ == '__main__':
    run_nose()
