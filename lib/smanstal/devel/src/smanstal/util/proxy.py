# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import (isclass, iscallable, 
        isfunction, isclassmethod, isbasemetaclass,
        isbuiltin, mro, numeric_methods_proxysafe)

__all__ = ('Proxy', 'proxy', 'MetaProxy')

class Proxy(object): #{{{
    __slots__ = ()
# End class #}}}

def isproxy(obj): #{{{
    try:
        object.__getattribute__(obj, '__proxyinst__')
    except AttributeError:
        return False
    else:
        return True
# End def #}}}

def _mkproxycallable(obj, name, wrap=tuple(), deco=None): #{{{
    def proxyfunc(self, *args, **kwargs): #{{{
#        print 'CALL', name, args
        ga = object.__getattribute__
        sa = object.__setattr__
        isga = name == '__getattribute__'
        issa = name == '__setattr__'
        if not isproxy(self):
            if isga:
                return ga(self, *args)
            elif issa:
                return sa(self, *args)
            return ga(self, name)(*args, **kwargs)
        args = tuple(getattr(a, '__proxyinst__', a) for a in args)
        kwargs = dict((k, getattr(v, '__proxyinst__', v)) for k, v in kwargs.iteritems())
        me_cls = ga(self, '__class__')
#        standard = ('__dict__', '__module__', '__doc__')
        found = False
        ret = None
#        if name == '__getattribute__' and not any(args[0] == n for n in standard):
        if isga:
            a = args[0]
            if any(a == n for cls in mro(me_cls) for n in cls.__dict__.keys()):
                try:
                    ret = ga(self, a)
                except AttributeError:
                    pass
                else:
                    found = True
        if not found or not iscallable(ret) or isclass(ret):
            curobj = ga(self, '__proxyinst__')
            if not found or (isga and hasattr(curobj, args[0])):
                ret = ga(curobj, name)(*args, **kwargs)
        if (ret is not None and not isinstance(ret, bool) and name in wrap and 
                (not isga or any(args == (n,) for n in wrap))):
            ret = proxy(ret)
        return ret
    # End def #}}}
    proxyfunc.__name__ = name
    if deco:
        proxyfunc = deco(proxyfunc)
    return proxyfunc
# End def #}}}

class MetaProxy(type): #{{{
    def __new__(cls, classname, bases, clsdict): #{{{
        if not isbasemetaclass(bases, cls):
            return super(MetaProxy, cls).__new__(cls, classname, bases, clsdict)
        obj = clsdict.pop('__proxyobj__')
        retproxy = tuple(n for n in clsdict.pop('__return_proxy__', tuple()))
        curobj = obj
        clsproxy = isclass(curobj)
        ga = object.__getattribute__
        block = ('__new__', '__init__', '__class__', '__name__', '__slots__')
        if clsproxy:
            def __init__(self, *args, **kwargs): #{{{
                object.__setattr__(self, '__proxyinst__', obj(*args, **kwargs))
            # End def #}}}
            clsdict['__init__'] = __init__
        objslots = getattr(curobj, '__slots__', None)
        curslots = clsdict['__slots__']
        if not isbuiltin(curobj) and (objslots is None or '__weakref__' in objslots):
            clsdict['__slots__'] += curslots + ('__weakref__',)
        for n in dir(curobj):
            if n in block:
                continue
            attr = getattr(curobj, n)
            if iscallable(attr) and not isclass(attr):
                res = None
                if isclassmethod(attr):
                    res = _mkproxycallable(obj, n, retproxy, classmethod)
                elif isfunction(attr):
                    res = _mkproxycallable(obj,n, retproxy, staticmethod)
                else:
                    res = _mkproxycallable(obj, n, retproxy)
                clsdict[n] = res
            else:
                clsdict[n] = attr
        return super(MetaProxy, cls).__new__(cls, classname, bases, clsdict)
    # End def #}}}
# End class #}}}

def proxy(obj, return_proxy=tuple()): #{{{
    class ObjectProxy(Proxy):
        __slots__ = ('__proxyinst__',)
        __metaclass__ = MetaProxy
        __proxyobj__ = obj
        __return_proxy__ = return_proxy
    if not isclass(obj):
        inst = ObjectProxy()
        object.__setattr__(inst, '__proxyinst__', obj)
        return inst
    return ObjectProxy
# End def #}}}
