# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from random import choice
from string import hexdigits

__all__ = ('randstr',)

def randstr(len=6): #{{{
    return ''.join(choice(hexdigits) for i in xrange(len))
# End def #}}}
