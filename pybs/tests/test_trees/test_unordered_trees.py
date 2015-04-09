# This Python file uses the following encoding: utf-8
import unittest
# from pybs.trees import ButcherTree, alpha, F, order, number_of_children, \
#    density, symmetry, isTall, isBinary, isBushy
from pybs.unordered_tree import UnorderedTree, leaf
from pybs.combinations import Forest


# class empty_tree(unittest.TestCase):
# #Does NOT test derivation, grafting and other operations.
#     def test_initialisation(self):
#         self.assertIsInstance(ButcherTree(), ButcherTree)
#
#     def test_str(self):
#         tree1 = ButcherTree.emptytree()
#         self.assertEqual('Ø', str(tree1))
#
#     def test_equality(self):
#         tree1 = ButcherTree.emptytree()
#         tree2 = ButcherNotTree()
#         self.assertEqual(tree1, tree2)
#
#     def test_number_of_subtrees(self):
#         tree1 = ButcherTree.emptytree()
#         self.assertEqual(0, tree1.m)
#
#     def test_order(self):
#         tree1 = ButcherTree.emptytree()
#         self.assertEqual(0, tree1.order)
#
#     def test_density(self):
#         tree1 = ButcherTree.emptytree()
#         self.assertEqual(1, tree1.gamma)
#
#     def test_symmetry(self):
#         tree1 = ButcherTree.emptytree()
#         self.assertEqual(1, tree1.sigma)
#
#     def test_alpha(self):
#         tree1 = ButcherTree.emptytree()
#         self.assertEqual(1, tree1.alpha)
#
#     def test_elementary_differential(self):
#         tree1 = ButcherTree.emptytree()
#         self.assertEqual('y', tree1.F)

class first_order_tree(unittest.TestCase):
    # Does NOT test derivation, grafting and other operations.
    def test_initialisation(self):
        self.assertIsInstance(leaf, UnorderedTree)
        self.assertIsInstance(UnorderedTree(), UnorderedTree)

    def test_str(self):
        tree1 = leaf
        self.assertEqual('[]', str(tree1))
        self.assertEqual('b', tree1._planar_forest_str())
        tree2 = UnorderedTree()
        self.assertEqual(str(tree1), str(tree2))

    def test_equality(self):
        tree1 = leaf
        tree2 = UnorderedTree()
        self.assertEqual(tree1, tree2)

    def test_number_of_subtrees(self):
        tree1 = leaf
        self.assertEqual(0, tree1.number_of_children())

    def test_order(self):
        tree1 = leaf
        self.assertEqual(1, tree1.order())

    def test_density(self):
        tree1 = leaf
        self.assertEqual(1, tree1.density())

    def test_symmetry(self):
        tree1 = leaf
        self.assertEqual(1, tree1.symmetry())

    def test_alpha(self):
        tree1 = leaf
        self.assertEqual(1, tree1.alpha())

    def test_elementary_differential(self):
        tree1 = leaf
        self.assertEqual('f', tree1.F())

    def test_properties(self):
        tree1 = leaf
        self.assertTrue(tree1.is_binary())
        self.assertTrue(tree1.is_tall())
        self.assertTrue(tree1.is_bushy())


class Second_order_tree(unittest.TestCase):
    # Does NOT test derivation, grafting and other operations.
    def setUp(self):
        tree1 = leaf
        forest1 = Forest([tree1])
        self.tree = UnorderedTree(forest1)

    def test_initialisation(self):
        self.assertIsInstance(self.tree, UnorderedTree)

    def test_str(self):
        self.assertEqual('[[]]', str(self.tree))
        self.assertEqual('b[b]', self.tree._planar_forest_str())

    def test_equality(self):
        tree2 = leaf
        forest2 = Forest([tree2])
        tree3 = UnorderedTree(forest2)
        self.assertEqual(tree3, self.tree)
        tree4 = UnorderedTree('[[]]')
        self.assertEqual(tree4, self.tree)

    def test_number_of_subtrees(self):
        self.assertEqual(1, self.tree.number_of_children())

    def test_order(self):
        self.assertEqual(2, self.tree.order())

    def test_density(self):
        self.assertEqual(2, self.tree.density())

    def test_symmetry(self):
        self.assertEqual(1, self.tree.symmetry())

    def test_alpha(self):
        self.assertEqual(1, self.tree.alpha())

    def test_elementary_differential(self):
        self.assertEqual("f'f", self.tree.F())

    def test_properties(self):
        self.assertTrue(self.tree.is_binary())
        self.assertTrue(self.tree.is_tall())
        self.assertTrue(self.tree.is_bushy())


class Third_order_tree_no1(unittest.TestCase):
    # Does NOT test derivation, grafting and other operations.
    def setUp(self):
        tree1 = leaf
        forest1 = Forest([tree1, tree1])
        self.tree = UnorderedTree(forest1)

    def test_initialisation(self):
        self.assertIsInstance(self.tree, UnorderedTree)

    def test_str(self):
        self.assertEqual('[[],[]]', str(self.tree))
        self.assertEqual('b[b,b]', self.tree._planar_forest_str())

    def test_equality(self):
        tree2 = UnorderedTree(Forest())
        forest2 = Forest([tree2, tree2])
        tree3 = UnorderedTree(forest2)
        self.assertEqual(tree3, self.tree)
        tree4 = UnorderedTree('[[],[]]')
        self.assertEqual(tree4, self.tree)
        tree5 = UnorderedTree('[[[],[]]]')

    def test_number_of_subtrees(self):
        self.assertEqual(2, self.tree.number_of_children())

    def test_order(self):
        self.assertEqual(3, self.tree.order())

    def test_density(self):
        self.assertEqual(3, self.tree.density())

    def test_symmetry(self):
        self.assertEqual(2, self.tree.symmetry())

    def test_alpha(self):
        self.assertEqual(1, self.tree.alpha())

    def test_elementary_differential(self):
        self.assertEqual("f''(f,f)", self.tree.F())

    def test_properties(self):
        self.assertTrue(self.tree.is_binary())
        self.assertFalse(self.tree.is_tall())
        self.assertTrue(self.tree.is_bushy())
