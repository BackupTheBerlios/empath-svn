-------------
Connect Tests
-------------

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
>>> def temp_after(ret, l):
...    return test_after(ret, l)
...
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

Connect category
=================
>>> signal.connect_after(dict(after=[test_after]))
>>> signal.connect_before(dict(before=[test_before]))
>>> print signal([])
['BEFORE', 'SIGNAL', 'AFTER']

Multi-category Connect
========================
>>> signal = Signal(test_signal)
>>> signal.connect(dict(after=dict(after=[test_after]),
...                     before=dict(before=[test_before])))
>>> print signal([])
['BEFORE', 'SIGNAL', 'AFTER']

Options
========

Weak option
-------------
>>> signal = Signal(test_signal)
>>> signal.connect(dict(after=dict(after=[temp_after])), weak=True)
>>> print signal([])
['SIGNAL', 'AFTER']
>>> del temp_after
>>> print signal([])
['SIGNAL']

