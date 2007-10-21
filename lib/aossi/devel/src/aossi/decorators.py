# Module: aossi.decorators
# File: decorators.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# stdlib imports
from functools import wraps
from operator import itemgetter
from new import function as newfunction, classobj as newclass
from compiler import compile as compile_str
import __builtin__

# 3rd-party imports
from eqobj.collections.sequences import Sequence
from eqobj.collections.mappings import Mapping
from eqobj.validators.type import InstanceType

# package imports
from aossi.core import BaseSignal
from aossi.signals import DefaultExtension, SignalExtension
from aossi.cwrapper import cid
from aossi.util import cargdefstr, StopCascade, isiterable, isclassmethod, isstaticmethod, property_, cref, bp_call_args, default_argvals, cgetargspec
from aossi.util.introspect import isclass, isbasemetaclass, mro, isfunction as _isf, ismethod as _ism, iscallable
from aossi.util.byteplay import (Code, CodeList, Label, LOAD_GLOBAL, LOAD_FAST, LOAD_CONST, 
                                 CALL_FUNCTION, RETURN_VALUE, SetLineno, BINARY_SUBSCR, STORE_FAST,
                                 JUMP_IF_FALSE, POP_TOP, RAISE_VARARGS, JUMP_FORWARD)

try:
    from aossi._speedups.decorators import (_DecoSignalExtension, CustomDecoSignal, make_signal, callfunc,
                                            OnReturnDecoSignal, ReplaceDecoSignal, AroundDecoSignal, 
                                            StreamDecoSignal, CondDecoSignal, WhenDecoSignal, CascadeDecoSignal,
                                            GenericMatchDecoSignal, MatchTypeDecoSignal, MatchDecoSignal)
except ImportError:
    from aossi._decorators import (_DecoSignalExtension, CustomDecoSignal, make_signal, callfunc,
                                    OnReturnDecoSignal, ReplaceDecoSignal, AroundDecoSignal, 
                                    StreamDecoSignal, CondDecoSignal, WhenDecoSignal, CascadeDecoSignal,
                                    GenericMatchDecoSignal, MatchTypeDecoSignal, MatchDecoSignal)

#ogetattr = object.__getattribute__

__all__ = ('DecoSignalExtension', 'CustomDecoSignal', 'GenericMatchDecoSignal',
            'OnReturnDecoSignal', 'ReplaceDecoSignal', 'AroundDecoSignal', 
            'StreamDecoSignal', 'CondDecoSignal', 'WhenDecoSignal', 'CascadeDecoSignal', 
            'MatchTypeDecoSignal', 'MatchDecoSignal',
            'make_signal', 'DefaultDecoSignal', 'signal')

# ==================================================================================
# Module Globals
# ==================================================================================
OPT_OVERLOAD_DEFAULT = False
# ==================================================================================
# Helpers
# ==================================================================================
#class callfunc(object): #{{{
#    __slots__ = ()
#    def __call__(self, sig, func, functype, pass_ret, ret, *args, **kwargs): #{{{
#        ismethod = False
#        custom_check = self._custom_check(sig, func, functype, pass_ret, ret, args, kwargs)
#        if not pass_ret or not custom_check:
#            ismethod = func.callable in sig._vars['methods']
#        if pass_ret and not ismethod and not custom_check:
#            ismethod = func_ismethod(func, *args)
#        if pass_ret:
#            kwargs = {}
#            newargs = args
#            if ismethod:
#                newargs = (args[0], ret)
#            else:
#                newargs = (ret,)
#            args = newargs
#            ismethod = ismethod or custom_check
#        if not ismethod:
#            prev = sig._vars['prev']
#            if prev.callable in sig._vars['methods'] and len(args) >= prev.maxargs:
#                args = args[1:]
#        if not custom_check:
#            sig._vars['prev'] = func
#        return func(*args, **kwargs)
#    # End def #}}}

