----------------------------
Category/slot: before/before
----------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_before(l):
...    l.append('BEFORE')
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``before`` slot
================
>>> signal.connect_before(dict(before=[test_before]))
>>> print signal([])
['BEFORE', 'SIGNAL']

