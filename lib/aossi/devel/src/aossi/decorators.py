# Module: aossi.decorators
# File: decorators.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from aossi.core import BaseSignal
from aossi.signals import DefaultExtension, SignalExtension
from aossi.cwrapper import cid
from inspect import isfunction as _isf, ismethod as _ism
from aossi.util import cargdefstr, StopCascade, isiterable, isclassmethod, isstaticmethod

from aossi.util.callobj import evalobj, q

from anyall.type import AllTypeSequences, AllTypeMappings
from anyall.value import AllValueSequences, AllValueMappings

from functools import wraps
ogetattr = object.__getattribute__

from smanstal.types.introspect import isclass

__all__ = ('DecoSignalExtension', 'CustomDecoSignal', 'GenericMatchDecoSignal',
            'OnReturnDecoSignal', 'ReplaceDecoSignal', 'AroundDecoSignal', 
            'StreamDecoSignal', 'CondDecoSignal', 'WhenDecoSignal', 'CascadeDecoSignal', 
            'MatchTypeDecoSignal', 'MatchValueDecoSignal',
            'make_signal', 'DefaultDecoSignal', 'signal')

# ==================================================================================
# Helpers
# ==================================================================================
class callfunc(object): #{{{
    __slots__ = ()
    def __call__(self, sig, func, functype, pass_ret, ret, *args, **kwargs): #{{{
        ismethod = False
        custom_check = self._custom_check(sig, func, functype, pass_ret, ret, args, kwargs)
        if not pass_ret or not custom_check:
            ismethod = func.callable in sig._vars['methods']
        if pass_ret and not ismethod and not custom_check:
            ismethod = func_ismethod(func, *args)
        if pass_ret:
            kwargs = {}
            newargs = args
            if ismethod:
                newargs = (args[0], ret)
            else:
                newargs = (ret,)
            args = newargs
            ismethod = ismethod or custom_check
        if not ismethod:
            prev = sig._vars['prev']
            if prev.callable in sig._vars['methods'] and len(args) >= prev.maxargs:
                args = args[1:]
        if not custom_check:
            sig._vars['prev'] = func
        return func(*args, **kwargs)
    # End def #}}}

    # If will be evaluating other types of callables beyond a 'slot' callable,
    # _custom_check() is used to detect non-slot callables
    def _custom_check(self, sig, func, functype, pass_ret, ret, args, kwargs): #{{{
        return False
    # End def #}}}
# End class #}}}

class chooser_callfunc(callfunc): #{{{
    __slots__ = ()
    def _custom_check(self, sig, func, functype, pass_ret, ret, args, kwargs): #{{{
        return functype in set(['chooser', 'return_chooser'])
    # End def #}}}
# End class #}}}

def func_ismethod(func, *args): #{{{
    if not args:
        return False
    s = args[0]
    sfunc = getattr(s, func.__name__, None)
    if sfunc:
        sfunc = _ism(sfunc) and cid(sfunc.im_func) == func.cid
    return bool(sfunc)
