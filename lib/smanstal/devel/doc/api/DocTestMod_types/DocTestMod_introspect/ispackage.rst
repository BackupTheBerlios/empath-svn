=============================================
ispackage
=============================================

.. contents:: Contents
      :depth: 2

Description
-------------
Determines if the passed in argument is a package.

Arguments
---------
obj
   Any python object instance.

Return Values
--------------
True
   The argument is a module instance corresponding to a python file on-disk names
   '__init__.py' and has no parent module i.e. a package.

False
   The argument is not a module instance or has no corresponding python file on-disk
   named '__init__.py' or has a parent module.

Example Usage
-------------
>>> import os
>>> from smanstal.types.introspect import ispackage
>>> ispackage(os)
False
>>> import smanstal
>>> ispackage(smanstal)
True

