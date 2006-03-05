################################################################################
# extras.types.module -- Description goes here
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

import os, sys
import dispatch
op = os.path

from extras.types import isfilemodule, isdirmodule

__all__ = ('DirHasPythonInit', 'AbsoluteModuleName', 'RootPackageOf', 'RootPackagePathOf',
            'ModuleObjectFromModulePath', 'ModuleObjectFromModuleName', 'ParentModule')

@dispatch.generic()
def DirHasPythonInit(dir):
   """Base generic function of 'DirHasPythonInit()'"""
   
@DirHasPythonInit.when('isinstance(dir, str) and str != ""')
def DirHasPythonInit(dir):
   path1 = op.join(dir, '__init__.py')
   path2 = path1 + 'c'
   path3 = path1 + 'o'
   return op.exists(path1) or op.exists(path2) or op.exists(path3)

@dispatch.generic()
def AbsoluteModuleName(module):
   """Base generic function of 'AbsoluteModuleName()'"""

@AbsoluteModuleName.when('isinstance(module, str) and module != ""')
def AbsoluteModuleName(module):
   root, ext = op.splitext(module)
   assert ext == ""
   temp, curdir = op.split(module)
   modpath = curdir
   while 1:
      if not DirHasPythonInit(temp):
         break
      temp, curdir = op.split(temp)
      modpath = "%s.%s" %(curdir, modpath)
   return modpath

@AbsoluteModuleName.when('isfilemodule(module)')
def AbsoluteModuleName(module):
   abspath = op.abspath(module.__file__)
   dir, file = op.split(abspath)
   ret = None
   if file.startswith('__init__.py'):
      ret = AbsoluteModuleName(dir)
   else:
      name, ext = op.splitext(abspath)
      ret = AbsoluteModuleName(name)
   return ret
   
@dispatch.generic()
def RootPackageOf(module):
   """Base generic function of 'RootPackageOf()'"""

@RootPackageOf.when('isfilemodule(module)')
def RootPackageOf(module):
   cur, ext = op.splitext(op.abspath(__file__))
   rootpkgstr = AbsoluteModuleName(cur).split('.', 1)[0]
   newcode = compile("import %s as rootpkg" %rootpkgstr, '<string>', 'exec')
   exec newcode in locals()
   return rootpkg

@dispatch.generic()
def RootPackagePathOf(module):
   """Base generic function of 'RootPackagePathOf()'"""

@RootPackagePathOf.when('isfilemodule(module)')
def RootPackagePathOf(module):
   rootpkg = RootPackageOf(module)
   curpath = op.abspath(rootpkg.__file__)
   dir = op.dirname(curpath)
   parent, cur = op.split(dir)
   return parent
   
@dispatch.generic()
def ModuleObjectFromModulePath(modpath):
   """Base generic function of 'ModuleObjectFromModulePath'"""
   
@ModuleObjectFromModulePath.when('isinstance(modpath, str) and op.exists(modpath)')
def ModuleObjectFromModulePath(modpath):
   abspath = op.abspath(modpath)
   path, file = op.split(abspath)
   if not file.startswith('__init__.py'):
      path, ext = op.splitext(abspath)
   modstr = AbsoluteModuleName(path)
   return ModuleObjectFromModuleName(modstr)
   
@dispatch.generic()
def ModuleObjectFromModuleName(modname):
   """Base generic function of 'ModuleObjectFromModuleName'"""
   
@ModuleObjectFromModuleName.when('isinstance(modname, str) and modname != ""')
def ModuleObjectFromModuleName(modname):
   newcode = compile("import %s as mod" %modname, '<string>', 'exec')
   exec newcode in locals()
   return mod
   
@dispatch.generic()
def ParentModule(module):
   """Base generic function of 'ParentModuleName()'"""
   
@ParentModule.when('isfilemodule(module)')
def ParentModule(module):
   absname = AbsoluteModuleName(module)
   parentname = absname.rsplit('.', 1)[0]
   if parentname == absname:
      return None
   return ModuleObjectFromModuleName(parentname)

@ParentModule.when('isinstance(module, str) and module != ""')
def ParentModule(module):
   abspath = op.abspath(module)
   path, file = op.split(abspath)
   if not file.startswith('__init__.py'):
      path, ext = op.splitext(abspath)
   absname = AbsoluteModuleName(path)
   parentname = absname.rsplit('.', 1)[0]
   if parentname == absname:
      return None
   return ModuleObjectFromModuleName(parentname)
