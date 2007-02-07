# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from smanstal.collections.multidict import MultiDictMixin
from smanstal.types.introspect import ismapping

__all__ = ('seqvalues', 'mixedvalues')

def seqvalues(d, seqtype=list): #{{{
    if not ismapping(d):
        raise TypeError("%s is not a valid mapping object" %d.__class__.__name__)
    elif isinstance(d, MultiDictMixin):
        return dict(d)
    else:
        return dict((k, seqtype([v])) for k, v in d.iteritems())
# End def #}}}

def mixedvalues(d, seqtype=list): #{{{
    if not ismapping(d):
        raise TypeError("%s is not a valid mapping object" %d.__class__.__name__)
    elif isinstance(d, MultiDictMixin):
        getall = d.getall
        def mkval(k): #{{{
            vals = getall(k)
            return seqtype(vals) if len(vals) > 1 else vals[0]
        # End def #}}}
        return dict((k, mkval(k)) for k in d)
    else:
        return dict(d)
# End def #}}}
