=============================================
isbfunction
=============================================

.. contents:: Contents
      :depth: 2

Description
-------------
Determines if the passed in argument is a builtin function.

Arguments
---------
obj
   Any python object instance.

Return Values
--------------
True
   The argument is a builtin function.
False
   The argument is not a function or is not considered builtin.

Example Usage
-------------
>>> from smanstal.types.introspect import isbfunction
>>> isbfunction(max)
True
>>> def test(): pass
...
>>> isbfunction(test)
False

