# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the pyssi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from warnings import warn
from weakref import proxy, getweakrefs, CallableProxyType
from itertools import repeat, chain
from functools import wraps
from types import GeneratorType, FunctionType as newfunction, ClassType as newclass, MethodType as newmethod

# package imports
from pyssi.util import property_, cref, iscallable, isclass, cgetargspec, bp_call_args, \
                        default_argvals, isfunction, ismethod
from pyssi.util.byteplay import Code, CodeList, Label, LOAD_GLOBAL, LOAD_FAST, LOAD_CONST, SLICE_1, \
                                 CALL_FUNCTION, RETURN_VALUE, SetLineno, BINARY_SUBSCR, STORE_FAST, \
                                 JUMP_IF_FALSE, POP_TOP, RAISE_VARARGS, JUMP_FORWARD, CALL_FUNCTION_VAR_KW

cdef class SignalType: #{{{
    cdef object _signal
    def __init__(self, signal, **options): #{{{
        weak = bool(options.get('weak', False))
        if weak:
            self._signal = proxy(signal, self._signal_callback)
        else:
            self._signal = signal
    # End def #}}}

    def _signal_callback(self, pobj): #{{{
        self._signal = None
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        sig = self._signal
        if sig != None:
            return sig(*args, **kwargs)
        warn('Calling an invalid signal', RuntimeWarning, stacklevel=2)
    # End def #}}}

    property func:
        def __get__(self): #{{{
            return self._signal
        # End def #}}}
# End class #}}}

