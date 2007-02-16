# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# ==================================================================================
# Connect Helpers
# ==================================================================================
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
def mkcallback(self, name): #{{{
    def callback(obj):
        for ret in self._cleanlist(name): pass
    return callback
# End def #}}}
def addfunc(self, a, lname, reverse=False, **kwargs): #{{{
    isweak = bool(kwargs.get('weak', True))
    l, use_prio, prio, test_store = self._funclist[lname], None, float(-1), []
    if l:
        prio = l[-1][0]
    for f in a:                
        prio, use_prio = prio+1, test_prio(f, use_prio)
        if use_prio:
            prio, f = test_prio_type(f[0]), f[1]
        if not iscallable(f):
            seqname = lname
            if lname == 'after':
                seqname = ''.join([lname, '_slots'])
            raise TypeError('Detected non-callable element of %s sequence' %seqname)
        c = CallableWrapper(f, mkcallback(self, lname), weak=isweak)
        if lname == 'stream':
            # NEEDS WORK
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
def addchoosefunc(self, cslots, name): #{{{
    (clist, cleanfunc, test_store, 
            use_prio, prio) = (self._funclist[name], mkcallback(self, name),
                                [], None, float(-1))
    if clist:
        prio = clist[-1][0]
    for tup in cslots: #{{{
        use_prio, prio = test_prio(tup, use_prio, 3), prio+1
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

def _validate_connect_args(self, *args, **other_slots): #{{{
    expected = ('before', 'around', 'onreturn', 'choose', 'chooseret', 'stream', 'weak', 'weakcondf')
    if [i for i in other_slots if i not in expected]:
        raise ValueError('valid keyword arguments are: %s' %', '.join(expected))
    b = other_slots.get('before', tuple())
    a = other_slots.get('around', tuple())
    r = other_slots.get('onreturn', tuple())
    c = other_slots.get('choose', tuple())
    cr = other_slots.get('choosereturn', tuple())
    s = other_slots.get('stream', tuple())
    w = bool(other_slots.get('weak', True))
    wcf = bool(other_slots.get('weakcondf', w))
    return b, a, r, c, cr, s, w, wcf
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
