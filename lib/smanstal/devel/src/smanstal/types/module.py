# Module: smanstal.types.module
# File: module.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import os, sys, re
from aossi.deco import signal, signal_settings
from validate.value import vv_and
from validate.type import vt
op = os.path

from smanstal.types import isfilemodule, ispackage, ismodule

__all__ = ('hasinit', 'absmodpath', 'rootpackage', 'pathmod', 'modpathmod', 'parent')

# =================================================
# hasinit
# =================================================
@signal_settings(globals=globals())
def hasinit(dir): #{{{
    raise TypeError("'%s' is not a directory path string" %str(dir))
# End def #}}}

@hasinit.when('isinstance(dir, basestring) and op.isdir(dir)')
def _hasinit(dir): #{{{
   path1 = op.join(dir, '__init__.py')
   path2, path3 = path1 + 'c', path1 + 'o'
   return True in (op.isfile(p) for p in (path1, path2, path3))
# End def #}}}

# =================================================
# absmodpath
# =================================================
@signal_settings(globals=globals(), policy='first')
def absmodpath(module): #{{{
    raise TypeError("Cannot determine module path of %s object" %module.__class__.__name__)
# End def #}}}

@absmodpath.match_type(basestring)
@signal_settings(globals=globals(), policy='first')
def _amp_str(module): #{{{
    raise ValueError("'%s' is not a valid file system path" %module)
# End def #}}}

@_amp_str.when("tuple(op.basename(module).split('.')) in (('__init__', ext) for ext in ('py', 'pyc', 'pyo'))")
def _amp_init(module): #{{{
    return absmodpath(op.dirname(op.abspath(module)))
# End def #}}}

@_amp_str.when('op.exists(module)')
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

@absmodpath.when('isfilemodule(module)')
def _amp_mod(module): #{{{
    p = op.abspath(module.__file__)
    if ispackage(module):
        p = op.dirname(p)
    return absmodpath(p)
# End def #}}}

@absmodpath.when('ismodule(module)')
def _amp_mod(module): #{{{
    return module.__name__
# End def #}}}

# =================================================
# rootpackage
# =================================================
@signal_settings(globals=globals(), policy='first')
def rootpackage(module): #{{{
    names = (module.__class__.__name__, str(module))
    raise TypeError("Cannot determine root package of %s object '%s'" %names)
# End def #}}}

@rootpackage.when('isfilemodule(module)')
def _rp_fmod(module): #{{{
    p = absmodpath(module.__file__)
    if not p:
        return None
    root = p.split('.')[0]
    return __import__(root)
# End def #}}}

@rootpackage.when('ismodule(module)')
def _rp_dmod(module): #{{{
    return module
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
@signal_settings(policy='first')
def modpathmod(modpath): #{{{
    raise TypeError('Cannot retrieve module from %s object' %modpath.__class__.__name__)
# End def #}}}

@modpathmod.match_value(None)
def _mpm_none(modpath): #{{{
    return None
# End def #}}}

@modpathmod.match_type(basestring)
@signal_settings(globals=globals())
def _mpm_str(modpath): #{{{
    raise ValueError("'%s' is not a valid python module path" %modpath)
# End def #}}}

_mpm_regex = re.compile(r'^([a-zA-Z_][a-zA-Z_0-9]*)([.][a-zA-Z_][a-zA-Z_0-9]*)*$')
@_mpm_str.when("_mpm_regex.match(modpath.strip())")
def _mpm_restr(modpath): #{{{
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

# =================================================
# parent
# =================================================

@signal_settings(globals=globals(), policy='first')
def parent(module): #{{{
    raise TypeError("Cannot import parent module of %s object" %module.__class__.__name__)
# End def #}}}

@parent.when('isfilemodule(module)')
def _parent_fmod(module): #{{{
    p = absmodpath(module)
    path = p.split('.')
    plen = len(path)
    mpath = None
    if not plen or plen == 1:
        return module
    else: 
        mpath = '.'.join(path[:-1])
    return modpathmod(mpath)
# End def #}}}

@parent.when('ismodule(module)')
def _parent_dmod(module): #{{{
    return module
# End def #}}}
