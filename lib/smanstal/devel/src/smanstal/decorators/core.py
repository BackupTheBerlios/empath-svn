# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('property_', 'addall')

# Based on the following recipe:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/205183
def property_(func): #{{{
    vals = dict((k, v) for k,v in func().iteritems() 
            if k in ('fdel', 'fset', 'fget', 'doc'))
    return property(**vals)
# End def #}}}

def addall(all_list): #{{{
    def wrap(func): #{{{
        if not isinstance(all_list, list):
            raise TypeError("Only lists are supported for __all__ with the addall decorator")
        all_list.append(func.__name__)
        return func
    # End def #}}}
    return wrap
# End def #}}}
