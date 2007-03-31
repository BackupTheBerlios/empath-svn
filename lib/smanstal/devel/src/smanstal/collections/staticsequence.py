# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.types.introspect import ishashable, iscallable, ismapping, isclass
#from smanstal.util.proxy import proxy  
from smanstal.types.proxy import proxy

__all__ = ('staticsequence', 'opair', 'unopair', 'disunopair')

def staticsequence(name, pcls, **options): #{{{
    n = options.get('n', 1)
    h = options.get('hashable', True)
    assert n >= 1, "cannot create static sequence type with less than 1 element"
    assert isclass(pcls), "cannot create static sequence from non-class"
    BaseSeq = proxy(pcls)
    class StaticSequence(BaseSeq): #{{{
        __slots__ = ()
        def __init__(self, *args): #{{{
            if not args:
                raise TypeError("'%s' object cannot be empty" %name)
            if len(args) == 1 and n > 1:
                args = args[0]
            exec compile('args = (%s) = args' %', '.join('v%i' %i for i in xrange(n)), '<string>', 'exec') in locals()
            super(StaticSequence, self).__init__(args)
            if h:
                hash(self) # Throw error if not hashable
        # End def #}}}

        def __repr__(self): #{{{
            return ' '.join([name, str(self)])
        # End def #}}}

        def __setattr__(self, n, val): #{{{
            raise AttributeError("'%s' object cannot set attribute '%s'" %(name, n))
        # End def #}}}

        def __delattr__(self, n): #{{{
            raise AttributeError("'%s' object cannot delete attribute '%s'" %(name, n))
        # End def #}}}

        def __eq__(self, obj): #{{{
            if not isinstance(obj, self.__class__):
                try:
                    obj = self.__class__(obj)
                except TypeError:
                    return False
            return super(StaticSequence, self).__eq__(obj)
        # End def #}}}

        def __ne__(self, obj): #{{{
            return not self.__eq__(obj)
        # End def #}}}
    # End class #}}}
    StaticSequence.__name__ = name
    return StaticSequence
# End def #}}}

opair = staticsequence('opair', tuple, n=2)

class baseunopair(tuple): #{{{
    __slots__ = ()
    def __eq__(self, o): #{{{
        try:
            val = (v1, v2) = o
        except:
            raise Exception(o)
        sup = super(baseunopair, self).__eq__
        return bool(sup(val) or sup(val[::-1]))
    # End def #}}}

    def __hash__(self): #{{{
        return hash((min(self), max(self)))
    # End def #}}}
# End class #}}}
unopair = staticsequence('unopair', baseunopair, n=2)

class basedisunopair(baseunopair): #{{{
    __slots__ = ()
    def __init__(self, *args): #{{{
        if len(args) == 1:
            args = args[0]
        if args:
            v1, v2 = args
            if v1 == v2:
                raise ValueError("Pairs must be of distinct values")
        super(basedisunopair, self).__init__(self, *args)
    # End def #}}}
# End class #}}}
disunopair = staticsequence('disunopair', basedisunopair, n=2)


