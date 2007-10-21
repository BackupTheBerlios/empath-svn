----------------------------
Category order tests
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
>>> def test_after(ret, l):
...    ret.append('AFTER')
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

Test Order
================
>>> signal.connect(dict(replace=dict(replace=[test_replace]),
...                     around=dict(around=[test_around]),
...                     before=dict(before=[test_before]),
...                     after=dict(after=[test_after])))
>>> print signal([])
['BEFORE', 'AROUND: BEFORE', 'REPLACE: BEFORE', 'SIGNAL', 'REPLACE: AFTER', 'AROUND: AFTER', 'AFTER']

