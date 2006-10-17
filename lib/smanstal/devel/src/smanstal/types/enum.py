# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# The following was taken and modified from v1.6 of the following recipe
# by Zoran Isailovski:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/413486
from smanstal.util.misc import increment
from smanstal.types.introspect import ismagicname

from weakref import ref

__all__ = ('enum',)

def enum(names=(), **options): #{{{
    assert names, "Empty enums are not supported"
    def enumvals(names, incfunc, start=0): #{{{
        inc = incfunc(start-1)
        inc.next()
        nfunc, cfunc = inc.next, inc.send
        for n in names: #{{{
            if isinstance(n, tuple):
                name, val = n
                if not isinstance(name, basestring):
                    raise TypeError("Non-string name detected: %s" %n.__class__.__name__)
                elif not isinstance(val, int) and not isinstance(val, long):
                    raise TypeError("Non-integer value detected: %s" %val.__class__.__name__)
                yield name, cfunc(val)
            elif not isinstance(n, basestring):
                raise TypeError("Non-string name detected: %s" %n.__class__.__name__)
            else:
                yield n, nfunc()
        # End for #}}}
        inc.close()
    # End def #}}}

    optget = options.get
    incfunc = optget('incfunc', increment)
    start = optget('start', 0)
    cur = []
    for n in names:
        if n not in cur:
            cur.append(n)
    names = cur
    constants = [(k, v) for k, v in enumvals(names, incfunc, start)]
    names = tuple(k for k, v in constants)
    constants = tuple(sorted(constants, key=lambda k: k[1]))
    chash, enumdict = hash(constants), dict(constants)
    del constants

    class EnumValues(object): #{{{
        __slots__ = ()
        def __get__(self, inst, owner): #{{{
            return self
        # End def #}}}

        def __getattribute__(self, name): #{{{
            ogetattr = object.__getattribute__
            if ismagicname(name) and name in dir(self):
                return ogetattr(self, name)
            try:
                return enumdict[name]
            except KeyError:
                return ogetattr(self, name)
        # End def #}}}

        def __getitem__(self, name):  return enumdict[name]
        def __iter__(self):        return (n for n in names)
    # End class #}}}

    class Enum(object): #{{{
        __slots__ = ()
        def __iter__(self):        return enumdict.__iter__()
        def __contains__(self, val):
            if isinstance(val, basestring):
                return val in enumdict
            return val in enumdict.itervalues()
        def __len__(self):         return len(enumdict)
        def __repr__(self):        return 'enum' + str(names)
        def __str__(self):         return 'enum ' + str(names)
        def __hash__(self):        return chash
        def __getitem__(self, name):  return enumdict[name]
        def __eq__(self, obj): return self.__contains__(obj)
        def keys(self):            return names[:]
        def values(self):          return [enumdict[n] for n in names]
        def items(self):           return [(n, enumdict[n]) for n in names]
        def iterkeys(self):        return enumdict.iterkeys()
        def itervalues(self):      return enumdict.itervalues()
        def iteritems(self):       return enumdict.iteritems()
        names = n = EnumValues()
    # End class #}}}

    EnumType = Enum()
    return EnumType
# End def #}}}
