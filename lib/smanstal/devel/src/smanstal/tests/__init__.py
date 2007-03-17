# Module: smanstal.tests
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


from unittest import TestCase, TestSuite, makeSuite, TextTestRunner
import doctest
import os, os.path as op, re, sys

from smanstal.types import (absmodpath, modpathmod, pathmod, hasinit, 
        ispackage, isfunction, iscallable, isclass, isobjclass, isiterable,
        fromfile, isfindable)
from smanstal.util.py import iff

__all__ = ('testmodules', 'testsuites', 'alltestnames', 'alltestobjects', 'addtest', 'BaseUnitTest')

_REType = type(re.compile(''))
_DefaultModNameRegex = re.compile(r'[Tt]est')
_DefaultDocTestRegex = re.compile(r'[Dd]oc[Tt]est')

# =================================================
# testmodules
# =================================================
def testmodules(suite, regex=None, filenames=False): #{{{
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(suite) or (isinstance(suite, basestring) and op.isdir(suite)):
        return _tm_gen(suite, regex, filenames)
    raise TypeError('Cannot walk through sub modules of %s object' %suite.__class__.__name__)
# End def #}}}

def _tm_gen(suite, regex, filenames): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    topdir = suite
    if ispackage(suite):
        topdir = op.dirname(suite.__file__)
    for dir, subdir, files in os.walk(topdir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.py' and regex.match(name):
                path = op.join(topdir, f)
                yield (path if filenames else absmodpath(path))
        break
# End def #}}}
# =================================================
# testsuites
# =================================================
def testsuites(suite, regex=None, filenames=False): #{{{
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(suite) or (isinstance(suite, basestring) and op.isdir(suite)):
        return _ts_gen(suite, regex, filenames)
    raise TypeError('Cannot walk through sub packages of %s object' %suite.__class__.__name__)
# End def #}}}

def _ts_gen(suite, regex, filenames): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    topdir = suite
    if ispackage(suite):
        topdir = op.dirname(suite.__file__)
    for dir, subdir, files in os.walk(topdir):
        for d in subdir:
            path = op.join(topdir, d)
            if hasinit(path) and regex.match(d):
                yield (path if filenames else absmodpath(path))
        break
# End def #}}}
# =================================================
# alltestnames
# =================================================
def alltestnames(suite, regex=None, filenames=False): #{{{
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(suite) or (isinstance(suite, basestring) and op.isdir(suite)):
        return _atn_gen(suite, regex, filenames)
    raise TypeError('Cannot walk through sub packages/modules of %s object' %suite.__class__.__name__)
# End def #}}}

def _atn_gen(suite, regex, filenames): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    topdir = suite
    if ispackage(suite):
        topdir = op.dirname(suite.__file__)
    for dir, subdir, files in os.walk(topdir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.py' and regex.match(name):
                path = op.join(topdir, f)
                yield path if filenames else absmodpath(path)
        for d in subdir:
            path = op.join(topdir, d)
            if hasinit(path) and regex.match(d):
                yield path if filenames else absmodpath(path)
        break
# End def #}}}
# =================================================
# alltestobjects
# =================================================
def alltestobjects(suite, regex=None, filenames=False): #{{{
    if not regex:
        regex = _DefaultModNameRegex
    if ispackage(suite) or (isinstance(suite, basestring) and op.isdir(suite)):
        return _ato_gen(suite, regex, filenames)
    raise TypeError("%s object is not a package" %suite.__class__.__name__)
# End def #}}}

def _ato_gen(suite, regex, filenames): #{{{
    if not isinstance(regex, _REType):
        raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
    for modname in alltestnames(suite, regex, filenames):
        if filenames:
            mod = fromfile(modname)
        else:
            mod = modpathmod(modname)
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
    elif isinstance(suite, basestring):
        return _addtest_str(suite)
    raise TypeError('Cannot create test suite from %s object' %suite.__class__.__name__)
# End def #}}}

def _addtest_testcase(testcase): #{{{
    def deco(func): #{{{
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
        wrapper.__name__ = func.__name__
        wrapper.__dict__ = func.__dict__
        wrapper.__doc__ = func.__doc__
        return wrapper
    # End def #}}}
    return deco
# End def #}}}

def _addtest_str(suite): #{{{
    suite = op.abspath(suite)
    def deco(func): #{{{
        def wrapper(): #{{{
            test = TestSuite()
            insys = isfindable(suite)
            selfmod = pathmod(suite) if insys else fromfile(suite)
            test.addTests(sfunc() for sfunc in alltestobjects(selfmod, filenames=(not insys)))
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
        wrapper.__name__ = func.__name__
        wrapper.__dict__ = func.__dict__
        wrapper.__doc__ = func.__doc__
        return wrapper
    # End def #}}}
    return deco
# End def #}}}

# =================================================
# BaseUnitTest
# =================================================
class BaseUnitTest(TestCase): #{{{
    def assertRaisesEx(self, exception, callable, *args, **kwargs):
        exc_args = kwargs.pop('exc_args', None)
        exc_pattern = kwargs.pop('exc_pattern', None)

        argv = [repr(a) for a in args]\
               + ["%s=%r" % (k,v)  for k,v in kwargs.items()]
        callsig = "%s(%s)" % (callable.__name__, ", ".join(argv))

        try:
            callable(*args, **kwargs)
        except exception, exc:
            if exc_args is not None:
                self.failIf(exc.args != exc_args,
                            "%s raised %s with unexpected args: "\
                            "expected=%r, actual=%r"\
                            % (callsig, exc.__class__, exc_args, exc.args))
            if exc_pattern is not None:
                self.failUnless(exc_pattern.search(str(exc)),
                                "%s raised %s, but the exception "\
                                "does not match '%s': %r"\
                                % (callsig, exc.__class__, exc_pattern.pattern,
                                   str(exc)))
        except:
            exc_info = sys.exc_info()
            print exc_info
            self.fail("%s raised an unexpected exception type: "\
                      "expected=%s, actual=%s"\
                      % (callsig, exception, exc_info[0]))
        else:
            self.fail("%s did not raise %s" % (callsig, exception))
# End class #}}}

# =================================================
# mksuite
# =================================================
def mksuite(magicfile, ignore=None): #{{{
    def suite(): #{{{
        mf = op.abspath(magicfile)
        curmod = pathmod(mf) if isfindable(mf) else fromfile(mf)
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
def allrstfiles(dir): #{{{
    if not op.isdir(dir):
        raise OSError("No such directory: %s" %dir)
    for root, dirs, files in os.walk(dir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.rst':
                yield f
        return
# End def #}}}
# =================================================
# mkdocsuite
# =================================================
def mkdocsuite(dir, recurse=True): #{{{
    def suite(): #{{{
        test = TestSuite()
        for f in allrstfiles(dir):
            test.addTest(doctest.DocFileSuite(op.join(dir, f), module_relative=False))
        if recurse:
            for curdir, subdir, files in os.walk(dir):
                for d in subdir:
                    adir = op.abspath(op.join(curdir, d))
                    for f in allrstfiles(adir):
                        test.addTest(doctest.DocFileSuite(op.join(adir, f), module_relative=False))
        return test
    # End def #}}}
    return suite
# End def #}}}

@addtest(__file__)
def suite(): #{{{
    pass
# End def #}}}

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite())
