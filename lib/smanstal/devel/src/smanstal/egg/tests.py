# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from unittest import TestCase, TestSuite, makeSuite, TextTestRunner
import doctest
import os, os.path as op, re, sys
import posixpath as pp

from smanstal.egg.resources import resource_isdir, resource_walk
from smanstal.egg.module import (absmodpath, modpathmod, pathmod, hasinit)
from smanstal.egg.introspect import ispackage
from smanstal.types import (isfunction, iscallable, isclass, isobjclass, isiterable)
from smanstal.util.py import iff
from smanstal.tests import BaseUnitTest

from functools import wraps

__all__ = ('testmodules', 'testsuites', 'alltestnames', 'alltestobjects', 'addtest', 'BaseUnitTest',
        'run_suite')

_REType = type(re.compile(''))
_DefaultModNameRegex = re.compile(r'[Tt]est')
_DefaultDocTestRegex = re.compile(r'[Dd]oc[Tt]est')

# =================================================
# Helpers
# =================================================
def pkg_dirname(por, obj): #{{{
    if not ispackage(por, obj):
        return obj
    topdir, ind = '', 0
    ppath = absmodpath(por, obj).split('.')
    if isinstance(por, basestring):
        ind = 1
    topdir = pp.join(*ppath[ind:])
    return topdir
# End def #}}}
# =================================================
# testmodules
# =================================================
def testmodules(package_or_requirement, suite, regex=None): #{{{
    por = package_or_requirement
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(por, suite) or (isinstance(suite, basestring) and resource_isdir(por, suite)):
        return _tm_gen(por, suite, regex)
    raise TypeError('Cannot walk through sub modules of %s object' %suite.__class__.__name__)
# End def #}}}

