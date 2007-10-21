----------------
Add Slot Tests
----------------

Setup
======
>>> from pyssi.core import BaseSignal
>>> def next_around(signal, iterfunc, **options): #**
...     inext = iterfunc.next
...     def nextfunc(*args, **kwargs): #*
...         try:
...             f = inext()
...         except StopIteration:
...             return signal(*args, **kwargs) #*
...         return f(nextfunc, *args, **kwargs) #*
...     return nextfunc
...
>>> def next_another(signal, iterfunc, **options): #**
...     return next_around(signal, iterfunc, **options) #**
...
>>> def next_before(iterfunc, **options): #**
...     def nextfunc(*args, **kwargs): #*
...         for f in iterfunc:
...             f(*args, **kwargs) #*
...     return nextfunc
... 
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_before(l):
...    l.append('BEFORE')
... 
>>> def test_other(l):
...    l.append('OTHER')
... 
>>> def test_around(next, l):
...    l.append('AROUND: BEFORE')
...    ret = next(l)
...    ret.append('AROUND: AFTER')
...    return ret
... 
>>> def test_another(next, l):
...    l.append('AROUND: BEFORE ANOTHER')
...    ret = next(l)
...    ret.append('AROUND: AFTER ANOTHER')
...    return ret
... 
>>> signal = BaseSignal(test_signal)
>>> print signal([])
['SIGNAL']

Simple add slot
=================
>>> signal.add_slot('before', 'before', next_before)
>>> signal.connect_before(dict(before=[test_before]))
>>> print signal([])
['BEFORE', 'SIGNAL']

Insert option
===============
>>> signal = BaseSignal(test_signal)
>>> signal.add_slot('before', 'before', next_before)
>>> signal.add_slot('other', 'before', next_before, insert=0)
>>> signal.connect_before(dict(before=[test_before]))
>>> signal.connect_before(dict(other=[test_other]))
>>> print signal([])
['OTHER', 'BEFORE', 'SIGNAL']

Weak option
============

Delete handler
---------------
>>> signal = BaseSignal(test_signal)
>>> signal.add_slot('before', 'before', next_before, weak=True)
>>> signal.connect_before(dict(before=[test_before]))
>>> print signal([])
['BEFORE', 'SIGNAL']
>>> del next_before
>>> print signal([])
['SIGNAL']

Recreates around/replace categories
------------------------------------
>>> signal.add_slot('around', 'around', next_around, weak=True)
>>> signal.add_slot('another', 'around', next_another, weak=True)
>>> signal.connect_around(dict(around=[test_around], another=[test_another]))
>>> print signal([])
['AROUND: BEFORE', 'AROUND: BEFORE ANOTHER', 'SIGNAL', 'AROUND: AFTER ANOTHER', 'AROUND: AFTER']
>>> del next_another
>>> print signal([])
['AROUND: BEFORE', 'SIGNAL', 'AROUND: AFTER']

