# Module: smanstal.types.module
# File: module.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import os, sys, re
op = os.path

from smanstal.types import isfilemodule, ispackage, ismodule

__all__ = ('hasinit', 'absmodpath', 'rootpackage', 'pathmod', 'modpathmod', 'parent')

# =================================================
# hasinit
# =================================================
def hasinit(dir): #{{{
    if isinstance(dir, basestring) and op.isdir(dir):
        path1 = op.join(dir, '__init__.py')
        path2, path3 = path1 + 'c', path1 + 'o'
        return True in (op.isfile(p) for p in (path1, path2, path3))
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
#@signal_settings(policy='first')
def modpathmod(modpath): #{{{
    if not modpath:
        return None
    elif isinstance(modpath, basestring):
        return _mpm_str(modpath)
    raise TypeError('Cannot retrieve module from %s object' %modpath.__class__.__name__)
# End def #}}}

#@modpathmod.match_value(None)
#def _mpm_none(modpath): #{{{
#    return None
## End def #}}}

#@modpathmod.match_type(basestring)
#@signal_settings(globals=globals())
_mpm_regex = re.compile(r'^([a-zA-Z_][a-zA-Z_0-9]*)([.][a-zA-Z_][a-zA-Z_0-9]*)*$')
def _mpm_str(modpath): #{{{
    if not _mpm_regex.match(modpath.strip()):
        raise ValueError("'%s' is not a valid python module path" %modpath)
    modpath = modpath.strip()
    p = modpath.split('.')
    root, last = p[:-1], p[-1]
    if not root:
        return __import__(last)
    istr = "from %s import %s" %('.'.join(root), last)
    vars = {}
    exec compile(istr, '<string>', 'exec') in vars
    return vars[last]
# End def #}}}

#_mpm_regex = re.compile(r'^([a-zA-Z_][a-zA-Z_0-9]*)([.][a-zA-Z_][a-zA-Z_0-9]*)*$')
#@_mpm_str.when("_mpm_regex.match(modpath.strip())")
#def _mpm_restr(modpath): #{{{
#    modpath = modpath.strip()
#    p = modpath.split('.')
#    root, last = p[:-1], p[-1]
#    if not root:
#        return __import__(last)
#    istr = "from %s import %s" %('.'.join(root), last)
#    vars = {}
#    exec compile(istr, '<string>', 'exec') in vars
#    return vars[last]
## End def #}}}

# =================================================
# parent
# =================================================

#@signal_settings(globals=globals(), policy='first')
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


