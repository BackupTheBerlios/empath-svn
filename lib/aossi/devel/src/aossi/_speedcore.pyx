# Module: aossi.core
# File: core.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from warnings import warn

# package imports
from aossi.cwrapper import CallableWrapper, cid
from aossi.util import property_, iscallable, ChooseCallable, ChoiceObject
from aossi.util.introspect import ismethod
from aossi.util.odict import odict

__all__ = ('_BaseSignal', 'cid', 'callfunc', 'mkcallback', 'connect_func', 'disconnect_func',
            'getsignal')
# ==================================================================================
# General Helpers
# ==================================================================================
def callfunc(sig, func, functype, pass_ret, ret, *args, **kwargs): #{{{
    sfunc = sig.func
    if pass_ret:
        args, kwargs = (ret,), {}
    # Going from a method signal to any callable, 
    # remove the `self` argument if required
    if sfunc.ismethod and len(args) >= sfunc.maxargs:
        obj = sfunc._object()
        fo = func._object
        if fo:
            fo = fo()
        if fo != obj and fo != obj.__class__:
            args = args[1:]
    return func(*args, **kwargs)
# End def #}}}
# ==================================================================================
# Connect Helpers
# ==================================================================================
#def mkcallback(name, cleanlist): #{{{
#    def callback(obj):
#        for ret in cleanlist(name): pass
#    return callback
## End def #}}}

class mkcallback(object): #{{{
    __slots__ = ()
    def __init__(self, name, cleanlist): #{{{
        self.name = name
        self.cleanlist = cleanlist
    # End def #}}}

    def __call__(self, obj): #{{{
        for ret in self.cleanlist(self.name): pass
    # End def #}}}
# End class #}}}

def connect_func(self, listname, slots): #{{{
    weak = bool(slots.get('weak', self.func.isweak))
    uniq = bool(slots.get('unique', True))
    l, vals = self._funclist[listname], slots.get(listname, ())
    cleanlist, test_store = self._cleanlist, []
    cleanfunc = mkcallback(listname, cleanlist)
    for f in vals:
        if not iscallable(f):
            raise TypeError('Detected non-callable element of \'%s\' slots' %listname)
        c = CallableWrapper(f, cleanfunc, weak=weak)
        found = self._find(f, listname)
        if not found:
            ccid = c.cid
            for o in test_store:
                found = (ccid == cid(o))
                if found:
                    break
#                if ccid == cid(o):
#                    found = True
#                    break
#        found = self._find(f, listname) or c.cid in (cid(o) for o in test_store)
        if found and uniq:
            continue
        test_store.append(c)
    if test_store:
        l.extend(test_store)
# End def #}}}

def disconnect_func(self, listname, slots): #{{{
    l = self._funclist[listname]
    delall = bool(slots.get('deleteall', False))
    if delall and (not (len(slots)-1) or listname in slots):
        while l:
            l.pop()
        return
    for f in slots.get(listname, ()):
        found = self._find(f, listname)
        if found:
            del l[found[0]]
# End def #}}}

class _slot_is_empty(object): #{{{
    __slots__ = ()
    def __init__(self, funclist): #{{{
        self.funclist = funclist
    # End def #}}}
    def __call__(self, name): #{{{
        return bool(self.funclist[name])
    # End def #}}}
# End class #}}}

def _mk_call_funclist(name): #{{{
    return (name, odict())
# End def #}}}

def _update_funclist(name): #{{{
    return (name, [])
# End def #}}}

class _call_before(object): #{{{
    def __init__(self, cleanlist, have_slotfunc): #{{{
        self.cleanlist = cleanlist
    # End def #}}}
    def __call__(self, sig, cw, func, ret, args, kwargs): #{{{
        callfunc = None
        for bfunc, t in self.cleanlist('before'):
            if not callfunc:
                callfunc = sig.caller
            callfunc(sig, bfunc, 'before', False, None, *args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}

