# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from aossi.impex import import_, CopyModuleImporter
_pre = ':aossi:'
_ab = import_(':aossi:__builtin__', importer=CopyModuleImporter(copy_prefix=_pre))

sys = import_(':aossi:sys', importer=CopyModuleImporter(copy_prefix=_pre))
logging = import_(':aossi:logging', importer=CopyModuleImporter(copy_prefix=_pre))
op = import_(':aossi:os.path', importer=CopyModuleImporter(copy_prefix=_pre))

from inspect import stack as istack, isclass

__all__ = ('TRACE_NAME', 'TRACE_EXEC', 'TRACE_RETURN', 'TRACE_OTHER',
            'TraceFormatter', 'TraceNameFormatter', 'TraceExecFormatter',
            'TraceReturnFormatter', 'TraceOtherFormatter',
            'create_loggers', 'create_tracer')

TRACE_NAME = 9
TRACE_EXEC = 8
TRACE_RETURN = 7
TRACE_OTHER = 6
TRACE_ALL_EVENTS = 6

class TraceFormatter(logging.Formatter): #{{{
    def __init__( self, fmt=None, datefmt=None ): #{{{
        logging.Formatter.__init__(self, fmt, datefmt)
        self.baseline = _ab.len(istack())
        self.current = None
    # End def #}}}

    def create_indent(self, indent_count): #{{{
#        pre = ' ' * max(0, indent_count - 1)
#        marker = ''.join(['+ ', '-' * 2]) * min(1, indent_count)

#        lead = ' ' * 4
        spaces = (' ' * 4) * max(0, indent_count)
#        pre = ' ' * indent_count
#        marker = ''.join(['+ ', '-' * 2]) * indent_count
#        post = ' ' * min(1, indent_count)
        return spaces
    # End def #}}}

    def format( self, rec ): #{{{
        stack = istack()
        cur = _ab.len(stack) - self.baseline
        if self.current is None:
            self.current = cur
#        cur_len = cur - self.current
        cur_len = max((cur - self.current) - 5, 0)
        rec.indent = self.create_indent(cur_len)
        out = logging.Formatter.format(self, rec)
        del rec.indent
        return out
    # End def #}}}
# End class #}}}

class TraceNameFormatter(TraceFormatter): #{{{
    def create_indent(self, indent_count): #{{{
        lead = ' ' * 4
        cur_stack = istack()[13]
        line_num = cur_stack[2]
        len = _ab.len
        if line_num > 9999999:
            line_num = '+9999999'
        else:
            line_num = '%i' %line_num
        cur_line = ' '.join([',', 'line', _ab.str(cur_stack[2])])
        filename = cur_stack[1]
        if len(filename) > 10:
            filename = ''.join(filename[:7], '...')
        file = ''.join(['<', filename, cur_line, '>'])
        flen = len(file)
        if flen < 27:
            lead = ''.join([lead, ' ' * (27 - flen)])
        cur_file = ''.join([file, lead])

        spaces = (' ' * 4) * max(0, indent_count)
        pre = ' ' * indent_count
        marker = ''.join(['+ ', '-' * 2]) * indent_count
        post = ' ' * min(1, indent_count)
        return ''.join([cur_file, spaces, pre])
    # End def #}}}
# End class #}}}

class TraceExecFormatter(TraceFormatter): #{{{
    def create_indent(self, indent_count): #{{{
        lead = ''.join([' ' * 4, ' ' * 27])
        spaces = (' ' * 4) * max(0, indent_count)
        pre = ' ' * indent_count
        marker = ''.join(['+ ', '-' * 2]) * indent_count
        post = ' ' * min(1, indent_count)
        return ''.join([lead, spaces, pre, '   '])
    # End def #}}}
# End class #}}}

class TraceReturnFormatter(TraceFormatter): #{{{
    def create_indent(self, indent_count): #{{{
        lead = ' ' * 4
        spaces = (' ' * 4) * max(0, indent_count)
        pre = ' ' * indent_count
        marker = ''.join(['+ ', '-' * 2]) * indent_count
        post = ' ' * min(1, indent_count)
        return ''.join([spaces, pre, marker, post])
    # End def #}}}
# End class #}}}

class TraceOtherFormatter(TraceFormatter): #{{{
    def create_indent(self, indent_count): #{{{
        lead = ' ' * 4
        spaces = (' ' * 4) * max(0, indent_count)
        pre = ' ' * indent_count
        marker = ''.join(['+ ', '-' * 2]) * indent_count
        post = ' ' * min(1, indent_count)
        return ''.join([spaces, pre, marker, post])
    # End def #}}}
# End class #}}}

def create_loggers(**kwargs): #{{{
    stream = kwargs.get('stream', sys.stdout)
    fmt = kwargs.get('fmt', "%(indent)s%(message)s")
    formatters = kwargs.get('formatters', TraceFormatter)
    trace_levels = kwargs.get('trace_levels', {})
    allow = kwargs.get('allow', ['tracer'])
    levels = {'trace_name': TRACE_NAME, 'trace_exec': TRACE_EXEC, 
                'trace_return': TRACE_RETURN,
                'trace_other': TRACE_OTHER}
    levels.update(trace_levels)
    logger = logging.getLogger('tracer')
#    handler = logging.StreamHandler(stream)
#    handler.setFormatter(TraceFormatter("%(indent)s%(message)s"))
#    logger.addHandler(handler)
    logger.setLevel(TRACE_ALL_EVENTS)
    for fname in allow:
        if fname != 'tracer':
            fname = '.'.join(['tracer', fname])
        filter = logging.Filter(fname)
        logger.addFilter(filter)

    for name, lvl in levels.iteritems():
        logging.addLevelName(lvl, name)
        absname = '.'.join(['tracer', name])
        child_logger = logging.getLogger(absname)
        handler = logging.StreamHandler(stream)
        fo = formatters
        fo_fmt = fmt
        if isinstance(formatters, dict):
            fo = formatters.get(name, TraceFormatter)
        if isinstance(fmt, dict):
            fo_fmt = fmt.get(name, "%(indent)s%(message)s")
        handler.setFormatter(fo(fo_fmt))
        child_logger.addHandler(handler)
        child_logger.setLevel(lvl)
    return logger
# End def #}}}

def create_tracer(): #{{{
    def trace_around(func): #{{{
        _tab = _ab
        _logging = logging
        str = _tab.str
        type = _tab.type
        def newcall(self, *args, **kwargs):
            cls = '?'
            if self._object:
                obj = self._object()
                if isclass(obj):
                    cls = obj.__name__
                else:
                    obj = self._object()
                    if _tab.hasattr(obj, '__class__'):
                        cls = obj.__class__.__name__
            trace_name = _logging.getLogger('tracer.trace_name')
            info = ' :: '.join([cls, self.__name__])
            trace_name.log(TRACE_NAME, info)

            trace_exec = _logging.getLogger('tracer.trace_exec')
            argstr = ', '.join([str(a) for a in args])
            if argstr:
                argstr = ': '.join(['Arguments', argstr])
                kwstr = ', '.join([' = '.join([kw, str(val)]) for kw, val in kwargs.iteritems()])
                j = [argstr]
                if kwstr:
                    j.append(kwstr)
                info = '--'.join(j)
                trace_exec.log(TRACE_EXEC, info)
            return func(*args, **kwargs)
        return newcall
    # End def #}}}
    return trace_around
# End def #}}}
