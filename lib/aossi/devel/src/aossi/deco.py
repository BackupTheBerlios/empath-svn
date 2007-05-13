# Module: aossi.deco
# File: deco.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from smanstal.util.misc import deprecated
deprecated("aossi.deco is deprecated: please use aossi.decorators")

from aossi.signal import Signal
from aossi.cwrapper import cid
from inspect import isfunction as _isf, ismethod as _ism
from aossi.util import cargdefstr, StopCascade, isiterable, isclassmethod, isstaticmethod

from aossi.util.callobj import evalobj, q

from anyall.type import AllTypeSequences, AllTypeMappings
from anyall.value import AllValueSequences, AllValueMappings

from functools import wraps
ogetattr = object.__getattribute__

__all__ = ('DecoSignal', 'signal', 'after', 'before', 'around',
            'onreturn', 'cond', 'return_cond', 'match_type', 'match_value', 'when', 'cascade', 
            'stream', 'streamin', 'settings', 'global_settings', 
            'match_return_type', 'match_return_value', 'when_return', 'cascade_return')

# ==================================================================================
# Helpers
# ==================================================================================
def callfunc(self, func, functype, pass_ret, ret, *args, **kwargs): #{{{
    ismethod = False
    ischooser = functype in ('chooser', 'return_chooser')
    if not pass_ret or not ischooser:
        ismethod = func.callable in self._vars['methods']
    if pass_ret and not ismethod and not ischooser:
        ismethod = func_ismethod(func, *args)
    if pass_ret:
        kwargs = {}
        newargs = args
        if ismethod:
            newargs = (args[0], ret)
        else:
            newargs = (ret,)
        args = newargs
        ismethod = ismethod or ischooser
    if not ismethod:
        prev = self._vars['prev']
        if prev.callable in self._vars['methods'] and len(args) >= prev.maxargs:
            args = args[1:]
    if not ischooser:
        self._vars['prev'] = func
    return func(*args, **kwargs)
# End def #}}}

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
# Signal
# ==================================================================================
class DecoSignal(Signal): #{{{
    __slots__ = ()
    __generic__ = frozenset(['after', 'before', 'onreturn', 'replace', 'around',
                                'streamin', 'stream'])
    def __init__(self, signal, **kwargs): #{{{
        self._vars = getattr(self, '_vars', dict())
        self._vars.update(settings={}, global_settings={}, methods=[], prev=None)
        super(DecoSignal, self).__init__(signal, **kwargs)
        self.caller = callfunc
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        self._vars['prev'] = self.func
        return super(DecoSignal, self).__call__(*args, **kwargs)
    # End def #}}}

    def __getattribute__(self, name): #{{{
        generic_deco = ogetattr(self, '__generic__')
        if name == '__generic__':
            return generic_deco
        elif name in generic_deco:
            return (lambda f: ogetattr(self, '_generic')(f, name))
        return super(DecoSignal, self).__getattribute__(name)
    # End def #}}}

    def _csettings(self): #{{{
        block = ('globals', 'chooser', 'return_chooser', 'policy', 'clear')
        block_startswith = ('margs_', 'mkw_', 'match_')
        startswith = lambda x: True in (x.startswith(s) for s in block_startswith)
        allset = self._allsettings()
        gen = ((k, v) for k, v in allset.iteritems() if k not in block and not startswith(k))
        temp = dict(gen)
        self._vars['settings'].clear()
        return temp
    # End def #}}}

    def _allsettings(self): #{{{
        temp = dict(self._vars['global_settings'].iteritems())
        temp.update(self._vars['settings'].iteritems())
        return temp
    # End def #}}}

    def _set_settings(self, kwargs, gset=None): #{{{
        if not isinstance(kwargs, dict):
            raise TypeError('connect_settings attribute must be a dict')
        expected = ('clear', 'weak', 'weakcondf', 'globals', 'chooser', 'return_chooser', 
                    'policy', 'return_policy', 'priority', 'ismethod', 'callmethod',
                    'MAKE_SIGNAL')
        exp_startswith = ('margs_', 'mkw_', 'match_')
        startswith = lambda x: True in (x.startswith(s) for s in exp_startswith)
        if any(i for i in kwargs if i not in expected and not startswith(i)):
            raise ValueError('got keywords: %s -- but valid keyword arguments are: %s' %(', '.join(kwargs.keys()), ', '.join(expected)))
        if not isinstance(kwargs.get('globals', {}), dict):
            raise TypeError('globals keyword must be a dictionary')
        if gset is None:
            gset = self._vars['global_settings']
        if gset is self._vars['global_settings']:
            self.chooser_policy = kwargs.get('policy', self.chooser_policy)
            self.chooser = kwargs.get('chooser', self.chooser)
            self.return_chooser_policy = kwargs.get('return_policy', self.return_chooser_policy)
            self.return_chooser = kwargs.get('return_chooser', self.return_chooser)
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

    def match_type(self, *margs, **mkwargs): #{{{
        return self._match_type(self.cond, *margs, **mkwargs)
    # End def #}}}

    def match_value(self, marg, *margs, **mkwargs): #{{{
        return self._match_value(self.cond, marg, *margs, **mkwargs)
    # End def #}}}

    def match_return_type(self, marg): #{{{
        return self._match_type(self.return_cond, marg)
    # End def #}}}

    def match_return_value(self, marg): #{{{
        return self._match_value(self.return_cond, marg)
    # End def #}}}

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
        generic = self.__generic__
        other = set(['global_settings', 'settings', 'cond', 'return_cond', 
                'match_type', 'match_value', 'when', 'cascade',
                'match_return_type', 'match_return_value', 'when_return', 
                'cascade_return'])
        return generic | other
    # End def #}}}

    # Properties #{{{
    connect_settings = property(lambda s: s._allsettings(), lambda s, cs: s._set_settings(cs))
    decorators = property(lambda s: s._get_decorators())
    # End properties #}}}
