# Module: smanstal.types.borg
# File: borg.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import isfunction, hasmagicname, isclass

class BorgCollective(type): #{{{
    __borg__ = {}
#    def __new__(bcoll, classname, bases, clsdict): #{{{
#        ret = type.__new__(bcoll, classname, bases, clsdict)
#        type.__setattr__(bcoll, '__borg__', {})
#        return ret
#    # End def #}}}

    def __init__(cls, classname, bases, clsdict): #{{{
        newdict = dict()
        block = ('__init__',)
        isinit = lambda v: hasmagicname(v) and v.__name__ in block
        def mkborgfunc(cls, key, val): #{{{
            if isfunction(val) and not isinit(val):
                val = classmethod(val)
                setattr(cls, key, val)
            return val
        # End def #}}}
        newdict = dict((k, mkborgfunc(cls, k, v)) for k, v in clsdict.iteritems())
        borgdict = cls.__borg__
        type.__setattr__(cls, '__borg__', borgdict)
        newdict['__borg__'] = borgdict
        cls.handle_slots(newdict)
        initfunc = newdict.get('__init__', None)
        if initfunc:
            type.__setattr__(cls, '__init__', cls.mkinit(initfunc, '__slots__' in newdict))
            newdict['__init__'] = cls.__init__
        if True not in (isinstance(b, BorgCollective) for b in bases):
            cls.mkattrfunc(cls, newdict)
        super(BorgCollective, cls).__init__(classname, bases, newdict)
    # End def #}}}

    def handle_slots(borg, newdict): #{{{
        slots = None
        try:
            slots = type.__getattribute__(borg, '__slots__')
        except AttributeError:
            pass
        if not slots:
            return
        for name in slots:
            if name not in newdict:
                type.__delattr__(borg, name)
    # End def #}}}

    def mkinit(borg, initfunc, haveslots): #{{{
        def __init__(self, *args, **kwargs): #{{{
            def setdict(haveslots, hive): #{{{
                if not haveslots:
                    object.__setattr__(self, '__dict__', hive)
            # End def #}}}
            before = borg.__borg__
            hive = dict(before)
            setdict(haveslots, before)
            initfunc(self, *args, **kwargs)
            # Trying to escape assimilation?
            type.__setattr__(borg, '__borg__', hive)
            type.__setattr__(self.__class__, '__borg__', hive)
            setdict(haveslots, hive)
        # End def #}}}
        __init__.__name__ = initfunc.__name__
        __init__.__doc__ = initfunc.__doc__
        __init__.__dict__ = initfunc.__dict__
        return __init__
    # End def #}}}

    def mkattrfunc(borg, cls, newdict): #{{{
        __getattribute__ = borg.__getattribute__.im_func
        __setattr__ = borg.__setattr__.im_func
        __delattr__ = borg.__delattr__.im_func
        afunc = ((k, v) for k, v in locals().items() if k.startswith('__'))
        for n, func in afunc:
            newf = classmethod(func).__get__(None, cls)
            newdict[n] = newf
            type.__setattr__(cls, n, newf)
    # End def #}}}

    def __getattribute__(borg, name): #{{{
        b = type.__getattribute__(borg, '__borg__')
        try:
            ret = b.__getitem__(name)
        except KeyError:
            ret = object.__getattribute__(borg, name)
        return ret
    # End def #}}}

    def __setattr__(borg, name, val): #{{{
        slots = None
        haveval = False
        try:
            getattr(borg, name)
        except AttributeError:
            haveval = False
        else:
            haveval = True
        try:
            slots = type.__getattribute__(borg, '__slots__')
        except AttributeError:
            pass
        if (not slots and slots is not None) or (slots and name not in slots):
            errmsg = "The Borg has denied access to '%s'" %name
            if not haveval:
                errmsg = "The Borg has no attribute '%s'" %name
            raise AttributeError(errmsg)
        borg.__borg__.__setitem__(name, val)
    # End def #}}}

    def __delattr__(borg, name): #{{{
        setattr(borg, name, None)
        borg.__borg__.__delitem__(name)
    # End def #}}}
# End class #}}}

class Borg(object): #{{{
    __metaclass__ = BorgCollective
# End class #}}}
