################################################################################
# extras.tests.Test_tests.Test_TestModules -- Description goes here
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
# Module: capabilities.tests.Test_roleregistry.Test_PluginAttributes.Test___init__

# =========================================================================

# =========================================================================
from smanstal.types.module import ParentModule
from smanstal.tests import AddTest
import dispatch as d

parentmod = ParentModule(__file__)
##import extras.tests.Test_tests as parentmod

class TestTestModules(parentmod.Test_tests):
# =========================================================================

# =========================================================================
   # --------------------------------------------------------
   # Start testNonModuleArg Method
   # --------------------------------------------------------
   def testNonModuleArg(self):
      """tests.TestModules - Non-module will generate a NoApplicableMethods error"""
      try:
         self.tests.TestModules(1)
      except d.NoApplicableMethods:
         self.assert_(True)
      except:
         self.assert_(False)
   # --------------------------------------------------------
   # End testNonModuleArg Method
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start testFileModuleArg Method
   # --------------------------------------------------------
   def testFileModuleArg(self):
      """tests.TestModules - File-module will generate a NoApplicableMethods error"""
      mod = __import__('smanstal.tests.Test_tests.Test___all__')
      try:
         self.tests.TestModules(mod)
      except d.NoApplicableMethods:
         self.assert_(True)
      except:
         self.assert_(False)
   # --------------------------------------------------------
   # End testFileModuleArg Method
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start testReturnsStrings Method
   # --------------------------------------------------------
   def testReturnsStrings(self):
      """tests.TestModules - Passing in a directory module will yield strings that start with 'Test_'"""
      mod = __import__('smanstal.tests.Test_tests')
      for i in self.tests.TestModules(mod):
         self.assert_(isinstance(i, str))
         self.assert_(i.startswith('Test_'))
   # --------------------------------------------------------
   # End testReturnsStrings Method
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start testReturnsExistingFileModules Method
   # --------------------------------------------------------
   def testReturnsExistingFileModules(self):
      """tests.TestModules - Passing in a directory module will yield all child file test modules"""
      mod = __import__('smanstal.tests.Test_tests')
      import os, os.path as op
      abspath = op.abspath(mod.__file__)
      dirpath = op.dirname(abspath)
      for i in self.tests.TestModules(mod):
         fullpyf = op.join(*(dirname, "%s.py" %i))
         self.assert_(op.isfile(fullpyf))
   # --------------------------------------------------------
   # End testReturnsExistingFileModules Method
   # --------------------------------------------------------
# =========================================================================

# =========================================================================
@AddTest(TestTestModules)
def suite():
   pass
