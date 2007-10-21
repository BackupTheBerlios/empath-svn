# Module: aossi.signals
# File: signals.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from types import GeneratorType

# package imports
#from aossi.core import *
from aossi.core import BaseSignal, cid, callfunc, mkcallback, connect_func, disconnect_func, getsignal
from aossi.cwrapper import CallableWrapper, cid
from aossi.util import property_, iscallable, ChooseCallable, ChoiceObject
from aossi.util.introspect import mro
from aossi.util.odict import odict

# pyrex imports
cimport signals
from signals cimport SignalExtension
#cimport signals
#from signals cimport _mkcaller, _choice_clean_iter, make_choice_helpers

#__all__ = ('SignalExtension', 'AroundExtension', 'OnReturnExtension', 'StreamExtension',
#            'ReplaceExtension', 'ChooseExtension', 'DefaultExtension', 'Signal')
__all__ = ('SignalExtension', 'AroundExtension', 'OnReturnExtension', 'StreamExtension',
            'ReplaceExtension')
# ==================================================================================
# General Helpers
# ==================================================================================
cdef class _mkcaller: #{{{
    cdef object args, name, pass_ret, ret
    def __init__(self, name, pass_ret, ret, args): #{{{
        self.args = args
        self.name = name
        self.pass_ret = pass_ret
        self.ret = ret
    # End def #}}}

    def __call__(self, chooser, *args, **kwargs): #{{{
        sig, callfunc = self.args[:2]
        return callfunc(sig, chooser, self.name, self.pass_ret, self.ret, *args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class _choice_clean_iter: #{{{
    cdef object iter
    def __init__(self, iter): #{{{
        self.iter = iter
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        i, t = self.iter.next()
        return (i.choosefunc, i.callable)
#            gen = ((i.choosefunc, i.callable) for i, t in cleanlist(chooselist))
    # End def #}}}
# End class #}}}

cdef class make_choice_helpers: #{{{
    cdef object args
    def __init__(self, sig, callfunc, cleanlist): #{{{
        self.args = (sig, callfunc, cleanlist)
    # End def #}}}

    def _mkcaller(self, name, pass_ret, ret): #{{{
        return _mkcaller(name, pass_ret, ret, self.args)
    # End def #}}}

    def choice(self, sig, chooselist, chooser, chooserpolicy, func, pass_ret, ret, *args, **kwargs): #{{{
        _, callfunc, cleanlist = self.args
        choice = None
        if chooselist:
            chooserfunc = getattr(sig, chooser)
            if not chooserfunc or chooserfunc.isdead:
                setattr(sig, chooser, ChooseCallable)
                chooserfunc = getattr(sig, chooser)
            gen = _choice_clean_iter(cleanlist(chooselist))
            choice = chooserfunc(gen, chooserpolicy, func, self._mkcaller('chooser', pass_ret, ret), *args, **kwargs)
        if not choice:
            if chooser == 'chooser':
                choice = [func]
            else:
                choice = []
        return choice
    # End def #}}}

    def callchoice(self, sig, val, func_choice, pass_ret, ret, *args, **kwargs): #{{{
        _, callfunc, cleanlist = self.args
        oldret = ret
        for f in func_choice:
            if pass_ret:
                ret = callfunc(sig, f, 'conditional return', True, oldret, *args, **kwargs)
            elif f is val:
                ret = f(*args, **kwargs)
            else:
                ret = callfunc(sig, f, 'conditional', False, None, *args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}

# ==================================================================================
# Connect Helpers
# ==================================================================================
def connect_choosefunc(self, listname, slots): #{{{
    cleanlist, vals = self._cleanlist, slots.get(listname, ())
    clist, cleanfunc, test_store = self._funclist[listname], mkcallback(listname, cleanlist), []
    weak = bool(slots.get('weak', self.func.isweak))
    wcf = bool(slots.get('weakcondf', weak))
    uniq = bool(slots.get('unique', True))
    for tup in vals:
        cond, f = tup
        if not iscallable(cond) or not iscallable(f):
            raise TypeError('Detected non-callable element of \'%s\' slots' %listname)
        found = self._find(f, listname, chooser=cond)
        if found and uniq:
            continue
        else:
            cfunc = CallableWrapper(cond, cleanfunc, weak=wcf)
            func = CallableWrapper(f, cleanfunc, weak=weak)
            test_store.append((ChoiceObject(cfunc, func)))
    if test_store:
        clist.extend(test_store)
# End def #}}}

def disconnect_choosefunc(self, listname, slots): #{{{
    l, vals = self._funclist[listname], slots.get(listname, ())
    delall = bool(slots.get('deleteall', False))
    if delall and (not (len(slots)-1) or listname in slots):
        while l:
            l.pop()
        return
    for tup in slots.get(listname, ()):
        f, cond = tup, None
        if not iscallable(f):
            cond, f = tup
        found = self._find(f, listname, chooser=None)
        if found:
            del l[found[0]]
# End def #}}}
# ==================================================================================
# SignalExtension
# ==================================================================================
#cdef class SignalExtension: #{{{
#    pass
## End class #}}}

cdef class _super_names_iter: #{{{
    cdef object iter, seq, ind, seqlen
    def __init__(self, cls, inst, seq, funcname): #{{{
        self.iter = getattr(super(cls, inst), funcname)()
        self.seq = seq
        self.seqlen = len(seq)
        self.ind = 0
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        iter = self.iter
        if iter:
            try:
                return self.iter.next()
            except StopIteration:
                iter = None
        if iter == None:
            ind = self.ind
            if ind == self.seqlen:
                raise StopIteration
            self.ind = ind + 1
            return self.seq[ind]
    # End def #}}}
# End class #}}}
# ==================================================================================
# AroundExtension
# ==================================================================================

cdef class _call_around_iter: #{{{
    cdef object iter
    def __init__(self, iter): #{{{
        self.iter = iter
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        arfunc, _ = self.iter.next()
        return arfunc
    # End def #}}}
# End def #}}}

cdef class _call_around: #{{{
    cdef object cleanlist
    def __init__(self, cleanlist): #{{{
        self.cleanlist = cleanlist
    # End def #}}}
    def __call__(self, sig): #{{{
        return _call_around_iter(self.cleanlist('around'))
    # End def #}}}
# End class #}}}

cdef class AroundExtension(SignalExtension): #{{{
    def _init_funclist_names(self): #{{{
        return _super_names_iter(AroundExtension, self, ['around'], '_init_funclist_names')
    # End def #}}}

    def _init_calls_around(self, cleanlist, have_slotfunc): #{{{
        call_around = _call_around(cleanlist)
        ret = super(AroundExtension, self)._init_calls_around(cleanlist, have_slotfunc)
        ret['around'] = call_around
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        return _super_names_iter(AroundExtension, self, ['around'], '_init_default_connections')
    # End def #}}}
# End class #}}}
# ==================================================================================
# OnReturnExtension
# ==================================================================================
cdef class _call_onreturn: #{{{
    cdef object cleanlist
    def __init__(self, cleanlist): #{{{
        self.cleanlist = cleanlist
    # End def #}}}
    def __call__(self, sig, cw, func, ret, args, kwargs): #{{{
        callfunc = None
        for rfunc, t in self.cleanlist('onreturn'):
            if not callfunc:
                callfunc = sig.caller
            callfunc(sig, rfunc, 'onreturn', True, ret, *args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}

cdef class OnReturnExtension(SignalExtension): #{{{
    def _init_funclist_names(self): #{{{
        return _super_names_iter(OnReturnExtension, self, ['onreturn'], '_init_funclist_names')
    # End def #}}}

    def _init_calls_after(self, cleanlist, have_slotfunc): #{{{
        call_onreturn = _call_onreturn(cleanlist)
        ret = super(OnReturnExtension, self)._init_calls_after(cleanlist, have_slotfunc)
        ret['onreturn'] = call_onreturn
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        return _super_names_iter(OnReturnExtension, self, ['onreturn'], '_init_default_connections')
    # End def #}}}
# End class #}}}
# ==================================================================================
# StreamExtension
# ==================================================================================
cdef class _streamin_wrap_func: #{{{
    cdef object sig, cleanlist, have_slotfunc, func
    def __init__(self, func, sig, cleanlist, have_slotfunc): #{{{
        self.sig = sig
        self.cleanlist = cleanlist
        self.have_slotfunc = have_slotfunc
        self.func = func
    # End def #}}}

    def __call__(self, cw, *args, **kwargs): #{{{
        signal = self.sig
        if self.have_slotfunc('streamin'):
            sig, signame = None, cw.__name__
            if args:
                for cls in mro(args[0].__class__):
                    sig = getsignal(getattr(cls, signame, None))
                    if sig and cw is sig.func:
                        break
                else:
                    sig = None
            if sig:
                args = (args[0], list(args[1:]), kwargs)
            else:
                args = (list(args), kwargs)
            callfunc = signal.caller
            for sfunc, t in self.cleanlist('streamin'):
                callfunc(signal, sfunc, 'streamin', False, None, *args)
            if sig:
                args, kwargs = [args[0]] + args[1], args[2]
            else:
                args, kwargs = args
        return self.func(*args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class _streamin_wrap: #{{{
    cdef object args
    def __init__(self, sig, cleanlist, have_slotfunc): #{{{
        self.args = (sig, cleanlist, have_slotfunc)
    # End def #}}}
    def __call__(self, func): #{{{
        return _streamin_wrap_func(func, *self.args)
    # End def #}}}
# End class #}}}

cdef class _call_streamin: #{{{
    cdef object args
    def __init__(self, cleanlist, have_slotfunc): #{{{
        self.args = (cleanlist, have_slotfunc)
    # End def #}}}
    def __call__(self, sig): #{{{
        return (_streamin_wrap(sig, *self.args),)
    # End def #}}}
# End class #}}}

cdef class _call_stream: #{{{
    cdef object cleanlist
    def __init__(self, cleanlist): #{{{
        self.cleanlist = cleanlist
    # End def #}}}
    def __call__(self, sig, cw, func, ret, args, kwargs): #{{{
        callfunc = None
        for sfunc, t in self.cleanlist('stream'):
            if not callfunc:
                callfunc = sig.caller
            ret = callfunc(sig, sfunc, 'stream', True, ret, *args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}
class StreamExtension(SignalExtension): #{{{
    __slots__ = ()
    def _init_funclist_names(self): #{{{
        return _super_names_iter(StreamExtension, self, ['streamin', 'stream'], '_init_funclist_names')
    # End def #}}}

    def _init_calls_around(self, cleanlist, have_slotfunc): #{{{
        call_streamin = _call_streamin(cleanlist, have_slotfunc)
        sup = super(StreamExtension, self)._init_calls_around(cleanlist, have_slotfunc)
        ret = odict(sup.iteritems())
        ret['streamin'] = call_streamin
        return ret
    # End def #}}}

    def _init_calls_after(self, cleanlist, have_slotfunc): #{{{
        call_stream = _call_stream(cleanlist)
        sup = super(StreamExtension, self)._init_calls_after(cleanlist, have_slotfunc)
        ret = odict()
        ret['stream'] = call_stream
        ret.update(sup.iteritems())
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        return _super_names_iter(StreamExtension, self, ['streamin', 'stream'], '_init_default_connections')
    # End def #}}}
# End class #}}}
# ==================================================================================
# ReplaceExtension
# ==================================================================================
cdef class _replace_newcall: #{{{
    cdef object args, func
    def __init__(self, func, sig, cleanlist, have_slotfunc): #{{{
        self.args = sig, cleanlist, have_slotfunc
        self.func = func
    # End def #}}}
    def __call__(self, cw, *args, **kwargs): #{{{
        sig, cleanlist, have_slotfunc = self.args
        callfunc, rfunc, ret = sig.caller, None, None
        for sfunc, t in cleanlist('replace'):
            rfunc = sfunc
        if rfunc:
            ret = callfunc(sig, rfunc, 'replace', False, ret, *args, **kwargs)
        else:
            ret = self.func(*args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}
cdef class _replace_do_wrap: #{{{
    cdef object args
    def __init__(self, sig, cleanlist, have_slotfunc): #{{{
        self.args = sig, cleanlist, have_slotfunc
    # End def #}}}
    def __call__(self, func): #{{{
        return _replace_newcall(func, *self.args)
    # End def #}}}
# End class #}}}
cdef class _call_replace: #{{{
    cdef object args
    def __init__(self, cleanlist, have_slotfunc): #{{{
        self.args = cleanlist, have_slotfunc
    # End def #}}}
    def __call__(self, sig): #{{{
        return (_replace_do_wrap(sig, *self.args),)
    # End def #}}}
# End def #}}}
cdef class ReplaceExtension(SignalExtension): #{{{
    def _init_funclist_names(self): #{{{
        return _super_names_iter(ReplaceExtension, self, ['replace'], '_init_funclist_names')
    # End def #}}}

    def _init_calls_replace(self, cleanlist, have_slotfunc): #{{{
        call_replace = _call_replace(cleanlist, have_slotfunc)
        ret = super(ReplaceExtension, self)._init_calls_replace(cleanlist, have_slotfunc)
        ret['replace'] = call_replace
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        return _super_names_iter(ReplaceExtension, self, ['replace'], '_init_default_connections')
    # End def #}}}
# End class #}}}
# ==================================================================================
# ChooseExtension
# ==================================================================================
def _update_connections(name): #{{{
    return (name, (connect_choosefunc, disconnect_choosefunc))
# End def #}}}

cdef class _call_choose_newcall: #{{{
    cdef object args, func, choice, callchoice
    def __init__(self, func, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.func = func
        self.args = sig, cleanlist, have_slotfunc
        self.choice = choice
        self.callchoice = callchoice
    # End def #}}}
    def __call__(self, cw, *args, **kwargs): #{{{
        sig, cleanlist, have_slotfunc = self.args
        func = self.func
        if not have_slotfunc('choose'):
            return func(*args, **kwargs)
        func_choice = self.choice(sig, 'choose', 'chooser', sig.chooser_policy, func, False, None, *args, **kwargs)
        return self.callchoice(sig, func, func_choice, False, None, *args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class _call_choose_do_wrap: #{{{
    cdef object args
    def __init__(self, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.args = sig, cleanlist, have_slotfunc, choice, callchoice
    # End def #}}}
    def __call__(self, func): #{{{
        return _call_choose_newcall(func, *self.args)
    # End def #}}}
# End class #}}}

cdef class _call_choose: #{{{
    cdef object args
    def __init__(self, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.args = cleanlist, have_slotfunc, choice, callchoice
    # End def #}}}
    def __call__(self, sig): #{{{
        return (_call_choose_do_wrap(sig, *self.args),)
    # End def #}}}
# End class #}}}

cdef class _call_choosereturn_newcall: #{{{
    cdef func, args
    def __init__(self, func, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.func = func
        self.args = sig, cleanlist, have_slotfunc, choice, callchoice
    # End def #}}}
    def __call__(self, cw, *args, **kwargs): #{{{
        func = self.func
        sig, cleanlist, have_slotfunc, choice, callchoice = self.args
        ret = func(*args, **kwargs)
        if not have_slotfunc('choosereturn'):
            return ret
        ret_choice = choice(sig, 'choosereturn', 'return_chooser', sig.return_chooser_policy, 
                func, True, ret, *args, **kwargs)
        return callchoice(sig, func, ret_choice, True, ret, *args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class _call_choosereturn_do_wrap: #{{{
    cdef object args
    def __init__(self, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.args = sig, cleanlist, have_slotfunc, choice, callchoice
    # End def #}}}
    def __call__(self, func): #{{{
        return _call_choosereturn_newcall(func, *self.args)
    # End def #}}}
# End class #}}}

cdef class _call_choosereturn: #{{{
    cdef object args
    def __init__(self, cleanlist, have_slotfuncm, choice, callchoice): #{{{
        self.args = cleanlist, have_slotfuncm, choice, callchoice
    # End def #}}}
    def __call__(self, sig): #{{{
        return (_call_choosereturn_do_wrap(sig, *self.args),)
    # End def #}}}
# End class #}}}

cdef class _call_chooseyield_mk_gen_iter: #{{{
    cdef object args, iter, input
    def __init__(self, iter, args, kwargs, func, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.iter = iter
        self.args = func, sig, cleanlist, have_slotfunc, choice, callchoice
        self.input = (args, kwargs)
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        args, kwargs = self.input
        func, sig, cleanlist, have_slotfunc, choice, callchoice = self.args
        ret = self.iter.next()
        ret_choice = choice(sig, 'chooseyield', 'yield_chooser', sig.yield_chooser_policy, 
                func, True, ret, *args, **kwargs)
        return callchoice(sig, func, ret_choice, True, ret, ret)
    # End def #}}}
# End class #}}}

cdef class _call_chooseyield_mk_gen: #{{{
    cdef object args
    def __init__(self, func, args, kwargs, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.args = args, kwargs, func, sig, cleanlist, have_slotfunc, choice, callchoice
    # End def #}}}
    def __call__(self, gen): #{{{
        return _call_chooseyield_mk_gen_iter(gen, *self.args)
    # End def #}}}
# End class #}}}

cdef class _call_chooseyield_newcall: #{{{
    cdef func, args
    def __init__(self, func, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.func = func
        self.args = sig, cleanlist, have_slotfunc, choice, callchoice
    # End def #}}}
    def __call__(self, cw, *args, **kwargs): #{{{
        func = self.func
        sig, cleanlist, have_slotfunc, choice, callchoice = self.args
        gen = func(*args, **kwargs)
        if not isinstance(gen, GeneratorType) or not have_slotfunc('chooseyield'):
            return gen
        return _call_chooseyield_mk_gen(func, args, kwargs, *self.args)(gen)
    # End def #}}}
# End class #}}}

cdef class _call_chooseyield_do_wrap: #{{{
    cdef object args
    def __init__(self, sig, cleanlist, have_slotfunc, choice, callchoice): #{{{
        self.args = sig, cleanlist, have_slotfunc, choice, callchoice
    # End def #}}}
    def __call__(self, func): #{{{
        return _call_chooseyield_newcall(func, *self.args)
    # End def #}}}
# End class #}}}

cdef class _call_chooseyield: #{{{
    cdef object args
    def __init__(self, cleanlist, have_slotfuncm, choice, callchoice): #{{{
        self.args = cleanlist, have_slotfuncm, choice, callchoice
    # End def #}}}
    def __call__(self, sig): #{{{
        return (_call_chooseyield_do_wrap(sig, *self.args),)
    # End def #}}}
# End class #}}}

cdef class _find_cond_fcond: #{{{
    cdef object args
    def __init__(self, choosercid, super_fcond): #{{{
        self.args = choosercid, super_fcond
    # End def #}}}
    def __call__(self, sig, listname, siglist, f, index): #{{{
        choosercid, super_fcond = self.args
        if not super_fcond(sig, listname, siglist, f, index):
            return False
        if choosercid and listname in ('choose', 'choosereturn', 'chooseyield'):
            if choosercid != f.choosefunc.cid:
                return False
        return True
    # End def #}}}
# End class #}}}

cdef class ChooseExtension(SignalExtension): #{{{
    def __init__(self, signal, **kwargs): #{{{
        self._vars = getattr(self, '_vars', dict())
        self._vars.update(choosepolicy=None, chooseretpolicy=None, chooseyieldpolicy=None)
        super(ChooseExtension, self).__init__(signal, **kwargs)
        self.chooser = ChooseCallable
        self.return_chooser = ChooseCallable
        self.yield_chooser = ChooseCallable
    # End def #}}}

    def _init_funclist_names(self): #{{{
        return _super_names_iter(ChooseExtension, self, ['choose', 'choosereturn', 'chooseyield'], '_init_default_connections')
    # End def #}}}

    def _init_connections(self, connections): #{{{
        super(ChooseExtension, self)._init_connections(connections)
        init = ('choose', 'choosereturn', 'chooseyield')
#        connections.update((n, (connect_choosefunc, disconnect_choosefunc)) for n in init)
        connections.update(map(_update_connections, init))
    # End def #}}}

    def _init_calls_replace(self, cleanlist, have_slotfunc): #{{{
        helpers = make_choice_helpers(self, callfunc, cleanlist)
        choice, callchoice = helpers.choice, helpers.callchoice
        call_choose = _call_choose(cleanlist, have_slotfunc, choice, callchoice)
        call_choosereturn = _call_choosereturn(cleanlist, have_slotfunc, choice, callchoice)
        call_chooseyield = _call_chooseyield(cleanlist, have_slotfunc, choice, callchoice)
        ret = super(ChooseExtension, self)._init_calls_replace(cleanlist, have_slotfunc)
        ret['choose'] = call_choose
        ret['choosereturn'] = call_choosereturn
        ret['chooseyield'] = call_chooseyield
        return ret
    # End def #}}}

    def _find_cond(self, **kw): #{{{
        chooser = kw.pop('chooser', None)
        choosercid = None
        if iscallable(chooser):
            choosercid = cid(chooser)
        super_fcond = super(ChooseExtension, self)._find_cond(**kw)
        return _find_cond_fcond(choosercid, super_fcond)
    # End def #}}}

    def _setpolicy(self, name, p): #{{{
        self._vars[name] = p
    # End def #}}}

    def _setchooser(self, name, c): #{{{
        if c is None:
            return
        elif not iscallable(c):
            raise TypeError('chooser property must be a valid callable object')
        self._vars[name] = CallableWrapper(c, weak=False)
    # End def #}}}

    # Properties #{{{
    property chooser_policy:
        def __get__(self): #{{{
            return self._vars['choosepolicy']
        # End def #}}}
        def __set__(self, p): #{{{
            self._setpolicy('choosepolicy', p)
        # End def #}}}
    property return_chooser_policy:
        def __get__(self): #{{{
            return self._vars['chooseretpolicy']
        # End def #}}}
        def __set__(self, p): #{{{
            self._setpolicy('chooseretpolicy', p)
        # End def #}}}
    property yield_chooser_policy:
        def __get__(self): #{{{
            return self._vars['chooseyieldpolicy']
        # End def #}}}
        def __set__(self, p): #{{{
            self._setpolicy('chooseyieldpolicy', p)
        # End def #}}}
    property chooser:
        def __get__(self): #{{{
            return self._vars['chooser']
        # End def #}}}
        def __set__(self, c): #{{{
            self._setchooser('chooser', c)
        # End def #}}}
    property return_chooser:
        def __get__(self): #{{{
            return self._vars['return_chooser']
        # End def #}}}
        def __set__(self, c): #{{{
            self._setchooser('return_chooser', c)
        # End def #}}}
    property yield_chooser:
        def __get__(self): #{{{
            return self._vars['yield_chooser']
        # End def #}}}
        def __set__(self, c): #{{{
            self._setchooser('yield_chooser', c)
        # End def #}}}
    # End properties #}}}
# End class #}}}
# ==================================================================================
# Signal
# ==================================================================================
#class DefaultExtension(OnReturnExtension, StreamExtension, ChooseExtension, ReplaceExtension, AroundExtension): #{{{
#    __slots__ = ()
## End class #}}}

#class Signal(DefaultExtension, BaseSignal): #{{{
#    __slots__ = ()
## End class #}}}
# ==================================================================================
#
# ==================================================================================
