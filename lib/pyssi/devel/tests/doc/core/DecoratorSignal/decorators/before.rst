-----------------
Before Decorator
-----------------

Setup
======
>>> from pyssi.core import signal
>>> @signal()
... def test_signal(l):
...    l.append('SIGNAL')
...    return l
... 
>>> @test_signal.before
... def test_before(l):
...    l.append('BEFORE')
... 
>>> @test_signal.before
... @test_signal.settings(overload=False)
... def test_other(l):
...    l.append('OTHER')
... 

``before``
===========
>>> print test_signal([])
['BEFORE', 'OTHER', 'SIGNAL']

Options
========

``overload``
-------------
>>> print test_signal is test_before
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
...    @imsignal.before
...    def imbefore(self, l):
...       l.append('IMBEFORE')
... 
>>> test = Test_ismethod()
>>> print test.imsignal([])
['IMBEFORE', 'IMSIGNAL']
>>> class Test_ismethod_other(object):
...    @signal()
...    def imsignal(self, l):
...       l.append('IMSIGNAL')
...       return l
...    @imsignal.before
...    def imbefore(self, l):
...       l.append('IMBEFORE')
... 
>>> test = Test_ismethod_other()
>>> print test.imsignal([])
['IMBEFORE', 'IMSIGNAL']

``callmethod``
---------------
>>> class Test_callmethod(object):
...    @signal(ismethod=True, callmethod=True, overload=False)
...    def cmsignal(self, l):
...       l.append('CMSIGNAL')
...       return l
...    @cmsignal.before
...    def cmcall(self, l):
...       l.append('CMBEFORE1')
...    @cmsignal.before
...    @cmsignal.settings(callmethod=False)
...    def cmnocall(self, l):
...       l.append('CMBEFORE2')
... 
>>> test = Test_callmethod()
>>> print test.cmsignal([])
['CMBEFORE1', 'CMBEFORE2', 'CMSIGNAL']
>>> class Test_child(Test_callmethod):
...     def cmcall(self, l):
...         l.append("CALL CHILD")
...     def cmnocall(self, l):
...         l.append("NO CALL CHILD")
... 
>>> test = Test_child()
>>> print test.cmsignal([])
['CALL CHILD', 'CMBEFORE2', 'CMSIGNAL']