#    # If will be evaluating other types of callables beyond a 'slot' callable,
#    # _custom_check() is used to detect non-slot callables
#    def _custom_check(self, sig, func, functype, pass_ret, ret, args, kwargs): #{{{
#        return False
#    # End def #}}}
## End class #}}}

#class chooser_callfunc(callfunc): #{{{
#    __slots__ = ()
#    def _custom_check(self, sig, func, functype, pass_ret, ret, args, kwargs): #{{{
#        return functype in set(['chooser', 'return_chooser'])
#    # End def #}}}
## End class #}}}

#def func_ismethod(func, *args): #{{{
#    if not args:
#        return False
#    s = args[0]
#    sfunc = getattr(s, func.__name__, None)
#    if sfunc:
#        sfunc = _ism(sfunc) and cid(sfunc.im_func) == func.cid
#    return bool(sfunc)
## End def #}}}
# ==================================================================================
# MetaDecoSignalExtension
# ==================================================================================
class MetaDecoSignalExtension(type): #{{{
    def __new__(mcls, classname, bases, clsdict): #{{{
        setup = {'__genericdecorators__': ['after', 'before'],
                 '__decorators__': ['global_settings', 'settings'],
                 '__dependencies__': []}
        def mkdeco(deconame): 
            def deco(self, f): return self._generic(f, deconame)
            return deco
        for name, default in setup.iteritems():
            clsdict[name] = gen = mcls._magic_sets(name, default, (classname, bases, clsdict))
            if name == '__genericdecorators__':
                for deconame in gen:
                    clsdict[deconame] = mkdeco(deconame)
        return super(MetaDecoSignalExtension, mcls).__new__(mcls, classname, bases, clsdict)
    # End def #}}}

    @classmethod
    def _magic_sets(mcls, name, default, newargs): #{{{
        classname, bases, clsdict = newargs
        past = set(default)
        cur = clsdict.pop(name, [])
        updatepast = past.update
        if not isbasemetaclass(bases, mcls):
            allowed = (CustomDecoSignal, DecoSignalExtension)
            for b in bases:
                if not issubclass(b, allowed):
                    continue
                for bcls in mro(b):
                    battr = getattr(bcls, name, None)
                    if battr is None or not issubclass(bcls, allowed):
                        continue
                    updatepast(battr)
        return frozenset(past) | frozenset(str(s) for s in cur)
    # End def #}}}
# End class #}}}
# ==================================================================================
# DecoSignalExtension
# ==================================================================================
class DecoSignalExtension(_DecoSignalExtension): #{{{
    __metaclass__ = MetaDecoSignalExtension
    __slots__ = ()
# End class #}}}
#class DecoSignalExtension(SignalExtension): #{{{
#    __metaclass__ = MetaDecoSignalExtension
#    __slots__ = ()

#    def __init__(self, signal, **kwargs): #{{{
#        for cls in self.__dependencies__:
#            if not isinstance(self, cls):
#                raise TypeError("CustomDecoSignal dependency not fulfilled: %s type required" %cls.__name__)
#        self._vars = getattr(self, '_vars', dict())
#        self._vars.update(settings={}, global_settings={}, methods=[], prev=None, sigfunc=None)
#        super(DecoSignalExtension, self).__init__(signal, **kwargs)
#        self.caller = callfunc()
#    # End def #}}}

#    def __call__(self, *args, **kwargs): #{{{
#        self._vars['prev'] = self.func
#        return super(DecoSignalExtension, self).__call__(*args, **kwargs)
#    # End def #}}}

##    def __getattribute__(self, name): #{{{
##        generic_deco = ogetattr(self, '__genericdecorators__')
##        if name == '__genericdecorators__':
##            return generic_deco
##        elif name in generic_deco:
##            return (lambda f: ogetattr(self, '_generic')(f, name))
##        return ogetattr(self, name)
###        return super(DecoSignalExtension, self).__getattribute__(name)
##    # End def #}}}

#    def _blocked_csettings(self): #{{{
#        return set(['globals', 'clear'])
#    # End def #}}}