# End def #}}}
# ==================================================================================
# DecoSignalExtension
# ==================================================================================
class DecoSignalExtension(SignalExtension): #{{{
    __slots__ = ()

    def __init__(self, signal, **kwargs): #{{{
        for cls in self.dependencies:
            if not isinstance(self, cls):
                raise TypeError("CustomDecoSignal dependency not fulfilled: %s type required" %cls.__name__)
        self._vars = getattr(self, '_vars', dict())
        self._vars.update(settings={}, global_settings={}, methods=[], prev=None)
        super(DecoSignalExtension, self).__init__(signal, **kwargs)
        self.caller = callfunc()
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        self._vars['prev'] = self.func
        return super(DecoSignalExtension, self).__call__(*args, **kwargs)
    # End def #}}}

    def _generic_names(self): #{{{
        return frozenset(['after', 'before'])
    # End def #}}}

    def __getattribute__(self, name): #{{{
        generic_deco = ogetattr(self, '_generic_names')
        if name == '_generic_names':
            return generic_deco
        elif name in generic_deco():
            return (lambda f: ogetattr(self, '_generic')(f, name))
        return super(DecoSignalExtension, self).__getattribute__(name)
    # End def #}}}

    def _blocked_csettings(self): #{{{
        return set(['globals', 'clear'])
    # End def #}}}

    def _custom_blocked_csettings(self, name): #{{{
        return False
    # End def #}}}

    def _csettings(self): #{{{
        block = self._blocked_csettings()
        custom_block = self._custom_blocked_csettings
        allset = self._allsettings()
        gen = ((k, v) for k, v in allset.iteritems() if k not in block and not custom_block(k))
        temp = dict(gen)
        self._vars['settings'].clear()
        return temp
    # End def #}}}

    def _allsettings(self): #{{{
        temp = dict(self._vars['global_settings'].iteritems())
        temp.update(self._vars['settings'].iteritems())
        return temp
    # End def #}}}

    def _set_custom_global_settings(self, kwargs, gset): #{{{
        pass
    # End def #}}}

    def _expected_settings(self, kwargs, gset): #{{{
        return frozenset(['clear', 'weak', 'weakcondf', 'globals', 
                    'ismethod', 'callmethod', 'MAKE_SIGNAL'])
    # End def #}}}

    def _custom_expected(self, varname, kwargs, gset): #{{{
        return False
    # End def #}}}

    def _set_settings(self, kwargs, gset=None): #{{{
        if not isinstance(kwargs, dict):
            raise TypeError('connect_settings attribute must be a dict')
        expected = self._expected_settings(kwargs, gset)
        custom_expected = self._custom_expected
        if any(i for i in kwargs if i not in expected and not custom_expected(i, kwargs, gset)):
            raise ValueError('got keywords: %s -- but valid keyword arguments are: %s' %(', '.join(kwargs.keys()), ', '.join(expected)))
        if not isinstance(kwargs.get('globals', {}), dict):
            raise TypeError('globals keyword must be a dictionary')
        if gset is None:
            gset = self._vars['global_settings']
        if gset is self._vars['global_settings']:
            self._set_custom_global_settings(kwargs, gset)
        if bool(kwargs.pop('clear', False)):
            gset.clear()
        gset.update(kwargs)
    # End def #}}}

    def _func_settings(self, func): #{{{
        mk_sig = self._vars['global_settings'].pop('MAKE_SIGNAL', 0)
        s = self._csettings()
        block = set(['ismethod', 'callmethod'])
        news = dict((k, v) for k, v in s.iteritems() if k not in block)
        ism = bool(s.get('ismethod', False))
        istup = isinstance(func, tuple)
        meth_app = self._vars['methods'].append
        # Add to methods var so callfunc can process both
        # conditional callables and target callables
        if ism:
            callmeth = bool(s.get('callmethod', False))
            if callmeth and not mk_sig:
                name, vardict = func.__name__, dict()
                defstr, callstr = cargdefstr(func)
                self_str = defstr.split(',', 1)[0].strip()
                callstr = callstr.split(',', 1)[1].strip()
                fstr = """
                def f(%s):
                    return getattr(%s, '%s')(%s)
                """ %(defstr, self_str, name, callstr)
                exec compile(fstr.strip(), '<string>', 'exec') in vardict
                f = vardict['f']
                func = (func[0], f) if istup else f
            if istup:
                for f in func:
                    meth_app(f)
            else:
                meth_app(func)
        return func, news
    # End def #}}}

    def global_settings(self, **kwargs): #{{{
        self._set_settings(kwargs)
        def donothing(func):
            if getattr(func, 'signal', None) is self:
                self._func_settings(self.func.callable)
            return func
        return donothing
    # End def #}}}

    def settings(self, **kwargs): #{{{
        self._set_settings(kwargs, self._vars['settings'])
        def donothing(func):
            if getattr(func, 'signal', None) is self:
                self._func_settings(self.func.callable)
            return func
        return donothing
    # End def #}}}

    def _generic(self, func, name): #{{{
        pfunc, s = self._func_settings(func)
        s[name] = [pfunc]
        self.connect(**s)
        return func
    # End def #}}}

    def _get_decorators(self): #{{{
        generic = self._generic_names()
        other = set(['global_settings', 'settings'])
        return generic | other
    # End def #}}}

    def _get_dependencies(self): #{{{
        return frozenset()
    # End def #}}}

    # Properties #{{{
    connect_settings = property(lambda s: s._allsettings(), lambda s, cs: s._set_settings(cs))
    decorators = property(lambda s: s._get_decorators())
    dependencies = property(lambda s: s._get_dependencies())
    # End properties #}}}