class _call_after(object): #{{{
    def __init__(self, cleanlist, have_slotfunc): #{{{
        self.cleanlist = cleanlist
    # End def #}}}
    def __call__(self, sig, cw, func, ret, args, kwargs): #{{{
        callfunc = None
        for afunc, t in self.cleanlist('after'):
            if not callfunc:
                callfunc = sig.caller
            callfunc(sig, afunc, 'after', False, None, *args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}


def _update_connections(n): #{{{
    return (n, (connect_func, disconnect_func))
# End def #}}}

def _find_cond_func(s, ln, sl, f, i): #{{{
    return True
# End def #}}}

class _cleanlist_iter(object): #{{{
    def __init__(self, sig, l): #{{{
        self.sig = sig
        self.name = l
        if not hasattr(sig, '_funclist'):
            self.vals = (0, 1)
        else:
            self.funclist = l = sig._funclist[l]
            # (llen, i)
            self.vals = (len(l), 0)
    # End def #}}}

    def __iter__(self): #{{{
        return self
    # End def #}}}

    def next(self): #{{{
        llen, i = self.vals
        if i < llen:
            l = self.funclist
            func = l[i]
            if func.isdead:
                del l[i]
                self.vals = (llen - 1, i)
                return self.next()
            else:
                self.vals = (llen, i+1)
                return (func, i)
        else:
            raise StopIteration
    # End def #}}}
# End class #}}}

class _wrapfunc(object): #{{{
    def __init__(self, sig, func, after, before): #{{{
        self.sig = sig
        self.func = func
        self.after = after
        self.before = before
    # End def #}}}
    def __call__(self, s, *args, **kwargs): #{{{
        ret, func = None, self.func
        sig, after, before = self.sig, self.after, self.before
        for name, cfunc in before():
            ret = cfunc(sig, s, func, ret, args, kwargs)
        ret = func(*args, **kwargs)
        for name, cfunc in after():
            ret = cfunc(sig, s, func, ret, args, kwargs)
        return ret
    # End def #}}}
# End class #}}}

class _wrapfactory(object): #{{{
    def __init__(self, sig): #{{{
        self.sig = sig
    # End def #}}}

    def __call__(self, func): #{{{
        sig = self.sig
        callfunclist = sig._call_funclist
        before = callfunclist['before'].iteritems
        after = callfunclist['after'].iteritems
        return _wrapfunc(sig, func, after, before)
    # End def #}}}
# End class #}}}

# ==================================================================================
# Signal
# ==================================================================================
# Reload function list -- odict listname/func
# Function lists -- dict listname/func list
# Call function list -- odict listname/func
# Connections function list -- odict listname/(cfunc, dfunc) 2-tuple
# Options -- dict option name/value
class _BaseSignal(object): #{{{
    __slots__ = ('__weakref__', '_func', '__name__', '_funclist',
                    '_call_funclist', '_connections', '_vars')
    def __init__(self, signal, **kwargs): #{{{
        if not iscallable(signal):
            raise TypeError("Argument must be callable.")
        expected = ('weak', 'active', 'activate_on_call')
        unexpected = []
        ueapp = unexpected.append
        for kw in kwargs:
            if kw not in expected:
                ueapp(kw)
#        unexpected = [kw for kw in kwargs if kw not in expected]
        if unexpected:
            raise ValueError("Detected unexpected arguments: %s" %', '.join(unexpected))
        weak = kwargs.get('weak', True)
        self._func = CallableWrapper(signal, weak=weak)
        self.__name__ = self._func.__name__
        funclist = self._funclist = dict()
        conn = self._connections = dict()
#        call_funclist = self._call_funclist = dict((n, odict()) for n in ('after', 'replace', 'around', 'before'))
        self._call_funclist = call_funclist = dict(map(_mk_call_funclist, ('after', 'replace', 'around', 'before')))
        self._vars = getattr(self, '_vars', dict())
        self._vars.update(active=kwargs.get('active', True),
                callactivate=kwargs.get('activate_on_call', False), caller=callfunc)

        # Initialize values of function lists
        self._init_funclist(funclist)
        self._init_calls(call_funclist)
        self._init_connections(conn)
    # End def #}}}

    def _init_funclist_names(self): #{{{
