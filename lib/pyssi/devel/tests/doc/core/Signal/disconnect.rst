-----------------
Disconnect Tests
-----------------

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
>>> signal = Signal(test_signal, weak=True)
>>> print signal([])
['SIGNAL']

Specific disconnect methods
==============================

>>> signal.connect(dict(after=dict(after=[test_after]), before=dict(before=[test_before])))
>>> signal.disconnect_after(dict(after=[test_after]))
>>> print signal([])
['BEFORE', 'SIGNAL']
>>> signal.disconnect_before(dict(before=[test_before]))
>>> print signal([])
['SIGNAL']

General disconnect
====================
>>> signal.connect(dict(after=dict(after=[test_after]), before=dict(before=[test_before])))
>>> print signal([])
['BEFORE', 'SIGNAL', 'AFTER']
>>> signal.disconnect([test_after])
>>> print signal([])
['BEFORE', 'SIGNAL']
>>> signal.disconnect([test_before])
>>> print signal([])
['SIGNAL']

Weak slots
===========
>>> signal.connect_after(dict(after=[test_after, test_after]), weak=True)
>>> print signal([])
['SIGNAL', 'AFTER', 'AFTER']
>>> signal.disconnect([test_after], count=0)
>>> print signal([])
['SIGNAL']

Options
========

``count``
----------

``count=1``
+++++++++++++
>>> signal.connect_after(dict(after=[test_after, test_after]))
>>> print signal([])
['SIGNAL', 'AFTER', 'AFTER']
>>> signal.disconnect([test_after], count=1)
>>> print signal([])
['SIGNAL', 'AFTER']
>>> signal.disconnect([test_after], count=0)
>>> print signal([])
['SIGNAL']


``count=0``
+++++++++++++++
>>> signal.connect_after(dict(after=[test_after, test_after]))
>>> signal.disconnect([test_after], count=0)
>>> print signal([])
['SIGNAL']
>>> def next_after(ret, iterfunc, **options): #**
...     def nextfunc(*args, **kwargs):
...         for f in iterfunc:
...             f(ret, *args, **kwargs) #**
...     return nextfunc
... 
>>> signal.add_slot('test', 'after', next_after)
>>> signal.connect_after(dict(after=[test_after, test_after], test=[test_after]))
>>> print signal([])
['SIGNAL', 'AFTER', 'AFTER', 'AFTER']
>>> signal.disconnect([test_after], count=1)
>>> print signal([])
['SIGNAL', 'AFTER', 'AFTER']
>>> signal.disconnect()
>>> print signal([])
['SIGNAL']