# End class #}}}
# ==================================================================================
# CustomDecoSignal
# ==================================================================================
class CustomDecoSignal(object): #{{{
    __slots__ = ()
# End class #}}}
# ==================================================================================
# OnReturnDecoSignal
# ==================================================================================
class OnReturnDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def _generic_names(self): #{{{
        sup = super(OnReturnDecoSignal, self)._generic_names()
        return sup | frozenset(['onreturn'])
    # End def #}}}
# End class #}}}
# ==================================================================================
# ReplaceDecoSignal
# ==================================================================================
class ReplaceDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def _generic_names(self): #{{{
        sup = super(ReplaceDecoSignal, self)._generic_names()
        return sup | frozenset(['replace'])
    # End def #}}}
# End class #}}}
# ==================================================================================
# AroundDecoSignal
# ==================================================================================
class AroundDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def _generic_names(self): #{{{
        sup = super(AroundDecoSignal, self)._generic_names()
        return sup | frozenset(['around'])
    # End def #}}}
# End class #}}}
# ==================================================================================
# StreamDecoSignal
# ==================================================================================
class StreamDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def _generic_names(self): #{{{
        sup = super(StreamDecoSignal, self)._generic_names()
        return sup | frozenset(['streamin', 'stream'])
    # End def #}}}
# End class #}}}
# ==================================================================================
# CondDecoSignal
# ==================================================================================
class CondDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def __init__(self, signal, **kwargs): #{{{
        super(CondDecoSignal, self).__init__(signal, **kwargs)
        self.caller = chooser_callfunc()
    # End def #}}}

    def _expected_settings(self, kwargs, gset): #{{{
        sup = super(CondDecoSignal, self)._expected_settings(kwargs, gset)
        return sup | frozenset(['chooser', 'return_chooser', 'policy', 'return_policy'])
    # End def #}}}

    def _blocked_csettings(self): #{{{
        sup = super(CondDecoSignal, self)._blocked_csettings()
        return sup | set(['chooser', 'return_chooser', 'policy', 'return_policy'])
    # End def #}}}

    def _set_custom_global_settings(self, kwargs, gset): #{{{
        self.chooser_policy = kwargs.get('policy', self.chooser_policy)
        self.chooser = kwargs.get('chooser', self.chooser)
        self.return_chooser_policy = kwargs.get('return_policy', self.return_chooser_policy)
        self.return_chooser = kwargs.get('return_chooser', self.return_chooser)
    # End def #}}}

    def _cond(self, name, condfunc): #{{{
        def factory(func): #{{{
            self._generic((condfunc, func), name)
            return func
        # End def #}}}
        return factory
    # End def #}}}

    def cond(self, condfunc): #{{{
        return self._cond('choose', condfunc)
    # End def #}}}

    def return_cond(self, condfunc): #{{{
        return self._cond('choosereturn', condfunc)
    # End def #}}}

    def _get_decorators(self): #{{{
        sup = super(CondDecoSignal, self)._get_decorators()
        return sup | set(['cond', 'return_cond'])
    # End def #}}}

