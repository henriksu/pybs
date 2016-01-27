import unittest
from pybs import unordered_tree
from pybs.unordered_tree import tree_generator, the_trees
from pybs.combinations import empty_tree


class simple_tree(unittest.TestCase):
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

    def test_generator(self):
        print "Hello World!"
        gen = unordered_tree.tree_generator(sort=True)
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
#        self.assertTrue(False)

    def test_graded_component(self):
        print("graded component")
        gen = unordered_tree.trees_of_order(4, True)
        for tree in gen:
            print(tree)

    def test_indexing(self):
        result = the_trees.index(self.t1_1)
        self.assertEqual(1, result)
        result = the_trees.index(self.t2_1)
        self.assertEqual(2, result)
        result = the_trees.index(self.t3_1)
        self.assertEqual(3, result)
        result = the_trees.index(self.t3_2)
        self.assertEqual(4, result)
        result = the_trees.index(self.t4_1)
        self.assertEqual(5, result)
        result = the_trees.index(self.t4_2)
        self.assertEqual(6, result)
        result = the_trees.index(self.t4_3)
        self.assertEqual(7, result)
        result = the_trees.index(self.t4_4)
        self.assertEqual(8, result)
        result = the_trees.index(self.t5_1)
        self.assertEqual(9, result)
        result = the_trees.index(self.t5_2)
        self.assertEqual(10, result)
        result = the_trees.index(self.t5_3)
        self.assertEqual(11, result)
        result = the_trees.index(self.t5_4)
        self.assertEqual(12, result)
        result = the_trees.index(self.t5_5)
        self.assertEqual(13, result)
        result = the_trees.index(self.t5_6)
        self.assertEqual(14, result)
        result = the_trees.index(self.t5_7)
        self.assertEqual(15, result)
        result = the_trees.index(self.t5_8)
        self.assertEqual(16, result)
        result = the_trees.index(self.t5_9)
        self.assertEqual(17, result)
