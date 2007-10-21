# Module: aossi.core
# File: core.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from warnings import warn

from aossi.cwrapper import CallableWrapper, cid
from aossi.util import iscallable, ChooseCallable, ChoiceObject

from aossi.util.odict import odict

__all__ = ('BaseSignal', 'callfunc', 'mkcallback', 'connect_func', 'disconnect_func')
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
def mkcallback(name, cleanlist): #{{{
    def callback(obj):
        for ret in cleanlist(name): pass
    return callback
# End def #}}}

def connect_func(self, listname, slots): #{{{
    weak = bool(slots.get('weak', True))
    uniq = bool(slots.get('unique', True))
    l, vals = self._funclist[listname], slots.get(listname, ())
    cleanlist, test_store = self._cleanlist, []
    cleanfunc = mkcallback(listname, cleanlist)
    for f in vals:
        if not iscallable(f):
            raise TypeError('Detected non-callable element of \'%s\' slots' %listname)
        c = CallableWrapper(f, cleanfunc, weak=weak)
        found = self._find(f, listname)
        if found and uniq:
            continue
        test_store.append(c)
    if test_store:
        l.extend(test_store)
# End def #}}}

def disconnect_func(self, listname, slots): #{{{
    l, vals = self._funclist[listname], slots.get(listname, ())
    delall = bool(slots.get('deleteall', False))
    if delall and not vals:
        while l:
            l.pop()
        return
    for f in vals:
        found = self._find(f, listname)
        if found:
            del l[found[0]]
# End def #}}}
# ==================================================================================
# Signal
# ==================================================================================
# Reload function list -- odict listname/func
# Function lists -- dict listname/func list
# Call function list -- odict listname/func
# Connections function list -- odict listname/(cfunc, dfunc) 2-tuple
# Options -- dict option name/value
class BaseSignal(object): #{{{
    __slots__ = ('__weakref__', '_func', '__name__', '_funclist',
                    '_call_funclist', '_connections', '_vars')
    def __init__(self, signal, **kwargs): #{{{
        if not iscallable(signal):
            raise TypeError("Argument must be callable.")
        expected = ('weak', 'active', 'activate_on_call')
        if any(kw for kw in kwargs if kw not in expected):
            raise ValueError("Detected unexpected arguments: %s" %', '.join([found]))
        weak = kwargs.get('weak', True)
        self._func = CallableWrapper(signal, weak=weak)
        self.__name__ = self._func.__name__
        funclist = self._funclist = dict()
        conn = self._connections = dict()
        call_funclist = self._call_funclist = dict((n, odict()) for n in ('after', 'replace', 'around', 'before'))
        self._vars = getattr(self, '_vars', dict())
        self._vars.update(active=kwargs.get('active', True),
                callactivate=kwargs.get('activate_on_call', False), caller=callfunc)

        # Initialize values of function lists
        self._init_functions(funclist)
        self._init_calls(call_funclist)
        self._init_connections(conn)
    # End def #}}}

    def _init_functions(self, funclist): #{{{
        init = ('before', 'after')
        funclist.update((name, []) for name in init)
    # End def #}}}

    def _init_calls(self, call_funclist): #{{{
        cleanlist = self._cleanlist
        ldict, j = locals(), '_'.join
        mkfunc = lambda n: (n, ldict[j(['call', n])])
        call_funclist['before'].update(self._init_calls_before(cleanlist).iteritems())
        call_funclist['replace'].update(self._init_calls_replace(cleanlist).iteritems())
        call_funclist['around'].update(self._init_calls_around(cleanlist).iteritems())
        call_funclist['after'].update(self._init_calls_after(cleanlist).iteritems())
    # End def #}}}

    def _init_calls_before(self, cleanlist): #{{{
        def call_before(self, cw, func, ret, args, kwargs): #{{{
            callfunc = self.caller
            for bfunc, t in cleanlist('before'):
                callfunc(self, bfunc, 'before', False, None, *args, **kwargs)
            return ret
        # End def #}}}
        return odict(before=call_before)
    # End def #}}}

    def _init_calls_replace(self, cleanlist): #{{{
        return odict()
    # End def #}}}

    def _init_calls_around(self, cleanlist): #{{{
        return odict()
    # End def #}}}

    def _init_calls_after(self, cleanlist): #{{{
        def call_after(self, cw, func, ret, args, kwargs): #{{{
            callfunc = self.caller
            for afunc, t in cleanlist('after'):
                callfunc(self, afunc, 'after', False, None, *args, **kwargs)
            return ret
        # End def #}}}
        return odict(after=call_after)
    # End def #}}}

    def _init_connections(self, connections): #{{{
        init = ('after', 'before')
        connections.update((n, (connect_func, disconnect_func)) for n in init)
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
        l = self._funclist[l]
        llen = l.__len__()
        i = 0
        while i < llen:
            func = l[i]
            if func.isdead:
                del l[i]
                llen -= 1
            else:
                yield func, i
                i += 1
    # End def #}}}

    def _generate_wrapfactory(self): #{{{
        def do_wrap(func): #{{{
            def newcall(s, *args, **kwargs): #{{{
                ret = None
                callfunclist = self._call_funclist
                for name, cfunc in callfunclist['before'].iteritems():
                    ret = cfunc(self, s, func, ret, args, kwargs)
                ret = func(*args, **kwargs)
                for name, cfunc in callfunclist['after'].iteritems():
                    ret = cfunc(self, s, func, ret, args, kwargs)
                return ret
            # End def #}}}
            return newcall
        # End def #}}}
        return do_wrap
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
        self.active = True
    # End def #}}}

    def _find_cond(self, **kw): #{{{
        return lambda s, ln, sl, f, i: True
    # End def #}}}

    def _find(self, func, siglistseq=None, **kw): #{{{
        temp_siglistseq = self._funclist
        if siglistseq not in temp_siglistseq:
            siglistseq = temp_siglistseq
        else:
            siglistseq = {siglistseq: temp_siglistseq[siglistseq]}
        del temp_siglistseq
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
        other_slots['after'] = list(after) + list(osg('after', []))
        no_slots = not any(osg(name, None) for name in self._funclist)
        other_slots['deleteall'] = no_slots

        for name, (_, dfunc) in self._connections.iteritems():
            dfunc(self, name, other_slots)

        if self.active:
            self.reload()
    # End def #}}}

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
    func = property(lambda s: s._func)
    valid = property(lambda s: not s._func.isdead)
    connected = property(lambda s: any(s._funclist.itervalues()))
    active = property(lambda s: s._vars['active'], lambda s, v: s._setactive(v))
    activate_on_call = property(lambda s: s._vars['callactivate'], lambda s, v: s._setcallactivate(v))
    caller = property(lambda s: s._vars['caller'], lambda s, c: s._setcaller(c))
    original = property(lambda s: s._func.original)
    # End properties #}}}
# End class #}}}
