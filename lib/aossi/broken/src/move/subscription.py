# Module: aossi.subscription
# File: subscription.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from warnings import warn
warn('This module is deprecated', DeprecationWarning)

from aossi.signal import Signal
from aossi.misc import iscallable

__all__ = ('subscribe', 'issue', 'cancel', 'publish')

_siglist = []

def _cleanlist(): #{{{
    lsl = len(_siglist)
    i = 0
    while i < lsl:
        io, signal = _siglist[i]
        delit = True
        if signal and signal.valid:
            yield io, signal, i
            delit = not bool(_siglist[i])
        if not delit:
            i += 1
        else:
            del _siglist[i]
            lsl -= 1
# End def #}}}

def issue(i): #{{{
    found = None
    for io, signal, index in _cleanlist():
        if found is None and io is i:
            found = signal
    return found
# End def #}}}

def _validate_subscribekw(iobj, c, t, choosefunc): #{{{
    expected = ('after', 'before', 'around', 'onreturn', 'choose')
    if iobj is None:
        raise TypeError('issue can not be None')
    elif not iscallable(c):
        raise TypeError('target must be callable')
    elif t and t not in expected:
        raise ValueError('detected unexpected type argument; must be one of the following: %s' %', '.join(expected))
    elif t == 'choose':
        if not choosefunc:
            raise ValueError("an ftype of 'choose' must be accompanied with an appropriate 'choosefunc'")
        elif not iscallable(choosefunc):
            raise TypeError('choosefunc argument must be callable')
# End def #}}}

def subscribe(iobj, target, ftype=None, choosefunc=None): #{{{
    _validate_subscribekw(iobj, target, ftype, choosefunc)
    i = issue(iobj)
    if i is None:
        if ftype:
            raise TypeError('Please subscribe an issue first.')
        i = Signal(target)
        _siglist.append((iobj, i))
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
# End def #}}}

def cancel(iobj=None, *after_slots, **other_slots): #{{{
    for io, signal, i in _cleanlist():
        if iobj is None:
            _siglist[i] = None
        elif io is iobj:
            if not after_slots and not other_slots:
                _siglist[i] = None
            else:
                signal.disconnect(*after_slots, **other_slots)
# End def #}}}

def publish(iobj, *args, **kwargs): #{{{
    i = issue(iobj)
    if i is None:
        warn('Publishing to unsubscribed issue', RuntimeWarning, stacklevel=2)
        return
    return i(*args, **kwargs)
# End def #}}}
