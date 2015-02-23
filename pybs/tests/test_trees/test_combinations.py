# This Python file uses the following encoding: utf-8
from itertools import islice
import unittest

from pybs.unordered_tree import UnorderedTree, leaf, tree_generator
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
    def setUp(self):
        a = tree_generator(sort=True)
        self.et = empty_tree()
        self.t1_1 = a.next()  # []
        self.t2_1 = a.next()  # [[]]
        self.t3_1 = a.next()  # [[[]]]
        self.t3_2 = a.next()  # [[],[]]
        self.t4_1 = a.next()  # [[[[]]]]
        self.t4_2 = a.next()  # [[[],[]]]
        self.t4_3 = a.next()  # [[[]],[]]
        self.t4_4 = a.next()  # [[],[],[]]

    def test_empty(self):
        result = subtrees(self.et)
        expected = LinearCombination()
        expected[(self.et, self.et)] = 1
        self.assertEqual(expected, result)

    def test_first(self):
        result = subtrees(self.t1_1)
        expected = LinearCombination()
        expected[(self.et, self.t1_1)] = 1
        expected[(Forest((self.t1_1,)), self.et)] = 1
        self.assertEqual(expected, result)

    def test_second(self):
        result = subtrees(self.t2_1)
        expected = LinearCombination()
        expected[(self.et, self.t2_1)] = 1
        expected[(Forest((self.t1_1,)), self.t1_1)] = 1
        expected[(Forest((self.t2_1,)), self.et)] = 1
        self.assertEqual(expected, result)

    def test_third(self):
        result = subtrees(self.t3_1)
        expected = LinearCombination()
        expected[(Forest((self.t3_1,)), self.et)] = 1
        expected[(Forest((self.t2_1,)), self.t1_1)] = 1
        expected[(Forest((self.t1_1,)), self.t2_1)] = 1
        expected[(self.et, self.t3_1)] = 1
        self.assertEqual(expected, result)

    def test_fourth(self):
        result = subtrees(self.t3_2)
        expected = LinearCombination()
        expected[(Forest((self.t3_2,)), self.et)] = 1
        expected[(Forest((self.t1_1, self.t1_1)), self.t1_1)] = 1
        expected[(Forest((self.t1_1,)), self.t2_1)] = 2
        expected[(self.et, self.t3_2)] = 1
        self.assertEqual(expected, result)

    def test_fifth(self):
        result = subtrees(self.t4_1)
        expected = LinearCombination()
        expected[(Forest((self.t4_1,)), self.et)] = 1
        expected[(Forest((self.t3_1,)), self.t1_1)] = 1
        expected[(Forest((self.t2_1,)), self.t2_1)] = 1
        expected[(Forest((self.t1_1,)), self.t3_1)] = 1
        expected[(self.et, self.t4_1)] = 1
        self.assertEqual(expected, result)

    def test_sixth(self):
        result = subtrees(self.t4_2)
        expected = LinearCombination()
        expected[(Forest((self.t4_2,)), self.et)] = 1
        expected[(Forest((self.t3_2,)), self.t1_1)] = 1
        expected[(Forest((self.t1_1, self.t1_1)), self.t2_1)] = 1
        expected[(Forest((self.t1_1,)), self.t3_1)] = 2
        expected[(self.et, self.t4_2)] = 1
        print expected
        print result
        self.assertEqual(expected, result)

    def test_seventh(self):
        result = subtrees(self.t4_3)
        expected = LinearCombination()
        expected[(Forest((self.t4_3,)), self.et)] = 1
        expected[(Forest((self.t2_1, self.t1_1)), self.t1_1)] = 1
        expected[(Forest((self.t2_1,)), self.t2_1)] = 1
        expected[(Forest((self.t1_1, self.t1_1)), self.t2_1)] = 1
        expected[(Forest((self.t1_1,)), self.t3_2)] = 1
        expected[(Forest((self.t1_1,)), self.t3_1)] = 1
        expected[(self.et, self.t4_3)] = 1
        self.assertEqual(expected, result)

    def test_eighth(self):
        result = subtrees(self.t4_4)
        expected = LinearCombination()
        expected[(Forest((self.t4_4,)), self.et)] = 1
        expected[(Forest((self.t1_1, self.t1_1, self.t1_1)), self.t1_1)] = 1
        expected[(Forest((self.t1_1, self.t1_1)), self.t2_1)] = 3
        expected[(Forest((self.t1_1,)), self.t3_2)] = 3
        expected[(self.et, self.t4_4)] = 1
        self.assertEqual(expected, result)


class test_Butcher_forest(unittest.TestCase):
    def setUp(self):
        self.basetree = leaf()

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
