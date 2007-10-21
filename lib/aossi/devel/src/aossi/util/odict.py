# Module: aossi.odict
# File: odict.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
try:
    from aossi._speedups.util import OrderedDictMixin
except ImportError:
    from aossi.util._odict import OrderedDictMixin

__all__ = ('OrderedDictMixin', 'odict')

class odict(OrderedDictMixin, dict): #{{{
    __slots__ = ('_keys',)
# End class #}}}