cdef class next_before: #{{{
    cdef object vals
    def __init__(self, iterfunc, **options): #{{{
        self.vals = list(iterfunc), options
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        iterfunc, options = self.vals
        for f in iterfunc:
            f(*args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class next_after: #{{{
    cdef object vals
    def __init__(self, ret, iterfunc, **options): #{{{
        self.vals = ret, list(iterfunc), options
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        ret, iterfunc, options = self.vals
        for f in iterfunc:
            f(ret, *args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class next_around: #{{{
    cdef object vals
    def __init__(self, signal, iterfunc, **options): #{{{
        iterfunc = list(iterfunc)
        self.vals = iterfunc, signal, iter(iterfunc).next, options
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        iterfunc, signal, inext, options = self.vals
        try:
            f = inext()
        except StopIteration:
            self.vals = iterfunc, signal, iter(iterfunc).next, options
            return signal(*args, **kwargs)
        return f(self, *args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class _Connect_CBFactory: #{{{
    cdef object cat, funclist, sig
    def __init__(self, sig, sigcat, cat, name): #{{{
        self.cat = cat
        order, sigslot = sigcat[cat]
        funchandler, funclist = sigslot[name]
        self.funclist = funclist
        self.sig = sig
    # End def #}}}
    def __call__(self, pobj): #{{{
        try:
            self.funclist.remove(pobj)
        except ValueError:
            pass
        else:
            if self.cat in ('around', 'replace'):
                self.sig.reload()
    # End def #}}}
# End class #}}}

cdef class _Slot_CBFactory: #{{{
    cdef object vals
    def __init__(self, sig, cat, name): #{{{
        self.vals = sig, cat, name
    # End def #}}}
    def __call__(self, pobj): #{{{
        sig, cat, name = self.vals
        sig.remove_slot(name, cat)
        if cat in ('around', 'replace'):
            sig.reload()
    # End def #}}}
# End class #}}}

def _iscallableproxy(pf): #{{{
    return isinstance(pf, CallableProxyType)
# End def #}}}

cdef class BaseSignal(SignalType): #{{{
    cdef object _categories, _wrapped_signal, _options
    def __init__(self, signal, **options): #{{{
        self._options = options
        self._wrapped_signal = None
        self._categories = {'before': ([], dict()),
                            'around': ([], dict()), 
                            'replace': ([], dict()), 
                            'after': ([], dict())}
        super(BaseSignal, self).__init__(signal, **options)
    # End def #}}}

    def slot_callback_factory(self, cat, name): #{{{
        return _Slot_CBFactory(self, cat, name)
    # End def #}}}

    def add_slot(self, name, cat, handler, **opt): #{{{
        sigcat = self._categories
        seqclass = opt.get('seqclass', list)
        insert = opt.get('insert', None)
        weak = bool(opt.get('weak', False))
        order, slots = sigcat[cat]
        if name in slots:
            raise TypeError("Slot '%s' already exists in signal category '%s'" %(name, cat))
        slothand, slist = (handler, [])
        if weak:
            slothand = proxy(handler, self.slot_callback_factory(cat, name))
        slots[name] = (slothand, slist)
        if insert == None:
            order.append(name)
        else:
            order.insert(int(insert), name)
    # End def #}}}

    def remove_slot(self, name, cat, **opt): #{{{
        sigcat = self._categories
        order, slots = sigcat[cat]
        del slots[name]
        order.remove(name)
        if cat in ('around', 'replace'):
            self.reload()
    # End def #}}}

    def connect_callback_factory(self, cat, name): #{{{
        return _Connect_CBFactory(self, self._categories, cat, name)
    # End def #}}}

    def _connect(self, cat, slots, **options): #{{{
        weak = bool(options.get('weak', False))
        s_ismethod = bool(options.get('ismethod', False))
        if isinstance(slots, dict):
            slots = slots.iteritems()
        sigcat = self._categories
        for name, funclist in slots:
            order, sigslot = sigcat[cat]
            slist_add = sigslot[name][1].append
            cbfactory = self.connect_callback_factory(cat, name)
            for f in funclist:
                if s_ismethod:
                    f.ismethod = True
                if weak and not isinstance(f, CallableProxyType):
                    wf = proxy(f, cbfactory)
                else:
                    wf = f
                slist_add(wf)
        if cat in ('around', 'replace'):
            self.reload()
    # End def #}}}

    def connect_before(self, slots, **options): #{{{
        self._connect('before', slots, **options)
    # End def #}}}

    def connect_around(self, slots, **options): #{{{
        self._connect('around', slots, **options)
    # End def #}}}

    def connect_replace(self, slots, **options): #{{{
        self._connect('replace', slots, **options)
    # End def #}}}

    def connect_after(self, slots, **options): #{{{
        self._connect('after', slots, **options)
    # End def #}}}

    # dict(after=dict(after=[], after2=[]), before=dict(before=[]))
    def connect(self, slots, **options): #{{{
        if not isinstance(slots, dict):
            raise TypeError("Expected dict object, got %s instead" %slots.__class__.__name__)
        connect = self._connect
        for cat, catslots in slots.iteritems():
            connect(cat, catslots, **options)
    # End def #}}}

    def _disconnect(self, cat, slots, **options): #{{{
        numdel = int(options.get('count', 1))
        if numdel < 0:
            numdel = 0
        if isinstance(slots, dict):
            slots = slots.iteritems()
        sigcat = self._categories
        order, sigslot = sigcat[cat]
        if not slots:
            for name, (funchandler, funclist) in sigslot.iteritems():
                del funclist[:]
        else:
            for name, funclist in slots:
                slist = sigslot[name][1]
                slist_rem = slist.remove
                if not funclist:
                    del slist[:]
                    continue
                for f in funclist:
                    count = 0
                    proxies = filter(_iscallableproxy, getweakrefs(f))
                    for flist in (proxies, repeat(f)):
                        for p in flist:
                            if numdel and count >= numdel:
                                break
                            try:
                                slist_rem(p)
                            except ValueError:
                                if p == f:
                                    break
                            else:
                                count = count + 1
        if cat in ('around', 'replace'):
            self.reload()
    # End def #}}}

    def disconnect_before(self, slots=(), **options): #{{{
        self._disconnect('before', slots, **options)
    # End def #}}}

    def disconnect_around(self, slots=(), **options): #{{{
        self._disconnect('around', slots, **options)
    # End def #}}}

    def disconnect_replace(self, slots=(), **options): #{{{
        self._disconnect('replace', slots, **options)
    # End def #}}}

    def disconnect_after(self, slots=(), **options): #{{{
        self._disconnect('after', slots, **options)
    # End def #}}}

    # dict(after=dict(after=[], after2=[]), before=dict(before=[]))
    def mdisconnect(self, slots=None, **options): #{{{
        if slots and not isinstance(slots, dict):
            raise TypeError("Expected dict object, got %s instead" %slots.__class__.__name__)
        disconnect = self._disconnect
        if not slots:
            for cat in self._categories:
                disconnect(cat, slots, **options)
        else:
            for cat, catslots in slots.iteritems():
                disconnect(cat, catslots, **options)
    # End def #}}}

    def _disconnect_helper(self, disconnect, count, origcount, options, funcseq=None): #{{{
        for cat, (order, sigslot) in self._categories.iteritems():
            for name, (funchandler, funclist) in sigslot.iteritems():
                if not funcseq:
                    disconnect(cat, [(name, ())], **options)
                else:
                    before = len(funclist)
                    disconnect(cat, [(name, funcseq)], **options)
                    numdel = 0
                    if before:
                        after = len(funclist)
                        if after < before:
                            numdel = before - after
                    if count >= numdel:
                        count = count - numdel
                        if origcount and not count:
                            break
                        options['count'] = count
    # End def #}}}

    def disconnect(self, slots=None, **options): #{{{
        disconnect = self._disconnect
        dhelper = self._disconnect_helper
        count = int(options.get('count', 1))
        if count < 0:
            count = 0
        origcount = count
        if not slots:
            self.mdisconnect(**options)
        else:
            for f in slots:
                dhelper(disconnect, count, origcount, dict(options), (f,))
    # End def #}}}

    def reload(self): #{{{
        sigcat = self._categories
        options = self._options
        afunc = self._around_func
        replace_func = afunc(self.func, sigcat['replace'], options)
        self._wrapped_signal = afunc(replace_func, sigcat['around'], options)
    # End def #}}}

    def _around_func(self, signal, sigcat, options): #{{{
        order, slots = sigcat
        sigfunc = signal
        for name in reversed(order):
            func, flist = slots[name]
            sigfunc = func(sigfunc, iter(flist), **options)
        return sigfunc
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        sigcat, options = self._categories, self._options
        wsig = self._wrapped_signal
        if wsig != None:
            signal = wsig
        else:
            signal = self.func
        order, slots = sigcat['before']
        for name in order:
            func, flist = slots[name]
            func(iter(flist), **options)(*args, **kwargs)
        ret = signal(*args, **kwargs)
        order, slots = sigcat['after']
        for name in order:
            func, flist = slots[name]
            func(ret, iter(flist), **options)(*args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}

# ==================================================================================
# next_onreturn
# ==================================================================================
# after category, onreturn slot
cdef class next_onreturn(next_after): #{{{
    def __call__(self, *args, **kwargs): #{{{
        ret, iterfunc, options = self.vals
        for f in iterfunc:
            if getattr(f, 'ismethod', False):
                f(ret, args[0])
            else:
                f(ret)
    # End def #}}}
# End class #}}}
# ==================================================================================
# next_stream
# ==================================================================================
# around category, streamin slot
cdef class next_streamin(next_around): #{{{
    def nextmeth(self, *varargs): #{{{
        sig, args, kwargs = varargs
        return self.nextfunc([sig]+args, kwargs)
    # End def #}}}

    def nextfunc(self, args, kwargs): #{{{
        iterfunc, signal, inext, options = self.vals
        try:
            f = inext()
        except StopIteration:
            self.vals = iterfunc, signal, iter(iterfunc).next, options
            return signal(*args, **kwargs)
        if getattr(f, 'ismethod', False):
            sig, callargs = args[0], args[1:]
            ret = f(self.nextmeth, sig, callargs, kwargs)
        else:
            ret = f(self.nextfunc, args, kwargs)
        return ret
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        return self.nextfunc(list(args), kwargs)
    # End def #}}}
# End class #}}}

# around category, stream slot
cdef class next_stream(next_around): #{{{
    def __call__(self, *args, **kwargs): #{{{
        iterfunc, signal, inext, options = self.vals
        sret = signal(*args, **kwargs)
        for f in iterfunc:
            if getattr(f, 'ismethod', False):
                sret = f(sret, args[0])
            else:
                sret = f(sret)
        return sret
    # End def #}}}
# End class #}}}
# ==================================================================================
# next_replace
# ==================================================================================
# replace category, replace slot
cdef class next_replace(next_around): #{{{
    def __init__(self, signal, iterfunc, **options): #{{{
        iterfunc = list(iterfunc)
        f = None
        if iterfunc:
            f = iterfunc[-1]
        self.vals = signal, f, options
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        signal, f, options = self.vals
        if f:
            return f(signal, *args, **kwargs)
        return signal(*args, **kwargs)
    # End def #}}}
# End class #}}}
# ==================================================================================
# next_choice
# ==================================================================================
class AmbiguousChoiceError(StandardError): pass
class StopCascade(Exception): pass

# replace
# choices: sequence of 2-tuples
#   - A function that computes whether or not its partner will be run
#   - A callable that runs if its partner evaluates to True
# policy: Default policies: default, cascade, first, last
# origfunc: The original callable that is wrapped
# callfunc: A callable that accepts three arguments:
#   - A callable to call
#   - Arguments passed to the given callable
#   - Keyword arguments passed to the given callable

# replace category, choose slot
cdef class next_choice(next_around): #{{{
    def __init__(self, signal, iterfunc, **options): #{{{
        policy = options.get('choose_policy', None)
        cascade = (policy == 'cascade')
        self.vals = signal, list(iterfunc), policy, cascade, options
    # End def #}}}
    def run_cascade(self, f, args, kwargs): #{{{
        ret, stop = None, False
        try:
            ret = f(*args, **kwargs)
        except StopCascade, err:
            if err.args:
                ret = bool(err.args[0])
            stop = True
        return ret, stop
    # End def #}}}
    def select(self, iterfunc, args, kwargs): #{{{
        signal, _, policy, cascade, options = self.vals
        if policy == 'default':
            return 
        run_cascade = self.run_cascade
        found = []
        fapp = found.append
        if cascade:
            fapp(signal)
        for (c, f) in iterfunc:
            if cascade:
                ret, stop = run_cascade(c, args, kwargs)
            else:
                ret = c(*args, **kwargs)
            if ret:
                fapp(f)
                if policy == 'first':
                    break
            if cascade and stop:
                break
        if not found:
            return None
        elif policy == 'last':
            return found[-1:]
        elif cascade or len(found) == 1:
            return found
        raise AmbiguousChoiceError('Found more than one selectable callable')
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        signal, iterfunc, policy, cascade, options = self.vals
        found = self.select(iterfunc, args, kwargs)
        if not found:
            return signal(*args, **kwargs)
        ret = None
        for f in found:
            ret = f(*args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}

# replace category, choosereturn slot
cdef class next_choosereturn(next_choice): #{{{
    def __init__(self, signal, iterfunc, **options): #{{{
        options['choose_policy'] = options.pop('choose_return_policy', None)
        super(next_choosereturn, self).__init__(signal, iterfunc, **options)
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        signal, iterfunc, policy, cascade, options = self.vals
        ret = signal(*args, **kwargs)
        found = self.select(iterfunc, (ret,), {})
        if not found:
            return ret
        for f in found:
            ret = f(ret)
        return ret
    # End def #}}}
# End class #}}}

# replace category, chooseyield slot
cdef class _chooseyield_next_yield: #{{{
    cdef object vals
    def __init__(self, select, iterfunc, gen): #{{{
        self.vals = select, iterfunc, gen
    # End def #}}}
    def __iter__(self): #{{{
        return self
    # End def #}}}
    def __next__(self): #{{{
        select, iterfunc, gen = self.vals
        ret = gen.next()
        found = select(iterfunc, (ret,), {})
        if not found:
            return ret
        for f in found:
            ret = f(ret)
        return ret
    # End def #}}}
# End class #}}}

cdef class next_chooseyield(next_choice): #{{{
    def __init__(self, signal, iterfunc, **options): #{{{
        options['choose_policy'] = options.pop('choose_yield_policy', None)
        super(next_chooseyield, self).__init__(signal, iterfunc, **options)
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        signal, iterfunc, policy, cascade, options = self.vals
        gen = signal(*args, **kwargs)
        if not isinstance(gen, GeneratorType):
            return gen
        return _chooseyield_next_yield(self.select, iterfunc, gen)
    # End def #}}}
# End class #}}}

# ==================================================================================
# Signal
# ==================================================================================
cdef class Signal(BaseSignal): #{{{
    def __init__(self, signal, **options): #{{{
        super(Signal, self).__init__(signal, **options)
        add_slot = self.add_slot
        # Before
        add_slot('before', 'before', next_before)

        # Around (last is closest to signal)
        add_slot('streamin', 'around', next_streamin)
        add_slot('stream', 'around', next_stream)
        add_slot('around', 'around', next_around)

        # Replace (last is closest to signal)
        add_slot('choosereturn', 'replace', next_choosereturn)
        add_slot('chooseyield', 'replace', next_chooseyield)
        add_slot('choose', 'replace', next_choice)
        add_slot('replace', 'replace', next_around)

        # After
        add_slot('after', 'after', next_after)
        add_slot('onreturn', 'after', next_onreturn)
    # End def #}}}
# End class #}}}

# ==================================================================================
# Decorators
# ==================================================================================

# ----------------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------------
cdef class DecoratorSettings: #{{{
    cdef object _vals
    def __init__(self, func, settings): #{{{
        oldset = settings
        if isinstance(func, DecoratorSettings):
            settings = dict(func.settings)
            settings.update(oldset)
        self._vals = func, settings
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        return self.func(*args, **kwargs)
    # End def #}}}

    property func:
        def __get__(self): #{{{
            return self._vals[0]
        # End def #}}}

    property settings:
        def __get__(self): #{{{
            return self._vals[1]
        # End def #}}}

    property vals:
        def __get__(self): #{{{
            return self._vals
        # End def #}}}
# End class #}}}

cdef class SignalDecorator: #{{{
    cdef object _args
    # args = (cat, slotname, signal, deconame, globals, sigopt, options)
    def __init__(self, args=None): #{{{
        self._args = args
    # End def #}}}

    def __call__(self, func): #{{{
        return func
    # End def #}}}
# End class #}}}

cdef class DecoratorFactory: #{{{
    cdef object _args, _decocls
    def __init__(self, cat, slotname, decocls, **options): #{{{
        self._args = (cat, slotname, options)
        if not isclass(decocls):
            raise TypeError('Expected SignalDecorator subclass, got %s object instead' %decocls.__class__.__name__)
        elif not issubclass(decocls, SignalDecorator):
            raise TypeError('Expected SignalDecorator subclass, got %s class instead' %decocls.__name__)
        self._decocls = decocls
    # End def #}}}

    def __call__(self, signal, deconame, globals, **sigopt): #{{{
        cat, slotname, options = self._args
        return self._decocls((cat, slotname, signal, deconame, globals, sigopt, options))
    # End def #}}}
# End class #}}}

# ----------------------------------------------------------------------------------
# LocalDecoratorSettings
# ----------------------------------------------------------------------------------
cdef class DecoratorSettingsFactory: #{{{
    cdef object _args
    def __init__(self, lopt): #{{{
        self._args = lopt
    # End def #}}}
    def __call__(self, func): #{{{
        return DecoratorSettings(func, self._args)
    # End def #}}}
# End class #}}}

cdef class LocalDecoratorSettings(SignalDecorator): #{{{
    def __call__(self, **lopt): #{{{
        return DecoratorSettingsFactory(lopt)
    # End def #}}}
# End class #}}}

# ----------------------------------------------------------------------------------
# GlobalDecoratorSettings
# ----------------------------------------------------------------------------------
cdef class GlobalDecoratorSettings(SignalDecorator): #{{{
    def __call__(self, **gopt): #{{{
        (cat, slotname, signal, deconame, globals, sigopt, options) = self._args
        globals.update(gopt)
        return SignalDecorator()
    # End def #}}}
# End class #}}}
# ----------------------------------------------------------------------------------
# GenericDecorator
# ----------------------------------------------------------------------------------
cdef class GenericDecorator_IsMethodChooser: #{{{
    cdef object _settings, _func
    cdef public object ismethod
    # ismethod is considered to be True
    def __init__(self, func, uses_sigarg, overload, callmethod): #{{{
        self._settings = func, uses_sigarg, overload, callmethod, func.__name__
        self.ismethod = True
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        func, uses_sigarg, overload, callmethod, funcname = self._settings
        if not overload and callmethod:
            if uses_sigarg: # cat != 'before'
                sigarg, sig = args[:2]
                return getattr(sig, funcname)(sigarg, *args[2:], **kwargs)
            else:
                sig = args[0]
                return getattr(sig, funcname)(*args[1:], **kwargs)
        elif uses_sigarg: # cat != 'before'
            sigarg, sig = args[:2]
            return func(sig, sigarg, *args[2:], **kwargs)
        else:
            return func(*args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class GenericDecorator(SignalDecorator): #{{{
    def __call__(self, func): #{{{
        (cat, slotname, signal, deconame, globals, sigopt, options) = self._args
        func, settings = self._init_settings(func, globals)
        retfunc, options = func, dict(options)
        args = (cat, slotname, signal, deconame, settings, sigopt, options)
        self._update_connopt(func, args)
        retfunc = self._update_func(retfunc, args)
        signal.connect({cat: {slotname: [retfunc]}}, **options)
        return self._return_func(func, retfunc, args)
    # End def #}}}

    def _init_settings(self, func, globals): #{{{
        settings = globals
        if isinstance(func, DecoratorSettings):
            func, local_settings = func.vals
            settings = dict(globals)
            settings.update(local_settings)
        return func, settings
    # End def #}}}

    def _update_connopt(self, func, args): #{{{
        (cat, slotname, signal, deconame, settings, sigopt, options) = args
        options['weak'] = settings.get('weak', False)
        overload = settings.get('overload', True)
        if overload:
            options['weak'] = False
    # End def #}}}

    def _update_func(self, func, args): #{{{
        (cat, slotname, signal, deconame, settings, sigopt, connopt) = args
        sget = settings.get
        s_ismethod = sget('ismethod', False)
        if s_ismethod:
            overload = sget('overload', True)
            callmethod = sget('callmethod', False)
            uses_sigarg = (cat in ('around', 'replace', 'after'))
            connopt['weak'] = False
            func = GenericDecorator_IsMethodChooser(func, uses_sigarg, overload, callmethod)
        return func
    # End def #}}}

    def _return_func(self, origfunc, retfunc, args): #{{{
        (cat, slotname, signal, deconame, settings, sigopt, options) = args
        overload = settings.get('overload', True)
        if overload:
            ret = signal.signalfunc
            if ismethod(retfunc):
                ret = newmethod(ret, retfunc.im_self, retfunc.im_class)
            retfunc = ret
        elif isinstance(retfunc, GenericDecorator_IsMethodChooser):
            retfunc = origfunc
        return retfunc
    # End def #}}}
# End class #}}}

# ----------------------------------------------------------------------------------
# BaseDecoratorSignal
# ----------------------------------------------------------------------------------
cdef class BaseDecoratorSignal(BaseSignal): #{{{
    cdef object _settings, _deco, _signalfunc
    def __init__(self, signal, **options): #{{{
        super(BaseDecoratorSignal, self).__init__(signal, **options)
        self._signalfunc = None
        self._settings = {}
        # name = decofunc
        self._deco = {}
    # End def #}}}

    def __getattr__(self, name): #{{{
        deco = self._deco
        if name in deco:
            return deco[name](self, name, self._settings, **self._options)
        raise AttributeError("'%s' object has no attribute '%s'" %(self.__class__.__name__, name))
    # End def #}}}

    def add_deco(self, name, cat, slotname, decocls, **options): #{{{
#        if not isinstance(deco, DecoratorFactory):
#            raise TypeError('Can only specify DecoratorFactory objects for the \'deco\' argument')
        self._deco[name] = DecoratorFactory(cat, slotname, decocls, **options)
    # End def #}}}

    def remove_deco(self, name): #{{{
        self._deco.pop(name, None)
    # End def #}}}

    property decorators:
        def __get__(self): #{{{
            return self._deco.keys()
        # End def #}}}

    property signalfunc:
        def __get__(self): #{{{
            ret = self._signalfunc
            if ret:
                ret = ret()
            return ret
        # End def #}}}
        def __set__(self, val): #{{{
            signalfunc = self._signalfunc
            if signalfunc is not None:
                raise ValueError("Can only set 'signalfunc' property once")
            if not iscallable(val) or getattr(val, 'signal', None) is not self:
                raise TypeError('Attempt to set invalid signalfunc')
            self._signalfunc = cref(val)
        # End def #}}}
# End class #}}}

# ----------------------------------------------------------------------------------
# signal_factory
# ----------------------------------------------------------------------------------
def _notnone(obj): #{{{
    return (obj != None)
# End def #}}}

cdef class signal_func_deco: #{{{
    cdef object _args
    def __init__(self, decosig, sigopt, options): #{{{
        self._args = decosig, sigopt, options
    # End def #}}}

    def __call__(self, func): #{{{
        decosig, sigopt, options = self._args
        signal = decosig(func, **sigopt)
        args, vargs, vkeys, defaults = spec = cgetargspec(func)
        # code_args = args + [v for v in (vargs, vkeys) if v != None]
        code_args = args + filter(_notnone, [vargs, vkeys])

        # Find name that is unbound 
        names, n, _join = set(code_args), 'dsfunc', ''.join
        while n in names:
            n = _join(n, '_')

        codelist = [(SetLineno, 2), (LOAD_GLOBAL, n)] + bp_call_args(*spec) + [(RETURN_VALUE, None)]
        fcode = Code(CodeList(codelist), (), code_args, bool(vargs), bool(vkeys), True, 'DecoSignalFunction', '<dyn>', 1, None)
        d = DecoSignalFunction = newfunction(fcode.to_code(), {n: signal}, 'DecoSignalFunction', default_argvals(args, defaults))
        d = wraps(func)(d)
        d.signal = signal
        signal.signalfunc = d
        for n in signal.decorators:
            setattr(d, n, getattr(signal, n))
        return global_settings(d, **options)(d)
    # End def #}}}
# End class #}}}

cdef class signal_func_factory: #{{{
    cdef object _args
    def __init__(self, decosig, sigopt): #{{{
        self._args = decosig, sigopt
    # End def #}}}
    def __call__(self, **options): #{{{
        args = self._args + (options,)
        return signal_func_deco(*args)
    # End def #}}}
# End class #}}}

def signal_factory(decosig, **sigopt): #{{{
    return signal_func_factory(decosig, sigopt)
# End def #}}}

# ----------------------------------------------------------------------------------
# DecoratorSignal
# ----------------------------------------------------------------------------------
cdef class DecoratorSignal(BaseDecoratorSignal): #{{{
    def __init__(self, signal, **options): #{{{
        super(DecoratorSignal, self).__init__(signal, **options)
        add_slot = self.add_slot

        # Before
        add_slot('before', 'before', next_before)

        # Around
        add_slot('streamin', 'around', next_streamin)
        add_slot('stream', 'around', next_stream)
        add_slot('around', 'around', next_around)

        # Replace (last is first)
        add_slot('replace', 'replace', next_replace)
        add_slot('chooseyield', 'replace', next_chooseyield)
        add_slot('choosereturn', 'replace', next_choosereturn)
        add_slot('choose', 'replace', next_choice)

        # After
        add_slot('after', 'after', next_after)
        add_slot('onreturn', 'after', next_onreturn)

        # Decorators: deconame, category, slotname, decocls
        add_deco = self.add_deco

        # Settings are not slots, so no category, slot names
        add_deco('settings', '', '', LocalDecoratorSettings)
        add_deco('global_settings', '', '', GlobalDecoratorSettings)

        # Generic decorators
        add_deco('before', 'before', 'before', GenericDecorator)
        add_deco('onreturn', 'after', 'onreturn', GenericDecorator)
        add_deco('replace', 'replace', 'replace', GenericDecorator)
        add_deco('around', 'around', 'around', GenericDecorator)
        add_deco('stream', 'around', 'stream', GenericDecorator)
        add_deco('streamin', 'around', 'streamin', GenericDecorator)
        add_deco('after', 'after', 'after', GenericDecorator)
    # End def #}}}
# End class #}}}

# ==================================================================================
# global_settings
# ==================================================================================
def global_settings(signal, **kwargs): #{{{
    if not isfunction(signal):
        raise TypeError('argument must be a python function')
    sig = getattr(signal, 'signal', None)
    if not isinstance(sig, BaseDecoratorSignal):
        raise TypeError("argument must have a signal attribute which must be a BaseDecoratorSignal instance")
    return signal.global_settings(**kwargs)
# End def #}}}
# ==================================================================================
# signal
# ==================================================================================
signal = signal_factory(DecoratorSignal)
# ==================================================================================
# 
# ==================================================================================
