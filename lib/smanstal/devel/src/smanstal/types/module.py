# Module: smanstal.types.module
# File: module.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import os, sys, re
op = os.path

from smanstal.types import isfilemodule, ispackage, ismodule
from types import ModuleType as module

__all__ = ('hasinit', 'absmodpath', 'rootpackage', 'pathmod', 'modpathmod', 
            'parent', 'pkgdir', 'fromfile', 'isfindable')

# =================================================
# hasinit
# =================================================
def hasinit(dir, source_first=True): #{{{
    source_first = (lambda seq: seq) if source_first else reversed
    if isinstance(dir, basestring) and op.isdir(dir):
        path1 = op.join(dir, '__init__.py')
        path2, path3 = path1 + 'c', path1 + 'o'
        for p in source_first((path1, path2, path3)):
            if op.isfile(p):
                return op.basename(p)
        return ''
#        return True in (op.isfile(p) for p in (path1, path2, path3))
    raise TypeError("'%s' is not a directory path string" %str(dir))
# End def #}}}
# =================================================
# absmodpath
# =================================================
def absmodpath(module): #{{{
    if isinstance(module, basestring):
        return _amp_str(module)
    elif isfilemodule(module):
        p = op.abspath(module.__file__)
        if ispackage(module):
            p = op.dirname(p)
        return absmodpath(p)
    elif ismodule(module):
        return module.__name__
    raise TypeError("Cannot determine module path of %s object" %module.__class__.__name__)
# End def #}}}

def _amp_str(module): #{{{
    if tuple(op.basename(module).split('.')) in (('__init__', ext) for ext in ('py', 'pyc', 'pyo')):
        return absmodpath(op.dirname(op.abspath(module)))
    elif op.exists(module):
        return _amp_strpath(module)
    raise ValueError("'%s' is not a valid file system path" %module)
# End def #}}}

def _amp_strpath(module): #{{{
    module = op.abspath(module)
    modpath = None
    curdir = module
    if op.isfile(module):
        curdir, file = op.split(module)
        modname, ext = op.splitext(file)
        if ext not in ('.py', '.pyc', '.pyo'):
            return None
        modpath = modname
    while 1:
        if not hasinit(curdir):
            break
        modname = op.basename(curdir)
        if not modpath:
            modpath = modname
        else:
            modpath = '.'.join((modname, modpath))
        parentdir, file = op.split(curdir)
        if parentdir == curdir:
            break
        curdir = parentdir
    return modpath
# End def #}}}
# =================================================
# rootpackage
# =================================================
def rootpackage(module): #{{{
    if isfilemodule(module):
        p = absmodpath(module.__file__)
        if not p:
            return None
        root = p.split('.')[0]
        return __import__(root)
    elif ismodule(module):
        return module
    names = (module.__class__.__name__, str(module))
    raise TypeError("Cannot determine root package of %s object '%s'" %names)
# End def #}}}
# =================================================
# pathmod
# =================================================
def pathmod(path): #{{{
    if not path:
        return None
    p = absmodpath(path)
    return modpathmod(p)
# End def #}}}

# =================================================
# modpathmod
# =================================================
def modpathmod(modpath): #{{{
    if not modpath:
        return None
    elif isinstance(modpath, basestring):
        return _mpm_str(modpath)
    raise TypeError('Cannot retrieve module from %s object' %modpath.__class__.__name__)
# End def #}}}

_mpm_regex = re.compile(r'^([a-zA-Z_][a-zA-Z_0-9]*)([.][a-zA-Z_][a-zA-Z_0-9]*)*$')
def _mpm_str(modpath): #{{{
    if not _mpm_regex.match(modpath.strip()):
        raise ValueError("'%s' is not a valid python module path" %modpath)
    modpath = modpath.strip()
    p = modpath.split('.')
    root, last = p[:-1], p[-1]
    if not root:
        return __import__(last)
    # Is the assumption that all modules imported by __import__
    # are placed into sys.modules correct?
    __import__(modpath)
    return sys.modules[modpath]
#    vars = {}
#    istr = "from %s import %s" %('.'.join(root), last)
#    exec compile(istr, '<string>', 'exec') in vars
#    return vars[last]
# End def #}}}

# =================================================
# parent
# =================================================

def parent(module): #{{{
    if isfilemodule(module):
        p = absmodpath(module)
        path = p.split('.')
        plen = len(path)
        mpath = None
        if not plen or plen == 1:
            return module
        else: 
            mpath = '.'.join(path[:-1])
        return modpathmod(mpath)
    elif ismodule(module):
        return module
    raise TypeError("Cannot import parent module of %s object" %module.__class__.__name__)
# End def #}}}


# =================================================
# pkgdir
# =================================================
def pkgdir(path): #{{{
    pypath = absmodpath(path)
    if not pypath:
        raise TypeError("Not a valid python file: %s" %path)
    mf = op.abspath(path)
    magicdir = mf
    if op.basename(mf) in ('__init__.py%s' %s for s in ('', 'c', 'o')):
        magicdir = op.dirname(mf)
    pypath = absmodpath(mf).split('.')
    rootfile = op.join(os.sep, *magicdir.split(os.sep)[:(-1*len(pypath))])
    return rootfile
# End def #}}}
# =================================================
# fromfile
# =================================================

def fromfile(path): #{{{
    pypath = absmodpath(path)
    if not pypath:
        raise TypeError("Not a valid python file: %s" %path)
    mod, isdir = None, op.isdir
    rootdir, osj, j = pkgdir(path), op.join, '.'.join
    path_isdir = isdir(path)
    pypath_list = pypath.split('.')
    maxlen = len(pypath_list)
    if path_isdir:
        path = osj(path, hasinit(path))
    elif op.basename(path) in ('__init__.py%s' %s for s in ('', 'c', 'o')):
        path_isdir = True
    sysmod = sys.modules
    mod = sysmod.get(pypath)
    if mod and mod.__file__ == path:
        return mod
    for ind in xrange(1, maxlen+1):
        cur = pypath_list[:ind]
        ospath, name = osj(rootdir, *cur), j(cur)
        filename = path if ind == maxlen else osj(ospath, hasinit(ospath))
        mod = sysmod.get(name)
        if mod and mod.__file__ == filename:
            continue
        mod = module(name)
        mod.__file__ = filename
        execfile(filename, mod.__dict__)
        sysmod[name] = mod
        if ind < maxlen or path_isdir:
            mod.__path__ = [ospath]
    return mod
# End def #}}}

# =================================================
# isfindable
# =================================================
def isfindable(path): #{{{
    try:
        sysp = pkgdir(path)
    except TypeError:
        return False
    return (sysp in sys.path)
# End def #}}}
