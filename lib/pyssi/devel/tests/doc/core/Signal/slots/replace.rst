----------------------------
Category/slot: replace/replace
----------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_replace(next, l):
...    l.append('REPLACE: BEFORE')
...    ret = next(l)
...    ret.append('REPLACE: AFTER')
...    return ret
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

``replace`` slot
================
>>> signal.connect_replace(dict(replace=[test_replace]))
>>> print signal([])
['REPLACE: BEFORE', 'SIGNAL', 'REPLACE: AFTER']

