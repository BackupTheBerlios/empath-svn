# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import sys
from smanstal.types.introspect import isclass

__all__ = ('user_input', 'eval_input', 'osetattr', 'odelattr', 'ogetattr', 'ohasattr')

def user_input(prompt=None): #{{{
    return sys.stdin.readline().strip() if not prompt or not sys.stdout.write(str(prompt)) else ''
# End def #}}}

def eval_input(prompt=None): #{{{
    return eval(user_input(prompt))
# End def #}}}

osetattr = object.__setattr__
odelattr = object.__delattr__
_getobjattr = object.__getattribute__
def ogetattr(obj, name, *default): #{{{
    largs = len(default)
    if largs > 1:
        raise ValueError("Expected 1 default value, got %i instead" %largs)
    ret = None
    try:
        ret = _getobjattr(obj, name)
    except AttributeError:
        if not default:
            raise
        ret = default[0]
    return ret
# End def #}}}

def ohasattr(o, name): #{{{
    try:
        ogetattr(o, name)
    except AttributeError:
        return False
    else:
        return True
# End def #}}}

def getslot(o, n): #{{{
    slots = ogetattr(o, '__slots__')
    if isclass(o):
        raise TypeError("Can only retrieve instance slots")
    if n not in slots:
        raise AttributeError("'%s' instance has no slot attribute '%s'" %(o.__class__.__name__, n))
    return ogetattr(o, n)
# End def #}}}
