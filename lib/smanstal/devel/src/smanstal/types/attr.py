# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
def attr(*mixins, **kw): #{{{
    assert kw, "Empty attribute containers not supported"
    oget = object.__getattribute__
    class Attributes(object): #{{{
        __slots__ = kw.keys()
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
            raise AttributeError("Attribute '%s' is read-only" %name)
        # End def #}}}

        def __setattr__(self, name, val): #{{{
            raise AttributeError("Attribute '%s' is read-only" %name)
        # End def #}}}
    # End class #}}}
    if mixins:
        sig = mixins + (Attributes,)
        newcls = """
        class MixedAttributes(%s): 
            __slots__ = ()
        """ %', '.join('sig[%i]' %i for i in xrange(len(sig)))
        exec compile(newcls.strip(), '<string>', 'exec') in locals()
        Attributes = MixedAttributes
    del locals()['kw']
    return Attributes()
# End def #}}}

