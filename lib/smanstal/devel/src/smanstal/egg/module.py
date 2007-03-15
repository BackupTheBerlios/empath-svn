# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pkg_resources import resource_isdir as isdir, resource_exists as exists, Requirement
from smanstal.egg.resources import resource_isfile as isfile
from smanstal.types.module import modpathmod as orig_modpathmod
from smanstal.egg.introspect import *

import posixpath as pp
import os.path as op

__all__ = ('hasinit', 'pkgname', 'absmodpath', 'rootpackage', 'pathmod', 'modpathmod', 'parent')

# =================================================
# Helpers
# =================================================
def _find_match(por, obj): #{{{
    isabs = pp.isabs(obj)
    pyfile = lambda obj: any(obj.endswith(ext) for ext in ('.py', '.pyc', '.pyo'))
    obj, join = obj.split(op.sep), pp.join
    for i in xrange(len(obj)):
        path = join(*obj[i:])
        if exists(por, path):
            ispymod = pyfile(path) or hasinit(por, path)
            if not ispymod:
                continue
            if isinstance(por, Requirement) or not isabs:
                ind = i
            else:
                ind = i-1
            return obj[ind:]
# End def #}}}

# =================================================
# hasinit
# =================================================
def hasinit(package_or_requirement, dir): #{{{
    por = package_or_requirement
    if isinstance(dir, basestring) and isdir(por, dir):
        path1 = pp.join(dir, '__init__.py')
        path2, path3 = path1 + 'c', path1 + 'o'
        return True in (isfile(por, p) for p in (path1, path2, path3))
    raise TypeError("'%s' is not a directory path string" %str(dir))
# End def #}}}

# =================================================
# pkgname
# =================================================
def pkgname(package_or_requirement, obj): #{{{
    por = package_or_requirement
    if ispackage(por, obj):
        return obj.__name__
    elif ismodule(por, obj):
        obj = op.dirname(obj.__file__)
    if not isinstance(obj, basestring):
        raise TypeError("pkgname expected basestring object, got %s object instead" %obj.__class__.__name__)
    ret = _find_match(por, obj)
    if ret:
        if isinstance(por, basestring) and not pp.isabs(obj):
            ret = [por]
        ret = ret[0]
    return ret
# End def #}}}
# =================================================
# absmodpath
# =================================================
def absmodpath(package_or_requirement, module): #{{{
    por = package_or_requirement
    if isinstance(module, basestring):
        return _amp_str(por, module)
    elif isfilemodule(por, module):
        return _amp_str(por, module.__file__)
    elif ismodule(por, module):
        return module.__name__
    raise TypeError("Cannot determine module path of %s object" %module.__class__.__name__)
# End def #}}}

def _amp_str(por, module): #{{{
    if tuple(op.basename(module).split('.')) in (('__init__', ext) for ext in ('py', 'pyc', 'pyo')):
        return absmodpath(por, op.dirname(op.abspath(module)))
    ret = _find_match(por, module)
    if not ret:
        last, pkg, err = op.basename(module), None, False
        try:
            pkg = __import__(last)
        except ImportError:
            err = True
        else:
            err = not ispackage(por, pkg) 
        if err:
            raise ValueError("'%s' is not a valid path" %module)
        return last
    last = ret[-1].rsplit('.', 1)
    if last[-1] in ('py', 'pyc', 'pyo'):
        ret[-1] = ''.join(last[:-1])
    if isinstance(por, basestring) and not pp.isabs(module):
        if len(ret) > 1 or ret[0]:
            ret = [por] + ret
        else:
            ret = [por]
    return '.'.join(ret)
# End def #}}}
# =================================================
# rootpackage
# =================================================
def rootpackage(package_or_requirement, module): #{{{
    por = package_or_requirement
    if isfilemodule(por, module):
        p = absmodpath(por, module.__file__)
        if not p:
            return None
        root = p.split('.')[0]
        return __import__(root)
    names = (module.__class__.__name__, str(module))
    raise TypeError("Cannot determine root package of %s object '%s'" %names)
# End def #}}}
# =================================================
# pathmod
# =================================================
def pathmod(package_or_requirement, path): #{{{
    por = package_or_requirement
    if not path:
        return None
    p = absmodpath(por, path)
    return modpathmod(por, p)
# End def #}}}

# =================================================
# modpathmod
# =================================================
def modpathmod(package_or_requirement, modpath): #{{{
    return orig_modpathmod(modpath)
# End def #}}}

# =================================================
# parent
# =================================================

def parent(package_or_requirement, module): #{{{
    por = package_or_requirement
    if isfilemodule(por, module):
        p = absmodpath(por, module)
        path = p.split('.')
        plen = len(path)
        mpath = None
        if not plen or plen == 1:
            return module
        else: 
            mpath = '.'.join(path[:-1])
        return modpathmod(por, mpath)
    raise TypeError("Cannot import parent module of %s object" %module.__class__.__name__)
# End def #}}}

# =================================================

# =================================================
