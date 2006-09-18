# Module: aossi.signal
# File: signal.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('Signal',)

from aossi.impex import import_, CopyModuleImporter
_ab = import_(':aossi:__builtin__', importer=CopyModuleImporter(copy_prefix=':aossi:'))
property = _ab.property

from warnings import warn

from aossi.cwrapper import CallableWrapper, cid
from aossi.misc import iscallable, ChooseCallable, ChoiceObject

def callfunc(sig, func, functype, pass_ret, ret, *args, **kwargs): #{{{
    sfunc = sig.func
    if pass_ret:
        kwargs = {}
        args = (ret,)
    # Going from a method signal to any callable, 
    # remove the `self` argument if required
    elif sfunc.ismethod and _ab.len(args) >= sfunc.maxargs:
        obj = sfunc._object()
        fo = func._object
        if fo:
            fo = fo()
        if fo != obj and fo != obj.__class__:
            args = args[1:]
    return func(*args, **kwargs)
# End def #}}}

class Signal(object): #{{{
    __slots__ = ('__weakref__', '_func', '_beforefunc', '_afterfunc', 
                    '_aroundfunc', '_onreturnfunc', '_choosefunc', 
                    '_chooseretfunc', '_streamfunc', '_chooser', '_retchooser', 
                    '_choosepolicy', '_chooseretpolicy', '__name__',
                    '_active', '_callactivate', '_caller')
    def __init__(self, signal, **kwargs): #{{{
        if not iscallable(signal):
            raise TypeError("Argument must be callable.");
        expected = ('weak', 'active', 'activate_on_call')
        found = [kw for kw in kwargs if kw not in expected]
        if found:
            raise ValueError("Detected unexpected arguments: %s" %', '.join([found]))
        weak = kwargs.get('weak', True)
        self._func = CallableWrapper(signal, weak=weak)
        self.__name__ = self._func.__name__
        self._beforefunc = []
        self._afterfunc = []
        self._aroundfunc = []
        self._onreturnfunc = []
        self._choosefunc = []
        self._chooseretfunc = []
        self._streamfunc = []
        self.chooser = ChooseCallable
        self.return_chooser = ChooseCallable
        self._choosepolicy = None
        self._chooseretpolicy = None
        self._active = kwargs.get('active', True)
        self._callactivate = kwargs.get('activate_on_call', False)
        self.caller = callfunc
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        if not self.valid:
            warn('Calling an invalid signal', RuntimeWarning, stacklevel=2)
            return
        if self.activate_on_call:
            self.active = True
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

    def _cleanchooseret(self, obj): #{{{
        for ret in self._cleanlist(self._chooseretfunc):
            pass
    # End def #}}}

    def _cleanstream(self, obj): #{{{
        for ret in self._cleanlist(self._streamfunc):
            pass
    # End def #}}}

    def _cleanlist(self, l): #{{{
        llen = l.__len__()
        i = 0
        while i < llen:
            prio, func = l[i]
            if func.isdead:
                del l[i]
                llen -= 1
            else:
                yield prio, func, i
                i += 1
    # End def #}}}

    def _generate_wrapfactory(self): #{{{
        cleanlist = self._cleanlist
        callfunc = self.caller
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
                gen = ((i.choosefunc, i.callable) for p, i, t in cleanlist(chooselist))
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
        def do_wrap(func): #{{{
            def newcall(s, *args, **kwargs): #{{{
                # Before
                for p, bfunc, t in cleanlist(self._beforefunc):
                    callfunc(self, bfunc, 'before', False, None, *args, **kwargs)

                # Choose function
                func_choice = choice(self, self._choosefunc, 'chooser', self.chooserpolicy, func, False, None, *args, **kwargs)
                ret = callchoice(self, func, func_choice, False, None, *args, **kwargs)

                # Choose return
                ret_choice = choice(self, self._chooseretfunc, 'return_chooser', self.retchooserpolicy, func, True, ret, *args, **kwargs)
                ret = callchoice(self, func, ret_choice, True, ret, *args, **kwargs)

                # Stream
                for p, sfunc, t in cleanlist(self._streamfunc):
                    ret = callfunc(self, sfunc, 'stream', True, ret, *args, **kwargs)

                # Other
                for p, afunc, t in cleanlist(self._afterfunc):
                    callfunc(self, afunc, 'after', False, None, *args, **kwargs)
                for p, rfunc, t in cleanlist(self._onreturnfunc):
                    callfunc(self, rfunc, 'onreturn', True, ret, *args, **kwargs)
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
        for p, cfunc, t in cleanlist(self._choosefunc):
            cfunc.callable.unwrap()
        for p, arfunc, t in cleanlist(self._aroundfunc):
            for p, cfunc, t in cleanlist(self._choosefunc):
                cfunc.callable.wrap(arfunc)
            self._func.wrap(arfunc)
        do_wrap = self._generate_wrapfactory()
        self._func.wrap(do_wrap)
        self._active = True
    # End def #}}}

    def _validate_connect_args(self, *args, **other_slots): #{{{
        expected = ('before', 'around', 'onreturn', 'choose', 'chooseret', 'stream', 'weak', 'weakcondf')
        if [i for i in other_slots if i not in expected]:
            raise ValueError('valid keyword arguments are: %s' %', '.join(expected))
        b = other_slots.get('before', tuple())
        a = other_slots.get('around', tuple())
        r = other_slots.get('onreturn', tuple())
        c = other_slots.get('choose', tuple())
        cr = other_slots.get('chooseret', tuple())
        s = other_slots.get('stream', tuple())
        w = bool(other_slots.get('weak', True))
        wcf = bool(other_slots.get('weakcondf', w))
        return b, a, r, c, cr, s, w, wcf
    # End def #}}}

    def _find(self, func, siglistseq=None, choosercid=None): #{{{
        ischooselist = lambda l: l is self._choosefunc or l is self._chooseretfunc
        temp_siglistseq = (self._afterfunc, self._beforefunc, self._aroundfunc, 
                            self._onreturnfunc, self._choosefunc, self._chooseretfunc, self._streamfunc)
        siglistseq = (siglistseq,)
        if siglistseq[0] not in temp_siglistseq:
            siglistseq = temp_siglistseq
        foundindex = None
        foundlist = None
        foundprio = None
        fid = cid(func)
        for siglist in siglistseq:
            for prio, f, index in self._cleanlist(siglist):
                if f.cid == fid:
                    if choosercid and ischooselist(siglist):
                        if choosercid != f.choosefunc.cid:
                            continue
                    foundindex = index
                    foundlist = siglist
                    foundprio = prio
                    break
            else:
                continue
            break
        if foundindex is not None:
            return foundindex, foundlist, foundprio
        return None

    # End def #}}}

    def connect(self, *after_slots, **other_slots): #{{{
        getattr = _ab.getattr
        activate = self.activate_on_call
        self.activate_on_call = False
        vargs = (before_slots, around_slots, onreturn_slots, choose_slots, chooseret_slots,
                stream_slots, isweak, wcf) = self._validate_connect_args(*after_slots, **other_slots)
        if False not in (not a for a in vargs[:-2]):
            return