#    def _custom_blocked_csettings(self, name): #{{{
#        return False
#    # End def #}}}

#    def _csettings(self): #{{{
#        block = self._blocked_csettings()
#        custom_block = self._custom_blocked_csettings
#        allset = self._allsettings()
#        gen = ((k, v) for k, v in allset.iteritems() if k not in block and not custom_block(k))
#        temp = dict(gen)
#        self._vars['settings'].clear()
#        return temp
#    # End def #}}}

#    def _allsettings(self): #{{{
#        temp = dict(self._vars['global_settings'].iteritems())
#        temp.update(self._vars['settings'].iteritems())
#        return temp
#    # End def #}}}

#    def _set_custom_global_settings(self, kwargs, gset): #{{{
#        pass
#    # End def #}}}

#    def _expected_settings(self, kwargs, gset): #{{{
#        return frozenset(['clear', 'weak', 'weakcondf', 'globals', 
#                    'ismethod', 'callmethod', 'MAKE_SIGNAL', 'overload'])
#    # End def #}}}

#    def _custom_expected(self, varname, kwargs, gset): #{{{
#        return False
#    # End def #}}}

#    def _set_settings(self, kwargs, gset=None): #{{{
#        if not isinstance(kwargs, dict):
#            raise TypeError('connect_settings attribute must be a dict')
#        expected = self._expected_settings(kwargs, gset)
#        custom_expected = self._custom_expected
#        if any(i for i in kwargs if i not in expected and not custom_expected(i, kwargs, gset)):
#            raise ValueError('got keywords: %s -- but valid keyword arguments are: %s' %(', '.join(kwargs.keys()), ', '.join(expected)))
#        if not isinstance(kwargs.get('globals', {}), dict):
#            raise TypeError('globals keyword must be a dictionary')
#        if gset is None:
#            gset = self._vars['global_settings']
#        if gset is self._vars['global_settings']:
#            self._set_custom_global_settings(kwargs, gset)
#        if bool(kwargs.pop('clear', False)):
#            gset.clear()
#        gset.update(kwargs)
#    # End def #}}}

#    def _blocked_func_settings(self): #{{{
#        return set(['ismethod', 'callmethod', 'overload'])
#    # End def #}}}

#    def _custom_blocked_func_settings(self, name): #{{{
#        return False
#    # End def #}}}

#    def _func_settings_options(self, lset, gset): #{{{
#        overload = bool(lset.get('overload', OPT_OVERLOAD_DEFAULT))
#        if overload:
#            lset['weak'] = lset['weakcondf'] = False
#        return dict(overload=overload)
#    # End def #}}}

#    def _func_settings(self, func): #{{{
#        global_settings = self._vars['global_settings']
#        mk_sig = global_settings.pop('MAKE_SIGNAL', 0)
#        s = self._csettings()
#        options = self._func_settings_options(s, global_settings)
#        block = self._blocked_func_settings()
#        custom_block = self._custom_blocked_func_settings
#        news = dict((k, v) for k, v in s.iteritems() if k not in block and not custom_block(k))
#        ism = bool(s.get('ismethod', False))
#        istup = isinstance(func, tuple)
#        meth_app = self._vars['methods'].append
#        # Add to methods var so callfunc can process both
#        # conditional callables and target callables
#        if ism:
#            callmeth = bool(s.get('callmethod', False))
#            if callmeth and not mk_sig:
#                if options['overload']:
#                    raise ValueError("Keywords 'overload' and 'callmethod' cannot be True at the same time")
#                func_obj = func[1] if istup else func
#                name, vardict = func_obj.__name__, dict()
#                # Low-level function creation to avoid use of exec
#                # which allows turning this class into a builtin type
#                args, vargs, vkeys, defaults = spec = cgetargspec(func_obj)
#                code_args = args + [v for v in (vargs, vkeys) if v != None]
#                fcode = Code(CodeList(), (), code_args, bool(vargs), bool(vkeys), True, 'f', '<dyn>', 1, None)
#                fcode.code[:] = ([(SetLineno, 2), (LOAD_GLOBAL, 'getattr'),
#                                  (LOAD_FAST, 'self'), (LOAD_CONST, name),
#                                  (CALL_FUNCTION, 2),
#                                ] + bp_call_args(callmethod=True, *spec) + 
#                                [(RETURN_VALUE, None)])
#                f = newfunction(fcode.to_code(), dict(getattr=getattr), 'f', default_argvals(args, defaults))
#                func = (func[0], f) if istup else f
#            if istup:
#                for f in func:
#                    meth_app(f)
#            else:
#                meth_app(func)
#        return func, news, options
#    # End def #}}}

