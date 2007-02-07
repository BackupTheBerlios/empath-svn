=============================================
isproperty
=============================================

.. contents:: Contents
      :depth: 2

Description
-------------
Determines if the value bound to a name is
an instance of the builtin property type.

Arguments
---------
obj
   Any python object instance.

Return Values
--------------
True
   The argument is an instance of the builtin property type.

False
   The argument is not an instance of the builtin property type.

Example Usage
-------------
>>> from smanstal.types.introspect import isproperty
>>> isproperty(1)
False
>>> class A(object):
...     test = property(lambda s: 1)
...
>>> isproperty(A.test)
True