# End class #}}}
# ==================================================================================
# WhenDecoSignal
# ==================================================================================
class WhenDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def _when(self, condfunc, s): #{{{
        if not isinstance(s, basestring):
            raise TypeError('argument must be a string')
        def factory(func):
            defstr, callstr = cargdefstr(func)
            n = ''.join([_n.strip().replace('*', '').split('=')[0] for _n in defstr.split(',')])
            if not n or n == defstr:
                n = '_'.join(('g', n))
            global_code = "%s = self.connect_settings.get('globals', None)" %n
            exec compile(global_code, '<string>', 'exec') in locals()
            fstr = """
            def whenfunc(%s):
                return bool(eval('%s', %s, locals()))
            """ %(defstr, s.replace("'", "\\'"), n)
            exec compile(fstr.strip(), '<string>', 'exec') in locals()
            self._vars['settings']['weakcondf'] = False
            return condfunc(whenfunc)(func)
        return factory
    # End def #}}}

    def when(self, s): #{{{
        return self._when(self.cond, s)
    # End def #}}}

    def when_return(self, s): #{{{
        return self._when(self.return_cond, s)
    # End def #}}}

    def _get_decorators(self): #{{{
        sup = super(WhenDecoSignal, self)._get_decorators()
        return sup | set(['when', 'when_return'])
    # End def #}}}

    def _get_dependencies(self): #{{{
        sup = super(WhenDecoSignal, self)._get_dependencies()
        return sup | frozenset([CondDecoSignal])
    # End def #}}}
# End class #}}}

# ==================================================================================
# CascadeDecoSignal
# ==================================================================================
class CascadeDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def _cascade(self, condfunc, s, stop=False): #{{{
        self._set_settings({'policy': 'cascade'})
        if not isinstance(s, basestring):
            raise TypeError('argument must be a string')
        elif not isinstance(stop, bool) and not isinstance(stop, basestring):
            raise TypeError("The 'stop' argument must be either a boolean or a string")
        def factory(func):
            defstr, callstr = cargdefstr(func)
            n = ''.join([_n.strip().replace('*', '').split('=')[0] for _n in defstr.split(',')])
            if not n or n == defstr:
                n = '_'.join(('g', n))
            global_code = "%s = self.connect_settings.get('globals', None)" %n
            exec compile(global_code, '<string>', 'exec') in locals()

            stoperr = StopCascade
            stop_code = "%s_stoperr = stoperr" %n
            exec compile(stop_code, '<string>', 'exec') in locals()
            fstr = """
            def cascadefunc(%s):
                ret = bool(eval('%s', %s, locals()))
                if bool(eval('%s', %s, locals())):
                    raise %s(ret)
                return ret
            """ %(defstr, s.replace("'", "\\'"), n, str(stop).replace("'", "\\'"), n, n + '_stoperr')
            exec compile(fstr.strip(), '<string>', 'exec') in locals()
            self._vars['settings']['weakcondf'] = False
            return condfunc(cascadefunc)(func)
        return factory
    # End def #}}}

    def cascade(self, s, stop=False): #{{{
        return self._cascade(self.cond, s, stop)
    # End def #}}}

    def cascade_return(self, s, stop=False): #{{{
        return self._cascade(self.return_cond, s, stop)
    # End def #}}}

    def _get_decorators(self): #{{{
        sup = super(CascadeDecoSignal, self)._get_decorators()
        return sup | set(['cascade', 'cascade_return'])
    # End def #}}}

    def _get_dependencies(self): #{{{
        sup = super(CascadeDecoSignal, self)._get_dependencies()
        return sup | frozenset([CondDecoSignal])
    # End def #}}}
# End class #}}}
# ==================================================================================
# GenericMatchDecoSignal
# ==================================================================================
class GenericMatchDecoSignal(CustomDecoSignal): #{{{
    __slots__ = ()
    def _custom_blocked_csettings(self, name): #{{{
        block_startswith = ('margs_', 'mkw_', 'match_')
        return ( True in (name.startswith(s) for s in block_startswith) )
    # End def #}}}

    def _custom_expected(self, varname, kwargs, gset): #{{{
        exp_startswith = ('margs_', 'mkw_', 'match_')
        return True in (varname.startswith(s) for s in exp_startswith)
    # End def #}}}

    def _get_dependencies(self): #{{{
        sup = super(GenericMatchDecoSignal, self)._get_dependencies()
        return sup | frozenset([CondDecoSignal])
    # End def #}}}