#        if (not after_slots and not before_slots and not around_slots and 
#                not onreturn_slots and not choose_slots and not chooseret_slots and not stream_slots):
#            return

        def have_prio(f, size=2):
            return isinstance(f, tuple) and len(f) == size
        def sort_key(x):
            return x[0]
        def test_prio(tup, use_prio, size=2): #{{{
            cur_prio = None
            if use_prio is None:
                use_prio = cur_prio = have_prio(tup, size)
            else:
                cur_prio = have_prio(tup, size)
            if use_prio and not cur_prio:
                raise TypeError("Expected 2-tuple (priority, callable), received %s" %str(type(tup)))
            elif not use_prio and cur_prio:
                raise TypeError("Expected callable, got 2-tuple (priority, callable) instead")
            return use_prio
        # End def #}}}
        def test_prio_type(prio): #{{{
            expected = (int, long, float)
            got = [t for t in expected if not isinstance(prio, t)]
            if got == expected:
                raise TypeError("Got unexpected type %s" %str(type(prio)))
            return float(prio)
        # End def #}}}
        def addfunc(a, l, lname, reverse=False): #{{{
            use_prio = None
            prio = float(-1)
            if l:
                prio = l[-1][0]
            test_store = []
            for f in a:                
                use_prio = test_prio(f, use_prio)
                prio += 1
                if use_prio:
                    prio, f = test_prio_type(f[0]), f[1]
                if not iscallable(f):
                    seqname = lname
                    if lname == 'after':
                        seqname = ''.join([lname, '_slots'])
                    raise TypeError('Detected non-callable element of %s sequence' %seqname)
                c = CallableWrapper(f, getattr(self, '_clean%s' %lname), weak=isweak)
                if lname == 'stream':
                    if not c.numargs or c.numargs > 2:
                        raise ValueError('Stream functions must accept a single value')
                found = self._find(f, l)
                if found: 
                    if found[2] != prio:
                        l[found[0]] = (prio, c)
                else:
                    test_store.append((prio, c))
            if test_store:
                l.extend(test_store)
            l.sort(key=sort_key, reverse=reverse)
        # End def #}}}

        addfunc(after_slots, self._afterfunc, 'after')
        addfunc(before_slots, self._beforefunc, 'before')
        addfunc(around_slots, self._aroundfunc, 'around', reverse=True)
        addfunc(onreturn_slots, self._onreturnfunc, 'onreturn')

        def addchoosefunc(clist, cslots, name): #{{{
            cleanfunc = getattr(self, '_clean%s' %name)
            test_store = []
            use_prio = None
            prio = float(-1)
            if clist:
                prio = clist[-1][0]
            for tup in cslots: #{{{
                use_prio = test_prio(tup, use_prio, 3)
                prio += 1
                c = f = None
                if use_prio:
                    prio, c, f = test_prio_type(f[0]), f[1], f[2]
                else:
                    c, f = tup
                if not iscallable(c) or not iscallable(f):
                    raise TypeError('Detected non-callable element of choose sequence')
                found = self._find(f, clist)
                if found:
                    i = found[0]
                    cf = clist[i].choosefunc
                    cfid = cid(cf)
                    if cfid != cid(c) or found[2] != prio:
                        cfunc = CallableWrapper(c, cleanfunc, weak=wcf)
                        func = CallableWrapper(f, cleanfunc, weak=isweak)
                        clist[i] = (prio, ChoiceObject(cfunc, func))
                if not found:
                    cfunc = CallableWrapper(c, cleanfunc, weak=wcf)
                    func = CallableWrapper(f, cleanfunc, weak=isweak)
                    test_store.append((prio, ChoiceObject(cfunc, func)))
            # End for #}}}
            if test_store:
                clist.extend(test_store)
            clist.sort(key=sort_key)
        # End def #}}}
        addchoosefunc(self._choosefunc, choose_slots, 'choose')
        addchoosefunc(self._chooseretfunc, chooseret_slots, 'chooseret')
        addfunc(stream_slots, self._streamfunc, 'stream')
        self.activate_on_call = activate
        if self.active:
            self.reload()
    # End def #}}}

    def disconnect(self, *after_slots, **other_slots): #{{{
        vargs = (before_slots, around_slots, onreturn_slots, choose_slots, chooseret_slots, 
                stream_slots, w, wcf) = self._validate_connect_args(*after_slots, **other_slots)
        noargs = False not in (not a for a in vargs[:-2])
