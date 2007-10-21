-------------------------------
Category/slot: replace/chooseyield
-------------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(numlist):
...    for i in numlist:
...       yield i
... 
>>> def is2(el):
...    return (el == 2)
... 
>>> def is42(el):
...    return (el == 42)
... 
>>> def change2(el):
...    return 'TWO'
... 
>>> def change42(el):
...    return 'ANSWER'
... 
>>> def change42ex(el):
...    return 'SUPER ANSWER'
... 
>>> NUMLIST = [1, 2, 3, 4, 42, 100, 200]
>>> signal = Signal(test_signal)
>>> print list(signal(NUMLIST))
[1, 2, 3, 4, 42, 100, 200]

``chooseyield`` slot
=====================

No policy
----------
>>> signal.connect_replace(dict(chooseyield=[(is2, change2), 
...                                          (is42, change42)]))
>>> print list(signal(NUMLIST))
[1, 'TWO', 3, 4, 'ANSWER', 100, 200]

Default policy
---------------
>>> signal = Signal(test_signal, choose_yield_policy='default')
>>> signal.connect_replace(dict(chooseyield=[(is2, change2), 
...                                          (is42, change42)]))
>>> print list(signal(NUMLIST))
[1, 2, 3, 4, 42, 100, 200]

First policy
-------------
>>> signal = Signal(test_signal, choose_yield_policy='first')
>>> signal.connect_replace(dict(chooseyield=[(is42, change42), 
...                                          (is42, change42ex)]))
>>> print list(signal(NUMLIST))
[1, 2, 3, 4, 'ANSWER', 100, 200]
>>> signal = Signal(test_signal, choose_yield_policy='first')
>>> signal.connect_replace(dict(chooseyield=[(is42, change42ex), 
...                                           (is42, change42)]))
>>> print list(signal(NUMLIST))
[1, 2, 3, 4, 'SUPER ANSWER', 100, 200]

Last policy
-------------
>>> signal = Signal(test_signal, choose_yield_policy='last')
>>> signal.connect_replace(dict(chooseyield=[(is42, change42), 
...                                          (is42, change42ex)]))
>>> print list(signal(NUMLIST))
[1, 2, 3, 4, 'SUPER ANSWER', 100, 200]
>>> signal = Signal(test_signal, choose_yield_policy='last')
>>> signal.connect_replace(dict(chooseyield=[(is42, change42ex), 
...                                           (is42, change42)]))
>>> print list(signal(NUMLIST))
[1, 2, 3, 4, 'ANSWER', 100, 200]

Ambiguous Choice
------------------
>>> signal = Signal(test_signal)
>>> signal.connect_replace(dict(chooseyield=[(is42, change42), 
...                                          (is42, change42ex)]))
>>> print list(signal(NUMLIST))
Traceback (most recent call last):
   ...
AmbiguousChoiceError: Found more than one selectable callable

