# Module: smanstal.types.multivalue
# File: multivalue.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import iscallable
from smanstal.types.mdict import mdict

from smanstal.builtins import ogetattr, osetattr

from weakref import ref

__all__ = ('MultiValueProperties', 'MultiValueValues', 'MultiValue', 'AnyValue', 'AllValues', 
            'EvalMixin', 'EvalMixinProperties', 'AnyResult', 'AllResults')

class MultiValueProperties(object): #{{{
    __slots__ = ('_mval',)
    def __init__(self, mval=None): #{{{
        if mval is not None:
            if not isinstance(mval, MultiValue) or not isinstance(self, mval.__class__.p.__class__):
                raise TypeError("Cannot use %s object as a multivalue" %mval.__class__.__name__)
            self._mval = ref(mval)
    # End def #}}}

    def __get__(self, inst, owner): #{{{
        return self.__class__(inst)
    # End def #}}}

    def _get_mval(self, raw=True): #{{{
        mval = self._mval()
        mvaldict = mval._mval
        if raw:
            mval = dict(mvaldict)
        else:
            tfunc = mval._tfunc
            mval = dict((k, tfunc(k, v)) for k, v in mvaldict.iteritems())
        return mval
    # End def #}}}

    def _getset_transformer(self, *args): #{{{
        mval = self._mval()
        if not args:
            func = mval._tfunc
            return func
        func = args[0]
        if not iscallable(func):
            raise TypeError("Transform function is not callable")
#        object.__setattr__(mval, '_tfunc', func)
        osetattr(mval, '_tfunc', func)
    # End def #}}}

    def _getset_eqfunc(self, *args): #{{{
        mval = self._mval()
        if not args:
            func = mval._eqfunc
            return func
        func = args[0]
        if not iscallable(func):
            raise TypeError("Equals function is not callable")
#        object.__setattr__(mval, '_eqfunc', func)
        osetattr(mval, '_eqfunc', func)
    # End def #}}}

    raw = property(lambda s: s._get_mval())
    mval = property(lambda s: s._get_mval(False))
    transformer = property(lambda s: s._getset_transformer(), lambda s, v: s._getset_transformer(v))
    eqfunc = property(lambda s: s._getset_eqfunc(), lambda s, v: s._getset_eqfunc(v))
# End class #}}}

class MultiValueValues(object): #{{{
    __slots__ = ('_mval',)
    def __init__(self, mval=None): #{{{
        if mval is not None:
            if not isinstance(mval, MultiValue) or not isinstance(self, mval.__class__.v.__class__):
                raise TypeError("Cannot use %s object as an multivalue" %mval.__class__.__name__)
#            object.__setattr__(self, '_mval', ref(mval))
            osetattr(self, '_mval', ref(mval))
    # End def #}}}

    def __get__(self, inst, owner): #{{{
        return self.__class__(inst)
    # End def #}}}

    def __getattribute__(self, name): #{{{
        if name in dir(object) + ['__get__', '__getitem__']:
            return object.__getattribute__(self, name)
#        mval = object.__getattribute__(self, '_mval')()
        mval = ogetattr(self, '_mval')()
        try:
            return mval.p.transformer(name, mval._mval[name])
        except KeyError:
#            return object.__getattribute__(self, name)
            return ogetattr(self, name)
    # End def #}}}

    def __getitem__(self, key): #{{{
#        mval = object.__getattribute__(self, '_mval')()
        mval = ogetattr(self, '_mval')()
        return mval.p.transformer(key, mval._mval[key])
    # End def #}}}

    def __delattr__(self, name): #{{{
        raise AttributeError("Attribute '%s' is read-only" %name)
    # End def #}}}

    def __setattr__(self, name, val): #{{{
        raise AttributeError("Attribute '%s' is read-only" %name)
    # End def #}}}

# End class #}}}

