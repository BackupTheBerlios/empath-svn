# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pkg_resources import resource_listdir, resource_isdir, resource_exists
import posixpath as pp

__all__ = ('resource_exists', 'resource_isdir', 'resource_listdir', 'resource_walk', 'resource_isfile')

def resource_walk(package_or_requirement, top, topdown=True, onerror=None): #{{{
    por = package_or_requirement
    if top in ('.', '..', '/'):
        top = ''
    dirpath = top
    listdir = resource_listdir(por, top)
    dirnames, filenames = [], []
    for name in listdir:
        cur = pp.join(top, name)
        if resource_isdir(por, cur):
            if not topdown:
                for t in resource_walk(por, cur, topdown, onerror):
                    yield t
            dirnames.append(name)
        else:
            filenames.append(name)
    yield dirpath, dirnames, filenames
    if topdown:
        for d in dirnames:
            for t in resource_walk(por, pp.join(dirpath, d), topdown, onerror):
                yield t
# End def #}}}

def resource_isfile(package_or_requirement, resource_name): #{{{
    return bool(resource_exists(package_or_requirement, resource_name) and 
            not resource_isdir(package_or_requirement, resource_name))
# End def #}}}
