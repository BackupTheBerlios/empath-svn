# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

__all__ = ('DictMixin',)

class DictMixin(object): #{{{
    __slots__ = ()

    def clear(self): #{{{
        super(DictMixin, self).clear()
    # End def #}}}

# End class #}}}
