###########################################################################
# extras.types.module -- Description goes here
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
   abspath = op.realpath(module.__file__)
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
   cur, ext = op.splitext(op.realpath(__file__))
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
   curpath = op.realpath(rootpkg.__file__)
   dir = op.dirname(curpath)
   parent, cur = op.split(dir)
   return parent
   
@dispatch.generic()
def ModuleObjectFromModulePath(modpath):
   """Base generic function of 'ModuleObjectFromModulePath'"""
   
@ModuleObjectFromModulePath.when('isinstance(modpath, str) and op.exists(modpath)')
def ModuleObjectFromModulePath(modpath):
   abspath = op.realpath(modpath)
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
   abspath = op.realpath(module)
   path, file = op.split(abspath)
   if not file.startswith('__init__.py'):
      path, ext = op.splitext(abspath)
   absname = AbsoluteModuleName(path)
   parentname = absname.rsplit('.', 1)[0]
   if parentname == absname:
      return None
   return ModuleObjectFromModuleName(parentname)
