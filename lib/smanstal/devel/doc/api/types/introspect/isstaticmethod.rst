=====================
isstaticmethod
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
Description

Metadata
----------
:Type: Function

Arguments
----------
``cls``
   Purpose
      Class which owns the attribute to be checked
   Values
      Python class
``attr``
   Purpose
      Attribute of ``cls`` argument to determine if is a static method
   Values
      Name of an attribute owned by ``cls`` 

Exceptions
-----------
TypeError
   This error is raised if ``cls`` argument is not a class or if
   the ``attr`` argument is not a string.
AttributeError
   This error is raised if ``cls`` argument does not contain an
   attribute named by the ``attr`` argument.

Return Values
--------------
True
   ``attr`` attribute of ``cls`` is a static method
False
   ``attr`` attribute of ``cls`` is not a static method

Example Usage
--------------
>>> from smanstal.types.introspect import isstaticmethod
>>> class Test(object):
...     @staticmethod
...     def static(): pass
...     @classmethod
...     def classmeth(cls): pass
...     def meth(self): pass
...     a = 1
...
>>> isstaticmethod(Test, 'static')
True


Any other kind of method or type returns False:

>>> isstaticmethod(Test, 'classmeth')
False
>>> isstaticmethod(Test, 'meth')
False
>>> isstaticmethod(Test, 'a')
False


Passing a non-class object as the first argument raises an error:

>>> isstaticmethod(1, 'meth')
Traceback (most recent call last):
   ...
TypeError: int object is not a class


Passing a non-string object as the second argument also raises an error:

>>> isstaticmethod(Test, 1)
Traceback (most recent call last):
   ...
TypeError: getattr(): attribute name must be string


If all arguments are of the expected type, but ``attr`` is not the
name of an attribute owned by ``cls``, an error is raised:

>>> isstaticmethod(Test, 'who')
Traceback (most recent call last):
   ...
AttributeError: type object 'Test' has no attribute 'who'

