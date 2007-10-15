# Module: template
# File: template.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the pyssi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from pyssi.util import property_, cref
try:
    from pyssi._speedups.core import (SignalType, BaseSignal, 
                                      next_before, 
                                      next_streamin, next_stream, next_around,
                                      next_replace, next_chooseyield, next_choosereturn, next_choice,
                                      next_after, next_onreturn, Signal, 
                                      LocalDecoratorSettings, GlobalDecoratorSettings,
                                      GenericDecorator, DecoratorSignal,
                                      signal, signal_factory)
except ImportError:
    from pyssi._core import (SignalType, BaseSignal, 
                              next_before, 
                              next_streamin, next_stream, next_around,
                              next_replace, next_chooseyield, next_choosereturn, next_choice,
                              next_after, next_onreturn, Signal, 
                              LocalDecoratorSettings, GlobalDecoratorSettings,
                              GenericDecorator, DecoratorSignal,
                              signal, signal_factory)

#from pyssi._speedups.core import (SignalType, BaseSignal, next_before, next_around, next_after, 
#                         Signal, DecoratorSignal, signal)
#from pyssi._core import (SignalType, BaseSignal, next_before, next_around, next_after, 
#                         Signal, DecoratorSignal, signal)