#        noargs = not after_slots and not other_slots
        def delfunc(a, l):
            if noargs:
                while l:
                    l.pop()
                return
            for f in a:
                found = self._find(f, l)
                if found:
                    del l[found[0]]
        delfunc(after_slots, self._afterfunc)
        delfunc(before_slots, self._beforefunc)
        delfunc(around_slots, self._aroundfunc)
        delfunc(onreturn_slots, self._onreturnfunc)
        delfunc(choose_slots, self._choosefunc)
        delfunc(chooseret_slots, self._chooseretfunc)
        delfunc(stream_slots, self._streamfunc)
        if self.active:
            self.reload()
    # End def #}}}

    def priority(self, **kwargs): #{{{
        if not kwargs:
            raise ValueError('Missing required keyword arguments')
        expected = ('after', 'before', 'around', 'onreturn', 'choose', 'chooseret', 'stream')
        unexpected = [kw for kw in kwargs if kw not in expected]
        if unexpected:
            raise ValueError("Unexpected keyword arguments detected: %s" %', '.join(unexpected))
        ret = {}
        for kw, val in kwargs.iteritems():
            lname = '_%sfunc' %kw
            if not iscallable(val):
                raise TypeError('Detected non-callable for %s keyword argument' %kw)
            found = self._find(val, getattr(self, lname))
            if not found:
                raise ValueError("Callable not found")
            ret[kw] = found[2]
        if len(ret) == 1:
            return ret.values()[0]
        return ret
    # End def #}}}

    def _setpolicy(self, name, p): #{{{
        setattr(self, name, p)
