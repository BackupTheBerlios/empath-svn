=====================
ismodule
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
Determines if the value bound to a name is
a module instance.

Metadata
----------
:Type: Function

Arguments
---------
``obj``
   Any python object instance.

Return Values
--------------
True
   The argument is a module instance.

False
   The argument is not a module instance.

Example Usage
-------------
>>> from smanstal.types.introspect import ismodule
>>> ismodule(1)
False
>>> import os
>>> ismodule(os)
True

