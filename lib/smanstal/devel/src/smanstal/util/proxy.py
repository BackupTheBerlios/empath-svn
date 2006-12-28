# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import (isclass, iscallable, 
        isfunction, isclassmethod, isbasemetaclass,
        isbuiltin, mro, dirdict, numeric_methods_proxysafe)

from functools import wraps

_ga = object.__getattribute__
_sa = object.__setattr__
_da = object.__delattr__
__all__ = ('Proxy', 'proxy', 'MetaProxy', 'isproxy')

class Proxy(object): #{{{
    __slots__ = ()
# End class #}}}

def isproxy(obj): #{{{
    try:
        _ga(obj, '__proxyinst__')
    except AttributeError:
        return False
    else:
        return True
# End def #}}}

def _mkproxycallable(func, funcname, isclass, wrap=(), deco=None, usewraps=True): #{{{
    def proxyfunc(self, *args, **kwargs): #{{{
        getp = lambda o: _ga(o, '__proxyinst__') if isproxy(o) else o
        args = tuple(getp(el) for el in args)
        obj = getp(self)
        ret = getattr(obj, funcname)(*args, **kwargs)
        if funcname in wrap:
            ret = proxy(ret)
        return ret
    # End def #}}}
    if deco:
        if usewraps:
            proxyfunc = wraps(func)(proxyfunc)
        proxyfunc = deco(proxyfunc)
    return proxyfunc
# End def #}}}

class MetaProxy(type): #{{{
    def __new__(cls, classname, bases, clsdict): #{{{
        if not isbasemetaclass(bases, cls):
            return super(MetaProxy, cls).__new__(cls, classname, bases, clsdict)
        proxyattr = clsdict.pop('proxyattr')
        curobj = proxyattr.proxyobj
        retproxy = proxyattr.return_proxy
        if not isinstance(retproxy, tuple):
            retproxy = tuple(retproxy)
        can_weakref = proxyattr.weakref
        clsproxy = isclass(curobj)
        proxyinst = None
        if clsproxy:
            proxyinst = {}

        # Set setattr
        temp_attr = {}
        def __setattr__(self, name, val): #{{{
            try:
                obj = _ga(self, '__proxyinst__')
            except KeyError:
                obj = curobj
            if clsproxy and obj is curobj:
                sid = id(self)
                vars = temp_attr.setdefault(sid, {})
                vars[name] = val
            else:
                try:
                    setattr(obj, name, val)
                except AttributeError:
                    _sa(self, name, val)
        # End def #}}}
        def __delattr__(self, name): #{{{
            try:
                obj = _ga(self, '__proxyinst__')
            except KeyError:
                obj = curobj
            if clsproxy and obj is curobj:
                sid = id(self)
                vars = temp_attr.setdefault(sid, {})
                try:
                    vars.pop(name)
                except KeyError:
                    raise AttributeError()
            else:
                try:
                    delattr(obj, name)
                except AttributeError:
                    if name in dir(self):
                        _da(self, name)
                    else:
                        raise
        # End def #}}}
        clsdict['__setattr__'] = __setattr__
        clsdict['__delattr__'] = __delattr__

        instblock = ('__new__', '__init__', '__getattribute__', '__setattr__', 
                        '__delattr__')
        instblock_retproxy = instblock + retproxy
        block = ('__class__', '__slots__', '__proxyinst__') + instblock

        # Set getattribute
        def __getattribute__(self, name): #{{{
            sid = id(self)
            if proxyinst is None:
                obj = curobj
            else:
                obj = proxyinst.get(sid, curobj)
#            obj = _ga(self, '__proxyinst__')
            if clsproxy:
                if obj is curobj:
                    vars = temp_attr.setdefault(sid, {})
                    if name in vars:
                        return vars[name]
            if name == '__class__' and not clsproxy:
                return _ga(obj, name)
            try:
                ret = _ga(self, name)
            except AttributeError:
                ret = _ga(obj, name)
            return ret
        # End def #}}}
        clsdict['__getattribute__'] = __getattribute__


        clsdict['__proxyinst__'] = property(lambda s: curobj)
        if clsproxy:
#            proxyinst = {}
            def __init__(self, *args, **kwargs): #{{{
                sid = id(self)
                proxyinst[sid] = inst = curobj(*args, **kwargs)
                vars = temp_attr.setdefault(sid, {})
                pi = vars.popitem
                while vars:
                    setattr(self, *pi())
                temp_attr.pop(sid)
            # End def #}}}
            clsdict['__init__'] = __init__
            clsdict['__proxyinst__'] = property(lambda s: proxyinst[id(s)])
        if can_weakref:
            objslots = getattr(curobj, '__slots__', None)
            curslots = clsdict['__slots__']
            if not isbuiltin(curobj) and (objslots is None or '__weakref__' in objslots):
                clsdict['__slots__'] += curslots + ('__weakref__',)
        attrblock = block if clsproxy else instblock
        for n in dir(curobj):
            if n in attrblock:
                continue
            attr = getattr(curobj, n)
            if iscallable(attr) and not isclass(attr):
                res = None
                if isclassmethod(attr):
                    res = _mkproxycallable(attr, n, clsproxy, retproxy, classmethod)
                elif isfunction(attr):
                    res = _mkproxycallable(attr,n, clsproxy, retproxy, staticmethod)
                else:
                    res = _mkproxycallable(attr, n, clsproxy, retproxy, usewraps=False)
                clsdict[n] = res
            else:
                clsdict[n] = attr
        if clsproxy:
            classname = curobj.__name__
        return super(MetaProxy, cls).__new__(cls, classname, bases, clsdict)
    # End def #}}}
