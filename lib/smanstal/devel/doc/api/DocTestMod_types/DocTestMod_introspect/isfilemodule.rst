=============================================
isfilemodule
=============================================

.. contents:: Contents
      :depth: 2

Description
-------------
Determines if the passed in argument is a module
object that corresponds to a file on-disk.

Arguments
---------
obj
   Any python object instance.

Return Values
--------------
True
   The argument is a module instance corresponding to a python file on-disk.

False
   The argument is not a module instance or has no corresponding python file on-disk.

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