def _tm_gen(por, suite, regex): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    topdir = pkg_dirname(por, suite)
    for dir, subdir, files in resource_walk(por, topdir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.py' and regex.match(name):
                yield absmodpath(por, pp.join(topdir, f))
        break
# End def #}}}
# =================================================
# testsuites
# =================================================
def testsuites(package_or_requirement, suite, regex=None): #{{{
    por = package_or_requirement
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(por, suite) or (isinstance(suite, basestring) and resource_isdir(por, suite)):
        return _ts_gen(por, suite, regex)
    raise TypeError('Cannot walk through sub packages of %s object' %suite.__class__.__name__)
# End def #}}}

def _ts_gen(por, suite, regex): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    topdir = pkg_dirname(por, suite)
    for dir, subdir, files in resource_walk(por, topdir):
        for d in subdir:
            path = pp.join(topdir, d)
            if hasinit(por, path) and regex.match(d):
                yield absmodpath(por, path)
        break
# End def #}}}
# =================================================
# alltestnames
# =================================================
def alltestnames(package_or_requirement, suite, regex=None): #{{{
    por = package_or_requirement
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(por, suite) or (isinstance(suite, basestring) and resource_isdir(por, suite)):
        return _atn_gen(por, suite, regex)
    raise TypeError('Cannot walk through sub packages/modules of %s object' %suite.__class__.__name__)
# End def #}}}

def _atn_gen(por, suite, regex): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    topdir = pkg_dirname(por, suite)
    for dir, subdir, files in resource_walk(por, topdir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.py' and regex.match(name):
                yield absmodpath(por, pp.join(topdir, f))
        for d in subdir:
            path = pp.join(topdir, d)
            if hasinit(por, path) and regex.match(d):
                yield absmodpath(por, path)
        break
# End def #}}}
# =================================================
# alltestobjects
# =================================================
def alltestobjects(package_or_requirement, suite, regex=None): #{{{
    por = package_or_requirement
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(por, suite) or (isinstance(suite, basestring) and resource_isdir(suite)):
        return _ato_gen(por, suite, regex)
    raise TypeError("%s object is not a package" %suite.__class__.__name__)
# End def #}}}

def _ato_gen(por, suite, regex): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    for modname in alltestnames(por, suite, regex):
        mod = modpathmod(por, modname)
        sfunc = getattr(mod, 'suite', None)
        if not sfunc or not iscallable(sfunc):
            raise ValueError("Test module '%s' is missing a suite callable" %modname)
        yield sfunc
# End def #}}}

# =================================================
# addtest
# =================================================
def addtest(suite=None): #{{{
    if not suite or isinstance(suite, TestSuite) or (isobjclass(suite) and issubclass(suite, TestCase)):
        return _addtest_testcase(suite)
    elif isfunction(suite):
        return addtest()(suite)
    elif isinstance(suite, tuple):
        por, suite = suite
        return _addtest_str(por, suite)
    raise TypeError('Cannot create test suite from %s object' %suite.__class__.__name__)
# End def #}}}

def _addtest_testcase(testcase): #{{{
    def deco(func): #{{{
        @wraps(func)
        def wrapper(): #{{{
            test = TestSuite()
            if testcase:
                tc = testcase
                if not isinstance(tc, TestSuite):
                    tc = makeSuite(tc)
                test.addTest(tc)
            ret = func()
            if isinstance(ret, TestCase) and ret not in test:
                test.addTest(ret)
                ret = None
            elif isinstance(ret, type) and issubclass(ret, TestCase):
                ret = makeSuite(ret)

            if isinstance(ret, TestSuite) and True not in (t in test for t in ret):
                test.addTest(ret)
            elif ret:
                raise TypeError("Cannot add %s object to test suite" %ret.__class__.__name__)
            return test
        # End def #}}}
        return wrapper
    # End def #}}}
    return deco
# End def #}}}

def _addtest_str(por, suite): #{{{
    def deco(func): #{{{
        @wraps(func)
        def wrapper(): #{{{
            test = TestSuite()
            selfmod = pathmod(por, suite)
            test.addTests(sfunc() for sfunc in alltestobjects(por, selfmod))
            ret = func()
            if isinstance(ret, TestCase) and ret not in test:
                test.addTest(ret)
                ret = None
            elif isinstance(ret, type) and issubclass(ret, TestCase):
                ret = makeSuite(ret)

            if isinstance(ret, TestSuite) and True not in (t in test for t in ret):
                test.addTest(ret)
            elif ret:
                raise TypeError("Cannot add %s object to test suite" %ret.__class__.__name__)
            return test
        # End def #}}}
        return wrapper
    # End def #}}}
    return deco
# End def #}}}

# =================================================
# mksuite
# =================================================
def mksuite(package_or_requirement, magicfile, ignore=None): #{{{
    por = package_or_requirement
    def suite(): #{{{
        curmod = pathmod(por, magicfile)
        test = TestSuite()
        count = 0
        for attr in dir(curmod):
            a = getattr(curmod, attr)
            if isobjclass(a) and issubclass(a, TestCase):
                if ignore:
                    if (isiterable(ignore) and a in ignore) or a is ignore:
                        continue
                test.addTest(makeSuite(a))
                count += 1
            elif isinstance(a, TestSuite):
                if ignore:
                    if (isiterable(ignore) and a in ignore) or a is ignore:
                        continue
                test.addTest(a)
                count += 1
        if count:
            return test
    # End def #}}}
    return suite
# End def #}}}


# =================================================
# allrstfiles
# =================================================
def allrstfiles(package_or_requirement, dir): #{{{
    por = package_or_requirement
    if not resource_isdir(por, dir):
        raise OSError("No such directory: %s" %dir)
    for root, dirs, files in resource_walk(por, dir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.rst':
                yield f
        return
# End def #}}}
# =================================================
# mkdocsuite
# =================================================
def mkdocsuite(package_or_requirement, dir, recurse=True): #{{{
    por = package_or_requirement
    def suite(): #{{{
        test = TestSuite()
        for f in allrstfiles(por, dir):
            test.addTest(doctest.DocFileSuite(pp.join(dir, f), module_relative=False))
        if recurse:
            for curdir, subdir, files in resource_walk(por, dir):
                for d in subdir:
                    adir = pp.join(curdir, d)
                    for f in allrstfiles(por, adir):
                        test.addTest(doctest.DocFileSuite(pp.join(adir, f), module_relative=False))
        return test
    # End def #}}}
    return suite
# End def #}}}

@addtest(('smanstal_tests', __file__))
def suite(): #{{{
    pass
# End def #}}}

def run_suite(module, verbosity=2): #{{{
    TextTestRunner(verbosity=verbosity).run(module.suite())
# End def #}}}

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite())
