################################################################################
# extras.tests -- Description goes here
# Copyright (c) 2006 Ariel De Ocampo
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
################################################################################


import unittest
import dispatch
import os, os.path as op
from smanstal.types.module import AbsoluteModuleName, ModuleObjectFromModuleName, ModuleObjectFromModulePath
from smanstal.types.introspect import isdirmodule, isfunction

__all__ = ('TestModules', 'TestSuites', 'AllTestNames', 'AllTestObjects', 'AddTest')

@dispatch.generic()
def TestModules(suite):
   """Base generic function of 'TestModules()'"""

@TestModules.when('isdirmodule(suite)')
def TestModules(suite):
   topdir = op.dirname(suite.__file__)
   for dir, subdir, files in os.walk(topdir):
      for f in files:
         if f.startswith('Test_') and f.endswith('py'):
            name, ext = op.splitext(f)
            yield name
      break

@dispatch.generic()
def TestSuites(suite):
   """Base generic function of 'TestSuites()'"""

@TestSuites.when('isdirmodule(suite)')
def TestSuites(suite):
   topdir = op.dirname(suite.__file__)
   for dir, subdir, files in os.walk(topdir):
      for d in subdir:
         if d.startswith('Test_'):
            yield d
      break

@dispatch.generic()
def AllTestNames(suite):
   """Base generic function of 'AllTestNames()'"""

@AllTestNames.when('isdirmodule(suite)')
def AllTestNames(suite):
   assert isdirmodule(suite)
   topdir = op.dirname(suite.__file__)
   for dir, subdir, files in os.walk(topdir):
      for f in files:
         if f.startswith('Test_') and f.endswith('py'):
            name, ext = op.splitext(f)
            yield name
      for d in subdir:
         if d.startswith('Test_'):
            yield d
      break

@dispatch.generic()
def AllTestObjects(suite):
   """Base generic function of 'AllTestObjects()'"""

@AllTestObjects.when('isdirmodule(suite)')
def AllTestObjects(suite):
   abssuitename = AbsoluteModuleName(suite)
   for modname in AllTestNames(suite):
      absmodpath = "%s.%s" %(abssuitename, modname)
      mod = ModuleObjectFromModuleName(absmodpath)
      if not hasattr(mod, 'suite') or not isfunction(mod.suite):
         raise ValueError, "Test module '%s' is missing a 'suite()' function" %absmodpath
      yield mod.suite()

@dispatch.generic()
def AddTest(x):
   """Base generic function of 'AddTest()'"""
   
@AddTest.when('isinstance(x, type) and issubclass(x, unittest.TestCase)')
def AddTest(x):
   testobj = x
   def deco(func):
      def wrapper():
         test = unittest.TestSuite()
         test.addTest(unittest.makeSuite(testobj))
         func()
         return test
      return wrapper
   return deco

@AddTest.when('isinstance(x, str)')
def AddTest(x):
   modname = x
   def deco(func):
      def wrapper():
         suite = unittest.TestSuite()
         selfmod = ModuleObjectFromModulePath(modname)
         suite.addTests(AllTestObjects(selfmod))
         func()
         return suite
      return wrapper
   return deco

@AddTest(__file__)
def suite():
   pass
