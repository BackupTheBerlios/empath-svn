-------------------------------
Category/slot: around/streamin
-------------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l += l.__class__(['SIGNAL'])
...    return l
... 
>>> def test_streamin(next, args, kwargs):
...    args[0] = tuple()
...    return next(args, kwargs)
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``streamin`` slot
================
>>> signal.connect_around(dict(streamin=[test_streamin]))
>>> print signal([])
('SIGNAL',)

