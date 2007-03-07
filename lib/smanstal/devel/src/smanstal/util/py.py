# Module: smanstal.util.py
# File: py.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from sys import _getframe

__all__ = ('callervars', 'iff', 'selfcaller')


def callervars(i=2): #{{{
    caller = _getframe(i-1)
    if caller.f_code.co_name != '?':
        caller = _getframe(i)
    return caller.f_locals, caller.f_globals
# End def #}}}

def iff(cond, tret, fret): #{{{
    if cond:
        return tret
    return fret
# End def #}}}

def selfcaller(i=1): #{{{
    caller = _getframe(i)
    n = caller.f_code.co_name
    glob = caller.f_globals
    if n == '?':
        raise NameError("Unknown caller -- main? interpreter?")
    elif n not in glob:
        raise NameError("'%s' object does not exist yet -- calling from a class definition?" %n)
    return glob.get(n)
# End def #}}}

# One implementation of properties
from smanstal.types.introspect import isfunction
class AutoProp(type): #{{{
    def __new__(apcls, classname, bases, clsdict): #{{{
        names = {}
        sd, clspop = names.setdefault, clsdict.pop
        for fname, f in clsdict.items():
            orig, ind = fname, fname.find('_')
            type = orig[:ind]
            if ind < 0 or ind+1 == len(orig):
                continue
            actions = set(['get', 'set', 'del', 'doc'])
            if type in actions:
                if not ((type == 'doc' and isinstance(f, basestring)) or isfunction(f)):
                    continue
                fname = orig[ind+1:]
                arg = type if type == 'doc' else 'f'+type
                sd(fname, {})[arg] = f
                clspop(orig)
        clsdict.update((n, property(**kw)) for n, kw in names.iteritems())
        return super(AutoProp, apcls).__new__(apcls, classname, bases, clsdict)
    # End def #}}}
# End class #}}}