# End class #}}}

def signal(**kwargs): #{{{
    def settings(func): #{{{
        if isinstance(getattr(func, 'signal', None), DecoSignal):
            signal = func.signal
            locals().update(DecoSignalFunction=func)
        elif not _isf(func):
            raise TypeError('argument must be a python function')
        else:
            defstr, callstr = cargdefstr(func)
            signal = DecoSignal(func)
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
        kwargs['MAKE_SIGNAL'] = 1
        return global_settings(d, **kwargs)(d)
    # End def #}}}
    return settings
# End def #}}}

def _validate_signal(func): #{{{
    @wraps(func)
    def wrapper(signal, *args, **kwargs): #{{{
        if not _isf(signal):
            raise TypeError('argument must be a python function')
        elif not isinstance(getattr(signal, 'signal', None), DecoSignal):
            raise TypeError("argument must have a signal attribute which must be a DecoSignal instance")
        return func(signal, *args, **kwargs)
    # End def #}}}
    return wrapper
# End def #}}}

@_validate_signal
def global_settings(signal, **kwargs): #{{{
    return signal.global_settings(**kwargs)
# End def #}}}

@_validate_signal
def settings(signal, **kwargs): #{{{
    return signal.settings(**kwargs)
# End def #}}}

@_validate_signal
def after(signal): #{{{
    return signal.after
# End def #}}}

@_validate_signal
def before(signal): #{{{
    return signal.before
# End def #}}}

@_validate_signal
def replace(signal): #{{{
    return signal.replace
# End def #}}}

@_validate_signal
def around(signal): #{{{
    return signal.around
# End def #}}}

@_validate_signal
def onreturn(signal): #{{{
    return signal.onreturn
# End def #}}}

@_validate_signal
def cond(signal, condfunc): #{{{
    return signal.cond(condfunc)
# End def #}}}

@_validate_signal
def return_cond(signal, condfunc): #{{{
    return signal.return_cond(condfunc)
# End def #}}}

@_validate_signal
def match_type(signal, *args, **kwargs): #{{{
    return signal.match_type(*args, **kwargs)
# End def #}}}

@_validate_signal
def match_value(signal, *args, **kwargs): #{{{
    return signal.match_value(*args, **kwargs)
# End def #}}}

@_validate_signal
def match_return_type(signal, *args, **kwargs): #{{{
    return signal.match_return_type(*args, **kwargs)
# End def #}}}

@_validate_signal
def match_return_value(signal, *args, **kwargs): #{{{
    return signal.match_return_value(*args, **kwargs)
# End def #}}}

@_validate_signal
def when(signal, s): #{{{
    return signal.when(s)
# End def #}}}

@_validate_signal
def when_return(signal, s): #{{{
    return signal.when_return(s)
# End def #}}}

@_validate_signal
def cascade(signal, s, stop=False): #{{{
    return signal.cascade(s, stop)
# End def #}}}

@_validate_signal
def cascade_return(signal, s, stop=False): #{{{
    return signal.cascade_return(s, stop)
# End def #}}}

@_validate_signal
def stream(signal): #{{{
    return signal.stream
# End def #}}}

@_validate_signal
def streamin(signal): #{{{
    return signal.streamin
# End def #}}}
