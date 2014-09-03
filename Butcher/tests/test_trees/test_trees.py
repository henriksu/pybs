# This Python file uses the following encoding: utf-8
import unittest
from forest import Forest
from trees.ButcherTrees import ButcherTree, ButcherNotTree


class empty_tree(unittest.TestCase):
#Does NOT test derivation, grafting and other operations.
    def test_initialisation(self):
        self.assertIsInstance(ButcherTree(), ButcherTree)

    def test_str(self):
        tree1 = ButcherTree.emptytree()
        self.assertEqual('Ø', str(tree1))

    def test_equality(self):
        tree1 = ButcherTree.emptytree()
        tree2 = ButcherNotTree()
        self.assertEqual(tree1, tree2)

    def test_number_of_subtrees(self):
        tree1 = ButcherTree.emptytree()
        self.assertEqual(0, tree1.m)

    def test_order(self):
        tree1 = ButcherTree.emptytree()
        self.assertEqual(0, tree1.order)

    def test_density(self):
        tree1 = ButcherTree.emptytree()
        self.assertEqual(1, tree1.gamma)

    def test_symmetry(self):
        tree1 = ButcherTree.emptytree()
        self.assertEqual(1, tree1.sigma)

    def test_alpha(self):
        tree1 = ButcherTree.emptytree()
        self.assertEqual(1, tree1.alpha)

    def test_elementary_differential(self):
        tree1 = ButcherTree.emptytree()
        self.assertEqual('y', tree1.F)

class first_order_tree(unittest.TestCase):
#Does NOT test derivation, grafting and other operations.

    def test_initialisation(self):
        self.assertIsInstance(ButcherTree(Forest()), ButcherTree)
    
    def test_str(self):
        tree1 = ButcherTree.basetree()
        self.assertEqual('*', str(tree1))

    def test_equality(self):
        tree1 = ButcherTree.basetree()
        tree2 = ButcherTree()
        self.assertEqual(tree1, tree2)

    def test_number_of_subtrees(self):
        tree1 = ButcherTree.basetree()
        self.assertEqual(0, tree1.m)

    def test_order(self):
        tree1 = ButcherTree.basetree()
        self.assertEqual(1, tree1.order)

    def test_density(self):
        tree1 = ButcherTree.basetree()
        self.assertEqual(1, tree1.gamma)

    def test_symmetry(self):
        tree1 = ButcherTree.basetree()
        self.assertEqual(1, tree1.sigma)

    def test_alpha(self):
        tree1 = ButcherTree.basetree()
        self.assertEqual(1, tree1.alpha)

    def test_elementary_differential(self):
        tree1 = ButcherTree.basetree()
        self.assertEqual('f', tree1.F)


class Second_order_tree(unittest.TestCase):
#Does NOT test derivation, grafting and other operations.
    def setUp(self):
        tree1 = ButcherTree.basetree()
        forest1 = Forest([tree1])
        self.tree = ButcherTree(forest1)

    def test_initialisation(self):
        self.assertIsInstance(self.tree, ButcherTree)
    
    def test_str(self):
        self.assertEqual('[*]', str(self.tree))

    def test_equality(self):
        tree2 = ButcherTree.basetree()
        forest2 = Forest([tree2])
        tree3 = ButcherTree(forest2)
        self.assertEqual(tree3, self.tree)

    def test_number_of_subtrees(self):
        self.assertEqual(1, self.tree.m)

    def test_order(self):
        self.assertEqual(2, self.tree.order)

    def test_density(self):
        self.assertEqual(2, self.tree.gamma)

    def test_symmetry(self):
        self.assertEqual(1, self.tree.sigma)

    def test_alpha(self):
        self.assertEqual(1, self.tree.alpha)

    def test_elementary_differential(self):
        self.assertEqual("f'f", self.tree.F)


class Third_order_tree_no1(unittest.TestCase):
#Does NOT test derivation, grafting and other operations.
    def setUp(self):
        tree1 = ButcherTree.basetree()
        forest1 = Forest([tree1, tree1])
        self.tree = ButcherTree(forest1)

    def test_initialisation(self):
        self.assertIsInstance(self.tree, ButcherTree)
    
    def test_str(self):
        self.assertEqual('[*,*]', str(self.tree))

    def test_equality(self):
        tree2 = ButcherTree(Forest())
        forest2 = Forest([tree2, tree2])
        tree3 = ButcherTree(forest2)
        self.assertEqual(tree3, self.tree)

    def test_number_of_subtrees(self):
        self.assertEqual(2, self.tree.m)

    def test_order(self):
        self.assertEqual(3, self.tree.order)

    def test_density(self):
        self.assertEqual(3, self.tree.gamma)

    def test_symmetry(self):
        self.assertEqual(2, self.tree.sigma)

    def test_alpha(self):
        self.assertEqual(1, self.tree.alpha)

    def test_elementary_differential(self):
        self.assertEqual("f''(f,f)", self.tree.F)
