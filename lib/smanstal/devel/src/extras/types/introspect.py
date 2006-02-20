###########################################################################
# extras.types.introspect -- Description goes here
# Copyright (C) 2006  Ariel De Ocampo
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###########################################################################
from types import FunctionType as function, MethodType as method

__all__ = ('isfunction', 'ismethod', 'ismetaclass', 'isclass', 'isbaseobject', 
            'isimmutabledef', 'isimmutable')

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
