-------------------------------
Category/slot: after/onreturn
-------------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_onreturn(ret):
...    ret.append('ONRETURN')
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``onreturn`` slot
================
>>> signal.connect_after(dict(onreturn=[test_onreturn]))
>>> print signal([])
['SIGNAL', 'ONRETURN']

