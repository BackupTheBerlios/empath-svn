# Module: smanstal.util.seq
# File: seq.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('groupby',)

class groupby_mixin(object):
    def __init__(self, seq, key=lambda x:x, store=False):
        self._store = store
        setdefault = self.setdefault
        for value in seq:
            k = key(value)
            if store:
                setdefault(k, []).append(value)
            else:
                setdefault(k, [0])[0] += 1
    def __iter__(self):
        if self._store:
            return self.iteritems()
        return ((k, v[0]) for k, v in self.iteritems())

class groupby(groupby_mixin, dict):
    pass
