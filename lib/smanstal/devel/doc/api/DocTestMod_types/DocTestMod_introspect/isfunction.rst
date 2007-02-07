=============================================
isfunction
=============================================

.. contents:: Contents
      :depth: 2

Description
-------------
Determines if the passed in argument is a non-builtin function.

Arguments
---------
obj
   Any python object instance.

Return Values
--------------
True
   The argument is a non-builtin function.
False
   The argument is not a function or is considered builtin.

Example Usage
-------------
>>> from smanstal.types.introspect import isfunction
>>> def test(): pass
...
>>> isfunction(test)
True
>>> isfunction(1)
False

