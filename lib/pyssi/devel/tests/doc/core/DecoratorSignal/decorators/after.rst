-----------------
After Decorator
-----------------

Setup
======
>>> from pyssi.core import signal
>>> @signal()
... def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> @test_signal.after
... def test_after(ret, l):
...    l.append('AFTER')
... 
>>> @test_signal.after
... @test_signal.settings(overload=False)
... def test_other(ret, l):
...    l.append('OTHER')
... 

``after``
===========
>>> print test_signal([])
['SIGNAL', 'AFTER', 'OTHER']

Options
========

``overload``
-------------
>>> print test_signal is test_after
True
>>> print test_signal is test_other
False
>>> olist = []
>>> print test_other(olist, olist)
None
>>> print olist
['OTHER']

``ismethod``
-------------
>>> class Test_ismethod(object):
...    @signal(ismethod=True)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.after
...    def imafter(self, ret, l):
...       ret.append('IMAFTER')
... 
>>> test = Test_ismethod()
>>> print test.imsignal([])
['IMSIGNAL', 'IMAFTER']
>>> class Test_ismethod_bad(object):
...    @signal(ismethod=False)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.after
...    def imafter(self, ret, l):
...       ret.append('IMAFTER')
... 
>>> test = Test_ismethod_bad()
>>> print test.imsignal([])
Traceback (most recent call last):
   ...
AttributeError: 'Test_ismethod_bad' object has no attribute 'append'

``callmethod``
---------------
>>> class Test_callmethod(object):
...    @signal(ismethod=True, callmethod=True, overload=False)
...    def cmsignal(self, l):
...       l.append('CMSIGNAL')
...       return l
...    @cmsignal.after
...    def cmcall(self, ret, l):
...       ret.append('CMAFTER1')
...    @cmsignal.after
...    @cmsignal.settings(callmethod=False)
...    def cmnocall(self, ret, l):
...       ret.append('CMAFTER2')
... 
>>> test = Test_callmethod()
>>> print test.cmsignal([])
['CMSIGNAL', 'CMAFTER1', 'CMAFTER2']
>>> class Test_child(Test_callmethod):
...     def cmcall(self, ret, l):
...         ret.append("CALL CHILD")
...     def cmnocall(self, ret, l):
...         ret.append("NO CALL CHILD")
... 
>>> test = Test_child()
>>> print test.cmsignal([])
['CMSIGNAL', 'CALL CHILD', 'CMAFTER2']

