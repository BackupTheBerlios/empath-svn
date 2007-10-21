-----------------
Stream Decorator
-----------------

Setup
======
>>> from pyssi.core import signal
>>> @signal()
... def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> @test_signal.stream
... def test1(ret):
...    ret.append('S1')
...    return ret
... 
>>> @test_signal.stream
... @test_signal.settings(overload=False)
... def test2(ret):
...    ret.append('S2')
...    return ret
... 

``stream``
===========
>>> print test_signal([])
['SIGNAL', 'S1', 'S2']

Options
========

``overload``
-------------
>>> print test_signal is test1
True
>>> print test_signal is test2
False
>>> olist = []
>>> print test2(olist)
['S2']
>>> print olist
['S2']

``ismethod``
-------------
>>> class Test_ismethod(object):
...    @signal(ismethod=True)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.stream
...    def imstream(self, ret):
...       ret.append('IMS1')
...       return ret
... 
>>> test = Test_ismethod()
>>> print test.imsignal([])
['IMSIGNAL', 'IMS1']
>>> class Test_ismethod_bad(object):
...    @signal(ismethod=False)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.stream
...    def imstream(self, ret):
...       ret.append('IMS1')
...       return ret
... 
>>> test = Test_ismethod_bad()
>>> print test.imsignal([])
Traceback (most recent call last):
   ...
TypeError: imstream() takes exactly 2 arguments (1 given)

``callmethod``
---------------
>>> class Test_callmethod(object):
...    @signal(ismethod=True, callmethod=True, overload=False)
...    def cmsignal(self, l):
...       l.append('CMSIGNAL')
...       return l
...    @cmsignal.stream
...    def cmcall(self, ret):
...       ret.append('CMS1')
...       return ret
... 
>>> test = Test_callmethod()
>>> print test.cmsignal([])
['CMSIGNAL', 'CMS1']
>>> class Test_child(Test_callmethod):
...    def cmcall(self, ret):
...       ret.append('CHILD')
...       return ret
... 
>>> test = Test_child()
>>> print test.cmsignal([])
['CMSIGNAL', 'CHILD']

