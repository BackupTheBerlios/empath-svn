-------------------------------
Category/slot: around/stream
-------------------------------

Setup
======
>>> from pyssi.core import Signal
>>> def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> def test_stream(ret):
...    ret.append('STREAM')
...    return ret
... 
>>> def test_laststream(ret):
...    ret.append('LAST')
...    return tuple(ret)
... 
>>> signal = Signal(test_signal)
>>> print signal([])
['SIGNAL']

``stream`` slot
================
>>> signal.connect_around(dict(stream=[test_stream, test_laststream]))
>>> print signal([])
('SIGNAL', 'STREAM', 'LAST')

