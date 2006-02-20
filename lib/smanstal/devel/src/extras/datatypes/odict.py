###########################################################################
# extras.datatypes.odict -- Ordered dictionary
# Copyright (C) 2004  Ariel De Ocampo
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###########################################################################

"""
Base Extension object.

This is the base class for all extension objects. The only thing anyone
can do with this class is set its name.

@version: 0.0.1
@since: Tuesday September 15, 2004
@status: Lab tested
@author: Ariel De Ocampo
@contact: ariel@lampware.ca
@organization: LAMPware
@copyright: (C) 2004 Ariel De Ocampo
@attention: Last updated Tuesday September 22 2004
@note: Changelog::

   09/22/2004
      * Updated all docstrings to epydoc format.
      * Included GPL license text.

"""

# =========================================================================

# ============================SOMEOBJECT===================================

# --------------------------------------------------------
# Start Import system modules
# --------------------------------------------------------
# --------------------------------------------------------
# End Import system modules
# --------------------------------------------------------

# --------------------------------------------------------
# Start Import custom modules
# --------------------------------------------------------
# Put custom module import statements here.
# --------------------------------------------------------
# End Import custom modules
# --------------------------------------------------------

# --------------------------------------------------------
# Start module variables
# --------------------------------------------------------
# Put module variables here.
# --------------------------------------------------------
# End module variables
# --------------------------------------------------------

# --------------------------------------------------------
# Start module exceptions
# --------------------------------------------------------
# Put module exceptions here.
# --------------------------------------------------------
# End module exceptions
# --------------------------------------------------------

class odict(dict):
   """Single line description of the class.

   A more detailed, multi-line description of what this class
   does.
   """
   # --------------------------------------------------------
   # Start Class Constants
   # --------------------------------------------------------
   # --------------------------------------------------------
   # End Class Constants
   # --------------------------------------------------------
# =========================================================================

# =========================BUILT-IN FUNCTIONS==============================
   # --------------------------------------------------------
   # Start __init__ Function
   # --------------------------------------------------------
   def __init__(self, *args, **kwargs):
      """
      Initializes all class instance variables. 
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: ExtensionLoader instance
      
      @precondition: Anything goes.
      @postcondition: All vars are initialized to their default values.
      """
      self._keys = []
      arglen = len(args)
      if arglen == 1:
         if isinstance(args[0], dict):
            self.update(args[0])
         else:
            for k, v in args[0]:
               self.__setitem__(k, v)
         self.update(kwargs)
      elif arglen == 0:
         self.update(kwargs)
      else:
         super(odict, self).__init__(*args, **kwargs)
   # --------------------------------------------------------
   # End __init__ Function
   # --------------------------------------------------------
   
   # --------------------------------------------------------
   # Start __eq__ Function
   # --------------------------------------------------------
   def __eq__(self, other):
      """
      Returns a generator that iterates over keys in the order they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: ExtensionLoader instance
      
      @precondition: Class must be instantiated.
      @postcondition: State of the class has not changed.
      """
      if not isinstance(other, odict): return False
      if super(odict, self).__eq__(other):
         return self._keys == other._keys
      return False
   # --------------------------------------------------------
   # End __eq__ Function
   # --------------------------------------------------------
   
   # --------------------------------------------------------
   # Start __iter__ Function
   # --------------------------------------------------------
   def __iter__(self):
      """
      Returns a generator that iterates over keys in the order they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: ExtensionLoader instance
      
      @precondition: Class must be instantiated.
      @postcondition: State of the class has not changed.
      """
      for k in self._keys: yield k
   # --------------------------------------------------------
   # End __iter__ Function
   # --------------------------------------------------------
   
   # --------------------------------------------------------
   # Start __setitem__ Function
   # --------------------------------------------------------
   def __setitem__(self, key, val):
      """
      Sets the key to the val.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: ExtensionLoader instance
      
      @precondition: Class must be instantiated.
      @postcondition: key is set to val.
      """
      super(odict, self).__setitem__(key, val)
      if key not in self._keys: self._keys.append(key)
   # --------------------------------------------------------
   # End __setitem__ Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start __delitem__ Function
   # --------------------------------------------------------
   def __delitem__(self, key):
      """
      Deletes they key from the dictionary.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: ExtensionLoader instance
      @param key: Anything at all.
      
      @precondition: Class must be instantiated.
      @postcondition: Key no longer exists in the dictionary.
      """
      super(odict, self).__delitem__(key)
      self._keys.remove(key)
   # --------------------------------------------------------
   # End __delitem__ Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start copy Function
   # --------------------------------------------------------
   def __copy__(self):
      """
      Makes a copy of the current dictionary.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Anything goes.
      @postcondition: State of the class has not changed.
      """
      od = odict()
      od.update(self)
      return od
   # --------------------------------------------------------
   # End copy Function
   # --------------------------------------------------------

