# Module: aossi
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#from aossi.impex import import_, CopyModuleImporter
#_ab = import_(':aossi:__builtin__', importer=CopyModuleImporter(copy_prefix=':aossi:'))

import aossi.util as _am, aossi.signal as _as, aossi.cwrapper as _acw
from aossi.util import *
from aossi.signal import *
from aossi.cwrapper import *

from inspect import (ismodule, isclass, isdatadescriptor, ismethoddescriptor, 
        isbuiltin, ismethod as _ism, isfunction as _isf)
from types import MethodType as method, FileType
#sys = import_(':aossi:sys', importer=CopyModuleImporter(copy_prefix=':aossi:'))
#import __builtin__
import sys, __builtin__ as _ab

__all__ = _am.__all__ + _acw.__all__ + _as.__all__
__all__ += ('connect', 'disconnect', 'original', 'getsignal')
del _am, _as, _acw

def _signal(c, reuse=True, **kwargs): #{{{
    getattr = _ab.getattr
    sig = getsignal(c)
    if sig and reuse and sig is not c:
        return c, sig
    if (not sig or not reuse) and not isinstance(c, Signal):
        sig = Signal(c, **kwargs)
    d = callable_wrapper(sig)
    d.__name__ = c.__name__
    d.__dict__ = getattr(c, '__dict__', d.__dict__)
    d.__doc__ = getattr(c, '__doc__', d.__doc__)
    d.signal = sig
    if _ism(c):
        d = method(d, c.im_self, c.im_class)
    return d, sig
# End def #}}}

def connect(c, *after_slots, **kwargs): #{{{    
    block = ('weak_signal', 'active', 'activate_on_call', 'reuse_signals')
    def _wsig(k):
        if k == 'weak_signal':
            k = 'weak'
        return k
    reuse_signals = _ab.bool(kwargs.get('reuse_signals', True))
    cset = dict((_wsig(k), v) for k, v in kwargs.iteritems() if k in block[:-1])
    other_slots = dict((k, v) for k, v in kwargs.iteritems() if k not in block)
    newfunc, sig = _signal(c, reuse_signals, **cset)
    sig.connect(*after_slots, **other_slots)
    return newfunc
# End def #}}}

def disconnect(sig, *after_slots, **other_slots): #{{{
    sig = getsignal(sig)
    if not sig:
        raise TypeError("'Signal' instance required for 'sig' argument")
    sig.disconnect(*after_slots, **other_slots)
# End def #}}}

def original(sig): #{{{
    sig = getsignal(sig)
    if not sig:
        raise TypeError("'Signal' instance required for 'sig' argument")
    return sig.original
# End def #}}}

def getsignal(c): #{{{
    if not iscallable(c):
        return None
    real_sig = c
    if not isinstance(c, Signal):
        if _ism(c):
            real_sig = c.im_func
        real_sig = _ab.getattr(real_sig, 'signal', None)
        if not real_sig or not isinstance(real_sig, Signal):
            return None
    return real_sig
# End def #}}}