# End class #}}}
# ==================================================================================
# MatchTypeDecoSignal
# ==================================================================================
class MatchTypeDecoSignal(GenericMatchDecoSignal): #{{{
    __slots__ = ()
    def _match_type(self, condfunc, *margs, **mkwargs): #{{{
        cs = self.connect_settings
        g = cs.get('globals', None)
        def mkcobj(obj, globals=None): #{{{
            if isinstance(obj, basestring):
                return evalobj(obj, globals)
            else:
                return obj
        # End def #}}}
        margs_len = len(margs)
        arg_opt = dict(subset=False, exact=False, shallow=True)
        kw_opt = dict(arg_opt)
        match = {'match_': [arg_opt, kw_opt], 'margs_': [arg_opt], 'mkw_': [kw_opt]}
        for k, v in cs.iteritems():
            klen, ind = len(k), k.find('_')
            frag = '' if ind < 0 else k[:ind+1]
            anchor = len(frag)
            if frag in match and klen > anchor:
                key, val = k[anchor:], bool(v)
                for l in match[frag]:
                    l[key] = val

        mseq = tuple(mkcobj(o, g) for o in margs)
        mdict = dict((k, mkcobj(v, g)) for k, v in mkwargs.iteritems())
        vargs = AllTypeSequences(mseq, **arg_opt)
        vmap = AllTypeMappings(mdict, **kw_opt)
        def checksig(*args, **kwargs): #{{{
            return vargs == args and vmap == kwargs
        # End def #}}}
        self._vars['settings']['weakcondf'] = False
        return condfunc(checksig)
    # End def #}}}

    def match_type(self, *margs, **mkwargs): #{{{
        return self._match_type(self.cond, *margs, **mkwargs)
    # End def #}}}

    def match_return_type(self, marg): #{{{
        return self._match_type(self.return_cond, marg)
    # End def #}}}

    def _get_decorators(self): #{{{
        sup = super(MatchTypeDecoSignal, self)._get_decorators()
        return sup | set(['match_type', 'match_return_type'])
    # End def #}}}

# End class #}}}
# ==================================================================================
# MatchValueDecoSignal
# ==================================================================================
class MatchValueDecoSignal(GenericMatchDecoSignal): #{{{
    __slots__ = ()
    def _match_value(self, condfunc, *margs, **mkwargs): #{{{
        cs = self.connect_settings
        margs_len = len(margs)
        arg_opt = dict(subset=False, exact=False, shallow=True)
        kw_opt = dict(arg_opt)
        match = {'match_': [arg_opt, kw_opt], 'margs_': [arg_opt], 'mkw_': [kw_opt]}
        for k, v in cs.iteritems():
            klen, ind = len(k), k.find('_')
            frag = '' if ind < 0 else k[:ind+1]
            anchor = len(frag)
            if frag in match and klen > anchor:
                key, val = k[anchor:], bool(v)
                for l in match[frag]:
                    l[key] = val

        v_arg = AllValueSequences(margs, **arg_opt)
        v_kw = AllValueMappings(mkwargs, **kw_opt)

        def checksig(*args, **kwargs): #{{{
            return v_arg == args and v_kw == kwargs
        # End def #}}}
        self._vars['settings']['weakcondf'] = False
        return condfunc(checksig)
    # End def #}}}

    def match_value(self, marg, *margs, **mkwargs): #{{{
        return self._match_value(self.cond, marg, *margs, **mkwargs)
    # End def #}}}

    def match_return_value(self, marg): #{{{
        return self._match_value(self.return_cond, marg)
    # End def #}}}

    def _get_decorators(self): #{{{
        sup = super(MatchValueDecoSignal, self)._get_decorators()
        return sup | set(['match_value', 'match_return_value'])
    # End def #}}}

