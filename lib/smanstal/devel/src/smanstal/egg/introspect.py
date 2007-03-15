# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.egg.resources import resource_isfile, resource_isdir
from smanstal.types.introspect import ismodule as ismod
import posixpath as pp
import os.path as op

__all__ = ('ismodule', 'isfilemodule', 'ispackage')

def ismodule(package_or_resource, obj): #{{{
    por = package_or_resource
    try:
        assert ismod(obj)
        assert all(hasattr(obj, a) for a in ('__name__', '__file__'))
        root = obj.__name__.split('.')[0]
        pkg = __import__(root)
        pkgdir = op.dirname(pkg.__file__)
        assert obj.__file__.startswith(pkgdir)
    except AssertionError:
        return False
    return True
# End def #}}}

def isfilemodule(package_or_resource, obj): #{{{
    por, isfile = package_or_resource, resource_isfile
    try:
        assert ismodule(por, obj)
        name, ind = obj.__name__, 0
        if isinstance(por, basestring):
            ind = 1
        path = pp.join(pp.sep, *name.split('.')[ind:])
        check = []
        if resource_isdir(por, path):
            check.append(pp.join(path, '__init__'))
        check.append(path)
        ext = ['py'+c for c in ('', 'c', 'o')]
        assert any(isfile(por, '.'.join([p, pext])) for pext in ext for p in check)
    except AssertionError:
        return False
    return True
# End def #}}}

def ispackage(package_or_resource, obj): #{{{
    try:
        assert isfilemodule(package_or_resource, obj)
        assert hasattr(obj, '__path__')
    except AssertionError:
        return False
    return True
# End def #}}}
