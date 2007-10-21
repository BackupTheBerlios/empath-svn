-------------------------------
Category/slot: replace/choose
-------------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l += l.__class__(['SIGNAL'])
...    return l
... 
>>> def islist(l):
...    return isinstance(l, list)
... 
>>> def istuple(l):
...    return isinstance(l, tuple)
... 
>>> def to_tuple(l):
...    return tuple(['TO_TUPLE'])
... 
>>> def to_list(l):
...    return ['TO_LIST']
... 
>>> def list_add(l):
...    l.append('ADD') 
...    return l
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``choose`` slot
================

No policy
----------
>>> signal.connect_replace(dict(choose=[(istuple, to_list), 
...                                     (islist, to_tuple)]))
>>> print signal([])
('TO_TUPLE',)
>>> print signal(())
['TO_LIST']

Default policy
---------------
>>> signal = Signal(test_signal, choose_policy='default')
>>> signal.connect_replace(dict(choose=[(istuple, to_list), 
...                                     (islist, to_tuple)]))
>>> print signal([])
['SIGNAL']

First policy
-------------
>>> signal = Signal(test_signal, choose_policy='first')
>>> signal.connect_replace(dict(choose=[(islist, list_add), 
...                                     (islist, to_tuple)]))
>>> print signal([])
['ADD']
>>> signal = Signal(test_signal, choose_policy='first')
>>> signal.connect_replace(dict(choose=[(islist, to_tuple), 
...                                     (islist, list_add)]))
>>> print signal([])
('TO_TUPLE',)

Last policy
-------------
>>> signal = Signal(test_signal, choose_policy='last')
>>> signal.connect_replace(dict(choose=[(islist, list_add), 
...                                     (islist, to_tuple)]))
>>> print signal([])
('TO_TUPLE',)
>>> signal = Signal(test_signal, choose_policy='last')
>>> signal.connect_replace(dict(choose=[(islist, to_tuple), 
...                                     (islist, list_add)]))
>>> print signal([])
['ADD']

Ambiguous Choice
------------------
>>> signal = Signal(test_signal)
>>> signal.connect_replace(dict(choose=[(islist, list_add), 
...                                     (islist, to_tuple)]))
>>> print signal([])
Traceback (most recent call last):
   ...
AmbiguousChoiceError: Found more than one selectable callable

