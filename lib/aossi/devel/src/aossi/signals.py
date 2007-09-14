# Module: aossi.signals
# File: signals.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from types import GeneratorType

# package imports
from aossi.core import *
from aossi.cwrapper import CallableWrapper, cid
from aossi.util import property_, iscallable, ChooseCallable, ChoiceObject
from aossi.util.introspect import mro
from aossi.util.odict import odict

__all__ = ('SignalExtension', 'AroundExtension', 'OnReturnExtension', 'StreamExtension',
            'ReplaceExtension', 'ChooseExtension', 'DefaultExtension', 'Signal')
# ==================================================================================
# General Helpers
# ==================================================================================
def make_choice_helpers(self, callfunc, cleanlist): #{{{
    def mkcaller(name, pass_ret, ret): #{{{
        def ch_caller(chooser, *args, **kwargs):
            return callfunc(self, chooser, name, pass_ret, ret, *args, **kwargs)
        return ch_caller
    # End def #}}}
    def choice(self, chooselist, chooser, chooserpolicy, func, pass_ret, ret, *args, **kwargs): #{{{
        choice = None
        if chooselist:
            chooserfunc = getattr(self, chooser)
            if not chooserfunc or chooserfunc.isdead:
                setattr(self, chooser, ChooseCallable)
                chooserfunc = getattr(self, chooser)
            gen = ((i.choosefunc, i.callable) for i, t in cleanlist(chooselist))
            choice = chooserfunc(gen, chooserpolicy, func, mkcaller('chooser', pass_ret, ret), *args, **kwargs)
        if not choice:
            if chooser == 'chooser':
                choice = [func]
            else:
                choice = []
        return choice
    # End def #}}}
    def callchoice(self, val, func_choice, pass_ret, ret, *args, **kwargs): #{{{
        oldret = ret
        for f in func_choice:
            if pass_ret:
                ret = callfunc(self, f, 'conditional return', True, oldret, *args, **kwargs)
            elif f is val:
                ret = f(*args, **kwargs)
            else:
                ret = callfunc(self, f, 'conditional', False, None, *args, **kwargs)
        return ret
    # End def #}}}
    return choice, callchoice
# End def #}}}

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
class SignalExtension(object): #{{{
    __slots__ = ()
# End class #}}}
# ==================================================================================
# AroundExtension
# ==================================================================================
class AroundExtension(SignalExtension): #{{{
    __slots__ = ()
    def _init_funclist_names(self): #{{{
        for n in super(AroundExtension, self)._init_funclist_names():
            yield n
        yield 'around'
    # End def #}}}

    def _init_calls_around(self, cleanlist): #{{{
        def call_around(self): #{{{
            return (arfunc for arfunc, _ in cleanlist('around'))
        # End def #}}}
        ret = super(AroundExtension, self)._init_calls_around(cleanlist)
        ret['around'] = call_around
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        for n in super(AroundExtension, self)._init_default_connections():
            yield n
        yield 'around'
    # End def #}}}
# End class #}}}
# ==================================================================================
# OnReturnExtension
# ==================================================================================
class OnReturnExtension(SignalExtension): #{{{
    __slots__ = ()
    def _init_funclist_names(self): #{{{
        for n in super(OnReturnExtension, self)._init_funclist_names():
            yield n
        yield 'onreturn'
    # End def #}}}

    def _init_calls_after(self, cleanlist): #{{{
        def call_onreturn(self, cw, func, ret, args, kwargs): #{{{
            callfunc = self.caller
            for rfunc, t in cleanlist('onreturn'):
                callfunc(self, rfunc, 'onreturn', True, ret, *args, **kwargs)
            return ret
        # End def #}}}
        ret = super(OnReturnExtension, self)._init_calls_after(cleanlist)
        ret['onreturn'] = call_onreturn
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        for n in super(OnReturnExtension, self)._init_default_connections():
            yield n
        yield 'onreturn'
    # End def #}}}
