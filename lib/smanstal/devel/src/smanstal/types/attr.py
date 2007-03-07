# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
def attr(w=(), d=(), mixins=(), **kw): #{{{
    assert kw, "Empty attribute containers not supported"
    oget = object.__getattribute__
    class Attributes(object): #{{{
        __slots__ = ()
        def __getattribute__(self, name): #{{{
            if name in dir(object) + ['__getitem__', '__iter__']:
                return oget(self, name)
            try:
                return kw[name]
            except KeyError:
                return oget(self, name)
        # End def #}}}

        def __iter__(self): #{{{
            return kw.iterkeys()
        # End def #}}}

        def __getitem__(self, key): #{{{
            return kw[key]
        # End def #}}}

        def __delattr__(self, name): #{{{
            if name in d:
                kw.pop(name, None)
            else:
                raise AttributeError("Attribute '%s' is read-only" %name)
        # End def #}}}

        def __setattr__(self, name, val): #{{{
            if name in w:
                kw[name] = val
            else:
                raise AttributeError("Attribute '%s' is read-only" %name)
        # End def #}}}
    # End class #}}}
    if mixins:
        sig = mixins + mixins.__class__((Attributes,))
        newcls = """
        class MixedAttributes(%s): 
            __slots__ = ()
        """ %', '.join('sig[%i]' %i for i in xrange(len(sig)))
        exec compile(newcls.strip(), '<string>', 'exec') in locals()
        Attributes = MixedAttributes
#    del locals()['kw']
    return Attributes()
# End def #}}}

# Mixin attribute class
class SetAttrOnce(object): #{{{
    __slots__ = ('_count',)
    def __init__(self): #{{{
        object.__setattr__(self, '_count', 0)
    # End def #}}}
    def __setattr__(self, name, val): #{{{
        c = self._count
        if c >= 1:
            raise AttributeError("Already set value %i times" %c)
        try:
            super(M, self).__setattr__(name, val)
        except:
            raise
        else:
            object.__setattr__(self, '_count', c + 1)
    # End def #}}}
# End class #}}}

class Attributes(object): #{{{
    __slots__ = ('_inst',)
    def __init__(self, owner=None): #{{{
        osetattr(self, '_inst', owner)
    # End def #}}}

    def __iter__(self): #{{{
        if self._inst is None:
            raise TypeError("TagAttributes needs an owner")
        return iter(self._inst._kwargs)
    # End def #}}}

    def iteritems(self): #{{{
        if self._inst is None:
            raise TypeError("TagAttributes needs an owner")
        return ((k, v()) for k, v in self._inst._kwargs.iteritems())
    # End def #}}}

    def iterkeys(self): #{{{
        if self._inst is None:
            raise TypeError("TagAttributes needs an owner")
        return iter(self._inst._kwargs)
    # End def #}}}

    def itervalues(self): #{{{
        if self._inst is None:
            raise TypeError("TagAttributes needs an owner")
        return (v() for v in self._inst._kwargs.itervalues())
    # End def #}}}

    def __getattr__(self, name): #{{{
        if not isinstance(name, basestring):
            raise TypeError('Tag attribute names must be strings: %s' %name.__class__.__name__)
        elif self._inst is None:
            raise TypeError("TagAttributes needs an owner")
        default = lambda: None
        return self._inst._kwargs.get(name, default)()
    # End def #}}}

    def __setattr__(self, name, val): #{{{
        if not isinstance(name, basestring):
            raise TypeError('Tag attribute names must be strings: %s' %name.__class__.__name__)
        elif self._inst is None:
            raise TypeError("TagAttributes needs an owner")
        isstr = isinstance(val, basestring)
        if isinstance(val, basestring):
            val = val.strip()
        if val is None:
            self._inst._kwargs.pop(name, None)
        else:
            self._inst._kwargs[name] = quote(val)
    # End def #}}}

    __getitem__ = __getattr__
    __setitem__ = __setattr__

    def __get__(self, inst, owner): #{{{
        return self.__class__(inst)
    # End def #}}}

# End class #}}}
