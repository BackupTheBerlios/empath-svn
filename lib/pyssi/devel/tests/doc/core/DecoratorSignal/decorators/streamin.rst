-----------------
StreamIn Decorator
-----------------

Setup
======
>>> from pyssi.core import signal
>>> @signal()
... def test_signal(l):
...    l += l.__class__(['SIGNAL'])
...    return l
... 
>>> @test_signal.streamin
... def test1(next, args, kwargs):
...    args[0] = ()
...    return next(args, kwargs)
... 
>>> @test_signal.streamin
... @test_signal.settings(overload=False)
... def test2(next, args, kwargs):
...    args[0] += ('START',)
...    return next(args, kwargs)
... 

``stream``
===========
>>> print test_signal([])
('START', 'SIGNAL')

Options
========

``overload``
-------------
>>> print test_signal is test1
True
>>> print test_signal is test2
False
>>> def custom(args, kwargs): return args[0]
>>> print test2(custom, [()], {})
('START',)

``ismethod``
-------------
>>> class Test_ismethod(object):
...    @signal(ismethod=True)
...    def imsignal(self, l):
...       l += l.__class__(['IMSIGNAL'])
...       return l
...    @imsignal.streamin
...    def imstreamin(self, next, args, kwargs):
...       args[0] = ()
...       return next(self, args, kwargs)
... 
>>> test = Test_ismethod()
>>> print test.imsignal([])
('IMSIGNAL',)
>>> class Test_ismethod_bad(object):
...    @signal(ismethod=False)
...    def imsignal(self, l):
...       l += l.__class__(['IMSIGNAL'])
...       return l
...    @imsignal.streamin
...    def imstreamin(self, next, args, kwargs):
...       args[0] = ()
...       return next(self, args, kwargs)
... 
>>> test = Test_ismethod_bad()
>>> print test.imsignal([])
Traceback (most recent call last):
   ...
TypeError: imstreamin() takes exactly 4 arguments (3 given)

``callmethod``
---------------
>>> class Test_callmethod(object):
...    @signal(ismethod=True, callmethod=True, overload=False)
...    def cmsignal(self, l):
...       l += l.__class__(['CMSIGNAL'])
...       return l
...    @cmsignal.streamin
...    def cmcall(self, next, args, kwargs):
...       args[0] = ()
...       return next(self, args, kwargs)
... 
>>> test = Test_callmethod()
>>> print test.cmsignal([])
('CMSIGNAL',)
>>> class Test_child(Test_callmethod):
...    def cmcall(self, next, args, kwargs):
...       args[0] = ('CHILD',)
...       return next(self, args, kwargs)
... 
>>> test = Test_child()
>>> print test.cmsignal([])
('CHILD', 'CMSIGNAL')