# =========================================================================

# ========================PUBLIC FUNCTIONS=================================

   # --------------------------------------------------------
   # Start clear Function
   # --------------------------------------------------------
   def clear(self):
      """
      Makes the dictionary empty.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Class must be instantiated.
      @postcondition: Dictionary is empty.
      """
      super(odict, self).clear()
      self._keys = []
   # --------------------------------------------------------
   # End clear Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start copy Function
   # --------------------------------------------------------
   def copy(self):
      """
      Makes a copy of the current dictionary.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Anything goes.
      @postcondition: State of the class has not changed.
      """
      return self.__copy__()
   # --------------------------------------------------------
   # End copy Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start items Function
   # --------------------------------------------------------
   def items(self):
      """
      Returns as per the zip built-in function. For each
      tuple in the list, the first item is the key, the second
      is the value for that key.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Anything goes.
      @postcondition: State of the class has not changed.
      """
      return zip(self._keys, self.values())
   # --------------------------------------------------------
   # End items Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start keys Function
   # --------------------------------------------------------
   def keys(self):
      """
      Returns the list of keys for this dictionary in the order
      they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Anything goes.
      @postcondition: State of the class has not changed.
      """
      return [x for x in self]
   # --------------------------------------------------------
   # End keys Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start values Function
   # --------------------------------------------------------
   def values(self):
      """
      Returns a list of values in the order they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Anything goes.
      @postcondition: State of the class had not changed.
      """
      return map(self.get, self._keys)
   # --------------------------------------------------------
   # End values Function
   # --------------------------------------------------------
   
   # --------------------------------------------------------
   # Start iterkeys Function
   # --------------------------------------------------------
   def iterkeys(self):
      """
      Returns a generator that returns the keys in the order
      they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Class must be instantiated.
      @postcondition: State of the class has not changed.
      """
      return self.__iter__()
   # --------------------------------------------------------
   # End iterkeys Function
   # --------------------------------------------------------
   
   # --------------------------------------------------------
   # Start itervalues Function
   # --------------------------------------------------------
   def itervalues(self):
      """
      Returns a generator that returns the values in the order
      they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Anything goes.
      @postcondition: State of the class has not changed.
      """
      for key in self: yield self.get(key)
   # --------------------------------------------------------
   # End itervalues Function
   # --------------------------------------------------------
   
   # --------------------------------------------------------
   # Start iteritems Function
   # --------------------------------------------------------
   def iteritems(self):
      """
      Returns a generator that returns key/value 2-tuples in the order
      they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      
      @precondition: Anything goes.
      @postcondition: State of the class has not changed.
      """
      for key in self: yield (key, self.get(key))
   # --------------------------------------------------------
   # End iteritems Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start pop Function
   # --------------------------------------------------------
   def fromkeys(self, seq, value = None):
      od = odict()
      for k in seq:
         od[k] = value
      return od
   # --------------------------------------------------------
   # End pop Function
   # --------------------------------------------------------
   
   # --------------------------------------------------------
   # Start pop Function
   # --------------------------------------------------------
   def pop(self, key, *args):
      try: self._keys.remove(key)
      except: pass
      return super(odict, self).pop(key, *args)
   # --------------------------------------------------------
   # End pop Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start popitem Function
   # --------------------------------------------------------
   def popitem(self):
      try:
         key = self._keys[-1]
      except IndexError:
         raise KeyError('dictionary is empty')

      val = self[key]
      del self[key]

      return (key, val)
   # --------------------------------------------------------
   # End popitem Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start setdefault Function
   # --------------------------------------------------------
   def setdefault(self, key, failobj = None):
      """
      Returns a list of values in the order they were added.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      @param newdict: 
         Instance of a dictionary object.
      @type self: L{Dictionary<dict>}
      
      @precondition: Anything goes.
      @postcondition: keys and values of this class are equal to those of C{newdict}.
      """
      if key not in self._keys: self._keys.append(key)
      return super(odict, self).setdefault(key, failobj)
   # --------------------------------------------------------
   # End setdefault Function
   # --------------------------------------------------------

   # --------------------------------------------------------
   # Start update Function
   # --------------------------------------------------------
   def update(self, newdict):
      """
      Updates the dictionary with the keys and values of newdict.
         
      @param self: 
         Instance of this class. Default Value: n/a
      @type self: odict instance
      @param newdict: 
         Instance of a dictionary object.
      @type self: L{Dictionary<dict>}
      
      @precondition: Anything goes.
      @postcondition: keys and values of this class are equal to those of C{newdict}.
      """
      for key, value in newdict.iteritems():
         self.__setitem__(key, value)
   # --------------------------------------------------------
   # Start update Function
   # --------------------------------------------------------
# =========================================================================
   
# =========================================================================
