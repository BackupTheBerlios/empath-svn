# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the pyssi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pyssi.util import cref

cdef class SignalType: #{{{
    cdef object _signal
    def __init__(self, signal, **options): #{{{
        weak = bool(options.get('weak', False))
        self._signal = cref(signal, weak=weak)
    # End def #}}}

    def connect(self, *slots, **options): #{{{
        raise NotImplementedError
    # End def #}}}

    def disconnect(self, *slots, **options): #{{{
        raise NotImplementedError
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        return self._signal()(*args, **kwargs)
    # End def #}}}

    property func:
        def __get__(self): #{{{
            return self._signal()
        # End def #}}}
# End class #}}}

cdef class next_before: #{{{
    cdef object iterfunc
    def __init__(self, iterfunc): #{{{
        self.iterfunc = iterfunc
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        for f in self.iterfunc:
            f(*args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class next_after: #{{{
    cdef object vals
    def __init__(self, ret, iterfunc): #{{{
        self.vals = ret, iterfunc
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        ret, iterfunc = self.vals
        for f in iterfunc:
            f(ret, *args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class next_around: #{{{
    cdef object vals
    def __init__(self, signal, iterfunc): #{{{
        self.vals = signal, iterfunc.next
    # End def #}}}
    def __call__(self, *args, **kwargs): #{{{
        signal, inext = self.vals
        try:
            f = inext()
        except StopIteration:
            return signal(*args, **kwargs)
        return f(self, *args, **kwargs)
    # End def #}}}
# End class #}}}

cdef class BaseSignal(SignalType): #{{{
    cdef object _categories
    def __init__(self, signal, **options): #{{{
        self._categories = {'before': ([], dict()),
                            'around': ([], dict()), 
                            'replace': ([], dict()), 
                            'after': ([], dict())}
        super(BaseSignal, self).__init__(signal, **options)
    # End def #}}}

    def add_slot(self, name, cat, handler, **opt): #{{{
        sigcat = self._categories
        seqclass = opt.get('seqclass', list)
        insert = opt.get('insert', None)
        order, slots = sigcat[cat]
        if name in slots:
            raise TypeError("Slot '%s' already exists in signal category '%s'" %(name, cat))
        slots[name] = (slothand, slist) = (handler, [])
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
    # End def #}}}

    def connect(self, cat, slots, **options): #{{{
        if isinstance(slots, dict):
            slots = slots.iteritems()
        sigcat = self._categories
        for name, funclist in slots:
            order, sigslot = sigcat[cat]
            sigslot[name][1].extend(funclist)
    # End def #}}}

    def disconnect(self, *slots, **options): #{{{
        raise NotImplementedError
    # End def #}}}

    def _around_func(self, signal, sigcat, args, kwargs): #{{{
        order, slots = sigcat
        sigfunc = signal
        for name in reversed(order):
            func, flist = slots[name]
            sigfunc = func(sigfunc, iter(flist))
        return sigfunc
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        sigcat = self._categories
        afunc = self._around_func
        replace_func = afunc(self.func, sigcat['replace'], args, kwargs)
        around_func = afunc(replace_func, sigcat['around'], args, kwargs)
        order, slots = sigcat['before']
        for name in order:
            func, flist = slots[name]
            func(iter(flist))(*args, **kwargs)
        ret = around_func(*args, **kwargs)
        order, slots = sigcat['after']
        for name in order:
            func, flist = slots[name]
            func(ret, iter(flist))(*args, **kwargs)
        return ret
    # End def #}}}
# End class #}}}

cdef class Signal(BaseSignal): #{{{
    def __init__(self, signal, **options): #{{{
        super(Signal, self).__init__(signal, **options)
        self.add_slot('before', 'before', next_before)
        self.add_slot('after', 'after', next_after)
    # End def #}}}
# End class #}}}
