# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

#try:
#    from aossi._speedups.util import cref
#except ImportError:
#    from aossi.util.callobj import quote as cref
from aossi.util.callobj import quote as cref

__all__ = ('ChooseCallable', 'AmbiguousChoiceError', 'StopCascade', 'callable_wrapper')

class AmbiguousChoiceError(StandardError): pass
class StopCascade(Exception): pass

def callable_wrapper(func): #{{{
    if not iscallable(func):
        raise TypeError('Argument is not callable')
    def callwrapper(*args, **kwargs): #{{{
        return func(*args, **kwargs)
    # End def #}}}
    return callwrapper
# End def #}}}

# choices: sequence of 2-tuples
#   - A function that computes whether or not its partner will be run
#   - A callable that runs if its partner evaluates to True
# policy: Default policies: default, cascade, first, last
# origfunc: The original callable that is wrapped
# callfunc: A callable that accepts three arguments:
#   - A callable to call
#   - Arguments passed to the given callable
#   - Keyword arguments passed to the given callable
def ChooseCallable(choices, policy, origfunc, callfunc, *args, **kwargs): #{{{
    if policy == 'default':
        return None
    cascade = policy == 'cascade'
    def build_found(): #{{{
        def cascade_chooser(chooser, *args, **kwargs): #{{{
            cret = stop = False
            try:
                cret = callfunc(chooser, *args, **kwargs)
            except StopCascade, err:
                if err.args:
                    cret = bool(err.args[0])
                stop = True
            return cret, stop
        # End def #}}}
        if cascade:
            yield origfunc
        for chooser, func in choices: #{{{
            cret = stop = False
            if cascade:
                cret, stop = cascade_chooser(chooser, *args, **kwargs)
            else:
                cret = callfunc(chooser, *args, **kwargs)
            if cret:
                yield func
                if policy == 'first':
                    return 
            if cascade and stop:
                break
        # End for #}}}
    # End def #}}}
    found = [f for f in build_found()]
    if not found:
        return None
    elif policy == 'last':
        return found[-1:]
    elif cascade or len(found) == 1:
        return found
    raise AmbiguousChoiceError('Found more than one selectable callable')
# End def #}}}
