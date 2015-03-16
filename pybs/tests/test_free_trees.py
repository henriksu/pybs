import unittest
from pybs.unordered_tree import tree_generator
from pybs.unordered_tree import trees_of_order, the_trees
from pybs.combinations.forests import empty_tree
from pybs.unordered_tree.freeTrees import partition_into_free_trees


class find_representative(unittest.TestCase):
    def setUp(self):
        a = tree_generator(sort=True)  # TODO: Implement indexing of functions.
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

    def test_leaf(self):
        result = self.t1_1.get_free_tree()
        self.assertEqual(self.t1_1, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t1_1])
        self.assertFalse(result.superfluous)
        self.assertEqual(1, the_trees.index(result))
        self.assertEqual(1, the_trees.non_superfluous_index(result))

    def test_second(self):
        result = self.t2_1.get_free_tree()
        self.assertEqual(self.t2_1, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t2_1])
        self.assertTrue(result.superfluous)
        self.assertEqual(2, the_trees.index(result))

    def test_third(self):
        result = self.t3_1.get_free_tree()
        self.assertEqual(self.t3_2, result.representative)
        self.assertEqual(-1, result._rooted_trees[self.t3_1])
        self.assertFalse(result.superfluous)
        self.assertEqual(3, the_trees.index(result))
        self.assertEqual(2, the_trees.non_superfluous_index(result))

    def test_fourth(self):
        result = self.t3_2.get_free_tree()
        self.assertEqual(self.t3_2, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t3_2])
        self.assertFalse(result.superfluous)
        self.assertEqual(3, the_trees.index(result))
        self.assertEqual(2, the_trees.non_superfluous_index(result))

    def test_fifth(self):
        result = self.t4_1.get_free_tree()
        self.assertEqual(self.t4_3, result.representative)
        self.assertEqual(-1, result._rooted_trees[self.t4_1])
        self.assertTrue(result.superfluous)
        self.assertEqual(4, the_trees.index(result))

    def test_sixth(self):
        result = self.t4_2.get_free_tree()
        self.assertEqual(self.t4_4, result.representative)
        self.assertEqual(-1, result._rooted_trees[self.t4_2])
        self.assertFalse(result.superfluous)
        self.assertEqual(5, the_trees.index(result))
        self.assertEqual(3, the_trees.non_superfluous_index(result))

    def test_seventh(self):
        result = self.t4_3.get_free_tree()
        self.assertEqual(self.t4_3, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t4_3])
        self.assertTrue(result.superfluous)
        self.assertEqual(4, the_trees.index(result))

    def test_eighth(self):
        result = self.t4_4.get_free_tree()
        self.assertEqual(self.t4_4, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t4_4])
        self.assertFalse(result.superfluous)
        self.assertEqual(5, the_trees.index(result))
        self.assertEqual(3, the_trees.non_superfluous_index(result))

    def test_ninth(self):
        result = self.t5_1.get_free_tree()
        self.assertEqual(self.t5_7, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t5_1])
        self.assertFalse(result.superfluous)
        self.assertEqual(6, the_trees.index(result))
        self.assertEqual(4, the_trees.non_superfluous_index(result))

    def test_tenth(self):
        result = self.t5_2.get_free_tree()
        self.assertEqual(self.t5_8, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t5_2])
        self.assertFalse(result.superfluous)
        self.assertEqual(7, the_trees.index(result))
        self.assertEqual(5, the_trees.non_superfluous_index(result))

    def test_eleventh(self):
        result = self.t5_3.get_free_tree()
        self.assertEqual(self.t5_8, result.representative)
        self.assertEqual(-1, result._rooted_trees[self.t5_3])
        self.assertFalse(result.superfluous)
        self.assertEqual(7, the_trees.index(result))
        self.assertEqual(5, the_trees.non_superfluous_index(result))

    def test_twelfth(self):
        result = self.t5_4.get_free_tree()
        self.assertEqual(self.t5_9, result.representative)
        self.assertEqual(-1, result._rooted_trees[self.t5_4])
        self.assertFalse(result.superfluous)
        self.assertEqual(8, the_trees.index(result))
        self.assertEqual(6, the_trees.non_superfluous_index(result))

    def test_thirteenth(self):
        result = self.t5_5.get_free_tree()
        self.assertEqual(self.t5_7, result.representative)
        self.assertEqual(-1, result._rooted_trees[self.t5_5])
        self.assertFalse(result.superfluous)
        self.assertEqual(6, the_trees.index(result))
        self.assertEqual(4, the_trees.non_superfluous_index(result))

    def test_fourteenth(self):
        result = self.t5_6.get_free_tree()
        self.assertEqual(self.t5_8, result.representative)
        self.assertEqual(-1, result._rooted_trees[self.t5_6])
        self.assertFalse(result.superfluous)
        self.assertEqual(7, the_trees.index(result))
        self.assertEqual(5, the_trees.non_superfluous_index(result))

    def test_fifteenth(self):
        result = self.t5_7.get_free_tree()
        self.assertEqual(self.t5_7, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t5_7])
        self.assertFalse(result.superfluous)
        self.assertEqual(6, the_trees.index(result))
        self.assertEqual(4, the_trees.non_superfluous_index(result))

    def test_sixteenth(self):
        result = self.t5_8.get_free_tree()
        self.assertEqual(self.t5_8, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t5_8])
        self.assertFalse(result.superfluous)
        self.assertEqual(7, the_trees.index(result))
        self.assertEqual(5, the_trees.non_superfluous_index(result))

    def test_seventeenth(self):
        result = self.t5_9.get_free_tree()
        self.assertEqual(self.t5_9, result.representative)
        self.assertEqual(1, result._rooted_trees[self.t5_9])
        self.assertFalse(result.superfluous)
        self.assertEqual(8, the_trees.index(result))
        self.assertEqual(6, the_trees.non_superfluous_index(result))


class find_partition(unittest.TestCase):
    # This is sequence A000055
    def test_first_order(self):
        result = partition_into_free_trees(trees_of_order(1))
        self.assertEqual(1, len(result))

    def test_second_order(self):
        result = partition_into_free_trees(trees_of_order(2))
        self.assertEqual(1, len(result))

    def test_third_order(self):
        result = partition_into_free_trees(trees_of_order(3))
        self.assertEqual(1, len(result))

    def test_fourth_order(self):
        result = partition_into_free_trees(trees_of_order(4))
        self.assertEqual(2, len(result))

    def test_fifth_order(self):
        result = partition_into_free_trees(trees_of_order(5))
        self.assertEqual(3, len(result))

    def test_sixth_order(self):
        result = partition_into_free_trees(trees_of_order(6))
        self.assertEqual(6, len(result))

    def test_seventh_order(self):
        result = partition_into_free_trees(trees_of_order(7))
        self.assertEqual(11, len(result))

    def test_eighth_order(self):
        result = partition_into_free_trees(trees_of_order(8))
        self.assertEqual(23, len(result))

    def test_ninth_order(self):
        result = partition_into_free_trees(trees_of_order(9))
        self.assertEqual(47, len(result))

    def test_tenth_order(self):
        result = partition_into_free_trees(trees_of_order(10))
        self.assertEqual(106, len(result))

    def test_eleventh_order(self):
        result = partition_into_free_trees(trees_of_order(11))
        self.assertEqual(235, len(result))

    def test_twelfth_order(self):
        result = partition_into_free_trees(trees_of_order(12))
        self.assertEqual(551, len(result))
