-------------------------------
Category/slot: replace/choosereturn
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
>>> def to_tuple(ret):
...    return tuple(ret + ['TO_TUPLE'])
... 
>>> def to_list(ret):
...    return list(ret) + ['TO_LIST']
... 
>>> def list_add(ret):
...    ret.append('ADD') 
...    return ret
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``choosereturn`` slot
======================

No policy
----------
>>> signal.connect_replace(dict(choosereturn=[(istuple, to_list), 
...                                           (islist, to_tuple)]))
>>> print signal([])
('SIGNAL', 'TO_TUPLE')
>>> print signal(())
['SIGNAL', 'TO_LIST']

Default policy
---------------
>>> signal = Signal(test_signal, choose_return_policy='default')
>>> signal.connect_replace(dict(choosereturn=[(istuple, to_list), 
...                                           (islist, to_tuple)]))
>>> print signal([])
['SIGNAL']

First policy
-------------
>>> signal = Signal(test_signal, choose_return_policy='first')
>>> signal.connect_replace(dict(choosereturn=[(islist, list_add), 
...                                           (islist, to_tuple)]))
>>> print signal([])
['SIGNAL', 'ADD']
>>> signal = Signal(test_signal, choose_return_policy='first')
>>> signal.connect_replace(dict(choosereturn=[(islist, to_tuple), 
...                                           (islist, list_add)]))
>>> print signal([])
('SIGNAL', 'TO_TUPLE')

Last policy
-------------
>>> signal = Signal(test_signal, choose_return_policy='last')
>>> signal.connect_replace(dict(choosereturn=[(islist, list_add), 
...                                           (islist, to_tuple)]))
>>> print signal([])
('SIGNAL', 'TO_TUPLE')
>>> signal = Signal(test_signal, choose_return_policy='last')
>>> signal.connect_replace(dict(choosereturn=[(islist, to_tuple), 
...                                           (islist, list_add)]))
>>> print signal([])
['SIGNAL', 'ADD']

Ambiguous Choice
------------------
>>> signal = Signal(test_signal)
>>> signal.connect_replace(dict(choosereturn=[(islist, list_add), 
...                                           (islist, to_tuple)]))
>>> print signal([])
Traceback (most recent call last):
   ...
AmbiguousChoiceError: Found more than one selectable callable