#    def global_settings(self, **kwargs): #{{{
#        self._set_settings(kwargs)
#        def donothing(func):
#            if getattr(func, 'signal', None) is self:
#                self._func_settings(self.func.callable)
#            return func
#        return donothing
#    # End def #}}}

#    def settings(self, **kwargs): #{{{
#        self._set_settings(kwargs, self._vars['settings'])
#        def donothing(func):
#            if getattr(func, 'signal', None) is self:
#                self._func_settings(self.func.callable)
#            return func
#        return donothing
#    # End def #}}}

#    def _generic(self, func, name): #{{{
#        pfunc, s, opts = self._func_settings(func)
#        s[name] = [pfunc]
#        self.connect(**s)
#        if opts['overload']:
#            return self.signalfunc
#        return func
#    # End def #}}}

#    @property_
#    def decorators(): #{{{
#        def fget(self): #{{{
#            return self.__genericdecorators__ | self.__decorators__
#        # End def #}}}
#        return locals()
#    # End def #}}}

#    @property_
#    def connect_settings(): #{{{
#        def fget(self): #{{{
#            return self._allsettings()
#        # End def #}}}
#        def fset(self, cs): #{{{
#            self._set_settings(cs)
#        # End def #}}}
#        return locals()
#    # End def #}}}

#    @property_
#    def signalfunc(): #{{{
#        def fget(self): #{{{
#            ret = self._vars['sigfunc']
#            return ret if not ret else ret()
#        # End def #}}}
#        def fset(self, val): #{{{
#            vars = self._vars
#            if vars['sigfunc'] is not None:
#                raise ValueError("Can only set 'signalfunc' property once")
#            if not iscallable(val) or getattr(val, 'signal', None) is not self:
#                raise TypeError('Attempt to set invalid signalfunc')
#            vars['sigfunc'] = cref(val)
#        # End def #}}}
#        return locals()
#    # End def #}}}
## End class #}}}
# ==================================================================================
# CustomDecoSignal
# ==================================================================================
#class CustomDecoSignal(object): #{{{
#    __slots__ = ()
## End class #}}}
# ==================================================================================
# OnReturnDecoSignal
# ==================================================================================
#class OnReturnDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __genericdecorators__ = ['onreturn']
## End class #}}}
# ==================================================================================
# ReplaceDecoSignal
# ==================================================================================
#class ReplaceDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __genericdecorators__ = ['replace']
## End class #}}}
# ==================================================================================
# AroundDecoSignal
# ==================================================================================
#class AroundDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __genericdecorators__ = ['around']
## End class #}}}
# ==================================================================================
# StreamDecoSignal
# ==================================================================================
#class StreamDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __genericdecorators__ = ['streamin', 'stream']
## End class #}}}
## ==================================================================================
## CondDecoSignal
## ==================================================================================
#class CondDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __decorators__ = ['cond', 'return_cond', 'yield_cond']
#    def __init__(self, signal, **kwargs): #{{{
#        super(CondDecoSignal, self).__init__(signal, **kwargs)
#        self.caller = chooser_callfunc()
#    # End def #}}}

#    def _expected_settings(self, kwargs, gset): #{{{
#        sup = super(CondDecoSignal, self)._expected_settings(kwargs, gset)
#        return sup | frozenset(['chooser', 'return_chooser', 'policy', 'return_policy', 'yield_chooser', 'yield_policy'])
#    # End def #}}}

