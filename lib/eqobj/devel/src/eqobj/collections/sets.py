# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the ${__name__} project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from eqobj.core import EqObj
from eqobj.util import EqObjOptions, MaxCount
from eqobj.collections.mappings import (AnyKeyMixin, AllKeysMixin, 
        TrimOption as TrimMapOption, MissingOption as MissingMapOption)

__all__ = ('MappingMixin', 'AnyKeyMixin', 'AnyKey', 'AllKeysMixin', 'AllKeys', 'MappingOptionMixin', 
            'TrimOption', 'MissingOption')

class SetMixin(object): #{{{
    def __transform__(self, obj): #{{{
        return set(obj)
    # End def #}}}
# End class #}}}

class AnySetElementMixin(SetMixin, AnyKeyMixin): pass
class AnySetElement(AnySetElementMixin, EqObj): pass
class AllSetElementsMixin(SetMixin, AllKeysMixin): pass
class AllSetElements(AllSetElements, EqObj): pass

class SetOptionMixin(MappingOptionMixin): #{{{
    def _rmfunc(self, obj): #{{{
        return obj.remove
    # End def #}}}
# End class #}}}

class TrimOption(SetOptionMixin, TrimMapOption): pass
class MissingOption(SetOptionMixin, MissingMapOption): pass
