################################################################################
# extras.tests.Test_tests.Test___all__ -- Description goes here
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
from extras.types.module import ParentModule
from extras.tests import AddTest
##import extras.tests.Test_tests as parentmod

parentmod = ParentModule(__file__)

class Test__all__(parentmod.Test_tests):
# =========================================================================

# =========================================================================
   # --------------------------------------------------------
   # Start testIsIterable Method
   # --------------------------------------------------------
   def testIsIterable(self):
      """tests.__all__ - Is an iterable"""
      try:
         for i in self.tests.__all__:
            break
      except:
         self.assert_(False)
      self.assert_(True)
   # --------------------------------------------------------
   # End testIsIterable Method
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start testHasFiveElements Method
   # --------------------------------------------------------
   def testHasFiveElements(self):
      """tests.__all__ - Contains only five elements"""
      count = 0
      for i in self.tests.__all__:
         count += 1
      self.assertEquals(count, 5)
   # --------------------------------------------------------
   # End testHasFiveElements Method
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start testContainsOnlyStringElements Method
   # --------------------------------------------------------
   def testContainsOnlyStringElements(self):
      """tests.__all__ - All elements are strings"""
      for i in self.tests.__all__:
         self.assert_(isinstance(i, str))
   # --------------------------------------------------------
   # End testContainsOnlyStringElements Method
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start testContainsOnlyKnownStrings Method
   # --------------------------------------------------------
   def testContainsOnlyKnownStrings(self):
      """tests.__all__ - Contains only known strings"""
      known = ('TestModules', 'TestSuites', 'AllTestNames', 'AllTestObjects', 'AddTest')
      for i in self.tests.__all__:
         self.assert_(i in known)
   # --------------------------------------------------------
   # End testContainsOnlyKnownStrings Method
   # --------------------------------------------------------
# =========================================================================

# =========================================================================
@AddTest(Test__all__)
def suite():
   pass
