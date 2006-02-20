###########################################################################
# extras.copy -- Description goes here
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
import dispatch

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
