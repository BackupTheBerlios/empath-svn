# Module: aossi.deco
# File: deco.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from aossi.signal import Signal
from aossi.cwrapper import cid
from inspect import isfunction as _isf, ismethod as _ism
from aossi.misc import cargdefstr, StopCascade, isiterable
from validate.base import evalobj, q
from validate.type import ValidateTypeSequence_And, ValidateTypeMapping_And
from validate.value import ValidateValueSequence_And, ValidateValueMapping_And

__all__ = ('DecoSignal', 'setsignal', 'signal', 'signal_settings', 'after', 'before', 'around',
            'onreturn', 'cond', 'retcond', 'match_type', 'match_value', 'when', 'cascade', 
            'stream', 'settings', 'global_settings', 
            'matchret_type', 'matchret_value', 'whenret', 'cascaderet')

class DecoSignal(Signal): #{{{
    __slots__ = ('_settings', '_global_settings', '_methods', '_prev')
    def __init__(self, signal, **kwargs): #{{{
        super(DecoSignal, self).__init__(signal, **kwargs)
        self._settings = {}
        self._global_settings = {}
        self._methods = []
        self.caller = self._deco_callfunc
        self._prev = None
    # End def #}}}

    def __call__(self, *args, **kwargs): #{{{
        self._prev = self.func
        return super(DecoSignal, self).__call__(*args, **kwargs)
    # End def #}}}

    def _func_ismethod(self, func, *args): #{{{
        s = args[0]
        sfunc = getattr(s, func.__name__, None)
        if sfunc:
            sfunc = _ism(sfunc) and cid(sfunc.im_func) == func.cid
        return bool(sfunc)
    # End def #}}}

    def _deco_callfunc(self, sig, func, functype, pass_ret, ret, *args, **kwargs): #{{{
        ismethod = False
        ischooser = functype in ('chooser', 'return_chooser')
        if not pass_ret or not ischooser:
            ismethod = func.callable in sig._methods
        if pass_ret and not ismethod and not ischooser:
            ismethod = self._func_ismethod(func, *args)
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
            prev = self._prev
            if prev.callable in sig._methods and len(args) >= prev.maxargs:
                args = args[1:]
        if not ischooser:
            self._prev = func
        return func(*args, **kwargs)
    # End def #}}}

    def _csettings(self): #{{{
        block = ('globals', 'chooser', 'return_chooser', 'policy', 'clear', 'match_subset', 'match_exact',
                    'matchargs_subset', 'matchkwargs_subset', 'matchargs_exact', 'matchkwargs_exact',
                    'matchargs_pad', 'matchargs_shallow', 'matchkwargs_shallow')
        allset = self._allsettings()
        gen = ((k, v) for k, v in allset.iteritems() if k not in block)
        temp = dict(gen)
        self._settings.clear()
        return temp
    # End def #}}}

    def _allsettings(self): #{{{
        temp = dict(self._global_settings.iteritems())
        temp.update(self._settings.iteritems())
        return temp
    # End def #}}}

    def _set_settings(self, kwargs, gset=None): #{{{
        if not isinstance(kwargs, dict):
            raise TypeError('connect_settings attribute must be a dict')
        expected = ('clear', 'weak', 'weakcondf', 'globals', 'chooser', 'return_chooser', 
                    'policy', 'return_policy', 'priority', 'ismethod',
                    'match_subset', 'match_exact', 'matchargs_subset', 'matchkwargs_subset', 
                    'matchargs_exact', 'matchkwargs_exact', 'matchargs_pad',
                    'matchargs_shallow', 'matchkwargs_shallow')
        if [i for i in kwargs if i not in expected]:
            raise ValueError('got keywords: %s -- but valid keyword arguments are: %s' %(', '.join(kwargs.keys()), ', '.join(expected)))
        if not isinstance(kwargs.get('globals', {}), dict):
            raise TypeError('globals keyword must be a dictionary')
        if gset is None:
            gset = self._global_settings
        if gset is self._global_settings:
            self.chooserpolicy = kwargs.get('policy', self.chooserpolicy)
            self.chooser = kwargs.get('chooser', self.chooser)
            self.retchooserpolicy = kwargs.get('return_policy', self.retchooserpolicy)
            self.return_chooser = kwargs.get('return_chooser', self.return_chooser)
        if bool(kwargs.pop('clear', False)):
            gset.clear()
        gset.update(kwargs)
    # End def #}}}

    def _func_settings(self, func): #{{{
        s = self._csettings()
        block = ('priority', 'ismethod')
        news = dict((k, v) for k, v in s.iteritems() if k not in block)
        prio = s.get('priority', None)
        ism = bool(s.get('ismethod', False))
        istup = isinstance(func, tuple)
        if ism:
            if istup:
                for f in func:
                    self._methods.append(f)
            else:
                self._methods.append(func)
        if prio is not None:
            if istup:
                func = (prio,) + func
            else:
                func = (prio, func)
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
        self._set_settings(kwargs, self._settings)
        def donothing(func):
            if getattr(func, 'signal', None) is self:
                self._func_settings(self.func.callable)
            return func
        return donothing
    # End def #}}}

    def after(self, func): #{{{
        pfunc, s = self._func_settings(func)
        self.connect(pfunc, **s)
        return func
    # End def #}}}

    def before(self, func): #{{{
        pfunc, s = self._func_settings(func)
        self.connect(before=[pfunc], **s)
        return func
    # End def #}}}

    def around(self, func): #{{{
        pfunc, s = self._func_settings(func)
        self.connect(around=[pfunc], **s)
        return func
    # End def #}}}

    def onreturn(self, func): #{{{
        pfunc, s = self._func_settings(func)
        self.connect(onreturn=[pfunc], **s)
        return func
    # End def #}}}

    def _cond(self, name, condfunc): #{{{
        def factory(func): #{{{
            pfunc, s = self._func_settings((condfunc, func))
            s[name] = [pfunc]
            self.connect(**s)
            return func
        # End def #}}}
        return factory
    # End def #}}}

    def cond(self, condfunc): #{{{
        return self._cond('choose', condfunc)
    # End def #}}}

    def retcond(self, condfunc): #{{{
        return self._cond('chooseret', condfunc)
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
        shallow_args = bool(cs.get('matchargs_shallow', True))
        shallow_kwargs = bool(cs.get('matchkwargs_shallow', True))
        subset_args = subset_kwargs = bool(cs.get('match_subset', False))
        exact_args = exact_kwargs = bool(cs.get('match_exact', False))
        subset_args = bool(cs.get('matchargs_subset', subset_args))
        subset_kwargs = bool(cs.get('matchkwargs_subset', subset_kwargs))
        exact_args = bool(cs.get('matchargs_exact', exact_args))
        exact_kwargs = bool(cs.get('matchkwargs_exact', exact_kwargs))
        arg_opt = dict(exact=exact_args, shrink=subset_args, shallow=shallow_args)
        kwarg_opt = dict(exact=exact_kwargs, missingkw=subset_kwargs, shallow=shallow_kwargs)

        mseq = tuple(mkcobj(o, g) for o in margs)
        mdict = dict((k, mkcobj(v, g)) for k, v in mkwargs.iteritems())
        vargs = ValidateTypeSequence_And(*mseq, **arg_opt)
        vmap = ValidateTypeMapping_And(mdict, **kwarg_opt)
        def checksig(*args, **kwargs): #{{{
            return vargs == args and vmap == kwargs
        # End def #}}}
        self._settings['weakcondf'] = False
        return condfunc(checksig)
    # End def #}}}

    def _match_value(self, condfunc, *margs, **mkwargs): #{{{
        cs = self.connect_settings
        margs_len = len(margs)
        subset_args = subset_kwargs = bool(cs.get('match_subset', False))
        subset_args = bool(cs.get('matchargs_subset', subset_args))
        subset_kwargs = bool(cs.get('matchkwargs_subset', subset_kwargs))
        arg_opt = dict(shrink=subset_args)
        kwarg_opt = dict(missingkw=subset_kwargs)

        v_arg = ValidateValueSequence_And(*margs, **arg_opt)
        v_kw = ValidateValueMapping_And(mkwargs, **kwarg_opt)

        def checksig(*args, **kwargs): #{{{
            return v_arg == args and v_kw == kwargs
        # End def #}}}
        self._settings['weakcondf'] = False
        return condfunc(checksig)
    # End def #}}}

    def match_type(self, *margs, **mkwargs): #{{{
        return self._match_type(self.cond, *margs, **mkwargs)
    # End def #}}}

    def match_value(self, marg, *margs, **mkwargs): #{{{
        return self._match_value(self.cond, marg, *margs, **mkwargs)
    # End def #}}}

    def matchret_type(self, marg): #{{{
        return self._match_type(self.retcond, marg)
    # End def #}}}

    def matchret_value(self, marg): #{{{
        return self._match_value(self.retcond, marg)
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
            self._settings['weakcondf'] = False
            return condfunc(whenfunc)(func)
        return factory
    # End def #}}}

    def when(self, s): #{{{
        return self._when(self.cond, s)
    # End def #}}}

    def whenret(self, s): #{{{
        return self._when(self.retcond, s)
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
            if not n or n == 'self':
                n = 'g'
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
            self._settings['weakcondf'] = False
            return condfunc(cascadefunc)(func)
        return factory
    # End def #}}}

    def cascade(self, s, stop=False): #{{{
        return self._cascade(self.cond, s, stop)
    # End def #}}}

    def cascaderet(self, s, stop=False): #{{{
        return self._cascade(self.retcond, s, stop)
    # End def #}}}

    def stream(self, func): #{{{
        pfunc, s = self._func_settings(func)
        self.connect(stream=[pfunc], **s)
        return func
    # End def #}}}

    # Properties #{{{
    connect_settings = property(lambda s: s._allsettings(), lambda s, cs: s._set_settings(cs))
    # End properties #}}}
