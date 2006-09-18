# Module: aossi.signal
# File: signal.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('Signal',)
from warnings import warn


from aossi.cwrapper import CallableWrapper, cid
from aossi.misc import iscallable, ChooseCallable, ChoiceObject

class Signal(object): #{{{
    __slots__ = ('__weakref__', '_func', '_beforefunc', '_afterfunc', 
                    '_aroundfunc', '_onreturnfunc', '_choosefunc', 
                    '_chooser', '_choosepolicy')
    def __init__(self, signal, weak=True): #{{{
        if not iscallable(signal):
            raise TypeError("Argument must be callable.");
        self._func = CallableWrapper(signal, weak=weak)
        self._beforefunc = []
        self._afterfunc = []
        self._aroundfunc = []
        self._onreturnfunc = []
        self._choosefunc = []
        self.chooser = ChooseCallable
        self._choosepolicy = None
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        if not self.valid:
            warn('Calling an invalid signal', RuntimeWarning, stacklevel=2)
            return
        return self._func(*args, **kwargs)
    # End def #}}}

    def _cleanbefore(self, obj): #{{{
        for ret in self._cleanlist(self._beforefunc):
            pass
    # End def #}}}

    def _cleanafter(self, obj): #{{{
        for ret in self._cleanlist(self._afterfunc):
            pass
    # End def #}}}

    def _cleanaround(self, obj): #{{{
        for ret in self._cleanlist(self._aroundfunc):
            pass
    # End def #}}}

    def _cleanonreturn(self, obj): #{{{
        for ret in self._cleanlist(self._onreturnfunc):
            pass
    # End def #}}}

    def _cleanchoose(self, obj): #{{{
        for ret in self._cleanlist(self._choosefunc):
            pass
    # End def #}}}

    def _cleanlist(self, l): #{{{
        llen = len(l)
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
        cleanlist = self._cleanlist
        def do_wrap(func): #{{{
            def newcall(s, *args, **kwargs): #{{{
                for bfunc, t in cleanlist(self._beforefunc):
                    bfunc(*args, **kwargs)
                choice = None
                if self._choosefunc:
                    chooser = self.chooser
                    if not chooser or chooser.isdead:
                        self.chooser = ChooseCallable
                    gen = ((i.choosefunc, i.callable) for i in self._choosefunc)
                    choice = self.chooser(gen, self.chooserpolicy, func, *args, **kwargs)
                if not choice:
                    choice = [func]
                for f in choice:
                    ret = f(*args, **kwargs)
                for afunc, t in cleanlist(self._afterfunc):
                    afunc(*args, **kwargs)
                for rfunc, t in cleanlist(self._onreturnfunc):
                    rfunc(ret)
                return ret
            # End def #}}}
            return newcall
        # End def #}}}
        return do_wrap
    # End def #}}}

    def reload(self): #{{{
        if self._func.isdead:
            return
        cleanlist = self._cleanlist
        self._func.unwrap()
        for cfunc, t in cleanlist(self._choosefunc):
            cfunc.callable.unwrap()
        for arfunc, t in cleanlist(self._aroundfunc):
            for cfunc, t in cleanlist(self._choosefunc):
                cfunc.callable.wrap(arfunc)
            self._func.wrap(arfunc)
        do_wrap = self._generate_wrapfactory()
        self._func.wrap(do_wrap)
    # End def #}}}

    def _validate_connect_args(self, *args, **other_slots): #{{{
        expected = ('before', 'around', 'onreturn', 'choose', 'weak', 'weakcondf')
        if [i for i in other_slots if i not in expected]:
            raise ValueError('valid keyword arguments are: %s' %', '.join(expected))
        b = other_slots.get('before', tuple())
        a = other_slots.get('around', tuple())
        r = other_slots.get('onreturn', tuple())
        c = other_slots.get('choose', tuple())
        w = bool(other_slots.get('weak', True))
        wcf = bool(other_slots.get('weakcondf', w))
        return b, a, r, c, w, wcf
    # End def #}}}

    def _find(self, func, siglistseq=None): #{{{
        temp_siglistseq = (self._afterfunc, self._beforefunc, self._aroundfunc, self._onreturnfunc, self._choosefunc)
        siglistseq = (siglistseq,)
        if siglistseq[0] not in temp_siglistseq:
            siglistseq = temp_siglistseq
        foundindex = None
        foundlist = None
        fid = cid(func)
        for siglist in siglistseq:
            for f, index in self._cleanlist(siglist):
                if f.cid == fid:
                    foundindex = index
                    foundlist = siglist
                    break
            else:
                continue
            break
        if foundindex is not None:
            return foundindex, foundlist
        return None

    # End def #}}}

    def connect(self, *after_slots, **other_slots): #{{{
        before_slots, around_slots, onreturn_slots, choose_slots, isweak, wcf = self._validate_connect_args(*after_slots, **other_slots)
        if not after_slots and not before_slots and not around_slots and not onreturn_slots and not choose_slots:
            return
        def addfunc(a, l, lname):
            for f in a:
                if not iscallable(f):
                    seqname = lname
                    if lname == 'after':
                        seqname = ''.join([lname, '_slots'])
                    raise TypeError('Detected non-callable element of %s sequence' %seqname)
                found = self._find(f, l)
                if not found:
                    l.append(CallableWrapper(f, getattr(self, '_clean%s' %lname), weak=isweak))

        addfunc(after_slots, self._afterfunc, 'after')
        addfunc(before_slots, self._beforefunc, 'before')
        addfunc(around_slots, self._aroundfunc, 'around')
        addfunc(onreturn_slots, self._onreturnfunc, 'onreturn')

        clist = self._choosefunc
        for c, f in choose_slots:
            if not iscallable(c) or not iscallable(f):
                raise TypeError('Detected non-callable element of choose sequence')
            found = self._find(f, clist)
            if found:
                i = found[0]
                cf = clist[i].choosefunc
                cfid = cid(cf)
                if cfid != cid(c):
                    cfunc = CallableWrapper(c, weak=wcf)
                    func = CallableWrapper(f, weak=isweak)
                    clist[i] = ChoiceObject(cfunc, func)
            if not found:
                cfunc = CallableWrapper(c, weak=wcf)
                func = CallableWrapper(f, weak=isweak)
                clist.append(ChoiceObject(cfunc, func))
        self.reload()
    # End def #}}}

    def disconnect(self, *after_slots, **other_slots): #{{{
        before_slots, around_slots, onreturn_slots, choose_slots, w, wcf = self._validate_connect_args(*after_slots, **other_slots)
        def delfunc(a, l):
            for f in a:
                found = self._find(f, l)
                if found:
                    del l[found[0]]
        delfunc(after_slots, self._afterfunc)
        delfunc(before_slots, self._beforefunc)
        delfunc(around_slots, self._aroundfunc)
        delfunc(onreturn_slots, self._onreturnfunc)
        delfunc(choose_slots, self._choosefunc)
        self.reload()
    # End def #}}}

    def disconnectAll(self): #{{{
        def delfunc(l):
            while l:
                l.pop()
        delfunc(self._afterfunc)
        delfunc(self._beforefunc)
        delfunc(self._aroundfunc)
        delfunc(self._onreturnfunc)
        delfunc(self._choosefunc)
        self.reload()
    # End def #}}}

    def _setpolicy(self, p): #{{{
        self._choosepolicy = p
    # End def #}}}

    def _setchooser(self, c): #{{{
        if c is None:
            return
        elif not iscallable(c):
            raise TypeError('chooser property must be a valid callable object')
        self._chooser = CallableWrapper(c, weak=False)
    # End def #}}}

    # Properties #{{{
    func = property(lambda s: s._func)
    beforefunc = property(lambda s: (i for i in s._beforefunc))
    afterfunc = property(lambda s: (i for i in s._afterfunc))
    aroundfunc = property(lambda s: (i for i in s._aroundfunc))
    onreturnfunc = property(lambda s: (i for i in s._onreturnfunc))
    choosefunc = property(lambda s: (i for i in s._choosefunc))
    valid = property(lambda s: not s._func.isdead)
    connected = property(lambda s: s._beforefunc and 
                                    s._afterfunc and 
                                    s._aroundfunc and 
                                    s._onreturnfunc and 
                                    s._choosefunc)
    chooserpolicy = property(lambda s: s._choosepolicy, lambda s, p: s._setpolicy(p))
    chooser = property(lambda s: s._chooser, lambda s, c: s._setchooser(c))
    # End properties #}}}

# End class #}}}