# End class #}}}
# ==================================================================================
# StreamExtension
# ==================================================================================
class StreamExtension(SignalExtension): #{{{
    __slots__ = ()
    def _init_funclist_names(self): #{{{
        for n in super(StreamExtension, self)._init_funclist_names():
            yield n
        yield 'streamin'
        yield 'stream'
    # End def #}}}

    def _init_calls_around(self, cleanlist): #{{{
        def call_streamin(self): #{{{
            def streamin_wrap(func): #{{{
                def wrap(cw, *args, **kwargs): #{{{
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
                    callfunc = self.caller
                    for sfunc, t in cleanlist('streamin'):
                        callfunc(self, sfunc, 'streamin', False, None, *args, **kwargs)
                    args, kwargs = args
                    return func(*args, **kwargs)
                # End def #}}}
                return wrap
            # End def #}}}
            yield streamin_wrap
        # End def #}}}
        sup = super(StreamExtension, self)._init_calls_around(cleanlist)
        ret = odict()
        ret['streamin'] = call_streamin
        ret.update(sup.iteritems())
        return ret
    # End def #}}}

    def _init_calls_after(self, cleanlist): #{{{
        def call_stream(self, cw, func, ret, args, kwargs): #{{{
            callfunc = self.caller
            for sfunc, t in cleanlist('stream'):
                ret = callfunc(self, sfunc, 'stream', True, ret, *args, **kwargs)
            return ret
        # End def #}}}
        sup = super(StreamExtension, self)._init_calls_after(cleanlist)
        ret = odict()
        ret['stream'] = call_stream
        ret.update(sup.iteritems())
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        for n in super(StreamExtension, self)._init_default_connections():
            yield n
        yield 'streamin'
        yield 'stream'
    # End def #}}}
# End class #}}}
# ==================================================================================
# ReplaceExtension
# ==================================================================================
class ReplaceExtension(SignalExtension): #{{{
    __slots__ = ()
    def _init_funclist_names(self): #{{{
        for n in super(ReplaceExtension, self)._init_funclist_names():
            yield n
        yield 'replace'
    # End def #}}}

    def _init_calls_replace(self, cleanlist): #{{{
        def call_replace(self): #{{{
            def do_wrap(func): #{{{
                def newcall(cw, *args, **kwargs): #{{{
                    callfunc, rfunc, ret = self.caller, None, None
                    for sfunc, t in cleanlist('replace'):
                        rfunc = sfunc
                    if rfunc:
                        ret = callfunc(self, rfunc, 'replace', False, ret, *args, **kwargs)
                    else:
                        ret = func(*args, **kwargs)
                    return ret
                # End def #}}}
                return newcall
            # End def #}}}
            # Need to return an iterator
            yield do_wrap
        # End def #}}}
        ret = super(ReplaceExtension, self)._init_calls_replace(cleanlist)
        ret['replace'] = call_replace
        return ret
    # End def #}}}

    def _init_default_connections(self): #{{{
        for n in super(ReplaceExtension, self)._init_default_connections():
            yield n
        yield 'replace'
    # End def #}}}
