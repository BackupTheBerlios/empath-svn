###########################################################################
# extras.types -- Description goes here
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
from extras.types.introspect import *
from extras.types.module import *

from extras.types.odict import odict

__all__ = ('ismodule', 'isfilemodule', 'isdirmodule', 'isfunction', 'ismethod', 'ismetaclass', 
            'isclass', 'isbaseobject', 'isimmutabledef', 'isimmutable', 'odict'
            'DirHasPythonInit', 'AbsoluteModuleName', 'RootPackageOf', 'RootPackagePathOf',
            'ModuleObjectFromModulePath', 'ModuleObjectFromModuleName', 'ParentModule')
