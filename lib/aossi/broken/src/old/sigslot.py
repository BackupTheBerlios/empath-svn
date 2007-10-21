# Module: aossi.sigslot
# File: sigslot.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('connect', 'disconnect', 'import')
from weakref import ref
from warnings import warn
from types import MethodType as method
from inspect import getargspec, isfunction as _isf, ismethod as _ism

METHODTYPE_NOTMETHOD = 0
METHODTYPE_UNBOUND = 1
METHODTYPE_CLASS = 2
METHODTYPE_INSTANCE = 3

class AmbiguousChoiceError(StandardError): pass

def iscallable(obj): #{{{
    if not callable(obj):
        return False
    elif _ism(obj) or _isf(obj):
        return True
    elif isinstance(obj, type(str.__call__)):
        return False
    elif hasattr(obj, '__call__'):
        return iscallable(obj.__call__)
    return False
# End def #}}}

def num_static_args(obj): #{{{
    if not iscallable(obj):
        return -1
    if _ism(obj):
        obj = obj.im_func
    if isinstance(obj, CallableWrapper):
        return obj._numargs
    if not _isf(obj):
        obj = obj.__call__
    argspec = getargspec(obj)
    l, d = len(argspec[0]), argspec[3]
    if d:
        l -= len(d)
    return l
# End def #}}}

def cid(obj): #{{{
    if isinstance(obj, CallableWrapper) or isinstance(obj, ChoiceObject):
        return obj.cid
    return hash(obj)
# End def #}}}

def methodtype(obj): #{{{
    if not _ism(obj):
        return METHODTYPE_NOTMETHOD
    elif obj.im_self is None:
        if obj.im_class is None:
            return METHODTYPE_UNBOUND
        return METHODTYPE_CLASS
    else:
        return METHODTYPE_INSTANCE
# End def #}}}

def methodname(obj): #{{{
    o = None
    mt = methodtype(obj)
    if mt == METHODTYPE_CLASS:
        o = obj.im_class
    elif mt == METHODTYPE_INSTANCE:
        o = obj.im_self
    else:
        return
    for i in dir(o):
        if getattr(o, i) == obj:
            return i
# End def #}}}

class cref(object): #{{{
    __slots__ = ('_ref', '_isweak', '__weakref__')
    def __init__(self, obj, callback=None, **kwargs): #{{{
        weak = bool(kwargs.get('weak', True))
        self._ref = obj
        self._isweak = weak
        if weak:
            self._ref = ref(obj, callback)
    # End def #}}}

    def __call__(self): #{{{
        if self._isweak:
            return self._ref()
        return self._ref
    # End def #}}}

    # Properties #{{{
    isweak = property(lambda s: s._isweak)
    ref = property(lambda s: s._ref)
    # End properties #}}}
# End class #}}}


class CallableWrapper(object): #{{{
    __slots__ = ('__weakref__', '_object', '_function', '_newcall', '_numargs', '_funcid')
    def __init__(self, obj, callback=None, **kwargs): #{{{
        if not iscallable(obj):
            raise TypeError('Argument must be a valid callable object')
        elif callback is not None and not callable(callback):
            raise TypeError('callback argument must be a callable object')

        self._object = None
        self._function = None
        self._newcall = self.call
        self._numargs = num_static_args(obj)
        isweak = bool(kwargs.get('weak', True))

        mtype = methodtype(obj)
        if mtype not in (METHODTYPE_NOTMETHOD, METHODTYPE_UNBOUND):
            o = obj.im_class
            if mtype == METHODTYPE_INSTANCE:
                o = obj.im_self
            self._object = cref(o, callback, weak=isweak)
            self._function = obj.im_func
        else:
            self._function = cref(obj, callback, weak=isweak)
        self._funcid = cid(obj)
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        if self._isdead():
            warn('Calling a dead wrapper', RuntimeWarning, stacklevel=2)
            return
        elif self._newcall:
            return self._newcall(*args, **kwargs)

        return self.call(*args, **kwargs)
    # End def #}}}

    def call(self, *args, **kwargs): #{{{
        f = self._getcallable()
        # If being called directly as a method instance and
        # no args got passed in i.e. no self reference,
        # add the object reference.
        if len(args) == self._numargs - 1:
            return f(self._object(), *args, **kwargs)
        else:
            return f(*args, **kwargs)
    # End def #}}}

    def unwrap(self): #{{{
        self._newcall = self.call
    # End def #}}}

    def wrap(self, func): #{{{
        if not iscallable(func):
            raise TypeError('Argument must be a valid callable object')
        newfunc = func(self._newcall)
        if not iscallable(newfunc):
            raise TypeError('Return value of wrapping callable must be a valid callable object')
        if not _ism(newfunc):
            newfunc = method(newfunc, self, self.__class__)
        self._newcall = newfunc
    # End def #}}}

    def _isdead(self): #{{{
        return self._getcallable() is None
    # End def #}}}

    def _getcallable(self): #{{{
        if self._object is None:
            return self._function()
        elif self._object() is None:
            return None
        return self._function
    # End def #}}}
    
    # Properties #{{{
    numargs = property(lambda s: s._numargs)
    isdead = property(lambda s: s._isdead())
    callable = property(lambda s: s._getcallable())
    cid = property(lambda s: s._funcid)
    # End properties #}}}