# End class #}}}

def setsignal(**kwargs): #{{{
    def newfunc(func):
        ret = signal(func)        
        return global_settings(ret, **kwargs)(ret)
    return newfunc
# End def #}}}

def signal_settings(**kwargs): #{{{
    def newfunc(func):
        ret = signal(func)        
        return global_settings(ret, **kwargs)(ret)
    return newfunc
# End def #}}}

def signal(func): #{{{
    if isinstance(getattr(func, 'signal', None), DecoSignal):
        return func
    elif not _isf(func):
        raise TypeError('argument must be a python function')
    defstr, callstr = cargdefstr(func)
    signal = DecoSignal(func)
    fstr = """
    def DecoSignalFunction(%s):
        return signal(%s)
    """ %(defstr, callstr)
    exec compile(fstr.strip(), '<string>', 'exec') in locals()
    d = DecoSignalFunction
    d.__name__ = func.__name__
    d.__dict__ = func.__dict__
    d.__doc__ = func.__doc__
    d.signal = signal
    d.global_settings = signal.global_settings
    d.settings = signal.settings
    d.after = signal.after
    d.before = signal.before
    d.onreturn = signal.onreturn
    d.around = signal.around
    d.cond = signal.cond
    d.retcond = signal.retcond
    d.match_type = signal.match_type
    d.match_value = signal.match_value
    d.when = signal.when
    d.cascade = signal.cascade
    d.matchret_type = signal.matchret_type
    d.matchret_value = signal.matchret_value
    d.whenret = signal.whenret
    d.cascaderet = signal.cascaderet
    d.stream = signal.stream
    return d
