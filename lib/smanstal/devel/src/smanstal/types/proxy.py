# Module: smastal.types.proxy
# File: proxy.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.collections.attrdict import attrdict
from smanstal.types.introspect import (iscallable, isclass, ismethod, isbuiltin, isbasemetaclass,
        isproperty, isclassmethod, isstaticmethod)
from smanstal.builtins import ogetattr, osetattr
from functools import wraps

__all__ = ('ProxyType', 'isproxy', 'proxy')
class ProxyType(object): #{{{
    __slots__ = ('__object__',)
# End class #}}}

def isproxy(obj): #{{{
    return isinstance(obj, ProxyType)
# End def #}}}

class CreateProxyType(object): #{{{
    __slots__ = ()
    def __call__(self, obj, **opts): #{{{
        return self.create_object_proxy(obj, opts)
    # End def #}}}

    def create_object_proxy(self, obj, opts): #{{{
        class ObjectProxy(ProxyType): 
            __slots__ = ()
            __metaclass__ = self.create_object_metaproxy(obj, opts)
        return ObjectProxy if isclass(obj) else ObjectProxy()
    # End def #}}}

    def convert_arg(self, arg): #{{{
        return ogetattr(arg, '__object__') if isproxy(arg) else arg
    # End def #}}}

    def create_proxy_func(self, obj, name, is_class=False, is_meth=True): #{{{
        conv = self.convert_arg
        def proxyfunc(*args, **kwargs): #{{{
            if is_meth and not is_class:
                args = args[1:]
            args = tuple(conv(a) for a in args)
            kwargs = dict((k, conv(v)) for k, v in kwargs.iteritems())
            return getattr(obj, name)(*args, **kwargs)
        # End def #}}}
        return proxyfunc
    # End def #}}}

    def create_object_metaproxy(self, obj, opts): #{{{
        objdict = attrdict(obj)
        is_class = isclass(obj)
        class MetaObjectProxy(type): #{{{
            def __new__(mpcls, classname, bases, clsdict): #{{{
                if isbasemetaclass(bases, mpcls):
                    is_builtin_object = isbuiltin(obj)
                    block = set(['__init__', '__new__', '__getattribute__']) | set(opts.get('block', ()))
                    for name, v in objdict.iteritems():
                        if name in block:
                            continue
                        if iscallable(v):
                            proxyfunc = self.create_proxy_func(obj, name, is_class, is_builtin_object or ismethod(v))
                            deco = lambda c: c
                            if isclassmethod(v):
                                deco = classmethod
                            elif not is_builtin_object and isstaticmethod(obj, name):
                                deco = staticmethod
                            clsdict[name] = deco(proxyfunc)
                        elif isproperty(v):
                            clsdict[name] = property(v.fget, v.fset, v.fdel, v.__doc__)
                        else:
                            clsdict[name] = v
                    conv = self.convert_arg
                    def __getattribute__(self, name): #{{{
                        if name not in objdict and name not in block:
                            return ogetattr(self, name)
                        return getattr(conv(self), '__getattribute__')(name)
                    # End def #}}}
                    clsdict['__getattribute__'] = __getattribute__
                    def init(self, *args, **kwargs): #{{{
                        inst = obj(*args, **kwargs) if is_class else obj
                        osetattr(self, '__object__', inst)
                    # End def #}}}
                    clsdict['__init__'] = init
                return super(MetaObjectProxy, mpcls).__new__(mpcls, classname, bases, clsdict)
            # End def #}}}
        # End class #}}}
        return MetaObjectProxy
    # End def #}}}
# End class #}}}

proxy = CreateProxyType()
