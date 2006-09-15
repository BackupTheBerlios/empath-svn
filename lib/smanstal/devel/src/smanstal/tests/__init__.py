# Module: smanstal.tests
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


from unittest import TestCase, TestSuite, makeSuite, TextTestRunner
import os, os.path as op, re, sys

from aossi.deco import signal, signal_settings
from smanstal.types import (absmodpath, modpathmod, pathmod, hasinit, 
        ispackage, isfunction, iscallable, isclass)
from validate.base import valTrue
from validate.value import vv_or
from validate.type import vt

__all__ = ('testmodules', 'testsuites', 'alltestnames', 'alltestobjects', 'addtest', 'BaseUnitTest')

_REType = type(re.compile(''))
_DefaultModNameRegex = re.compile(r'[Tt]est')

# =================================================
# testmodules
# =================================================
@signal_settings(globals=globals(), policy='first')
def testmodules(suite, regex=None): #{{{
    raise TypeError('Cannot walk through sub modules of %s object' %suite.__class__.__name__)
# End def #}}}

@testmodules.match_value(valTrue, None)
def _tm_noregex(suite, regex): #{{{
    return testmodules(suite, _DefaultModNameRegex)
# End def #}}}

@testmodules.when('ispackage(suite)')
@signal
def _tm_pkg(suite, regex): #{{{
    raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
# End def #}}}

@_tm_pkg.match_type(valTrue, _REType)
def _tm_regex(suite, regex): #{{{
    topdir = op.dirname(suite.__file__)
    for dir, subdir, files in os.walk(topdir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.py' and regex.match(name):
                yield absmodpath(op.join(topdir, f))
        break
# End def #}}}
# =================================================
# testsuites
# =================================================
@signal_settings(globals=globals(), policy='first')
def testsuites(suite, regex=None): #{{{
    raise TypeError('Cannot walk through sub packages of %s object' %suite.__class__.__name__)
# End def #}}}

@testsuites.match_value(valTrue, None)
def _ts_noregex(suite, regex): #{{{
    return testsuites(suite, _DefaultModNameRegex)
# End def #}}}

@testsuites.when('ispackage(suite)')
@signal
def _ts_pkg(suite, regex): #{{{
    raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
# End def #}}}

@_ts_pkg.match_type(valTrue, _REType)
def _ts_regex(suite, regex): #{{{
    topdir = op.dirname(suite.__file__)
    for dir, subdir, files in os.walk(topdir):
        for d in subdir:
            if hasinit(op.join(topdir, d)) and regex.match(d):
                yield absmodpath(op.join(topdir, d))
        break
# End def #}}}

# =================================================
# alltestnames
# =================================================
@signal_settings(globals=globals(), policy='first')
def alltestnames(suite, regex=None): #{{{
    raise TypeError('Cannot walk through sub packages/modules of %s object' %suite.__class__.__name__)
# End def #}}}

@alltestnames.match_value(valTrue, None)
def _atn_noregex(suite, regex): #{{{
    return alltestnames(suite, _DefaultModNameRegex)
# End def #}}}

@alltestnames.when('ispackage(suite)')
@signal
def _atn_pkg(suite, regex): #{{{
    raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
# End def #}}}

@_atn_pkg.match_type(valTrue, _REType)
def _atn_regex(suite, regex): #{{{
    topdir = op.dirname(suite.__file__)
    for dir, subdir, files in os.walk(topdir):
        for f in files:
            name, ext = op.splitext(f)
            if ext == '.py' and regex.match(name):
                yield absmodpath(op.join(topdir, f))
        for d in subdir:
            if hasinit(op.join(topdir, d)) and regex.match(d):
                yield absmodpath(op.join(topdir, d))
        break
# End def #}}}

# =================================================
# alltestobjects
# =================================================
@signal_settings(globals=globals(), policy='first')
def alltestobjects(suite, regex=None): #{{{
    raise TypeError("%s object is not a package" %suite.__class__.__name__)
# End def #}}}

@alltestobjects.match_value(valTrue, None)
def _ato_noregex(suite, regex): #{{{
    return alltestobjects(suite, _DefaultModNameRegex)
# End def #}}}

@alltestobjects.when('ispackage(suite)')
@signal
def _ato_pkg(suite, regex): #{{{
    raise TypeError("%s object is not a compiled regular expression" %regex.__class__.__name__)
# End def #}}}

@_ato_pkg.match_type(valTrue, _REType)
def _ato_regex(suite, regex): #{{{
    for modname in alltestnames(suite, regex):
        mod = modpathmod(modname)
        sfunc = getattr(mod, 'suite', None)
        if not sfunc or not iscallable(sfunc):
            raise ValueError("Test module '%s' is missing a suite callable" %modname)
        yield sfunc
# End def #}}}

# =================================================
# addtest
# =================================================
@signal_settings(globals=globals(), policy='first')
def addtest(suite=None): #{{{
    raise TypeError('Cannot create test suite from %s object' %suite.__class__.__name__)
# End def #}}}

@addtest.when('not testcase or isinstance(testcase, TestSuite) or (testcase == vt(type) and issubclass(testcase, TestCase))')
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

@addtest.when('isfunction(func)')
def _addtest_func(func): #{{{
    return addtest()(func)
# End def #}}}

@addtest.match_type(basestring)
def _addtest_str(suite): #{{{
    def deco(func): #{{{
        def wrapper(): #{{{
            test = TestSuite()
            selfmod = pathmod(suite)
            test.addTests(sfunc() for sfunc in alltestobjects(selfmod))
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
def mksuite(magicfile): #{{{
    def suite(): #{{{
        curmod = pathmod(magicfile)
        test = TestSuite()
        count = 0
        for attr in dir(curmod):
            a = getattr(curmod, attr)
            if isclass(a) and issubclass(a, TestCase):
                test.addTest(makeSuite(a))
                count += 1
            elif isinstance(a, TestSuite):
                test.addTest(a)
                count += 1
        if count:
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
