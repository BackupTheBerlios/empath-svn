# Module: smanstal.util.misc
# File: misc.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

def increment(val=0, step=1): #{{{
    while 1:
        next = (yield val)
        if isinstance(next, StopIteration):
            break
        elif next is None:
            val += step
        else:
            val = next
# End def #}}}

# This is v1.0 of imerge by Raymond Hettinger taken from:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/491285
import heapq
def imerge(*iterables): #{{{
    '''Merge multiple sorted inputs into a single sorted output.

    >>> list(imerge([1,3,5,7], [0,2,4,8], [5,10,15,20], [], [25]))
    [0, 1, 2, 3, 4, 5, 5, 7, 8, 10, 15, 20, 25]
    '''
    heappop, heappush = heapq.heappop, heapq.heappush
    its = map(iter, iterables)
    h = []
    for it in its:
        try:
            v = it.next()
        except StopIteration:
            continue
        heappush(h, (v, it.next))
    while h:
        v, next = heappop(h)
        yield v
        try:
            v = next()
        except StopIteration:
            continue
        heappush(h, (v, next))
# End def #}}}
