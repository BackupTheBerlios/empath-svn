# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj
from eqobj.util import EqObjOptions, MaxCount
from eqobj.collections.mappings import (AnyKeyMixin, AllKeysMixin, MappingOptionMixin,
        TrimOption as TrimMapOption, MissingOption as MissingMapOption)

__all__ = ('MappingMixin', 'AnyKeyMixin', 'AnyKey', 'AllKeysMixin', 'AllKeys', 'MappingOptionMixin', 
            'TrimOption', 'MissingOption')

class SetMixin(object): #{{{
    __slots__ = ()
    def __transform__(self, obj): #{{{
        return set(obj)
    # End def #}}}
# End class #}}}

class AnySetElementMixin(SetMixin, AnyKeyMixin): #{{{
    __slots__ = ()
# End class #}}}

class AnySetElement(AnySetElementMixin, EqObj): #{{{
    __slots__ = ('_options',)
# End class #}}}

class AllSetElementsMixin(SetMixin, AllKeysMixin): #{{{
    __slots__ = ()
# End class #}}}

class AllSetElements(AllSetElementsMixin, EqObj): #{{{
    __slots__ = ('_options',)
# End class #}}}

class SetOptionMixin(MappingOptionMixin): #{{{
    __slots__ = ()
    def _rmfunc(self, obj): #{{{
        return obj.remove
    # End def #}}}
# End class #}}}

class TrimOption(SetOptionMixin, TrimMapOption): #{{{
    __slots__ = ()

class MissingOption(SetOptionMixin, MissingMapOption): #}}}
    __slots__ = ()
    pass
# End class #}}}
