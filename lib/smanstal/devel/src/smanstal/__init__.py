# Module: smanstal
# File: __init__.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# These are retro 'builtin' functions

import sys

__all__ = ('user_input', 'eval_input')

def user_input(prompt=None): #{{{
    return sys.stdin.readline().strip() if not prompt or not sys.stdout.write(str(prompt)) else ''
# End def #}}}

def eval_input(prompt=None): #{{{
    return eval(user_input(prompt))
# End def #}}}
