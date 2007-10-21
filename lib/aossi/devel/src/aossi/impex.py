# Module: aossi.simport
# File: simport.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the aossi project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
import imp, sys, os.path as op, types

# ======================================================
# PYPY implemented (w/ slight modifications)
# ======================================================
def find_module(name, path=None): #{{{
    """find_module(name, [path]) -> (file, filename, (suffix, mode, type))
    Search for a module.  If path is omitted or None, search for a
    built-in, frozen or special module and continue search in sys.path.
    The module name cannot contain '.'; to search for a submodule of a
    package, pass the submodule name and the package's __path__.
    """
    if path is None:
        if name in sys.builtin_module_names:
            return (None, name, ('', '', imp.C_BUILTIN))
        path = sys.path
    for base in path:
        filename = op.join(base, name)
        if op.isdir(filename):
            return (None, filename, ('', '', imp.PKG_DIRECTORY))
        for ext, mode, kind in imp.get_suffixes():
            if op.exists(filename+ext):
                return (file(filename+ext, mode), filename+ext, (ext, mode, kind))
    raise ImportError, 'No module named %s' % (name,)
# End def #}}}

def load_module(name, file, filename, description): #{{{
    """Load a module, given information returned by find_module().
    The module name must include the full package name, if any.
    """
    suffix, mode, type = description

    if type == imp.PY_SOURCE:
        return load_source(name, filename, file)

    if type == imp.PY_COMPILED:
       return load_compiled(name, filename, file)

    if type == imp.PKG_DIRECTORY:
        initfilename = op.join(filename, '__init__.py')
        names = (''.join([initfilename, v]) for v in ('o', 'c'))
        for n in names:
            if op.exists(n):
                if name == 'xml.dom':
                    raise Exception(n)
                return load_compiled(name, n, file)
        source = get_source(name, initfilename, file)
        co = compile(source, initfilename, 'exec')
        return run_module(name, filename, co)

    if type in (imp.C_EXTENSION, imp.PY_RESOURCE, imp.C_BUILTIN, imp.PY_FROZEN):
        return imp.load_module(name, file, filename, description)
    raise ValueError, 'invalid description argument: %r' % (description,)
# End def #}}}

def get_source(pathname, file=None): #{{{
    autoopen = file is None
    if autoopen:
        file = open(pathname, 'U')
    source = file.read()
    if autoopen:
        file.close()
    return source
# End def #}}}

def load_source(name, pathname, file=None): #{{{
    source = get_source(pathname, file)
    co = compile(source, pathname, 'exec')
    return run_module(name, pathname, co)
# End def #}}}

def get_code(pathname, file=None): #{{{
    import marshal
    autoopen = file is None
    if autoopen:
        file = open(pathname, 'rb')
    magic = file.read(4)
    if magic != imp.get_magic():
        raise ImportError("Bad magic number in %s" % pathname)
    file.read(4)    # skip timestamp
    co = marshal.load(file)
    if autoopen:
        file.close()
    return co
# End def #}}}

def load_compiled(name, pathname, file=None): #{{{
    co = get_code(pathname, file)
    return run_module(name, pathname, co)
# End def #}}}

def run_module(name, pathname, co): #{{{
    module = sys.modules.setdefault(name, imp.new_module(name))
    module.__name__ = name
    module.__doc__ = None
    module.__file__ = pathname
    try:
        exec co in module.__dict__
    except :
        sys.modules.pop(name,None)
        raise
    return sys.modules.get(name)
# End def #}}}
# ======================================================

# ======================================================

class BaseLoader(object): #{{{
    def __init__(self, file, pathname, desc, mod=None): #{{{
        self._file = file
        self._pathname = pathname
        self._desc = desc
        self._mod = mod
    # End def #}}}

    def __del__(self): #{{{
        if self._file:
            self._file.close()
    # End def #}}}

    def load_module(self, fullname): #{{{
        mod = self._mod
        if mod:
            return mod
        try:
            mod = imp.load_module(fullname, self._file, self._pathname, self._desc)
        finally:
            if self._file:
                self._file.close()
        mod = sys.modules.get(fullname)
        return mod
    # End def #}}}