#    def _blocked_csettings(self): #{{{
#        sup = super(CondDecoSignal, self)._blocked_csettings()
#        return sup | set(['chooser', 'return_chooser', 'policy', 'return_policy', 'yield_chooser', 'yield_policy'])
#    # End def #}}}

#    def _set_custom_global_settings(self, kwargs, gset): #{{{
#        self.chooser_policy = kwargs.get('policy', self.chooser_policy)
#        self.chooser = kwargs.get('chooser', self.chooser)
#        self.return_chooser_policy = kwargs.get('return_policy', self.return_chooser_policy)
#        self.return_chooser = kwargs.get('return_chooser', self.return_chooser)
#        self.yield_chooser_policy = kwargs.get('yield_policy', self.yield_chooser_policy)
#        self.yield_chooser = kwargs.get('yield_chooser', self.yield_chooser)
#        super(CondDecoSignal, self)._set_custom_global_settings(kwargs, gset)
#    # End def #}}}

#    def _cond(self, name, condfunc): #{{{
#        def factory(func): #{{{
#            condtup = (condfunc, func)
#            ret = self._generic(condtup, name)
#            if ret is condtup:
#                return func
#            return ret
#        # End def #}}}
#        return factory
#    # End def #}}}

#    def cond(self, condfunc): #{{{
#        return self._cond('choose', condfunc)
#    # End def #}}}

#    def return_cond(self, condfunc): #{{{
#        return self._cond('choosereturn', condfunc)
#    # End def #}}}

#    def yield_cond(self, condfunc): #{{{
#        return self._cond('chooseyield', condfunc)
#    # End def #}}}
## End class #}}}
## ==================================================================================
## WhenDecoSignal
## ==================================================================================
#class WhenDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __decorators__ = ['when', 'when_return', 'when_yield']
#    __dependencies__ = [CondDecoSignal]
#    def _when(self, condfunc, s): #{{{
#        if not isinstance(s, basestring):
#            raise TypeError('argument must be a string')
#        def factory(func):
#            args, vargs, vkeys, defaults = spec = cgetargspec(func)
#            names = set(list(args) + [vargs, vkeys])
#            n, _join, csg = 'cs_str', ''.join, dict(__builtin__.__dict__)
#            csg.update(self.connect_settings.get('globals', {}))

#            # Find name that is unbound 
#            while n in names or n in csg:
#                n = _join(n, '_')

#            # Pre-compile expression into a code object
#            csg[n] = compile_str(s.strip(), __file__, 'eval')

#            # Build a new function
#            code_args = args + [v for v in (vargs, vkeys) if v != None]
#            fcode = Code(CodeList(), (), code_args, bool(vargs), bool(vkeys), True, 'whenfunc', '<dynamic when function>', 1, None)
#            fcode.code[:] = ([(SetLineno, 2), (LOAD_GLOBAL, 'bool'), (LOAD_GLOBAL, 'eval'),
#                                (LOAD_GLOBAL, n), (CALL_FUNCTION, 1), (CALL_FUNCTION, 1), 
#                                (RETURN_VALUE, None)])
#            whenfunc = newfunction(fcode.to_code(), csg, 'whenfunc', default_argvals(args, defaults))

#            self._vars['settings']['weakcondf'] = False
#            return condfunc(whenfunc)(func)
#        return factory
#    # End def #}}}

#    def when(self, s): #{{{
#        return self._when(self.cond, s)
#    # End def #}}}

#    def when_return(self, s): #{{{
#        return self._when(self.return_cond, s)
#    # End def #}}}

#    def when_yield(self, s): #{{{
#        return self._when(self.yield_cond, s)
#    # End def #}}}
## End class #}}}