# End class #}}}
# ==================================================================================
# signal
# ==================================================================================
def make_signal(**kwargs): #{{{
    def mkdeco(f, kwargs): #{{{
        signature = []
        sigapp = signature.append
        for ext in kwargs.pop('decoext', ()):
            if not isclass(ext) or not issubclass(ext, CustomDecoSignal):
                raise TypeError("The 'decoext' keyword expected CustomDecoSignal classes, got %s instead" %ext.__name__)
            sigapp(ext)
        sigapp(DecoSignalExtension)
        for ext in kwargs.pop('sigext', ()):
            if not isclass(ext) or not issubclass(ext, SignalExtension):
                raise TypeError("The 'sigext' keyword expected SignalExtension classes, got %s instead" %ext.__name__)
            sigapp(ext)
        sigapp(BaseSignal)
#        signature = list(kwargs.pop('decoext', ()))
#        signature.extend([DecoSignalExtension] + list(kwargs.pop('sigext', ())) + [BaseSignal])
        cstr = """
        class _NewDecoSignal(%s):
            __slots__ = ()
        """ %', '.join('signature[%i]' %i for i in xrange(len(signature)))
        exec compile(cstr.strip(), '<string>', 'exec') in locals()
        return _NewDecoSignal(f)
    # End def #}}}
    def settings(func): #{{{
        signal = getattr(func, 'signal', None)
        if isinstance(signal, DecoSignalExtension) and isinstance(signal, BaseSignal):
            locals().update(DecoSignalFunction=func)
        elif not _isf(func):
            raise TypeError('argument must be a python function')
        else:
            defstr, callstr = cargdefstr(func)
            signal = mkdeco(func, kwargs)
            fstr = """
            def DecoSignalFunction(%s):
                return signal(%s)
            """ %(defstr, callstr)
            exec compile(fstr.strip(), '<string>', 'exec') in locals()
        d = DecoSignalFunction
        d = wraps(func)(d)
        d.signal = signal
        for n in signal.decorators:
            setattr(d, n, getattr(signal, n))
        kwargs.pop('decoext', ())
        kwargs.pop('sigext', ())
        kwargs['MAKE_SIGNAL'] = 1
        return global_settings(d, **kwargs)(d)
    # End def #}}}
    return settings
# End def #}}}

# ==================================================================================
# _validate_signal
# ==================================================================================
def _validate_signal(func): #{{{
    @wraps(func)
    def wrapper(signal, *args, **kwargs): #{{{
        if not _isf(signal):
            raise TypeError('argument must be a python function')
        sig = getattr(signal, 'signal', None)
        if not isinstance(sig, DecoSignalExtension):
            raise TypeError("argument must have a signal attribute which must be a DecoSignalExtension instance")
        if not isinstance(sig, BaseSignal):
            raise TypeError("argument must have a signal attribute which must be a BaseSignal instance")
        return func(signal, *args, **kwargs)
    # End def #}}}
    return wrapper
# End def #}}}

# ==================================================================================
# global_settings
# ==================================================================================
@_validate_signal
def global_settings(signal, **kwargs): #{{{
    return signal.global_settings(**kwargs)
# End def #}}}

# ==================================================================================
# signal
# ==================================================================================
class DefaultDecoSignal(OnReturnDecoSignal, ReplaceDecoSignal, AroundDecoSignal, 
                StreamDecoSignal, CondDecoSignal, WhenDecoSignal, CascadeDecoSignal, 
                MatchTypeDecoSignal, MatchValueDecoSignal): #{{{
    __slots__ = ()
# End class #}}}

def signal(**kwargs): #{{{
    sigext = [DefaultExtension]
    decoext = [DefaultDecoSignal]
    kwargs['sigext'] = sigext
    kwargs['decoext'] = decoext
    return make_signal(**kwargs)
# End def #}}}
# ==================================================================================
# 
# ==================================================================================