# End class #}}}

class BaseImporter(object): #{{{
    def __init__(self, loader=BaseLoader): #{{{
        self._initvals()
        self._loader = loader
    # End def #}}}

    def _initvals(self): #{{{
        self._from = 'meta_path'
        self._path = None
    # End def #}}}

    def __call__(self, path=None): #{{{
        self._from = 'path_hooks'
        self._path = path
        return self
    # End def #}}}

    def get_loader(self, fullname, *args, **kwargs): #{{{
        return self._loader(*args, **kwargs)
    # End def #}}}

    def find_module(self, fullname, path=None, **kwargs): #{{{
        if self._from == 'path_hooks':
            path = self._path
            self._initvals()
        origName = fullname
        fp = None
        pathname = None
        desc = None
        if not path:
            mod = sys.modules.get(fullname, None)
            if mod and isinstance(mod, types.ModuleType):
                return self.get_loader(fullname, fp, pathname, desc, mod)
        if '.' in fullname:
            head, fullname = fullname.rsplit('.', 1)
            mod = sys.modules.get(head, None)
            if not mod:
                return None
            path = getattr(mod, '__path__', path)

        try:
            fp, pathname, description = imp.find_module(fullname, path)
            return self.get_loader(fullname, fp, pathname, description)
        except ImportError:
            return None
    # End def #}}}

#    def is_package(self, fullname): #{{{
#        mod, allprop = import_(fullname, get_props=True, importer=self)
#        prop = allprop['properties']
#        return prop and prop[2] is imp.PKG_DIRECTORY
#    # End def #}}}

#    def get_filename(self, fullname): #{{{
#        mod, allprop = import_(fullname, get_props=True, importer=self)
#        prop = allprop['properties']
#        pathname = allprop['pathname']
#        modtype = (imp.PY_SOURCE, imp.PKG_DIRECTORY)
#        ftype = None
#        if prop:
#            ftype = prop[2]
#        if not pathname or ftype not in modtype:
#            return None
#        if ftype == imp.PKG_DIRECTORY:
#            pathname = op.join(pathname, '__init__.py')

#        if not op.isfile(pathname):
#            return None
#        return pathname
#    # End def #}}}

#    def get_code(self, fullname): #{{{
#        mod, allprop = import_(fullname, get_props=True, importer=self)
#        prop = allprop['properties']
#        pathname = allprop['pathname']
#        modtype = (imp.PY_SOURCE, imp.PY_COMPILED, imp.PKG_DIRECTORY)
#        ftype = None
#        if prop:
#            ftype = prop[2]
#        if not pathname or ftype not in modtype:
#            return None
#        if ftype == imp.PKG_DIRECTORY:
#            pathname = op.join(pathname, '__init__.py')
#            ftype = imp.PY_SOURCE
#        if ftype == imp.PY_SOURCE:
#            co_file = (''.join([pathname, v]) for v in ('o', 'c'))
#            for f in co_file:
#                if op.isfile(f):
#                    pathname = f
#                    break

#        return get_code(pathname)
#    # End def #}}}

#    def get_source(self, fullname): #{{{
#        filename = self.get_filename(fullname)
#        if not filename:
#            return None
#        return get_source(filename)
#    # End def #}}}

#    def get_data(self, path): #{{{
#        f = open(path, 'rb')
#        ret = None
#        try:
#            ret = f.read()
#        finally:
#            if f:
#                f.close()
#        return ret
#    # End def #}}}

#    # Properties #{{{
#    properties = property(lambda s: dict(s._found))
#    # End properties #}}}
# End class #}}}