## ==================================================================================
## CascadeDecoSignal
## ==================================================================================
#class CascadeDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __decorators__ = ['cascade', 'cascade_return', 'cascade_yield']
#    __dependencies__ = [CondDecoSignal]
#    def _cascade(self, condfunc, s, stop=False): #{{{
#        self._set_settings(dict((n, 'cascade') for n in ('policy', 'return_policy', 'yield_policy')))
#        if not isinstance(s, basestring):
#            raise TypeError('argument must be a string')
#        elif not isinstance(stop, bool) and not isinstance(stop, basestring):
#            raise TypeError("The 'stop' argument must be either a boolean or a string")
#        def factory(func):
#            args, vargs, vkeys, defaults = cgetargspec(func)
#            names = set(list(args) + [vargs, vkeys])
#            n, sn, _join, csg = 'cs_str', 'cs_stop_str', ''.join, dict(__builtin__.__dict__)
#            csg['StopCascade'] = StopCascade
#            csg.update(self.connect_settings.get('globals', {}))

#            # Find names that are unbound 
#            while n in names or n in csg:
#                n = _join(n, '_')
#            while sn in names or sn in csg:
#                sn = _join(sn, '_')

#            # Pre-compile expression into a code object
#            csg[n] = compile_str(s.strip(), '<dynamic cascade expression>', 'eval')
#            csg[sn] = (stop if not isinstance(stop, basestring) 
#                            else compile_str(str(stop).strip(), '<dynamic cascade stop condition>', 'eval'))

#            # Build a new function:
#            # def cascadefunc(*args, **kwargs): # Not really, dynamically generate args
#            #     ret = bool(eval(s))
#            #     if isinstance(stop, basestring):
#            #         stop = eval(stop)
#            #     if bool(stop):
#            #         raise StopCascade(ret)
#            #     return ret
#            code_args = args + [v for v in (vargs, vkeys) if v != None]
#            fcode = Code(CodeList(), (), code_args, bool(vargs), bool(vkeys), True, 'cascadefunc', '<dynamic cascade function>', 1, None)
#            labels = map(lambda i: Label(), xrange(4))
#            fcode.code[:] = ([(SetLineno, 2), 
#                              (LOAD_GLOBAL, 'bool'), 
#                              (LOAD_GLOBAL, 'eval'),
#                              (LOAD_GLOBAL, n), 
#                              (CALL_FUNCTION, 1), 
#                              (CALL_FUNCTION, 1), 
#                              (STORE_FAST, 'ret'), 

#                              (SetLineno, 3), 
#                              (LOAD_GLOBAL, sn), 
#                              (STORE_FAST, 'stop'), 

#                              (SetLineno, 4), 
#                              (LOAD_GLOBAL, 'isinstance'),
#                              (LOAD_FAST, 'stop'),
#                              (LOAD_GLOBAL, 'basestring'),
#                              (CALL_FUNCTION, 2), 
#                              (JUMP_IF_FALSE, labels[0]),
#                              (POP_TOP, None),

#                              (SetLineno, 5), 
#                              (LOAD_GLOBAL, 'eval'),
#                              (LOAD_FAST, 'stop'),
#                              (CALL_FUNCTION, 1), 
#                              (STORE_FAST, 'stop'), 
#                              (JUMP_FORWARD, labels[1]), 
#                              (labels[0], None), 
#                              (POP_TOP, None),
#                              (labels[1], None), 

#                              (SetLineno, 6), 
#                              (LOAD_FAST, 'stop'),
#                              (JUMP_IF_FALSE, labels[2]),
#                              (POP_TOP, None),

#                              (SetLineno, 7), 
#                              (LOAD_GLOBAL, 'StopCascade'),
#                              (LOAD_FAST, 'ret'),
#                              (CALL_FUNCTION, 1),
#                              (RAISE_VARARGS, 1),
#                              (JUMP_FORWARD, labels[3]),
#                              (labels[2], None),
#                              (POP_TOP, None),

#                              (SetLineno, 8),
#                              (labels[3], None),
#                              (LOAD_FAST, 'ret'),

