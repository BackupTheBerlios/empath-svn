-----------------
OnReturn Decorator
-----------------

Setup
======
>>> from pyssi.core import signal
>>> @signal()
... def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> @test_signal.onreturn
... def test_onreturn(ret):
...    ret.append('ONRETURN')
... 
>>> @test_signal.onreturn
... @test_signal.settings(overload=False)
... def test_other(ret):
...    ret.append('OTHER')
... 

``onreturn``
===========
>>> print test_signal([])
['SIGNAL', 'ONRETURN', 'OTHER']

Options
========

``overload``
-------------
>>> print test_signal is test_onreturn
True
>>> print test_signal is test_other
False
>>> olist = []
>>> print test_other(olist)
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
...    @imsignal.onreturn
...    def imonreturn(self, ret):
...       ret.append('IMONRETURN')
... 
>>> test = Test_ismethod()
>>> print test.imsignal([])
['IMSIGNAL', 'IMONRETURN']
>>> class Test_ismethod_bad(object):
...    @signal(ismethod=False)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.onreturn
...    def imonreturn(self, ret):
...       ret.append('IMONRETURN')
... 
>>> test = Test_ismethod_bad()
>>> print test.imsignal([])
Traceback (most recent call last):
   ...
TypeError: imonreturn() takes exactly 2 arguments (1 given)

``callmethod``
---------------
>>> class Test_callmethod(object):
...    @signal(ismethod=True, callmethod=True, overload=False)
...    def cmsignal(self, l):
...       l.append('CMSIGNAL')
...       return l
...    @cmsignal.onreturn
...    def cmcall(self, ret):
...       ret.append('CMONRETURN1')
...    @cmsignal.onreturn
...    @cmsignal.settings(callmethod=False)
...    def cmnocall(self, ret):
...       ret.append('CMONRETURN2')
... 
>>> test = Test_callmethod()
>>> print test.cmsignal([])
['CMSIGNAL', 'CMONRETURN1', 'CMONRETURN2']
>>> class Test_child(Test_callmethod):
...     def cmcall(self, ret):
...         ret.append("CALL CHILD")
...     def cmnocall(self, ret):
...         ret.append("NO CALL CHILD")
... 
>>> test = Test_child()
>>> print test.cmsignal([])
['CMSIGNAL', 'CALL CHILD', 'CMONRETURN2']