class CopyModuleImporter(BaseImporter): #{{{
    def __init__(self, **kwargs): #{{{        
        loader = kwargs.get('loader', BaseLoader)
        self._copy = set(kwargs.get('copy', []))
        self._return_copy = bool(kwargs.get('return_copy', False))
        self._place_copy = bool(kwargs.get('place_copy', False))
        self._prefix = kwargs.get('copy_prefix', '')
        super(CopyModuleImporter, self).__init__(loader)
    # End def #}}}

    def copy_module(self, mod, fullname, **defaults): #{{{
        modcopy = imp.new_module(fullname)
        if mod:
            defaults.update(mod.__dict__)
        modcopy.__dict__.update(defaults)
        modcopy.__name__ = fullname
        return modcopy
    # End def #}}}

    def find_module(self, fullname, path=None, **kwargs): #{{{
        return_copy = self._return_copy
        place_copy = self._place_copy
        name = fullname
        pre = self._prefix
        if fullname in self._copy:
            place_copy = True
        if pre and name.find(pre) >= 0:
            name = fullname.replace(pre, '')
            if not name:
                return None
#            fullname = '.'.join([''.join([pre, n]) for n in name.split('.')])
            fullname = ''.join([pre, name])
            place_copy = True
            return_copy = True

        mod = None
        if return_copy or place_copy:
            if name != fullname:
                mod = sys.modules.get(fullname, None)
            if not mod:
                l = super(CopyModuleImporter, self).find_module(name, path, **kwargs)
                if not l:
                    return None
                mod = l.load_module(name)
                mod = self.copy_module(mod, fullname)
            else:
                return self.get_loader(fullname, None, None, None, mod)
            if place_copy:
                newname = fullname
                if name == fullname:
#                    newname = '.'.join([''.join([pre, n]) for n in name.split('.')])
                    newname = ''.join([pre, name])
                sys.modules[newname] = mod
            if return_copy:
                assert mod
                return self.get_loader(fullname, None, None, None, mod)
        return super(CopyModuleImporter, self).find_module(fullname, path, **kwargs)
    # End def #}}}
# End class #}}}

def import_(*mods, **kwargs): #{{{
    sub = kwargs.get('attr', [])
    all = sub is True
    silent = bool(kwargs.get('silent', False))
    i = kwargs.get('importer', BaseImporter())
    if sub and sub is not True and len(mods) > 1:
        raise ImportError('When importing a module attribute, can only specify a single module')
    ret = []
    names = []
    for m in mods:
        mlist = m.split('.')
        mlist_len = len(mlist)
        count = 0
        path = None
        mod = None
        loader = None
        for name in ('.'.join(mlist[:x + 1]) for x in xrange(mlist_len)):
            loader = i.find_module(name, path)
            if not loader:
                if silent:
                    return None
                raise ImportError('cannot import module %s' %name)
            mod = loader.load_module(name)
            path = getattr(mod, '__path__', None)
        if not mod:
            if silent:
                return None
            raise ImportError('cannot import module %s' %m)
        elif not all and not sub:
            ret.append(mod)
        else:
            if all:
                if hasattr(mod, '__all__'):
                    sub = [attr for attr in getattr(mod, '__all__')]
                else:
                    sub = [attr for attr in dir(mod) if not attr.startswith('_')]
            for s in sub:
                if not hasattr(mod, s):
                    sname = '.'.join([m, s])
                    try:
                        l = i.find_module(sname, mod.__path__)
                        if not l:
                            if silent:
                                return None
                            raise Exception()
                        ret.append(l.load_module(sname))
                        if all:
                            names.append(s)
                    except:
                        if silent:
                            return None
                        raise ImportError('cannot import name %s' %s)
                else:
                    ret.append(getattr(mod, s))
                    if all:
                        names.append(s)
            break
    zipit = []
    if names:
        zipit.append(names)
    if zipit:
        zipit.append(ret)
        ret = zip(*tuple(zipit))
    if not all and len(ret) == 1:
        return ret[0]
    return tuple(ret)
# End def #}}}
