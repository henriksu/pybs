# This Python file uses the following encoding: utf-8
import unittest

from pybs.utils import LinearCombination
from pybs.unordered_tree import UnorderedTree, leaf, tree_generator
from pybs.combinations.forests import empty_tree
from pybs.combinations import Forest, differentiate as D, \
    tree_commutator
from pybs.combinations.functions import subtrees, \
    _subtrees_for_antipode, antipode_ck, symp_split


class test_commutator(unittest.TestCase):
    def test_empty(self):
        tree = empty_tree
        self.assertEqual(tree_commutator(tree, tree), LinearCombination())

    def test_first_and_empty(self):
        tree1 = empty_tree
        tree2 = leaf
        self.assertEqual(tree_commutator(tree1, tree2), LinearCombination())
        self.assertEqual(tree_commutator(tree2, tree2), LinearCombination())

    def test_first_second(self):
        tree1 = leaf
        tree2 = D(tree1).keys()[0]
        expected = LinearCombination()
        forest1 = Forest([tree1, tree1])
        tree3 = UnorderedTree(forest1)
        expected -= tree3
        result = tree_commutator(tree2, tree1)
        self.assertEqual(result, expected)


class test_subtrees(unittest.TestCase):
    def setUp(self):
        a = tree_generator(sort=True)
        self.et = empty_tree
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


class test_subtrees_for_antipode(unittest.TestCase):
    def setUp(self):
        a = tree_generator(sort=True)
        self.et = empty_tree
        self.t1_1 = a.next()  # []
        self.t2_1 = a.next()  # [[]]
        self.t3_1 = a.next()  # [[[]]]
        self.t3_2 = a.next()  # [[],[]]
        self.t4_1 = a.next()  # [[[[]]]]
        self.t4_2 = a.next()  # [[[],[]]]
        self.t4_3 = a.next()  # [[[]],[]]
        self.t4_4 = a.next()  # [[],[],[]]

    def test_empty(self):
        result = _subtrees_for_antipode(self.et)
        expected = LinearCombination()
        self.assertEqual(expected, result)

    def test_first(self):
        result = _subtrees_for_antipode(self.t1_1)
        expected = LinearCombination()
        self.assertEqual(expected, result)

    def test_second(self):
        result = _subtrees_for_antipode(self.t2_1)
        expected = LinearCombination()
        expected[(Forest((self.t1_1,)), self.t1_1)] = 1
        self.assertEqual(expected, result)

    def test_third(self):
        result = _subtrees_for_antipode(self.t3_1)
        expected = LinearCombination()
        expected[(Forest((self.t2_1,)), self.t1_1)] = 1
        expected[(Forest((self.t1_1,)), self.t2_1)] = 1
        self.assertEqual(expected, result)

    def test_fourth(self):
        result = _subtrees_for_antipode(self.t3_2)
        expected = LinearCombination()
        expected[(Forest((self.t1_1, self.t1_1)), self.t1_1)] = 1
        expected[(Forest((self.t1_1,)), self.t2_1)] = 2
        self.assertEqual(expected, result)

    def test_fifth(self):
        result = _subtrees_for_antipode(self.t4_1)
        expected = LinearCombination()
        expected[(Forest((self.t3_1,)), self.t1_1)] = 1
        expected[(Forest((self.t2_1,)), self.t2_1)] = 1
        expected[(Forest((self.t1_1,)), self.t3_1)] = 1
        self.assertEqual(expected, result)

    def test_sixth(self):
        result = _subtrees_for_antipode(self.t4_2)
        expected = LinearCombination()
        expected[(Forest((self.t3_2,)), self.t1_1)] = 1
        expected[(Forest((self.t1_1, self.t1_1)), self.t2_1)] = 1
        expected[(Forest((self.t1_1,)), self.t3_1)] = 2
        print expected
        print result
        self.assertEqual(expected, result)

    def test_seventh(self):
        result = _subtrees_for_antipode(self.t4_3)
        expected = LinearCombination()
        expected[(Forest((self.t2_1, self.t1_1)), self.t1_1)] = 1
        expected[(Forest((self.t2_1,)), self.t2_1)] = 1
        expected[(Forest((self.t1_1, self.t1_1)), self.t2_1)] = 1
        expected[(Forest((self.t1_1,)), self.t3_2)] = 1
        expected[(Forest((self.t1_1,)), self.t3_1)] = 1
        self.assertEqual(expected, result)

    def test_eighth(self):
        result = _subtrees_for_antipode(self.t4_4)
        expected = LinearCombination()
        expected[(Forest((self.t1_1, self.t1_1, self.t1_1)), self.t1_1)] = 1
        expected[(Forest((self.t1_1, self.t1_1)), self.t2_1)] = 3
        expected[(Forest((self.t1_1,)), self.t3_2)] = 3
        self.assertEqual(expected, result)


