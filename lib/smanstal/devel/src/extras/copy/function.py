################################################################################
# extras.function -- Description goes here
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
from types import FunctionType as function, MethodType as method
import dispatch

__all__ = ('copyfunction', 'copymethod')

@dispatch.generic()
def copyfunction(func, name = None):
   """Base generic function for 'copyfunction()'"""
   
@copyfunction.when('not isinstance(func, function) and not isinstance(func, method)')
def copyfunction(func, name = None):
   raise TypeError, "The 'func' argument must be a python function or method."
   
@copyfunction.when('name is not None and not isinstance(name, str)')
def copyfunction(func, name = None):
   raise TypeError, "The 'name' argument must be either a string or None."
   
@copyfunction.when('name is None or (isinstance(name, str) and name == "")')
def copyfunction(func, name = None):
   return copyfunction(func, func.func_name)
   
@copyfunction.when('isinstance(name, str) and name != ""')
def copyfunction(func, name = None):
   tempfunc = function(func.func_code, func.func_globals, name, func.func_defaults, func.func_closure)
   tempfunc.func_doc = None
   return tempfunc
   
@dispatch.generic()
def copymethod(meth, name = None):
   """Base generic function for 'copymethod()'"""
   
@copymethod.when('not isinstance(meth, method)')   
def copymethod(meth, name = None):
   raise TypeError, "The 'meth' argument must be a python method object."

@copymethod.when('name is not None and not isinstance(name, str)')   
def copymethod(meth, name = None):
   raise TypeError, "The 'name' argument must be a string or None."

@copymethod.when('name is None or (isinstance(name, str) and name == "")')   
def copymethod(meth, name = None):
   copymethod(meth, meth.func_name)

@copymethod.when('isinstance(name, str)')
def copymethod(meth, name = None):
   tempmeth = copyfunction(meth, name)
   return method(tempmeth, None)
