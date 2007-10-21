# Module: aossi.msgsub
# File: msgsub.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from warnings import warn

from aossi.signal import Signal
from aossi.misc import iscallable, callableobj

from types import ClassType
from inspect import isfunction as _isf, ismethod as _ism

__all__ = ('subscribe', 'issue', 'cancel', 'publish', 'Message', 'Arguments')

_siglist = {}

def ishashable(obj): #{{{
    ret = True
    try:
        hash(obj)
    except TypeError:
        ret = False
    return ret
# End def #}}}

def isnewclass(obj): #{{{
    """Return true if the object is a class.

    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
    return (isinstance(obj, ClassType) or hasattr(obj, '__bases__')) and issubclass(obj, object) 
# End def #}}}

class Message(object): #{{{
    def __init__(self, argobj): #{{{
        self._args = argobj
        self.returnval = None
    # End def #}}}

    def _set_returnval(self, val): #{{{
        self._returnval = val
    # End def #}}}

    # Properties #{{{
    args = property(lambda s: s._args)
    returnval = property(lambda s: s._returnval, lambda s, v: s._set_returnval(v))
    # End properties #}}}
# End class #}}}

class Arguments(object): #{{{
    def __init__(self, **kwargs): #{{{
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    # End def #}}}
# End class #}}}

def _cleanlist(): #{{{
    for ki, vi in _siglist.items():
        for km, vm in vi.items():
            for args, signal in vm.items():
                delit = True
                if signal and signal.valid:
                    yield ki, km, vm, args, signal
                    delit = not bool(vm[args])
                if delit:
                    vm.pop(args)
            if not vm:
                vi.pop(km)
        if not vi:
            _siglist.pop(ki)
# End def #}}}

def issue(i, msg=Message, args=Arguments): #{{{
    found = None
    for io, smsg, all_sargs, sargs, signal in _cleanlist():
        if found is None and io is i and smsg is msg and sargs is args:
            found = signal
    return found
# End def #}}}

def _validate_subscribekw(iobj, c, m, a, t, choosefunc): #{{{
    expected = ('after', 'before', 'around', 'onreturn', 'choose')
    if iobj is None:
        raise TypeError('issue can not be None')
    elif not ishashable(iobj):
        raise TypeError('issue must be hashable')
    elif not iscallable(c):
        raise TypeError('target must be callable')
    elif not isnewclass(m):
        raise TypeError('msgobj must be a new style class')
    elif not isnewclass(a):
        raise TypeError('argsobj must be a new style class')
    elif t and t not in expected:
        raise ValueError('detected unexpected type argument; must be one of the following: %s' %', '.join(expected))
    elif t == 'choose':
        if not choosefunc:
            raise ValueError("an ftype of 'choose' must be accompanied with an appropriate 'choosefunc'")
        elif not iscallable(choosefunc):
            raise TypeError('choosefunc argument must be callable')
# End def #}}}

def subscribe(iobj, target, msgobj=Message, argsobj=Arguments, ftype=None, choosefunc=None): #{{{
    _validate_subscribekw(iobj, target, msgobj, argsobj, ftype, choosefunc)
    i = issue(iobj, msgobj, argsobj)
    if i is None:
        if ftype:
            raise TypeError('Please subscribe an issue first.')
        i = Signal(target)
        cobj = callableobj(target)
        numargs = i.func.numargs
        if _isf(cobj) and numargs != 1:
            raise ValueError("'target' argument is a function: it must accept exactly 1 argument; instead got %i" %numargs)
        elif _ism(cobj) and numargs != 2:
            raise ValueError("'target' argument is a method: it must accept exactly 2 arguments; instead got %i" %numargs)
        smsg = _siglist.get(iobj, {})
        sargs = smsg.get(msgobj, {})
        sargs.update({argsobj: i})
        smsg.update({msgobj: sargs})
        _siglist.update({iobj: smsg})
    elif not ftype or ftype == 'after':
        i.connect(target)
    elif ftype == 'before':
        i.connect(before=[target])
    elif ftype == 'around':
        i.connect(around=[target])
    elif ftype == 'onreturn':
        i.connect(onreturn=[target])
    elif ftype == 'choose':
        i.connect(choose=[(choosefunc, target)])
    return i
# End def #}}}

def cancel(iobj=None, msgobj=None, argsobj=None, *after_slots, **kwargs): #{{{
    other_slots = kwargs.get('other_slots', {})
    keep_signal = bool(kwargs.get('keep_signal', False))
    for io, smsg, all_sargs, sargs, signal in _cleanlist():
        if iobj is None:
            all_sargs[sargs] = None
        elif io is not iobj:
            continue
        elif not msgobj or (smsg is msgobj and not argsobj) or (smsg is msgobj and sargs is argsobj):
            if not after_slots and not other_slots:
                if keep_signal:
                    signal.disconnect()
                else:
                    all_sargs[sargs] = None
            else:
                signal.disconnect(*after_slots, **other_slots)
# End def #}}}

def publish(iobj, msgobj=Message, argsobj=Arguments, **kwargs): #{{{
    i = issue(iobj, msgobj, argsobj)
    if i is None:
        warn('Publishing to unsubscribed issue', RuntimeWarning, stacklevel=2)
        return
    m = msgobj(argsobj(**kwargs))
    i(m)
    return m
# End def #}}}