#        yield 'before'
#        yield 'after'
        return iter(('before', 'after'))
    # End def #}}}

    def _init_funclist(self, funclist): #{{{
        init = self._init_funclist_names()
#        funclist.update((name, []) for name in init)
        funclist.update(map(_update_funclist, init))
    # End def #}}}

    def _init_calls(self, call_funclist): #{{{
        cleanlist, funclist = self._cleanlist, self._funclist
#        def slot_is_empty(name): return bool(funclist[name])
        slot_is_empty = _slot_is_empty(funclist)
        for cftype in ('before', 'replace', 'around', 'after'):
            call_funclist[cftype].update(getattr(self, '_init_calls_%s' %cftype)(cleanlist, slot_is_empty).iteritems())
    # End def #}}}

    def _init_calls_before(self, cleanlist, have_slotfunc): #{{{
#        def call_before(self, cw, func, ret, args, kwargs): #{{{
#            callfunc = None
#            for bfunc, t in cleanlist('before'):
#                if not callfunc:
#                    callfunc = self.caller
#                callfunc(self, bfunc, 'before', False, None, *args, **kwargs)
#            return ret
#        # End def #}}}
        return odict(before=_call_before(cleanlist, have_slotfunc))
    # End def #}}}

    def _init_calls_replace(self, *args): #{{{
        return odict()
    # End def #}}}

    def _init_calls_around(self, cleanlist, have_slotfunc): #{{{
        return odict()
    # End def #}}}

    def _init_calls_after(self, cleanlist, have_slotfunc): #{{{
#        def call_after(self, cw, func, ret, args, kwargs): #{{{
#            callfunc = None
#            for afunc, t in cleanlist('after'):
#                if not callfunc:
#                    callfunc = self.caller
#                callfunc(self, afunc, 'after', False, None, *args, **kwargs)
#            return ret
#        # End def #}}}
        return odict(after=_call_after(cleanlist, have_slotfunc))
    # End def #}}}

    def _init_default_connections(self): #{{{
        init = ('after', 'before')
        return iter(init)
#        for n in init:
#            yield n
    # End def #}}}

    def _init_connections(self, connections): #{{{
        init = self._init_default_connections()
#        connections.update((n, (connect_func, disconnect_func)) for n in init)
        connections.update(map(_update_connections, init))
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        if not self.valid:
            warn('Calling an invalid signal', RuntimeWarning, stacklevel=2)
            return
        if self.activate_on_call:
            self.active = True
        return self._func(*args, **kwargs)
    # End def #}}}

    def _cleanlist(self, l): #{{{
        # If everything is being deleted e.g. program termination
        # don't do anything and just return
#        if not hasattr(self, '_funclist'):
#            return
#        l = self._funclist[l]
#        llen, i = len(l), 0
#        while i < llen:
#            func = l[i]
#            if func.isdead:
#                del l[i]
#                llen -= 1
#            else:
#                yield func, i
#                i += 1
        return iter(_cleanlist_iter(self, l))
    # End def #}}}

    def _generate_wrapfactory(self): #{{{
        return _wrapfactory(self)