# End class #}}}
# ==================================================================================
# ChooseExtension
# ==================================================================================
class ChooseExtension(SignalExtension): #{{{
    __slots__ = ()
    def __init__(self, signal, **kwargs): #{{{
        self._vars = getattr(self, '_vars', dict())
        self._vars.update(choosepolicy=None, chooseretpolicy=None, chooseyieldpolicy=None)
        super(ChooseExtension, self).__init__(signal, **kwargs)
        self.chooser = ChooseCallable
        self.return_chooser = ChooseCallable
        self.yield_chooser = ChooseCallable
    # End def #}}}

    def _init_funclist_names(self): #{{{
        for n in super(ChooseExtension, self)._init_funclist_names():
            yield n
        yield 'choose'
        yield 'choosereturn'
        yield 'chooseyield'
    # End def #}}}

    def _init_connections(self, connections): #{{{
        super(ChooseExtension, self)._init_connections(connections)
        init = ('choose', 'choosereturn', 'chooseyield')
        connections.update((n, (connect_choosefunc, disconnect_choosefunc)) for n in init)
    # End def #}}}

    def _init_calls_replace(self, cleanlist): #{{{
        choice, callchoice = make_choice_helpers(self, callfunc, cleanlist)
        def call_choose(self): #{{{
            def do_wrap(func): #{{{
                def newcall(cw, *args, **kwargs): #{{{
                    func_choice = choice(self, 'choose', 'chooser', self.chooser_policy, func, False, None, *args, **kwargs)
                    return callchoice(self, func, func_choice, False, None, *args, **kwargs)
                # End def #}}}
                return newcall
            # End def #}}}
            # Need to return an iterator
            yield do_wrap
        # End def #}}}
        def call_choosereturn(self): #{{{
            def do_wrap(func): #{{{
                def newcall(cw, *args, **kwargs): #{{{
                    ret = func(*args, **kwargs)
                    ret_choice = choice(self, 'choosereturn', 'return_chooser', self.return_chooser_policy, 
                            func, True, ret, *args, **kwargs)
                    return callchoice(self, func, ret_choice, True, ret, *args, **kwargs)
                # End def #}}}
                return newcall
            # End def #}}}
            # Need to return an iterator
            yield do_wrap
        # End def #}}}
        def call_chooseyield(self): #{{{
            def do_wrap(func): #{{{
                def newcall(cw, *args, **kwargs): #{{{
                    gen = func(*args, **kwargs)
                    if not isinstance(gen, GeneratorType):
                        gen = (gen,)
                    def mk_gen(gen): #{{{
                        for ret in gen:
                            ret_choice = choice(self, 'chooseyield', 'yield_chooser', self.yield_chooser_policy, 
                                    func, True, ret, *args, **kwargs)
                            yield callchoice(self, func, ret_choice, True, ret, *args, **kwargs)
                    # End def #}}}
                    return mk_gen(gen)
                # End def #}}}
                return newcall
            # End def #}}}
            # Need to return an iterator
            yield do_wrap
        # End def #}}}
        ret = super(ChooseExtension, self)._init_calls_replace(cleanlist)
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
        def fcond(self, listname, siglist, f, index): #{{{
            if not super_fcond(self, listname, siglist, f, index):
                return False
            if choosercid and listname in ('choose', 'choosereturn', 'chooseyield'):
                if choosercid != f.choosefunc.cid:
                    return False
            return True
        # End def #}}}
        return fcond
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
    chooser_policy = property(lambda s: s._vars['choosepolicy'], lambda s, p: s._setpolicy('choosepolicy', p))
    return_chooser_policy = property(lambda s: s._vars['chooseretpolicy'], lambda s, p: s._setpolicy('chooseretpolicy', p))
    yield_chooser_policy = property(lambda s: s._vars['chooseyieldpolicy'], lambda s, p: s._setpolicy('chooseyieldpolicy', p))
    chooser = property(lambda s: s._vars['chooser'], lambda s, c: s._setchooser('chooser', c))
    return_chooser = property(lambda s: s._vars['return_chooser'], lambda s, c: s._setchooser('return_chooser', c))
    yield_chooser = property(lambda s: s._vars['yield_chooser'], lambda s, c: s._setchooser('yield_chooser', c))
    # End properties #}}}
# End class #}}}
# ==================================================================================
# Signal
# ==================================================================================
class DefaultExtension(OnReturnExtension, StreamExtension, ChooseExtension, ReplaceExtension, AroundExtension): #{{{
    __slots__ = ()
# End class #}}}

class Signal(DefaultExtension, BaseSignal): #{{{
    __slots__ = ()
# End class #}}}
# ==================================================================================
#
# ==================================================================================
