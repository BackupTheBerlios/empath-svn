----------------------------
Category/slot: around/around
----------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_around(next, l):
...    l.append('AROUND: BEFORE')
...    ret = next(l)
...    ret.append('AROUND: AFTER')
...    return ret
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``around`` slot
================
>>> signal.connect_around(dict(around=[test_around]))
>>> print signal([])
['AROUND: BEFORE', 'SIGNAL', 'AROUND: AFTER']