#                              (RETURN_VALUE, None)])
#            cascadefunc = newfunction(fcode.to_code(), csg, 'cascadefunc', default_argvals(args, defaults))
#            self._vars['settings']['weakcondf'] = False
#            return condfunc(cascadefunc)(func)
#        return factory
#    # End def #}}}

#    def cascade(self, s, stop=False): #{{{
#        return self._cascade(self.cond, s, stop)
#    # End def #}}}

#    def cascade_return(self, s, stop=False): #{{{
#        return self._cascade(self.return_cond, s, stop)
#    # End def #}}}

#    def cascade_yield(self, s, stop=False): #{{{
#        return self._cascade(self.yield_cond, s, stop)
#    # End def #}}}
## End class #}}}
## ==================================================================================
## GenericMatchDecoSignal
## ==================================================================================
#class GenericMatchDecoSignal(CustomDecoSignal): #{{{
#    __slots__ = ()
#    __dependencies__ = [CondDecoSignal]
#    def _custom_blocked_csettings(self, name): #{{{
#        sw = name.startswith
#        block_startswith = ('margs_', 'mkw_', 'match_')
#        return any(sw(s) for s in block_startswith)
#    # End def #}}}

#    def _custom_expected(self, varname, kwargs, gset): #{{{
#        sw = varname.startswith
#        exp_startswith = ('margs_', 'mkw_', 'match_')
#        return any(sw(s) for s in exp_startswith)
#    # End def #}}}
## End class #}}}
## ==================================================================================
## MatchTypeDecoSignal
## ==================================================================================
#class MatchTypeDecoSignal(GenericMatchDecoSignal): #{{{
#    __slots__ = ()
#    __decorators__ = ['match_type', 'match_return_type', 'match_yield_type']

#    def _match_type(self, condfunc, *margs, **mkwargs): #{{{
#        it = InstanceType
#        cs = self.connect_settings
#        autotype = cs.pop('mkw_autotype', False)
#        def mk_itype(o): #{{{
#            if autotype:
#                if not isclass(o):
#                    o = o.__class__
#                return InstanceType(o)
#            return o
#        # End def #}}}
#        margs_len = len(margs)
#        arg_opt = dict()
#        kw_opt = dict(arg_opt)
#        match = {'match_': [arg_opt, kw_opt], 'margs_': [arg_opt], 'mkw_': [kw_opt]}
#        for k, v in cs.iteritems():
#            klen, ind = len(k), k.find('_')
#            frag = '' if ind < 0 else k[:ind+1]
#            anchor = len(frag)
#            if frag in match and klen > anchor:
#                key, val = k[anchor:], bool(v)
#                for l in match[frag]:
#                    l[key] = val

#        vargs = Sequence((it(t) for t in margs), **arg_opt)
#        vmap = Mapping(((mk_itype(k), v) for k, v in mkwargs.iteritems()), **kw_opt)
#        def checksig(*args, **kwargs): #{{{
#            return vargs == args and vmap == kwargs
#        # End def #}}}
#        self._vars['settings']['weakcondf'] = False
#        return condfunc(checksig)
#    # End def #}}}

#    def match_type(self, *margs, **mkwargs): #{{{
#        return self._match_type(self.cond, *margs, **mkwargs)
#    # End def #}}}

#    def match_return_type(self, marg): #{{{
#        return self._match_type(self.return_cond, marg)
#    # End def #}}}

#    def match_yield_type(self, marg): #{{{
#        return self._match_type(self.yield_cond, marg)
#    # End def #}}}

## End class #}}}
## ==================================================================================
## MatchDecoSignal
## ==================================================================================
#class MatchDecoSignal(GenericMatchDecoSignal): #{{{
#    __slots__ = ()
#    __decorators__ = ['match', 'match_return', 'match_yield']
#    def _match(self, condfunc, *margs, **mkwargs): #{{{
#        cs = self.connect_settings
#        margs_len = len(margs)
#        arg_opt = dict()
#        kw_opt = dict(arg_opt)
#        match = {'match_': [arg_opt, kw_opt], 'margs_': [arg_opt], 'mkw_': [kw_opt]}
#        for k, v in cs.iteritems():
#            klen, ind = len(k), k.find('_')
#            frag = '' if ind < 0 else k[:ind+1]
#            anchor = len(frag)
#            if frag in match and klen > anchor:
#                key, val = k[anchor:], bool(v)
#                for l in match[frag]:
#                    l[key] = val

