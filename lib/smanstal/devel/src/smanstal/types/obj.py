# Module: smanstal.types.obj
# File: obj.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

class attr(object): #{{{
    __slots__ = ('_obj', '_func')
    def __init__(self, obj, func=getattr): #{{{
        self._obj = obj
        self._func = func
    # End def #}}}

    def __call__(self, *args): #{{{
        obj, func = self._obj, self._func
        if not args:
            return obj
        ret = tuple(func(obj, a) for a in args)
        if len(ret) == 1:
            return ret[0]
        return ret
    # End def #}}}

    # Properties #{{{
    obj = property(lambda s: s._obj)
    func = property(lambda s: s._func)
    # End properties #}}}
# End class #}}}

class item(attr): #{{{
    __slots__ = ()
    def __init__(self, obj): #{{{
        super(item, self).__init__(obj, lambda o, x: o[x])
    # End def #}}}
# End class #}}}

class func(object): #{{{
    __slots__ = ('_funcs',)
    def __init__(self, *func): #{{{
        if [f for f in func if not hasattr(f, '__call__')]:
            raise TypeError("Non-callable object")
        self._funcs = func
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        funcs = self._funcs
        if len(funcs) == 1:
            return funcs[0](*args, **kwargs)
        return tuple(f(*args, **kwargs) for f in funcs)
    # End def #}}}

# End class #}}}
