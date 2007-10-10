=============
Signal Tests
=============

Connect
========

>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_before(l):
...    l.append('BEFORE')
... 
>>> def test_after(ret, l):
...    ret.append('AFTER')
... 
>>> signal = Signal(test_signal, weak=True)
>>> print signal([])
['SIGNAL']
>>> signal.connect('after', dict(after=[test_after]))
>>> signal.connect('before', dict(before=[test_before]))
>>> print signal([])
['BEFORE', 'SIGNAL', 'AFTER']

