=====================
isfilemodule
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
Determines if the passed in argument is a module
object that corresponds to a file on-disk.

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
   The argument is a module instance corresponding to a python file on-disk.

False
   The argument is not a module instance or has no corresponding python 
   file on-disk.

Example Usage
-------------
>>> import os
>>> from smanstal.types.introspect import isfilemodule
>>> from new import module
>>> test = module('blah')
>>> isfilemodule(test)
False
>>> isfilemodule(os)
True

