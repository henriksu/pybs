# This Python file uses the following encoding: utf-8
import unittest

from src.trees import ButcherTree, ButcherEmptyTree
from src.combinations import Forest, LinearCombination, differentiate as D, \
    treeCommutator


class test_commutator(unittest.TestCase):
    def test_empty(self):
        tree = ButcherEmptyTree()
        self.assertEqual(treeCommutator(tree, tree), LinearCombination())

    def test_first_and_empty(self):
        tree1 = ButcherEmptyTree()
        tree2 = ButcherTree.basetree()
        self.assertEqual(treeCommutator(tree1, tree2), LinearCombination())
        self.assertEqual(treeCommutator(tree2, tree2), LinearCombination())

    def test_first_second(self):
        tree1 = ButcherTree.basetree()
        tree2 = D(tree1).keys()[0]
        expected = LinearCombination()
        forest1 = Forest([tree1, tree1])
        tree3 = ButcherTree(forest1)
        expected -= tree3
        result = treeCommutator(tree1, tree2)
        self.assertEqual(result, expected)


class test_Butcher_forest(unittest.TestCase):
    def setUp(self):
        self.basetree = ButcherTree(Forest())

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
        for i in xrange(11):
            i
            self.basetree = D(self.basetree)
            result.append(self.basetree.dimensions())
        expected = [1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766]
        self.assertListEqual(expected, result)
# In the long run test_count_forests would give
# a=[1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973, 87811,
# 235381, 634847, 1721159]
# When it was finished, about 2GB of memory was used.