# End class #}}}

def ChooseCallable(choices, policy, *args, **kwargs): #{{{
    found = []
    for chooser, func in choices: #{{{
        if chooser(*args, **kwargs):
            if policy == 'first':
                return func
            found.append(func)
    if found:
        flen = len(found)
        if policy == 'last':
            return found[-1]
        elif flen == 1:
            return found[0]
        elif flen > 1:
            if policy == 'default':
                return None
        raise AmbiguousChoiceError('Found more than one selectable callable')
    return None
    # End for #}}}
# End def #}}}

class ChoiceObject(object): #{{{
    __slots__ = ('_choosefunc', '_func')
    def __init__(self, choosefunc, func): #{{{
        self._choosefunc = choosefunc
        self._func = func
    # End def #}}}

    # Properties #{{{
    choosefunc = property(lambda s: s._choosefunc)
    callable = property(lambda s: s._func)
    cid = property(lambda s: s._func.cid)
    isdead = property(lambda s: s._func.isdead or s._choosefunc.isdead)
    # End properties #}}}
# End class #}}}

class Signal(object): #{{{
    __slots__ = ('__weakref__', '_func', '_beforefunc', '_afterfunc', 
                    '_aroundfunc', '_onreturnfunc', '_choosefunc', 
                    '_chooser', '_choosepolicy')
    def __init__(self, signal): #{{{
        if not iscallable(signal):
            raise TypeError("Argument must be callable.");
        self._func = CallableWrapper(signal)
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
                    choice = self.chooser(gen, self.chooserpolicy, *args, **kwargs)
                if not choice:
                    choice = func
                ret = choice(*args, **kwargs)
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
        expected = ('before', 'around', 'onreturn', 'choose', 'weak')
        if [i for i in other_slots if i not in expected]:
            raise ValueError('valid keyword arguments are: %s' %', '.join(expected))
        b = other_slots.get('before', tuple())
        a = other_slots.get('around', tuple())
        r = other_slots.get('onreturn', tuple())
        c = other_slots.get('choose', tuple())
        w = bool(other_slots.get('weak', True))
        return b, a, r, c, w
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
        before_slots, around_slots, onreturn_slots, choose_slots, isweak = self._validate_connect_args(*after_slots, **other_slots)
        if not after_slots and not before_slots and not around_slots and not onreturn_slots and not choose_slots:
            return
        def addfunc(a, l, lname):
            for f in a:
                if not iscallable(f):
                    seqname = lname
                    if lname == 'after':
                        seqname += '_slots'
                    raise TypeError('Detected non-callable element of %s sequence' %seqname)
                found = self._find(f, l)
                if not found:
                    l.append(CallableWrapper(f, eval('self._clean%s' %lname), weak=isweak))

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
                    cfunc = CallableWrapper(c, weak=isweak)
                    func = CallableWrapper(f, weak=isweak)
                    clist[i] = ChoiceObject(cfunc, func)
            if not found:
                cfunc = CallableWrapper(c, weak=isweak)
                func = CallableWrapper(f, weak=isweak)
                clist.append(ChoiceObject(cfunc, func))
        self.reload()
    # End def #}}}

    def disconnect(self, *after_slots, **other_slots): #{{{
        before_slots, around_slots, onreturn_slots, choose_slots, w = self._validate_connect_args(*after_slots, **other_slots)
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

    def _setpolicy(self, p): #{{{
        self._choosepolicy = p
    # End def #}}}

    def _setchooser(self, c): #{{{
        if not iscallable(c):
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

# Signal-slot map
# Keep track of:
#   - original function
#   - new function
#   - all before functions
#   - all after functions
#   - all wrapping functions
_ssmap = []

def _find(signal): #{{{
    pass
# End def #}}}

def connect(object, signal_name, *after_slots, **other_slots): #{{{
    pass
# End def #}}}

def disconnect(object, signal_name, *after_slots, **other_slots): #{{{
    pass
# End def #}}}

def import_(*names, **from_names): #{{{
    pass
# End def #}}}


