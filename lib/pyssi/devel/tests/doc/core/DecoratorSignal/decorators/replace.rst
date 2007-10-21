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
>>> @test_signal.replace
... def test_old(next, l):
...    l.append('NO SEE')
...    return l
... 
>>> @test_signal.replace
... @test_signal.settings(overload=False)
... def test_replace(next, l):
...    l.append('REPLACE')
...    return l
... 

``replace``
===========
>>> print test_signal([])
['REPLACE']

Options
========

``overload``
-------------
>>> print test_signal is test_old
True
>>> print test_signal is test_replace
False
>>> olist = []
>>> print test_replace(test_signal, olist)
['REPLACE']
>>> print olist
['REPLACE']

``ismethod``
-------------
>>> class Test_ismethod(object):
...    @signal(ismethod=True)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.replace
...    def imreplace(self, next, l):
...       l.append('IMREPLACE')
...       return l
... 
>>> test = Test_ismethod()
>>> print test.imsignal([])
['IMREPLACE']
>>> class Test_ismethod_bad(object):
...    @signal(ismethod=False)
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.replace
...    def imreplace(self, next, l):
...       assert isinstance(self, Test_ismethod_bad), "BAD"
...       l.append('IMREPLACE')
...       return l
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
...    @cmsignal.replace
...    def cmcall(self, next, l):
...       l.append('CMREPLACE')
...       return l
... 
>>> test = Test_callmethod()
>>> print test.cmsignal([])
['CMREPLACE']
>>> class Test_child(Test_callmethod):
...    def cmcall(self, next, l):
...       l.append("CALL CHILD")
...       return l
... 
>>> test = Test_child()
>>> print test.cmsignal([])
['CALL CHILD']

