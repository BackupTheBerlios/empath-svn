# Module: smanstal.util.str 
# File: str.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from string import Template

from smanstal.util.py import callervars

__all__ = ('VarExpansion', 'expand', 'varexpand', 'safe_expand', 'safe_varexpand')

class VarExpansion(Template): #{{{
    idpattern = r'(%s) | ([0-9]|[1-9][0-9]*)' %Template.idpattern
# End class #}}}

def expand(s, *args, **kw): #{{{
    kw.update((str(i), v) for i, v in enumerate(args))
    return VarExpansion(s).substitute(kw)
# End def #}}}

def varexpand(s, *args, **kw): #{{{
    clvar, cgvar = callervars()
    env = dict(cgvar)
    env.update(clvar)
    env.update(kw)
    return expand(s, *args, **env)
# End def #}}}

def safe_expand(s, *args, **kw): #{{{
    kw.update((str(i), v) for i, v in enumerate(args))
    return VarExpansion(s).safe_substitute(kw)
# End def #}}}

def safe_varexpand(s, *args, **kw): #{{{
    clvar, cgvar = callervars()
    env = dict(cgvar)
    env.update(clvar)
    env.update(kw)
    return safe_expand(s, *args, **env)
# End def #}}}