# End def #}}}

def _validate_signal(signal): #{{{
    if not _isf(signal):
        raise TypeError('argument must be a python function')
    elif not isinstance(getattr(signal, 'signal', None), DecoSignal):
        raise TypeError("argument must have a signal attribute which must be a DecoSignal instance")
# End def #}}}

def global_settings(signal, **kwargs): #{{{
    _validate_signal(signal)
    return signal.global_settings(**kwargs)
# End def #}}}

def settings(signal, **kwargs): #{{{
    _validate_signal(signal)
    return signal.settings(**kwargs)
# End def #}}}

def after(signal): #{{{
    _validate_signal(signal)
    return signal.after
# End def #}}}

def before(signal): #{{{
    _validate_signal(signal)
    return signal.before
# End def #}}}

def around(signal): #{{{
    _validate_signal(signal)
    return signal.around
# End def #}}}

def onreturn(signal): #{{{
    _validate_signal(signal)
    return signal.onreturn
# End def #}}}

def cond(signal, condfunc): #{{{
    _validate_signal(signal)
    return signal.cond(condfunc)
# End def #}}}

def retcond(signal, condfunc): #{{{
    _validate_signal(signal)
    return signal.retcond(condfunc)
# End def #}}}

def match_type(signal, *args, **kwargs): #{{{
    _validate_signal(signal)
    return signal.match_type(*args, **kwargs)
# End def #}}}

def match_value(signal, *args, **kwargs): #{{{
    _validate_signal(signal)
    return signal.match_value(*args, **kwargs)
# End def #}}}

def matchret_type(signal, *args, **kwargs): #{{{
    _validate_signal(signal)
    return signal.matchret_type(*args, **kwargs)
# End def #}}}

def matchret_value(signal, *args, **kwargs): #{{{
    _validate_signal(signal)
    return signal.matchret_value(*args, **kwargs)
# End def #}}}

def when(signal, s): #{{{
    _validate_signal(signal)
    return signal.when(s)
# End def #}}}

def whenret(signal, s): #{{{
    _validate_signal(signal)
    return signal.whenret(s)
# End def #}}}

def cascade(signal, s, stop=False): #{{{
    _validate_signal(signal)
    return signal.cascade(s, stop)
# End def #}}}

def cascaderet(signal, s, stop=False): #{{{
    _validate_signal(signal)
    return signal.cascaderet(s, stop)
# End def #}}}

def stream(signal): #{{{
    _validate_signal(signal)
    return signal.stream
# End def #}}}
