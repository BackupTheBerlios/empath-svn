# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the eqobj project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj
from eqobj.util import isclass, mro
from eqobj.validators.user import UserDefined

__all__ = ('InstanceType', 'SubType', 'ObjectType')

class InstanceType(UserDefined): #{{{
    __slots__ = ()
    def __init__(self, obj): #{{{
        if not isinstance(obj, tuple):
            obj = (obj,)
        for o in obj:
            if not isclass(o):
                raise TypeError('InstanceType objects can only initialize on class objects')
        def checker(o): #{{{
            return isinstance(o, obj)
        # End def #}}}
        super(InstanceType, self).__init__(checker)
    # End def #}}}
# End class #}}}

class SubType(UserDefined): #{{{
    __slots__ = ()
    def __init__(self, obj): #{{{
        if not isinstance(obj, tuple):
            obj = (obj,)
        for o in obj:
            if not isclass(o):
                raise TypeError('SubType objects can only initialize on class objects')
        def checker(o): #{{{
            return isclass(o) and issubclass(o, obj)
        # End def #}}}
        super(SubType, self).__init__(checker)
    # End def #}}}
# End class #}}}

class ObjectType(SubType): #{{{
    __slots__ = ()
    def __init__(self, obj): #{{{
        if not isclass(obj):
            obj = obj.__class__
        obj = tuple(o for o in mro(obj) if o is not object)
        super(ObjectType, self).__init__(obj)
    # End def #}}}

    def __transform__(self, obj): #{{{
        if not isclass(obj):
            obj = obj.__class__
        return obj
    # End def #}}}
# End class #}}}
