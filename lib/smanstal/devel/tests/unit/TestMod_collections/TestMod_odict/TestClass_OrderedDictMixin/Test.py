# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import unittest, re
from smanstal.tests import BaseUnitTest, addtest, mksuite

from smanstal.collections.odict import odict
from string import ascii_lowercase

class Test_odict(BaseUnitTest): #{{{
    def setUp(self): #{{{
        self.mkinput = lambda input: ((v, k) for k, v in enumerate(input))
        self.d1 = ascii_lowercase[:13]
        self.d2 = ascii_lowercase[13:]
        self.data = list(self.mkinput(self.d1))
    # End def #}}}

    def tearDown(self): #{{{
        pass
    # End def #}}}

    def testNonOrderedDictMixin(self): #{{{
        '''Non-OrderedDictMixin will always fail equality test'''
        d = self.data
        other = dict(d)
        od = odict(d)
        self.assertNotEqual(od, other)
        other = dict()
        od = odict()
        self.assertNotEqual(od, other)
    # End def #}}}

    def testCompareKeys(self): #{{{
        '''If equal dictionaries, test equality of _keys vars'''
        d = self.data
        other = odict()
        od = odict()
        self.assertEqual(od, other)
        other = odict(d)
        od = odict(d)
        self.assertEqual(od, other)
        other._keys[:] = []
        self.assertNotEqual(od, other)
    # End def #}}}

    def testStrRepr(self): #{{{
        '''String repr shows key/value pairs in order'''
        d = self.data
        expected = '{%s}'
        inner = ', '.join('%s: %s' %(repr(k), repr(v)) for k, v in d)
        expected = expected %inner
        self.assertEqual(str(odict(d)), expected)
    # End def #}}}

    def test_iterkeys(self): #{{{
        '''Iterate keys in order key/value pairs were added'''
        d = self.data
        od = odict(d)
        expected = list(k for k, v in d)
        self.assertEqual(list(od.iterkeys()), expected)
        self.assertEqual(list(od), expected)
        self.assertEqual(od.keys(), expected)
    # End def #}}}

    def test_setitem(self): #{{{
        '''Only add to _keys list if key doesn't exist in the list'''
        od = odict()
        self.assertEqual(od._keys, [])
        od['a'] = 1
        self.assertEqual(od._keys, ['a'])
        od['c'] = 2
        od['e'] = 3
        od['a'] = 4
        self.assertEqual(od._keys, ['a', 'c', 'e'])
    # End def #}}}

    def test_setitem_error(self): #{{{
        '''Error setting item does not set _keys list'''
        od = odict()
        self.assertRaisesEx(TypeError, od.__setitem__, [], 1)
        self.assertEqual(od._keys, [])
    # End def #}}}

    def test_add_key(self): #{{{
        '''Adds to _keys list'''
        od = odict()
        od._add_key(1)
        self.assertEqual(od._keys, [1])
    # End def #}}}

    def test_setitem_keycheck(self): #{{{
        '''True if key is not in _keys, False otherwise'''
        od = odict()
        self.assertTrue(od._setitem_keycheck(1))
        od[1] = 'a'
        self.assertFalse(od._setitem_keycheck(1))
    # End def #}}}

    def test_copy(self): #{{{
        '''Make a shallow copy'''
        od = odict(self.data)
        for cfunc in ('copy', '__copy__'):
            new = getattr(od, cfunc)()
            self.assertEqual(od, new)
            self.assertNotEqual(id(od), id(new))
            self.assertTrue(isinstance(new, odict))
    # End def #}}}

    def test_clear(self): #{{{
        '''Clears dict and _keys'''
        od = odict(self.data)
        od.clear()
        self.assertFalse(od)
        self.assertFalse(od._keys)
    # End def #}}}

    def test_iteritems(self): #{{{
        '''Return list of items in order key/value pairs were added'''
        d = self.data
        od = odict(d)
        self.assertEqual(list(od.iteritems()), d)
        self.assertEqual(od.items(), d)
    # End def #}}}

    def test_itervalues(self): #{{{
        '''Return list of values in order key/value pairs were added'''
        d = self.data
        expected = list(v for k, v in d)
        od = odict(d)
        self.assertEqual(list(od.itervalues()), expected)
        self.assertEqual(od.values(), expected)
    # End def #}}}

#    def test_itergetfunc(self): #{{{
#        '''itergetfunc function gets called'''
#        count = [0]
#        class test(odict): #{{{
#            def _itergetfunc(self): #{{{
#                supfunc = super(test, self)._itergetfunc()
#                def func(index): #{{{
#                    count[0] += 1
#                    return supfunc(index)
#                # End def #}}}
#                return func
#            # End def #}}}
#        # End class #}}}

#        od = test(self.data)
#        od.items()
#        self.assertEqual(count[0], len(self.data))
#    # End def #}}}

    def test_fromkeys(self): #{{{
        '''Test fromkeys'''
        od = odict(self.data)
        exp = odict((k, 42) for k in xrange(10))
        fod = od.fromkeys(xrange(10), 42)
        self.assertTrue(od is not fod)
        self.assertTrue(isinstance(fod, odict))
        self.assertNotEqual(fod, od)
        self.assertEqual(fod, exp)
    # End def #}}}

    def test_pop_removekey(self): #{{{
        '''Remove key from _keys'''
        od = odict(self.data)
        od._pop_removekey('a')
        self.assertTrue('a' not in od._keys)
    # End def #}}}

    def test_pop(self): #{{{
        '''Popping removes key from _keys'''
        m = dict(self.data)
        od = odict(self.data)
        diff = 0
        for i in ('a', 'd'):
            ret = od.pop(i)
            self.assertEqual(ret, m[i])
            self.assertTrue(i not in od._keys)
            self.assertTrue(i not in od)
            diff += 1
            self.assertEqual(len(od), len(self.data)-diff)
    # End def #}}}

    def test_popitem(self): #{{{
        '''Pop last added item'''
        od = odict(self.data)
        ret = od.popitem()
        self.assertEqual(ret, self.data[-1])
        self.assertEqual(len(od), len(self.data)-1)
        self.assertTrue(ret not in od._keys)
        self.assertEqual(od._keys, [k for k, v in self.data[:-1]])
    # End def #}}}

    def test_setdefault(self): #{{{
        '''Similar to setitem'''
        od = odict()
        ret = od.setdefault('a', 42)
        self.assertEqual(ret, 42)
        self.assertTrue('a' in od._keys)
        self.assertTrue('a' in od)
        self.assertEqual(od['a'], 42)
    # End def #}}}

    def test_update_kw_overrides_args(self): #{{{
        '''Keyword arguments overrides args to update()'''
        od = odict()
        kw = dict(a=42, e=52, c=62)
        od.update(self.data, **kw)
        for k, v in kw.iteritems():
            self.assertEqual(od[k], v)
    # End def #}}}

    def test_update_onearg(self): #{{{
        '''Passing more than one arg to update() is bad'''
        od = odict()
        regex = re.compile(r'odict expected at most 1 argument, got 2')
        self.assertRaisesEx(TypeError, od.update, 1, 2, exc=regex)
    # End def #}}}
# End class #}}}

# Create suite function for this module
suite = addtest(mksuite(__file__))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

