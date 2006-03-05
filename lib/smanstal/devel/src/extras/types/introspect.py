################################################################################
# extras.types.introspect -- Description goes here
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
from protocols import Interface, declareAdapter, NO_ADAPTER_NEEDED

from types import FunctionType as function, MethodType as method, ModuleType

__all__ = ('ismodule', 'isfilemodule', 'isdirmodule', 'isfunction', 'ismethod', 'ismetaclass', 
            'isclass', 'isbaseobject', 'isimmutabledef', 'isimmutable')

def ismodule(obj):
   return isinstance(obj, ModuleType)
   
def isfilemodule(obj):
   try:
      assert ismodule(obj)
      assert hasattr(obj, '__file__')
   except:
      return False
   return True

def isdirmodule(obj):
   try:
      assert hasattr(obj, '__path__')
      assert isfilemodule(obj)
   except:
      return False
   return True

def isfunction(obj):
   return isinstance(obj, function)

def ismethod(obj):
   return isinstance(obj, method)

def ismetaclass(obj):
   return isclass(obj) and issubclass(obj, type)

def isclass(obj):
   return isinstance(obj, type)

def isbaseobject(obj):
   return (obj is object or obj is type)

def isimmutabledef(cls):
   if not isclass(cls):
      raise TypeError("class object expected")
   imm = (tuple, str, int, float, long, complex, bool, frozenset)
   for i in imm:
      if issubclass(cls, i): return True
   if isbaseobject(cls): return False
   imm_funcs = ('__hash__', '__cmp__', '__eq__')
   a = [i for i in cls.__dict__ if i in imm_funcs and ismethod(getattr(cls, i))]
   if len(a) >= 2 and '__hash__' in a:
      return True
   for basecls in cls.__bases__:
      if not isimmutabledef(basecls): return False
   return True

def isimmutable(obj):
   imm = (tuple, str, int, float, long, complex, bool, frozenset)
   for i in imm:
      if isinstance(obj, i): return True
   if isbaseobject(obj): return True
   cls = obj.__class__
   return isimmutabledef(cls)