#        def do_wrap(func): #{{{
#            callfunclist = self._call_funclist
#            before = callfunclist['before'].iteritems
#            after = callfunclist['after'].iteritems
#            def newcall(s, *args, **kwargs): #{{{
#                ret = None
#                for name, cfunc in before():
#                    ret = cfunc(self, s, func, ret, args, kwargs)
#                ret = func(*args, **kwargs)
#                for name, cfunc in after():
#                    ret = cfunc(self, s, func, ret, args, kwargs)
#                return ret
#            # End def #}}}
#            return newcall
#        # End def #}}}
#        return do_wrap
    # End def #}}}

    def reload(self): #{{{
        sfunc = self._func
        if sfunc.isdead:
            return
        sfunc.unwrap()
        sfunc_wrap = sfunc.wrap
        callfunclist = self._call_funclist
        for ctype in ('replace', 'around'):
            for name, citer in callfunclist[ctype].iteritems():
                for cfunc in citer(self):
                    sfunc_wrap(cfunc)
        do_wrap = self._generate_wrapfactory()
        sfunc_wrap(do_wrap)
        self._vars['active'] = True
    # End def #}}}

    def _find_cond(self, **kw): #{{{
        return _find_cond_func
    # End def #}}}

    def _find(self, func, siglistseq=None, **kw): #{{{
        temp_siglistseq = self._funclist
        if siglistseq not in temp_siglistseq:
            siglistseq = temp_siglistseq
        else:
            siglistseq = {siglistseq: temp_siglistseq[siglistseq]}
        foundindex = foundlist = None
        fid, cleanlist = cid(func), self._cleanlist
        fcond = self._find_cond(**kw)
        for listname, siglist in siglistseq.iteritems():
            for f, index in cleanlist(listname):
                if f.cid == fid:
                    if not fcond(self, listname, siglist, f, index):
                        continue
                    foundindex, foundlist = index, siglist
                    break
            else:
                continue
            break
        if foundindex is not None:
            return foundindex, foundlist
        return None
    # End def #}}}

    def connect(self, *after, **other_slots): #{{{
        activate = self.activate_on_call
        self.activate_on_call = False
        osg = other_slots.get
        other_slots['after'] = list(after) + list(osg('after', []))

        for name, (cfunc, _) in self._connections.iteritems():
            cfunc(self, name, other_slots)

        self.activate_on_call = activate
        if self.active:
            self.reload()
    # End def #}}}

    def disconnect(self, *after, **other_slots): #{{{
        osg = other_slots.get
        if after or 'after' in other_slots:
            other_slots['after'] = list(after) + list(osg('after', []))
#        no_slots = not any(osg(name, None) for name in self._funclist)
        no_slots = not any(map(osg, self._funclist))
        if 'deleteall' not in other_slots:
            other_slots['deleteall'] = no_slots

        for name, (_, dfunc) in self._connections.iteritems():
            dfunc(self, name, other_slots)

        if self.active:
            self.reload()
    # End def #}}}

#    def slot(self, name): #{{{
#        return (f for f, _ in self._cleanlist(name))
#    # End def #}}}

    def _setactive(self, v): #{{{
        opt = self._vars
        orig = opt['active']
        v = bool(v)
        opt['active'] = v
        if orig and not v:
            self._func.unwrap()
        elif not orig and v:
            self.reload()
    # End def #}}}

    def _setcallactivate(self, v): #{{{
        self._vars['callactivate'] = bool(v)
    # End def #}}}

    def _setcaller(self, c): #{{{
        if c is None:
            return
        elif not iscallable(c):
            raise TypeError('caller property must be a valid callable object')
        self._vars['caller'] = CallableWrapper(c, weak=False)
    # End def #}}}

    # Properties #{{{
#    func = property(lambda s: s._func)
#    valid = property(lambda s: not s._func.isdead)
#    connected = property(lambda s: any(s._funclist.itervalues()))
#    active = property(lambda s: s._vars['active'], lambda s, v: s._setactive(v))
#    activate_on_call = property(lambda s: s._vars['callactivate'], lambda s, v: s._setcallactivate(v))
#    caller = property(lambda s: s._vars['caller'], lambda s, c: s._setcaller(c))
#    original = property(lambda s: s._func.original)
    # End properties #}}}
# End class #}}}

def getsignal(obj): #{{{
    if isinstance(obj, BaseSignal):
        return obj
    sig = getattr(obj, 'signal', None)
    if sig:
        sig = getsignal(sig)
    elif ismethod(obj):
        sig = getsignal(obj.im_func)
    return sig
# End def #}}}
