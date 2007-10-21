=======================
4.1.1 Before and After
=======================

One of the simplest things that can be done with signals
is to run code either before or after a signal is run.

The ``BaseSignal`` class that is provided in ``aossi.core`` already
comes with the functionality to run code before or after a signal:

>>> from aossi.core import BaseSignal
>>> def test_signal(l):
...     l.append('test_signal')
...     return l
...
>>> def test_before(l):
...     l.append('test_before')
...
>>> def test_after(l):
...     l.append('test_after')
...
>>> signal = BaseSignal(test_signal)
>>> signal.connect(before=[test_before])
>>> signal.connect(after=[test_after])
>>> print signal([])
['test_before', 'test_signal', 'test_after']

Generally, what determines when a function or some other callable
runs in relation to some defined signal is the **slot type** that
the callable is connected to the signal as. The ``BaseSignal``
class predefines the **before** and **after** slot types as above.

As an aside, a signal's connect method also accepts callables
as unnamed arguments which get connected to the after slot type:


>>> def test_after2(l):
...     l.append('test_after2')
...
>>> def test_after3(l):
...     l.append('test_after3')
...
>>> signal.connect(test_after2, test_after3)
>>> print signal([])
['test_before', 'test_signal', 'test_after', 'test_after2', 'test_after3']


