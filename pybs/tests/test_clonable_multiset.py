import unittest
from pybs.utils import ClonableMultiset


class simple_multisets(unittest.TestCase):
    def test_empty(self):
        a = ClonableMultiset()
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
        self.assertEqual(a.add('a'), ClonableMultiset(['a']))
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

    def test_one_element(self):
        a = ClonableMultiset()
        b = ClonableMultiset({'a': 1})
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
        self.assertEqual(b.add('a'), ClonableMultiset(['a', 'a']))
        self.assertEqual(b.add('b'), ClonableMultiset(['a', 'b']))
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