class MultiValue(object): #{{{
    __slots__ = ('_mval', '_tfunc', '_eqfunc', '__weakref__')
    def __init__(self, *anon, **mval): #{{{
        prop, values = self.p, self.v
        if not isinstance(prop, MultiValueProperties):
            raise TypeError("%s object is not a valid properties object" %prop.__class__.__name__)
        elif not isinstance(values, MultiValueValues):
            raise TypeError("%s object is not a valid values object" %values.__class__.__name__)

        if not anon and not mval:
            raise ValueError("Cannot create empty mval")
        block = ['__get__', '__getitem__']
        reserved = [n for n in mval if n in block + dir(object)]
        if reserved:
            raise AttributeError("The following attribute names are reserved: %s" %', '.join(reserved))
        tfunc, eqfunc = self._mktfunc(), self._mkeqfunc()
        if [a for a in (tfunc, eqfunc) if not iscallable(a)]:
            raise TypeError("Attempt to set transform or equals function to a non-callable")
        anon = ((k, v) for k, v in enumerate(anon))
        mval = mdict(anon, mval)
        mval.clearmerged()
#        object.__setattr__(self, '_mval', mval)
#        object.__setattr__(self, '_tfunc', tfunc)
#        object.__setattr__(self, '_eqfunc', eqfunc)
        osetattr(self, '_mval', mval)
        osetattr(self, '_tfunc', tfunc)
        osetattr(self, '_eqfunc', eqfunc)
    # End def #}}}

    def __delattr__(self, name): #{{{
        raise AttributeError("Attribute '%s' is read-only" %name)
    # End def #}}}

    def __setattr__(self, name, val): #{{{
        raise AttributeError("Attribute '%s' is read-only" %name)
    # End def #}}}

    def __eq__(self, val): #{{{
        eqfunc = self.p.eqfunc
        return self._interpret_eq(eqfunc(sval, val) for sval in self)
    # End def #}}}

    def __ne__(self, val): #{{{
        return not self.__eq__(val)
    # End def #}}}

    def __nonzero__(self): #{{{
        return bool(self._mval)
    # End def #}}}

    def _interpret_eq(self, res): #{{{
        return True in res
    # End def #}}}

    def __iter__(self): #{{{
        mval, tfunc = self._mval, self.p.transformer
        return (tfunc(k, v) for k, v in mval.iteritems())
    # End def #}}}

    def _mkeqfunc(self): #{{{
        return self.__compare__
#        return lambda s, o: s == o
    # End def #}}}

    def _mktfunc(self): #{{{
        return self.__transform__
#        return lambda k, v: v
    # End def #}}}

    def __compare__(self, o1, o2): #{{{
        return o1 == o2
    # End def #}}}

    def __transform__(self, name, value): #{{{
        return value
    # End def #}}}

    # Properties #{{{
    p = properties = MultiValueProperties()
    v = values = MultiValueValues()
    # End properties #}}}
# End class #}}}

class AnyValue(MultiValue): #{{{
    __slots__ = ()
# End class #}}}

class AllValues(MultiValue): #{{{
    __slots__ = ()
    def _interpret_eq(self, res): #{{{
        return False not in res
    # End def #}}}
# End class #}}}

class EvalMixinProperties(MultiValueProperties): #{{{
    __slots__ = ()
    transformer = property(lambda s: super(EvalMixinProperties, s).transformer)
    eqfunc = property(lambda s: super(EvalMixinProperties, s).eqfunc)
# End class #}}}

class EvalMixin(object): #{{{
    __slots__ = ()
    def __init__(self, *anon, **mval): #{{{
        super(EvalMixin, self).__init__(*anon, **mval)
        mval = self._mval
        for v in mval.itervalues():
            if not iscallable(v):
                mval.clear()
                raise TypeError("'%s' object is not callable" %v.__class__.__name__)
        object.__setattr__(self, '_eqfunc', lambda s, o: bool(s(o)))
    # End def #}}}

    # Properties #{{{
    p = properties = EvalMixinProperties()
    # End properties #}}}
# End class #}}}

class AnyResult(EvalMixin, AnyValue): #{{{
    __slots__ = ()
# End class #}}}

class AllResults(EvalMixin, AllValues): #{{{
    __slots__ = ()
# End class #}}}
