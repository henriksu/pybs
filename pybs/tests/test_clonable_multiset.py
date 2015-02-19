import unittest
from pybs.utils import ClonableMultiset, ClonableMultisets

Multiset = ClonableMultisets()

class simple_multisets(unittest.TestCase):
    def test_empty(self):
        a = Multiset()
        self.assertFalse(bool(a))
        self.assertTrue(a.is_immutable())
        with self.assertRaises(ValueError):
            a['a'] = 1
        self.assertEqual(a['a'], 0)
        with self.assertRaises(ValueError):
            del a['a']
        with self.assertRaises(ValueError):
            a.inplace_multiset_sum(a)
        with self.assertRaises(ValueError):
            a.inplace_add('a')
        self.assertEqual(a, a)
        self.assertEqual(a.add('a'), Multiset(['a']))
        self.assertNotEqual(a, a.add('a'))
        with self.assertRaises(ValueError):
            a.inplace_multiset_difference(a)
        #
        self.assertEqual(a, a.scalar_mul(0))
        self.assertEqual(a, a.scalar_mul(1))
        self.assertEqual(a, a.scalar_mul(2))
        #
        self.assertEqual(a, a.multiset_difference(a))
        #
        self.assertEqual(a, a | a)
        self.assertEqual(a, a & a)
        #
        self.assertEqual(a.cardinality(), 0)
        self.assertEqual(a.no_uniques(), 0)
        self.assertEqual(a.most_common(), [])  # TODO: Wanted?
        self.assertEqual(list(a.elements()), [])
        #
        with self.assertRaises(AttributeError):
            a.tmp = 0
        with self.assertRaises(AttributeError):
            a._ms = []
        self.assertEqual(repr(a), 'ClonableMultiset()')
        self.assertEqual(a._latex_(), '\\emptyset')
        #
        self.assertTrue(a.is_finite())

    def test_one_element(self):
        a = Multiset()
        b = Multiset({'a': 1})
        self.assertTrue(bool(b))
        self.assertTrue(b.is_immutable())
        with self.assertRaises(ValueError):
            b['a'] = 1
        self.assertEqual(b['a'], 1)
        self.assertEqual(b['b'], 0)
        with self.assertRaises(ValueError):
            del b['a']
        with self.assertRaises(ValueError):
            del b['b']
        with self.assertRaises(ValueError):
            b.inplace_multiset_sum(a)
        with self.assertRaises(ValueError):
            b.inplace_add('a')
        with self.assertRaises(ValueError):
            b.inplace_add('b')
        self.assertEqual(b, b)
        self.assertEqual(b.add('a'), Multiset(['a', 'a']))
        self.assertEqual(b.add('b'), Multiset(['a', 'b']))
        self.assertNotEqual(b, b.add('a'))
        self.assertNotEqual(b, b.add('b'))
        with self.assertRaises(ValueError):
            b.inplace_multiset_difference(a)
        #
        self.assertNotEqual(b, b.scalar_mul(0))
        self.assertEqual(b, b.scalar_mul(1))
        self.assertNotEqual(b, b.scalar_mul(2))
        #
        self.assertEqual(b, b.multiset_difference(a))
        self.assertEqual(a, b.multiset_difference(b))
        #
        self.assertEqual(b, b | b)
        self.assertEqual(b, b | a)
        self.assertEqual(b, b & b)
        self.assertEqual(a, b & a)
        #
        self.assertEqual(b.cardinality(), 1)
        self.assertEqual(b.no_uniques(), 1)
        self.assertEqual(b.most_common(), [('a', 1)])
        self.assertEqual(list(b.elements()), ['a'])
        #
        with self.assertRaises(AttributeError):
            b.tmp = 0
        with self.assertRaises(AttributeError):
            b._ms = []
        self.assertEqual(repr(b), "ClonableMultiset({'a': 1})")
        self.assertEqual(b._latex_(), "\\left[\\text{\\texttt{a}} ^{ 1 }\\right]")
        self.assertTrue('a' in b)
        self.assertFalse('b' in b)

    def test_double_element(self):
        a = Multiset()
        b = Multiset({'a': 1})
        c = Multiset({'a': 2})
        self.assertTrue(bool(c))
        self.assertTrue(c.is_immutable())
        with self.assertRaises(ValueError):
            c['a'] = 1
        self.assertEqual(c['a'], 2)
        self.assertEqual(c['b'], 0)
        with self.assertRaises(ValueError):
            del c['a']
        with self.assertRaises(ValueError):
            del c['b']
        with self.assertRaises(ValueError):
            c.inplace_multiset_sum(a)
        with self.assertRaises(ValueError):
            c.inplace_add('a')
        with self.assertRaises(ValueError):
            c.inplace_add('b')
        self.assertEqual(c, c)
        self.assertEqual(c.add('a'), Multiset(['a', 'a', 'a']))
        self.assertEqual(c.add('b'), Multiset(['a', 'a', 'b']))
        self.assertNotEqual(c, c.add('a'))
        self.assertNotEqual(c, c.add('b'))
        with self.assertRaises(ValueError):
            c.inplace_multiset_difference(a)
        #
        self.assertNotEqual(c, c.scalar_mul(0))
        self.assertEqual(c, c.scalar_mul(1))
        self.assertNotEqual(c, c.scalar_mul(2))
        #
        self.assertEqual(c, c.multiset_difference(a))
        self.assertEqual(b, c.multiset_difference(b))
        self.assertEqual(a, c.multiset_difference(c))
        #
        self.assertEqual(c, c | c)
        self.assertEqual(c, c | b)
        self.assertEqual(c, c | a)
        self.assertEqual(c, c & c)
        self.assertEqual(b, c & b)
        self.assertEqual(a, c & a)
        #
        self.assertEqual(c.cardinality(), 2)
        self.assertEqual(c.no_uniques(), 1)
        self.assertEqual(c.most_common(), [('a', 2)])
        self.assertEqual(list(c.elements()), ['a', 'a'])
        #
        with self.assertRaises(AttributeError):
            c.tmp = 0
        with self.assertRaises(AttributeError):
            c._ms = []
        self.assertEqual(repr(c), "ClonableMultiset({'a': 2})")
        self.assertEqual(c._latex_(), "\\left[\\text{\\texttt{a}} ^{ 2 }\\right]")
