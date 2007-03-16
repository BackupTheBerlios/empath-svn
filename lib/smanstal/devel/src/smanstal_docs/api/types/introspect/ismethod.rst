=====================
ismethod
=====================
:Version: 1.0
:Created: March 16 2007
:Author: Ariel De Ocampo
:Email: arieldeocampo@gmail.com
:License: MIT

.. contents:: Contents
   :depth: 2

Description
------------
Determines if an object is a pure python method or not.

Metadata
----------
:Type: Function

Arguments
----------
``obj``
   Purpose
      Object to run a check against. 
   Values
      Any python object

Return Values
--------------
True
   The argument is a pure python method

Example Usage
--------------
>>> from StringIO import StringIO
>>> from smanstal.types.introspect import ismethod
>>> ismethod(StringIO.read)
True
>>> ismethod(property)
False

