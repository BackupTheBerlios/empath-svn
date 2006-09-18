# Module: aossi
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from aossi.impex import import_, CopyModuleImporter
_ab = import_(':aossi:__builtin__', importer=CopyModuleImporter(copy_prefix=':aossi:'))

import aossi.misc as _am, aossi.signal as _as, aossi.cwrapper as _acw
from aossi.misc import *
from aossi.signal import *
from aossi.cwrapper import *

from inspect import (ismodule, isclass, isdatadescriptor, ismethoddescriptor, 
        isbuiltin, ismethod as _ism, isfunction as _isf)
from types import MethodType as method, FileType
sys = import_(':aossi:sys', importer=CopyModuleImporter(copy_prefix=':aossi:'))
import __builtin__

__all__ = _am.__all__ + _acw.__all__ + _as.__all__
__all__ += ('connect', 'disconnect', 'original', 'getsignal', 'MakeClassSignals',
            'MakeInstanceSignals', 'install_import', 'uninstall_import')
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

def _MakeObjectSignals(o, check_func, errmsg, found, *after_slots, **other_slots): #{{{
    getattr = _ab.getattr
    setattr = _ab.setattr
    issubclass = _ab.issubclass
    isinstance = _ab.isinstance
    if isclass(o) and not issubclass(o, object):
        return
    elif hasattr(o, '__class__') and not issubclass(o.__class__, object):
        return
    elif ismethoddescriptor(o) or isdatadescriptor(o):
        return
    if not check_func(o):
        raise TypeError(errmsg)
    if not isinstance(found, list):
        found = []
    for aname in dir(o):
        if aname in ('__class__',):
            continue
        attr = getattr(o, aname)
        if isinstance(attr, Signal) or attr in found:
            continue
        yield o, aname, attr
        attr = getattr(o, aname)
        if iscallable(attr):
            if ismethoddescriptor(attr) or isdatadescriptor(attr):
                continue
            if isreadonly(o, aname, attr):
                continue
            sig = Signal(attr, weak=False, active=False, activate_on_call=False)
            assert sig.valid
            sig.connect(*after_slots, **other_slots)
            setattr(o, aname, sig)
            found.append(sig)
        elif check_func(attr):
            if ismethoddescriptor(attr) or isdatadescriptor(attr):
                continue
            found.append(attr)
            for ret in _MakeObjectSignals(attr, check_func, errmsg, found, *after_slots, **other_slots):
                yield ret
# End def #}}}

def MakeClassSignals(cls, *after_slots, **other_slots): #{{{
    callable = _ab.callable
    isinstance = _ab.isinstance
    head = bool(other_slots.pop('head', True))
    found = []
    for c, aname, attr in _MakeObjectSignals(cls, isclass, 'argument must be a class', found, *after_slots, **other_slots):
        if ismodule(attr):
            modname = attr.__name__
            pre = ':aossi-wrapped:'
            if modname in sys.modules and not modname.startswith(pre):
                name = ''.join([pre, attr.__name__])
                attr = import_(name, importer=CopyModuleImporter(copy_prefix=pre))
                setattr(c, aname, attr)
        if not callable(attr):
            MakeInstanceSignals(attr, head=False, *after_slots, **other_slots)
    if head:
        for attr in found:
            if isinstance(attr, Signal):
                attr.activate_on_call = True
# End def #}}}

def MakeInstanceSignals(inst, *after_slots, **other_slots): #{{{
    callable = _ab.callable
    isinstance = _ab.isinstance
    head = bool(other_slots.pop('head', True))
    def isinst(i):
        return not callable(i)
    found = []
    for i, aname, attr in _MakeObjectSignals(inst, isinst, 'argument must be an instance', found, *after_slots, **other_slots):
        if isclass(attr):
            MakeClassSignals(attr, head=False, *after_slots, **other_slots)
        elif ismodule(attr):
            modname = attr.__name__
            pre = ':aossi-wrapped:'
            if modname in sys.modules and not modname.startswith(pre):
                name = ''.join([pre, modname])
                mod = import_(name, importer=CopyModuleImporter(copy_prefix=pre))
                setattr(i, aname, mod)
    if head:
        for attr in found:
            if isinstance(attr, Signal):
                attr.activate_on_call = True
# End def #}}}

def startswith(name, prefixes=[]): #{{{
    for prefix in prefixes:
        if name.startswith(prefix):
            return True
    return False
# End def #}}}

def create_import(*after_slots, **kwargs): #{{{
    def around_import(func): #{{{
        _sys = sys
        mksig = MakeInstanceSignals
        blacklist = kwargs.get('blacklist', [])
        a = after_slots
        o = kwargs.get('other_slots', {})
        pre = ':aossi-wrapped:'
        inblacklist = startswith
        def newcall(self, name, globals=None, locals=None, fromlist=None): #{{{
            origname = name.replace(pre, '')
#            name = '.'.join([''.join([pre, n]) for n in origname.split('.')])
            name = ''.join([pre, origname])
            origmod = func(origname, globals, locals, fromlist)
            if inblacklist(origname, blacklist):
                return origmod
            if not fromlist:
                name = name.split('.', 1)[0]
#            assert origname in sys.modules, '%s not in sys.modules' %origname
            mod = import_(name, importer=CopyModuleImporter(copy_prefix=pre))
            mksig(mod, *a, **o)
            return mod
        # End def #}}}
        return newcall
    # End def #}}}
    return around_import
# End def #}}}

def install_import(*after_slots, **kwargs): #{{{
    make_modsignals = bool(kwargs.get('make_modsignals', False))
    make_current_modsignals = bool(kwargs.get('make_current_modsignals', False))
    other_slots = kwargs.get('other_slots', {})
    ublacklist = [i for i in kwargs.get('blacklist', [])]
    blacklist = [':aossi:', ':aossi-wrapped:', 'aossi'] + ublacklist
    make_copies = ('__builtin__',)
    b = __builtin__
    kw = {'other_slots': other_slots, 'blacklist': blacklist}
    b.__import__ = Signal(_ab.__import__, weak=False)
    b.__import__.connect(around=[create_import(*after_slots, **kw)])
# End def #}}}

def uninstall_import(): #{{{
    __builtin__.__import__ = _ab.__import__
# End def #}}}
