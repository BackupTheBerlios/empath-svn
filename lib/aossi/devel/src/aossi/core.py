# Module: aossi.core
# File: core.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from warnings import warn

# package imports
try:
    from aossi._speedups.core import (_BaseSignal, cid, callfunc, mkcallback, 
                                  connect_func, disconnect_func, getsignal)
except ImportError:
    from aossi._core import (_BaseSignal, cid, callfunc, mkcallback, 
                             connect_func, disconnect_func, getsignal)
#from aossi.cwrapper import CallableWrapper, cid
#from aossi.util import property_, iscallable, ChooseCallable, ChoiceObject
#from aossi.util.introspect import ismethod
#from aossi.util.odict import odict

__all__ = ('BaseSignal', 'cid', 'callfunc', 'mkcallback', 'connect_func', 'disconnect_func',
            'getsignal')
# ==================================================================================
# General Helpers
# ==================================================================================
# ==================================================================================
# Connect Helpers
# ==================================================================================
# ==================================================================================
# Signal
# ==================================================================================
# Reload function list -- odict listname/func
# Function lists -- dict listname/func list
# Call function list -- odict listname/func
# Connections function list -- odict listname/(cfunc, dfunc) 2-tuple
# Options -- dict option name/value
class BaseSignal(_BaseSignal): #{{{
    __slots__ = ('__weakref__',)
# End class #}}}