# End class #}}}

def proxy(obj, ret_proxy=(), wref=False): #{{{
    class ObjectProxy(Proxy):
        __slots__ = ()
        __metaclass__ = MetaProxy
        class proxyattr(object):
            proxyobj = obj
            return_proxy = ret_proxy
            weakref = wref
    if not isclass(obj):
        inst = ObjectProxy()
        return inst
    return ObjectProxy
# End def #}}}

#def _mkproxycallable(obj, name, wrap=tuple(), deco=None): #{{{
#    def proxyfunc(self, *args, **kwargs): #{{{
##        print 'CALL', name, args
#        ga = object.__getattribute__
#        sa = object.__setattr__
#        isga = name == '__getattribute__'
#        issa = name == '__setattr__'
##        if not isproxy(self):
##            if isga:
##                return ga(self, *args)
##            elif issa:
##                return sa(self, *args)
##            return ga(self, name)(*args, **kwargs)
#        args = tuple(getattr(a, '__proxyinst__', a) for a in args)
#        kwargs = dict((k, getattr(v, '__proxyinst__', v)) for k, v in kwargs.iteritems())
#        me_cls = ga(self, '__class__')
##        standard = ('__dict__', '__module__', '__doc__')
#        found = False
#        ret = None
##        if name == '__getattribute__' and not any(args[0] == n for n in standard):
#        if isga:
#            a = args[0]
#            if any(a == n for cls in mro(me_cls) for n in cls.__dict__.keys()):
#                try:
#                    ret = ga(self, a)
#                except AttributeError:
#                    pass
#                else:
#                    found = True
#        if not found or not iscallable(ret) or isclass(ret):
#            curobj = ga(self, '__proxyinst__')
#            if not found or (isga and hasattr(curobj, args[0])):
#                ret = ga(curobj, name)(*args, **kwargs)
#        if (ret is not None and not isinstance(ret, bool) and name in wrap and 
#                (not isga or any(args == (n,) for n in wrap))):
#            ret = proxy(ret)
#        return ret
#    # End def #}}}
#    proxyfunc.__name__ = name
#    if deco:
#        proxyfunc = deco(proxyfunc)
#    return proxyfunc
## End def #}}}

#class MetaProxy(type): #{{{
#    def __new__(cls, classname, bases, clsdict): #{{{
#        if not isbasemetaclass(bases, cls):
#            return super(MetaProxy, cls).__new__(cls, classname, bases, clsdict)
#        obj = clsdict.pop('__proxyobj__')
#        retproxy = tuple(n for n in clsdict.pop('__return_proxy__', tuple()))
#        curobj = obj
#        clsproxy = isclass(curobj)
#        ga = object.__getattribute__
#        block = ('__new__', '__init__', '__class__', '__name__', '__slots__', '__proxyinst__')
#        if clsproxy:
#            def __init__(self, *args, **kwargs): #{{{
#                object.__setattr__(self, '__proxyinst__', obj(*args, **kwargs))
#            # End def #}}}
#            clsdict['__init__'] = __init__
#        objslots = getattr(curobj, '__slots__', None)
#        curslots = clsdict['__slots__']
#        if not isbuiltin(curobj) and (objslots is None or '__weakref__' in objslots):
#            clsdict['__slots__'] += curslots + ('__weakref__',)
#        for n in dir(curobj):
#            if n in block:
#                continue
#            attr = getattr(curobj, n)
#            if iscallable(attr) and not isclass(attr):
#                res = None
#                if isclassmethod(attr):
#                    res = _mkproxycallable(obj, n, retproxy, classmethod)
#                elif isfunction(attr):
#                    res = _mkproxycallable(obj,n, retproxy, staticmethod)
#                else:
#                    res = _mkproxycallable(obj, n, retproxy)
#                clsdict[n] = res
#            else:
#                clsdict[n] = attr
#        return super(MetaProxy, cls).__new__(cls, classname, bases, clsdict)
#    # End def #}}}
## End class #}}}

#def proxy(obj, return_proxy=tuple()): #{{{
#    class ObjectProxy(Proxy):
#        __slots__ = ('__proxyinst__',)
#        __metaclass__ = MetaProxy
#        __proxyobj__ = obj
#        __return_proxy__ = return_proxy
#    if not isclass(obj):
#        inst = ObjectProxy()
#        object.__setattr__(inst, '__proxyinst__', obj)
#        return inst
#    return ObjectProxy
## End def #}}}