class test_antipode(unittest.TestCase):
    def setUp(self):
        a = tree_generator(sort=True)
        self.et = empty_tree
        self.t1_1 = a.next()  # []
        self.t2_1 = a.next()  # [[]]
        self.t3_1 = a.next()  # [[[]]]
        self.t3_2 = a.next()  # [[],[]]
        self.t4_1 = a.next()  # [[[[]]]]
        self.t4_2 = a.next()  # [[[],[]]]
        self.t4_3 = a.next()  # [[[]],[]]
        self.t4_4 = a.next()  # [[],[],[]]

    def test_empty(self):
        result = antipode_ck(self.et)
        expected = LinearCombination()
        expected[empty_tree] = 1
        self.assertEqual(expected, result)

    def test_first(self):
        result = antipode_ck(self.t1_1)
        expected = LinearCombination()
        expected[Forest((leaf,))] = -1
        self.assertEqual(expected, result)

    def test_second(self):
        result = antipode_ck(self.t2_1)
        expected = LinearCombination()
        expected[Forest((self.t2_1,))] = -1
        expected[Forest((self.t1_1, self.t1_1))] = 1
        self.assertEqual(expected, result)

    def test_third(self):
        result = antipode_ck(self.t3_1)
        expected = LinearCombination()
        expected[Forest((self.t3_1,))] = -1
        expected[Forest((self.t2_1, self.t1_1))] = 2
        expected[Forest((self.t1_1, self.t1_1, self.t1_1))] = -1
        self.assertEqual(expected, result)

    def test_fourth(self):
        result = antipode_ck(self.t3_2)
        expected = LinearCombination()
        expected[Forest((self.t3_2,))] = -1
        expected[Forest((self.t2_1, self.t1_1))] = 2
        expected[Forest((self.t1_1, self.t1_1, self.t1_1))] = -1
        self.assertEqual(expected, result)


class test_symp_split(unittest.TestCase):
    def setUp(self):
        a = tree_generator(sort=True)
        self.et = empty_tree
        self.t1_1 = a.next()  # []
        self.t2_1 = a.next()  # [[]]
        self.t3_1 = a.next()  # [[[]]]
        self.t3_2 = a.next()  # [[],[]]
        self.t4_1 = a.next()  # [[[[]]]]
        self.t4_2 = a.next()  # [[[],[]]]
        self.t4_3 = a.next()  # [[[]],[]]
        self.t4_4 = a.next()  # [[],[],[]]
        self.t5_1 = a.next()  # [[[[[]]]]]
        self.t5_2 = a.next()  # [[[[],[]]]]
        self.t5_3 = a.next()  # [[[[]],[]]]
        self.t5_4 = a.next()  # [[[],[],[]]]
        self.t5_5 = a.next()  # [[[[]]],[]
        self.t5_6 = a.next()  # [[[],[]],[]]
        self.t5_7 = a.next()  # [[[]],[[]]]
        self.t5_8 = a.next()  # [[[]],[],[]]
        self.t5_9 = a.next()  # [[],[],[],[]]

    def test_first(self):
        result = symp_split(self.t1_1)
        expected = LinearCombination()  # TODO: right way to do it?
        self.assertEqual(expected, result)

    def test_second(self):
        result = symp_split(self.t2_1)
        expected = LinearCombination()
        expected += self.t1_1
        self.assertEqual(expected, result)

    def test_third(self):
        result = symp_split(self.t3_1)
        expected = LinearCombination()
        expected[self.t2_1] = 1
        self.assertEqual(expected, result)

    def test_fourth(self):
        result = symp_split(self.t3_2)
        expected = LinearCombination()
        expected[self.t2_1] = 2
        self.assertEqual(expected, result)

    def test_fifth(self):
        result = symp_split(self.t4_1)
        expected = LinearCombination()
        expected[self.t3_1] = 1
        self.assertEqual(expected, result)

    def test_sixth(self):
        result = symp_split(self.t4_2)
        expected = LinearCombination()
        expected[self.t3_1] = 2
        self.assertEqual(expected, result)

    def test_seventh(self):
        result = symp_split(self.t4_3)
        expected = LinearCombination()
        expected[self.t3_1] = 1
        expected[self.t3_2] = 1
        self.assertEqual(expected, result)

    def test_eighth(self):
        result = symp_split(self.t4_4)
        expected = LinearCombination()
        expected[self.t3_2] = 3
        self.assertEqual(expected, result)

    def test_ninth(self):
        result = symp_split(self.t5_1)
        expected = LinearCombination()
        expected[self.t4_1] = 1
        self.assertEqual(expected, result)

    def test_tenth(self):
        result = symp_split(self.t5_2)
        expected = LinearCombination()
        expected[self.t4_1] = 2
        self.assertEqual(expected, result)

    def test_eleventh(self):
        result = symp_split(self.t5_3)
        expected = LinearCombination()
        expected[self.t4_1] = 1
        expected[self.t4_2] = 1
        self.assertEqual(expected, result)

    def test_twelfth(self):
        result = symp_split(self.t5_4)
        expected = LinearCombination()
        expected[self.t4_2] = 3
        self.assertEqual(expected, result)

    def test_thirteenth(self):
        result = symp_split(self.t5_5)
        expected = LinearCombination()
        expected[self.t4_1] = 1
        expected[self.t4_3] = 1
        self.assertEqual(expected, result)

    def test_fourteenth(self):
        result = symp_split(self.t5_6)
        expected = LinearCombination()
        expected[self.t4_2] = 1
        expected[self.t4_3] = 2
        self.assertEqual(expected, result)

    def test_fifthteenth(self):
        result = symp_split(self.t5_7)
        expected = LinearCombination()
        expected[self.t4_3] = 2
        self.assertEqual(expected, result)

    def test_sixthteenth(self):
        result = symp_split(self.t5_8)
        expected = LinearCombination()
        expected[self.t4_4] = 1
        expected[self.t4_3] = 2
        self.assertEqual(expected, result)

    def test_seventeenth(self):
        result = symp_split(self.t5_9)
        expected = LinearCombination()
        expected[self.t4_4] = 4
        self.assertEqual(expected, result)

    def test_last(self):
        t1 = UnorderedTree([self.t3_2, self.t3_2])
        result = symp_split(t1)
        t2 = UnorderedTree([self.t3_2, self.t2_1])
        expected = LinearCombination()
        expected[t2] = 4
        self.assertEqual(expected, result)


class test_Butcher_forest(unittest.TestCase):
    def setUp(self):
        self.basetree = leaf

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