#        self._choosepolicy = p
    # End def #}}}

    def _setchooser(self, name, c): #{{{
        if c is None:
            return
        elif not iscallable(c):
            raise TypeError('chooser property must be a valid callable object')
        setattr(self, name, CallableWrapper(c, weak=False))
#        self._chooser = CallableWrapper(c, weak=False)
    # End def #}}}

    def _setactive(self, v): #{{{
        orig = self._active
        v = bool(v)
        self._active = v
        if orig and not v:
            self._func.unwrap()
        elif not orig and v:
            self.reload()
    # End def #}}}

    def _setcallactivate(self, v): #{{{
        self._callactivate = bool(v)
    # End def #}}}

    def _setcaller(self, c): #{{{
        if c is None:
            return
        elif not iscallable(c):
            raise TypeError('caller property must be a valid callable object')
        self._caller = CallableWrapper(c, weak=False)
    # End def #}}}


    # Properties #{{{
    func = property(lambda s: s._func)
    beforefunc = property(lambda s: (i for i in s._beforefunc))
    afterfunc = property(lambda s: (i for i in s._afterfunc))
    aroundfunc = property(lambda s: (i for i in s._aroundfunc))
    onreturnfunc = property(lambda s: (i for i in s._onreturnfunc))
    choosefunc = property(lambda s: (i for i in s._choosefunc))
    valid = property(lambda s: not s._func.isdead)
    connected = property(lambda s: bool(s._beforefunc or
                                    s._afterfunc or
                                    s._aroundfunc or
                                    s._onreturnfunc or
                                    s._choosefunc or
                                    s._chooseretfunc or
                                    s._streamfunc))
    chooserpolicy = property(lambda s: s._choosepolicy, lambda s, p: s._setpolicy('_choosepolicy', p))
    retchooserpolicy = property(lambda s: s._choosepolicy, lambda s, p: s._setpolicy('_chooseretpolicy', p))
    chooser = property(lambda s: s._chooser, lambda s, c: s._setchooser('_chooser', c))
    return_chooser = property(lambda s: s._retchooser, lambda s, c: s._setchooser('_retchooser', c))
    active = property(lambda s: s._active, lambda s, v: s._setactive(v))
    activate_on_call = property(lambda s: s._callactivate, lambda s, v: s._setcallactivate(v))
    caller = property(lambda s: s._caller, lambda s, c: s._setcaller(c))
    original = property(lambda s: s._func.original)
    # End properties #}}}

# End class #}}}
