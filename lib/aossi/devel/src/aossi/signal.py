# Module: aossi.signal
# File: signal.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from aossi.core import *
from aossi.cwrapper import CallableWrapper, cid
from aossi.util import iscallable, ChooseCallable, ChoiceObject
from aossi.util.introspect import mro

from aossi.util.odict import odict

__all__ = ('Signal',)
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
    weak = bool(slots.get('weak', True))
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
    if delall and not vals:
        while l:
            l.pop()
        return
    for tup in vals:
        f, cond = tup, None
        if not iscallable(f):
            cond, f = tup
        found = self._find(f, listname, chooser=None)
        if found:
            del l[found[0]]
# End def #}}}
# ==================================================================================
# Signal
# ==================================================================================
class Signal(BaseSignal): #{{{
    __slots__ = ()
    def __init__(self, signal, **kwargs): #{{{
        self._vars = getattr(self, '_vars', dict())
        self._vars.update(choosepolicy=None, chooseretpolicy=None)
        super(Signal, self).__init__(signal, **kwargs)
        self.chooser = ChooseCallable
        self.return_chooser = ChooseCallable
    # End def #}}}

    def _init_functions(self, funclist): #{{{
        super(Signal, self)._init_functions(funclist)
        init = ('around', 'onreturn', 'choose', 'choosereturn', 'streamin', 'stream', 'replace')
        funclist.update((name, []) for name in init)
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
        ret = odict()
        ret['replace'] = call_replace
        ret['choose'] = call_choose
        ret['choosereturn'] = call_choosereturn
        return ret
    # End def #}}}

    def _init_calls_around(self, cleanlist): #{{{
        def call_around(self): #{{{
            return (arfunc for arfunc, _ in cleanlist('around'))
        # End def #}}}
        return odict(around=call_around)
    # End def #}}}

    def _init_calls_after(self, cleanlist): #{{{
        def call_streamin(self, cw, func, ret, args, kwargs): #{{{
            callfunc, cnam = self.caller, 'streamin'
            for cls in mro(args[0].__class__):
                sig = getsignal(getattr(cls, cw.__name__, None)) if args else None
                if sig and cw is sig.func:
                    args = (args[0], list(args[1:]), kwargs)
                    break
            else:
                args = (list(args), kwargs)
            for sfunc, t in cleanlist(cnam):
                callfunc(self, sfunc, cnam, False, ret, *args)
            return ret
        # End def #}}}
        def call_stream(self, cw, func, ret, args, kwargs): #{{{
            callfunc = self.caller
            for sfunc, t in cleanlist('stream'):
                ret = callfunc(self, sfunc, 'stream', True, ret, *args, **kwargs)
            return ret
        # End def #}}}
        def call_onreturn(self, cw, func, ret, args, kwargs): #{{{
            callfunc = self.caller
            for rfunc, t in cleanlist('onreturn'):
                callfunc(self, rfunc, 'onreturn', True, ret, *args, **kwargs)
            return ret
        # End def #}}}
        sup = super(Signal, self)._init_calls_after(cleanlist)
        ret = odict()
        ret['streamin'] = call_streamin
        ret['stream'] = call_stream
        ret.update(sup.iteritems())
        ret['onreturn'] = call_onreturn
        return ret
    # End def #}}}

    def _init_connections(self, connections): #{{{
        super(Signal, self)._init_connections(connections)
        init = ('streamin', 'stream', 'onreturn', 'around', 'replace')
        connections.update((n, (connect_func, disconnect_func)) for n in init)
        init = ('choose', 'choosereturn')
        connections.update((n, (connect_choosefunc, disconnect_choosefunc)) for n in init)
    # End def #}}}

    def _find_cond(self, **kw): #{{{
        chooser = kw.get('chooser', None)
        choosercid = None
        if iscallable(chooser):
            choosercid = cid(chooser)
        def fcond(self, listname, siglist, f, index): #{{{
            if choosercid and listname in ('choose', 'choosereturn'):
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
    chooser = property(lambda s: s._vars['chooser'], lambda s, c: s._setchooser('chooser', c))
    return_chooser = property(lambda s: s._vars['return_chooser'], lambda s, c: s._setchooser('return_chooser', c))
    # End properties #}}}
# End class #}}}
