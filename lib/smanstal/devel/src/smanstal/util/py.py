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
