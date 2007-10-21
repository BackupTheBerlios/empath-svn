# Module: aossi.cwrapper
# File: cwrapper.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
#from warnings import warn
#from types import MethodType as method
#from inspect import getargspec, isfunction as _isf, ismethod as _ism, isbuiltin as _isb, isclass

# package imports
#from aossi.util import (iscallable, needs_wrapping, cgetargspec, methodtype, cref, ChoiceObject, callableobj,
#        METHODTYPE_NOTMETHOD, METHODTYPE_UNBOUND, METHODTYPE_INSTANCE, METHODTYPE_CLASS)
#from aossi._speedups.cwrapper import cid, num_static_args, _CallableWrapper
#from aossi._cwrapper import cid, num_static_args, _CallableWrapper
try:
    from aossi._speedups.cwrapper import cid, num_static_args, _CallableWrapper
except ImportError:
    from aossi._cwrapper import cid, num_static_args, _CallableWrapper

__all__ = ('cid', 'num_static_args', 'CallableWrapper')

class CallableWrapper(_CallableWrapper): #{{{
    __slots__ = ('__weakref__',)
# End class #}}}


