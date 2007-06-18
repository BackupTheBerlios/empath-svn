# Module: smanstal.util.script
# File: script.py
# Copyright (C) 2007 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the smanstal project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from subprocess import Popen, PIPE

from smanstal.types.callobj import callcallable, quote as q
from smanstal.util.str import safe_varexpand as namexpand
from os import environ as ENV

__all__ = ('cmdname', 'cmd', 'cmdpipe', 'callcmd',
            'CMD_STDOUT', 'CMD_STDERR', 'CMD_BOTH',
            'CommandError', 'PipeError', 'InvalidDestinationError',
            'namexpand')

CMD_STDOUT = 0
CMD_STDERR = 1
CMD_BOTH = 2

class CommandError(StandardError): pass
class PipeError(CommandError): pass
class InvalidDestinationError(PipeError): pass

class makecmd(object): #{{{
    __slots__ = ()
    def __call__(self, *args): #{{{
        return cmd(*args)
    # End def #}}}

    def __getattr__(self, name): #{{{
        def setargs(*args): #{{{
            return cmd(name, *args)
        # End def #}}}
        return setargs
    # End def #}}}
# End class #}}}
cmdname = makecmd()

class cmd(callcallable): #{{{
    def __init__(self, *args): #{{{
        super(cmd, self).__init__(Popen, args, **dict(stdout=PIPE, env=ENV))
    # End def #}}}

    def __or__(self, dest): #{{{
        if isinstance(dest, cmdpipe):
            raise InvalidDestinationError("Cannot send data to an already established command pipe")
        return cmdpipe(q(self, weak=False), q(dest, weak=False))
    # End def #}}}

    def __call__(self, **kwargs): #{{{
        output = int(kwargs.get('output', CMD_STDOUT))
        buffer = bool(kwargs.get('buffer', True))
        command = super(cmd, self).__call__()
        if buffer:
            ret = command.communicate()
        else:
            ret = [command.stdout, command.stderr]
        if output == CMD_BOTH:
            return ret
        return ret[output]
    # End def #}}}

    @classmethod
    def name(cls, name): #{{{
        return getattr(cmdname, name)
    # End def #}}}
# End class #}}}

class cmdpipe(cmd): #{{{
    def __init__(self, p1, p2): #{{{
        def mkpipe(p1, p2): #{{{
            p1kw = dict(p1.kwargs)
            p1 = p1.callable(tuple(p1.args)[0], **p1kw)
            p2kw = dict(p2.kwargs)
            p2kw.update(stdin=p1.stdout)
            p2 = p2.callable(tuple(p2.args)[0], **p2kw)
            return p2
        # End def #}}}
        super(cmd, self).__init__(mkpipe, p1, p2)
    # End def #}}}

    def __or__(self, dest): #{{{
        if isinstance(dest, cmdpipe):
            raise InvalidDestinationError("Cannot send data to an already established command pipe")
        selfcall = callcallable.__call__
        qself = q(self, weak=False)
        p1 = q(callcallable(selfcall, qself), weak=False)
        return cmdpipe(p1, q(dest, weak=False))
    # End def #}}}

# End class #}}}

def callcmd(ret, *args, **kwargs): #{{{
    if isinstance(ret, basestring):
        ret = cmd(ret, *args)
    return ret(**kwargs)
# End def #}}}
