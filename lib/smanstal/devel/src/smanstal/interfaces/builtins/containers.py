################################################################################
# extras.interfaces.builtins.containers -- Description goes here
# Copyright (c) 2006 Ariel De Ocampo
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
################################################################################
from protocols import Interface, declareAdapter, NO_ADAPTER_NEEDED

__all__ = ('IIterable', 'IContainer', 'ISequence', 'IMutableContainer', 'IMutableSequence', 
            'IMapping', 'IMutableMapping')

class IIterable(Interface):
   def __iter__():
      """Return an iterator to iterate over objects in container"""

class IContainer(IIterable):
   def __len__():
      """Called to implement the built-in function len()"""

   def __getitem__(key):
      """Called to implement evaluation of container[key]"""

   def __contains__(item):
      """Called to implement membership test operators"""

class ISequence(IContainer):
   def __add__(other):
      """called to implement the binary arithmetic operation '+'"""

   def __mul__(other):
      """called to implement the binary arithmetic operation '*'"""
   
   def __rmul__(other):
      """called to implement the binary arithmetic operation '*' for left side of expression"""

class IMutableContainer(IContainer):
   def __setitem__(key, value):
      """Called to implement assignment to container[key]"""
   
   def __delitem__(key):
      """Called to implement deletion of container[key]"""

class IMutableSequence(IMutableContainer, ISequence): 
   def append(obj):
      """L.append(obj) -- append object to end"""
   
   def count(value):
      """L.count(value) -> integer -- return number of occurrences of value"""

   def extend(x):
      """L.extend(iterable) -- extend list by appending elements from the iterable"""

   def index(value, start = 0, stop = -1):
      """L.index(value, [start, [stop]]) -> integer -- return first index of value"""

   def insert(index, obj):
      """L.insert(index, object) -- insert object before index"""

   def pop(i = -1):
      """L.pop([index]) -> item -- remove and return item at index (default last)"""

   def remove(x):
      """L.remove(value) -- remove first occurrence of value"""

   def reverse():
      """L.reverse() -- reverse *IN PLACE*"""

   def sort(cmp=None, key=None, reverse=False):
      """ L.sort(cmp=None, key=None, reverse=False) -- stable sort *IN PLACE*;"""

   def __setslice__(i, j, seq):
      """x.__setslice__(i, j, y) <==> x[i:j]=y
      
         Use  of negative indices is not supported."""

   def __delslice__(i, j):
      """x.__delslice__(i, j) <==> del x[i:j]
      
         Use of negative indices is not supported."""

   def __iadd__(other):
      """Called to implement the augmented arithmetic operation '+='"""

   def __imul__(other):
      """Called to implement the augmented arithmetic operation '*='"""

   def __radd__(other):
      """Called to implement the binary arithmetic operation '+' with reflected (swapped) operands"""

class IMapping(IContainer): 
   def keys():
      """D.keys() -> list of D's keys"""

   def values():
      """D.values() -> list of D's values"""
   
   def items():
      """D.items() -> list of D's (key, value) pairs, as 2-tuples"""

   def has_key(key):
      """D.has_key(k) -> True if D has a key, else False"""

   def get(key, default = None):
      """D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None."""

   def iterkeys():
      """D.iterkeys() -> an iterator over the keys of D"""

   def itervalues():
      """D.itervalues() -> an iterator over the values of D"""

   def iteritems():
      """D.iteritems() -> an iterator over the (key, value) items of D"""

   def copy():
      """D.copy() -> a shallow copy of D"""

class IMutableMapping(IMapping, IMutableContainer): 
   def clear():
      """D.clear() -> None.  Remove all items from D."""

   def setdefault(key, default = None):
      """D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D"""

   def pop(key, *val):
      """D.pop(k[,d]) -> v, remove specified key and return the corresponding value
         If key is not found, d is returned if given, otherwise KeyError is raised"""

   def popitem():
      """D.popitem() -> (k, v), remove and return some (key, value) pair as a
         2-tuple; but raise KeyError if D is empty"""

   def update(i, **kw):
      """D.update(E, **F) -> None.  Update D from E and F: for k in E: D[k] = E[k]
        (if E has keys else: for (k, v) in E: D[k] = v) then: for k in F: D[k] = F[k]"""

declareAdapter(NO_ADAPTER_NEEDED, provides=[IMutableMapping], forTypes=[dict])
declareAdapter(NO_ADAPTER_NEEDED, provides=[ISequence], forTypes=[tuple])
declareAdapter(NO_ADAPTER_NEEDED, provides=[IMutableSequence], forTypes=[list])