#        v_arg = Sequence(margs, **arg_opt)
#        v_kw = Mapping(mkwargs, **kw_opt)

#        def checksig(*args, **kwargs): #{{{
#            return v_arg == args and v_kw == kwargs
#        # End def #}}}
#        self._vars['settings']['weakcondf'] = False
#        return condfunc(checksig)
#    # End def #}}}

#    def match(self, marg, *margs, **mkwargs): #{{{
#        return self._match(self.cond, marg, *margs, **mkwargs)
#    # End def #}}}

#    def match_return(self, marg): #{{{
#        return self._match(self.return_cond, marg)
#    # End def #}}}

#    def match_yield(self, marg): #{{{
#        return self._match(self.yield_cond, marg)
#    # End def #}}}

## End class #}}}
# ==================================================================================
# signal
# ==================================================================================
def make_signal(**kwargs): #{{{
    def mkdeco(f, kwargs): #{{{
        sigkw = kwargs.pop('sigkw_', {})
        if 'overload' in kwargs:
            sigkw['weak'] = False
        signature = []
        sigapp = signature.append
        for ext in kwargs.pop('decoext_', ()):
            if not isclass(ext) or not issubclass(ext, CustomDecoSignal):
                raise TypeError("The 'decoext' keyword expected CustomDecoSignal classes, got %s instead" %ext.__name__)
            sigapp(ext)
        sigapp(DecoSignalExtension)
        for ext in kwargs.pop('sigext_', ()):
            if not isclass(ext) or not issubclass(ext, SignalExtension):
                raise TypeError("The 'sigext' keyword expected SignalExtension classes, got %s instead" %ext.__name__)
            sigapp(ext)
        sigapp(BaseSignal)
        _NewDecoSignal = newclass('_NewDecoSignal', tuple(signature), 
                                  dict(__slots__ = ()))
        return _NewDecoSignal(f, **sigkw)
    # End def #}}}
    def settings(func): #{{{
        signal = getattr(func, 'signal', None)
        if isinstance(signal, DecoSignalExtension) and isinstance(signal, BaseSignal):
            DecoSignalFunction = func
        elif not _isf(func) and not isclass(func):
            raise TypeError('argument must be a python function or a python class')
        else:
            signal = mkdeco(func, kwargs)
            args, vargs, vkeys, defaults = spec = cgetargspec(func)
            code_args = args + [v for v in (vargs, vkeys) if v != None]
            fcode = Code(CodeList(), (), code_args, bool(vargs), bool(vkeys), True, 'f', '<dynamic decorator signal function>', 1, None)
            fcode.code[:] = ([(SetLineno, 2), (LOAD_GLOBAL, 'signal')] + bp_call_args(*spec) + 
                            [(RETURN_VALUE, None)])
            DecoSignalFunction = newfunction(fcode.to_code(), locals(), 'DecoSignalFunction', default_argvals(args, defaults))
        d = DecoSignalFunction
        d = wraps(func)(d)
        d.signal = signal
        signal.signalfunc = d
        for n in signal.decorators:
            setattr(d, n, getattr(signal, n))
        kwargs.pop('decoext_', ())
        kwargs.pop('sigext_', ())
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
                MatchTypeDecoSignal, MatchDecoSignal): #{{{
    __slots__ = ()
# End class #}}}

def signal(**kwargs): #{{{
    sigext = [DefaultExtension]
    decoext = [DefaultDecoSignal]
    kwargs['sigext_'] = sigext
    kwargs['decoext_'] = decoext
    return make_signal(**kwargs)
# End def #}}}
# ==================================================================================
# 
# ==================================================================================
