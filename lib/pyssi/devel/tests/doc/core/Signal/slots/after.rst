----------------------------
Category/slot: after/after 
----------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_after(ret, l):
...    ret.append('AFTER')
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``after`` slot
===============
>>> signal.connect_after(dict(after=[test_after]))
>>> print signal([])
['SIGNAL', 'AFTER']

