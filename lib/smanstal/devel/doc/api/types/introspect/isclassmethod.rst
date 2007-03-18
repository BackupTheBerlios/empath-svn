=====================
isclassmethod
=====================
:Version: 1.0
:Created: March 18 2007
:Author: Ariel De Ocampo
:Email: arieldeocampo@gmail.com
:License: MIT

.. contents:: Contents
   :depth: 2

Description
------------
Determines whether an object is a classmethod or not.

Metadata
----------
:Type: Function

Arguments
----------
``obj``
   Purpose
      Object to check
   Values
      Any python object

Return Values
--------------
True
   The passed in argument is a classmethod
False
   The passed in argument is not a classmethod

Example Usage
--------------
Check any arbitrary python object:

>>> from smanstal.types.introspect import isclassmethod
>>> isclassmethod(1)
False


Check a pure python function:

>>> def test(): pass
...
>>> isclassmethod(test)
False


Check classmethod of a class:

>>> class Test(object):
...     @classmethod
...     def test(cls): pass
...
>>> isclassmethod(Test.test)
True


Check classmethod of an instance:

>>> isclassmethod(Test().test)
True

