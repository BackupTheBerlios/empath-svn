-----------------
Around Decorator
-----------------

Setup
======
>>> from pyssi.core import signal
>>> @signal()
... def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> @test_signal.around
... def test1(next, l):
...    l.append('A1: BEFORE')
...    ret = next(l)
...    ret.append('A1: AFTER')
...    return ret
... 
>>> @test_signal.around
... @test_signal.settings(overload=False)
... def test2(next, l):
...    l.append('A2: BEFORE')
...    ret = next(l)
...    ret.append('A2: AFTER')
...    return ret
... 

``around``
===========
>>> print test_signal([])
['A1: BEFORE', 'A2: BEFORE', 'SIGNAL', 'A2: AFTER', 'A1: AFTER']

Options
========

``overload``
-------------
>>> print test_signal is test1
True
>>> print test_signal is test2
False
>>> olist = []
>>> def custom(l): l.append('CUSTOM'); return l
>>> print test2(custom, olist)
['A2: BEFORE', 'CUSTOM', 'A2: AFTER']
>>> print olist
['A2: BEFORE', 'CUSTOM', 'A2: AFTER']

``ismethod``
-------------
>>> class Test_ismethod(object):
...    @signal(ismethod=True)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.around
...    def imaround(self, next, l):
...       l.append('IMA: BEFORE')
...       ret = next(self, l)
...       ret.append('IMA: AFTER')
...       return ret
... 
>>> test = Test_ismethod()
>>> print test.imsignal([])
['IMA: BEFORE', 'IMSIGNAL', 'IMA: AFTER']
>>> class Test_ismethod_bad(object):
...    @signal(ismethod=False)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.replace
...    def imaround(self, next, l):
...       assert isinstance(self, Test_ismethod_bad), "BAD"
...       l.append('IMA: BEFORE')
...       ret = next(self, l)
...       ret.append('IMA: AFTER')
...       return ret
... 
>>> test = Test_ismethod_bad()
>>> print test.imsignal([])
Traceback (most recent call last):
   ...
AssertionError: BAD

``callmethod``
---------------
>>> class Test_callmethod(object):
...    @signal(ismethod=True, callmethod=True, overload=False)
...    def cmsignal(self, l):
...       l.append('CMSIGNAL')
...       return l
...    @cmsignal.around
...    def cmcall(self, next, l):
...       l.append('CMA: BEFORE')
...       ret = next(self, l)
...       ret.append('CMA: AFTER')
...       return ret
... 
>>> test = Test_callmethod()
>>> print test.cmsignal([])
['CMA: BEFORE', 'CMSIGNAL', 'CMA: AFTER']
>>> class Test_child(Test_callmethod):
...    def cmcall(self, next, l):
...       l.append('NEW: BEFORE')
...       ret = next(self, l)
...       ret.append('NEW: AFTER')
...       return ret
... 
>>> test = Test_child()
>>> print test.cmsignal([])
['NEW: BEFORE', 'CMSIGNAL', 'NEW: AFTER']

