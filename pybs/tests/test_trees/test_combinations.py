# This Python file uses the following encoding: utf-8
from itertools import islice
import unittest

from pybs.unordered_tree import UnorderedTree, leaf
from pybs.combinations.forests import empty_tree
from pybs.combinations import Forest, LinearCombination, differentiate as D, \
    treeCommutator
from pybs.combinations.functions import subtrees


class test_commutator(unittest.TestCase):
    def test_empty(self):
        tree = empty_tree()
        self.assertEqual(treeCommutator(tree, tree), LinearCombination())

    def test_first_and_empty(self):
        tree1 = empty_tree()
        tree2 = leaf()
        self.assertEqual(treeCommutator(tree1, tree2), LinearCombination())
        self.assertEqual(treeCommutator(tree2, tree2), LinearCombination())

    def test_first_second(self):
        tree1 = leaf()
        tree2 = D(tree1).keys()[0]
        expected = LinearCombination()
        forest1 = Forest([tree1, tree1])
        tree3 = UnorderedTree(forest1)
        expected -= tree3
        result = treeCommutator(tree1, tree2)
        self.assertEqual(result, expected)


class test_subtrees(unittest.TestCase):
    def test_first(self):
        a = leaf()
        result = subtrees(a)
        print result
        self.assertTrue(True)  # Todo make proper test.

    def test_second(self):
        a = UnorderedTree('[[]]')
        result = subtrees(a)
        print result
        self.assertTrue(False)


class test_Butcher_forest(unittest.TestCase):
    def setUp(self):
        self.basetree = UnorderedTree(Forest())

    def test_first(self):
        self.assertEqual('[]', str(self.basetree))

    def test_second(self):
        forest = D(self.basetree)
        self.assertEqual('1*[[]]', str(forest))

    def test_third(self):
        thesum = D(self.basetree)
        thesum = D(thesum)
        self.assertEqual('1*[[[]]] + 1*[[],[]]', str(thesum))

    def test_fourth(self):
        thingy = D(D(D(self.basetree)))
        self.assertEqual(
            '3*[[[]],[]] + 1*[[[[]]]] + 1*[[],[],[]] + 1*[[[],[]]]',
            str(thingy))

    def test_fifth(self):
        forest = D(D(D(D(self.basetree))))
        expected = '4*[[],[[[]]]] + 1*[[[[[]]]]] + 1*[[[],[],[]]] + ' + \
            '1*[[[[],[]]]] + 3*[[[]],[[]]] + 4*[[],[[],[]]] + 3*[[[[]],[]]] + ' + \
            '1*[[],[],[],[]] + 6*[[[]],[],[]]'
        self.assertEqual(expected, str(forest))

    def test_count_forests(self):  # Also a stress test.
        # self.assertTrue(False)
        result = [1]
        for _ in xrange(11):
            self.basetree = D(self.basetree)
            result.append(self.basetree.dimensions())
        expected = [1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766]
        self.assertListEqual(expected, result)

    # def test_ordering(self):
    #    n = 17
    #    result = list(tree for tree in islice(treeGenerator(), 0, n+1))
    #    result.sort()
    #    expected = None
#         expected = [ButcherEmptyTree(),
#                     ButcherTree('[]'),
#                     ButcherTree('[[]]'),
#                     ButcherTree('[[[]]]'),
#                     ButcherTree('[[],[]]'),
#                     ButcherTree('[[[[]]]]'),
#                     ButcherTree('[[[],[]]]'),
#                     ButcherTree('[[[]],[]]'),
#                     ButcherTree('[[],[],[]]'),
#                     ButcherTree('[[[[[]]]]]'),
#                     ButcherTree('[[[[],[]]]]'),
#                     ButcherTree('[[[[]],[]]]'),
#                     ButcherTree('[[[],[],[]]]'),
#                     ButcherTree('[[],[[[]]]]'),
#                     ButcherTree('[[],[[],[]]]'),
#                     ButcherTree('[[[]],[[]]]'),
#                     ButcherTree('[[[]],[],[]]'),
#                     ButcherTree('[[],[],[],[]]]')]
#        self.assertEqual(expected, result)
     #   self.assertTrue(True)
# In the long run test_count_forests would give
# a=[1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973, 87811,
# 235381, 634847, 1721159]
# When it was finished, about 2GB of memory was used.
