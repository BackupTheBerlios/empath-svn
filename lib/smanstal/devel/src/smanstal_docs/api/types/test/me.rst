>>> from smanstal.types.introspect import *
>>> isproperty(1)
False
>>> class A(object):
...     test = property(lambda s: 1)
...
>>> isproperty(A.test)
True
