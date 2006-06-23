# Module: aossi.deco
# File: deco.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from aossi.signal import Signal
from inspect import isfunction as _isf, stack
from aossi.misc import cargdefstr

__all__ = ('DecoSignal', 'setsignal', 'signal', 'after', 'before', 'around',
            'onreturn', 'cond', 'when', 'settings', 'global_settings')

class DecoSignal(Signal): #{{{
    __slots__ = ['_settings', '_global_settings']
    __slots__ += [i for i in Signal.__slots__ if i != '__weakref__']
    def __init__(self, signal, weak=True): #{{{
        super(DecoSignal, self).__init__(signal, weak)
        self._settings = {}
        self._global_settings = {}

#        temp = stack()[2][0].f_locals
#        raise Exception(temp.keys())
#        if 'var' not in temp:
#            raise Exception(temp.keys())
    # End def #}}}

    def _csettings(self): #{{{
        block = ('globals', 'chooser', 'policy')
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
        expected = ('weak', 'weakcondf', 'globals', 'chooser', 'policy')
        if [i for i in kwargs if i not in expected]:
            raise ValueError('got keywords: %s -- but valid keyword arguments are: %s' %(', '.join(kwargs.keys()), ', '.join(expected)))
        if not isinstance(kwargs.get('globals', {}), dict):
            raise TypeError('globals keyword must be a dictionary')
        if gset is None:
            gset = self._global_settings
        if gset is self._global_settings:
            if 'policy' in kwargs:
                self.chooserpolicy = kwargs['policy']
            if 'chooser' in kwargs:
                self.chooser = kwargs['chooser']
        gset.clear()
        gset.update(kwargs)
    # End def #}}}

    def global_settings(self, **kwargs): #{{{
        self._set_settings(kwargs)
        def donothing(func):
            return func
        return donothing
    # End def #}}}

    def settings(self, **kwargs): #{{{
        self._set_settings(kwargs, self._settings)
        def donothing(func):
            return func
        return donothing
    # End def #}}}

    def after(self, func): #{{{
        self.connect(func, **self._csettings())
        return func
    # End def #}}}

    def before(self, func): #{{{
        self.connect(before=[func], **self._csettings())
        return func
    # End def #}}}

    def around(self, func): #{{{
        self.connect(around=[func], **self._csettings())
        return func
    # End def #}}}

    def onreturn(self, func): #{{{
        self.connect(onreturn=[func], **self._csettings())
        return func
    # End def #}}}

    def cond(self, condfunc): #{{{
        cset = self._csettings()
        def factory(func): #{{{
            self.connect(choose=[(condfunc, func)], **cset)
            return func
        # End def #}}}
        return factory
    # End def #}}}

    def when(self, s): #{{{
        g = self.connect_settings.get('globals', None)
        if not isinstance(s, basestring):
            raise TypeError('argument must be a string')
        def factory(func):
            fglob = dict(func.func_globals)
            if g:
                fglob.update(g)
#            else:
#                temp = stack()[1][0].f_locals
            fglob.update(locals())
            defstr, callstr = cargdefstr(func)
            fstr = """
            def whenfunc(%s):
                return bool(%s)
            """ %(defstr, s)
            exec compile(fstr.strip(), '<string>', 'exec') in fglob, locals()
            self._settings['weakcondf'] = False
            return self.cond(whenfunc)(func)
        return factory
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
    d.when = signal.when
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

def when(signal, s): #{{{
    _validate_signal(signal)
    return signal.when(s)
# End def #}}}
