# This Python file uses the following encoding: utf-8
import unittest
from forest import Forest
from trees.LabeledTrees.ColouredTrees.BiColouredTrees import \
    BiColouredTree, black, white, BiColouredNotTree


class empty_tree(unittest.TestCase):
    #Does NOT test derivation, grafting and other operations.
    def test_initialisation(self):
        self.assertIsInstance(BiColouredTree(black), BiColouredTree)
        self.assertIsInstance(BiColouredTree(white), BiColouredTree)

    def test_str(self):
        tree_b = BiColouredTree.emptytree(black)
        self.assertEqual('Øy', str(tree_b))
        tree_w = BiColouredTree.emptytree(white)
        self.assertEqual('Øz', str(tree_w))

    def test_equality(self):
        tree1 = BiColouredTree.emptytree(black)
        tree2 = BiColouredNotTree(colour=black)
        self.assertEqual(tree1, tree2)
        tree1 = BiColouredTree.emptytree(white)
        tree2 = BiColouredNotTree(colour=white)
        self.assertEqual(tree1, tree2)

    def test_number_of_subtrees(self):
        tree1 = BiColouredTree.emptytree(black)
        self.assertEqual(0, tree1.m)
        self.assertEqual(0, tree1.m_black)
        self.assertEqual(0, tree1.m_white)
        
    def test_order(self):
        tree1 = BiColouredTree.emptytree(black)
        self.assertEqual(0, tree1.order)
        tree1 = BiColouredTree.emptytree(white)
        self.assertEqual(0, tree1.order)

    def test_density(self): #  TODO: Verify mathematically that these defaults are meaningful.
        tree1 = BiColouredTree.emptytree(black)
        self.assertEqual(1, tree1.gamma)
        tree1 = BiColouredTree.emptytree(white)
        self.assertEqual(1, tree1.gamma)

    def test_symmetry(self): #  TODO: Verify mathematically that these defaults are meaningful.
        tree1 = BiColouredTree.emptytree(black)
        self.assertEqual(1, tree1.sigma)
        tree1 = BiColouredTree.emptytree(white)
        self.assertEqual(1, tree1.sigma)

    def test_alpha(self):
        pass #  TODO: Implement alpha

    def test_elementary_differential(self):
        tree1 = BiColouredTree.emptytree(black)
        self.assertEqual('y', tree1.F)
        tree1 = BiColouredTree.emptytree(white)
        self.assertEqual('z', tree1.F)

class first_order_tree(unittest.TestCase):
#Does NOT test derivation, grafting and other operations.

    def test_initialisation(self):
        self.assertIsInstance(BiColouredTree(black, Forest()), BiColouredTree)
        self.assertIsInstance(BiColouredTree(white, Forest()), BiColouredTree)
    
    def test_str(self):
        tree1 = BiColouredTree.basetree(black)
        self.assertEqual('*', str(tree1))
        tree1 = BiColouredTree.basetree(white)
        self.assertEqual('o', str(tree1))

    def test_equality(self):
        tree1 = BiColouredTree.basetree(black)
        tree2 = BiColouredTree(black, Forest())
        self.assertEqual(tree1, tree2)
        tree1 = BiColouredTree.basetree(white)
        tree2 = BiColouredTree(white, Forest())
        self.assertEqual(tree1, tree2)

    def test_number_of_subtrees(self):
        tree1 = BiColouredTree.basetree(black)
        self.assertEqual(0, tree1.m)
        self.assertEqual(0, tree1.m_black)
        self.assertEqual(0, tree1.m_white)
        tree1 = BiColouredTree.basetree(white)
        self.assertEqual(0, tree1.m)
        self.assertEqual(0, tree1.m_black)
        self.assertEqual(0, tree1.m_white)

    def test_order(self):
        tree1 = BiColouredTree.basetree(black)
        self.assertEqual(1, tree1.order)
        tree1 = BiColouredTree.basetree(white)
        self.assertEqual(1, tree1.order)

    def test_density(self):
        tree1 = BiColouredTree.basetree(black)
        self.assertEqual(1, tree1.gamma)
        tree1 = BiColouredTree.basetree(white)
        self.assertEqual(1, tree1.gamma)

    def test_symmetry(self):
        tree1 = BiColouredTree.basetree(black)
        self.assertEqual(1, tree1.sigma)
        tree1 = BiColouredTree.basetree(white)
        self.assertEqual(1, tree1.sigma)

    def test_alpha(self):
        pass #  TODO: Implement

    def test_elementary_differential(self):
        tree1 = BiColouredTree.basetree(black)
        self.assertEqual('f', tree1.F)
        tree1 = BiColouredTree.basetree(white)
        self.assertEqual('g', tree1.F)


class Second_order_tree(unittest.TestCase):
#Does NOT test derivation, grafting and other operations.
    def setUp(self):
        tmp_b = BiColouredTree.basetree(black)
        tmp_w = BiColouredTree.basetree(white)
        forest_b = Forest([tmp_b])
        forest_w = Forest([tmp_w])
        self.tree1 = BiColouredTree(black, forest_b)
        self.tree2 = BiColouredTree(black, forest_w)
        self.tree3 = BiColouredTree(white, forest_b)
        self.tree4 = BiColouredTree(white, forest_w)

    def test_initialisation(self):
        self.assertIsInstance(self.tree1, BiColouredTree)
        self.assertIsInstance(self.tree2, BiColouredTree)
        self.assertIsInstance(self.tree3, BiColouredTree)
        self.assertIsInstance(self.tree4, BiColouredTree)

    def test_str(self):
        self.assertEqual('[*]y', str(self.tree1))
        self.assertEqual('[o]y', str(self.tree2))
        self.assertEqual('[*]z', str(self.tree3))
        self.assertEqual('[o]z', str(self.tree4))

    #def test_equality(self): #  Not implemented.
    def test_number_of_subtrees(self):
        self.assertEqual(1, self.tree1.m)
        self.assertEqual(1, self.tree1.m_black)
        self.assertEqual(0, self.tree1.m_white)
        self.assertEqual(1, self.tree2.m)
        self.assertEqual(0, self.tree2.m_black)
        self.assertEqual(1, self.tree2.m_white)
        self.assertEqual(1, self.tree3.m)
        self.assertEqual(1, self.tree3.m_black)
        self.assertEqual(0, self.tree3.m_white)
        self.assertEqual(1, self.tree4.m)
        self.assertEqual(0, self.tree4.m_black)
        self.assertEqual(1, self.tree4.m_white)

    def test_order(self):
        self.assertEqual(2, self.tree1.order)
        self.assertEqual(2, self.tree2.order)
        self.assertEqual(2, self.tree3.order)
        self.assertEqual(2, self.tree4.order)

    def test_density(self):
        self.assertEqual(2, self.tree1.gamma)
        self.assertEqual(2, self.tree2.gamma)
        self.assertEqual(2, self.tree3.gamma)
        self.assertEqual(2, self.tree4.gamma)

    def test_symmetry(self):
        self.assertEqual(1, self.tree1.sigma)
        self.assertEqual(1, self.tree2.sigma)
        self.assertEqual(1, self.tree3.sigma)
        self.assertEqual(1, self.tree4.sigma)

    def test_alpha(self):
        pass #  TODO: Implement

    def test_elementary_differential(self):
        self.assertEqual("f_yf", self.tree1.F)
        self.assertEqual("f_zg", self.tree2.F)
        self.assertEqual("g_yf", self.tree3.F)
        self.assertEqual("g_zg", self.tree4.F)


class Third_order_tree_no1(unittest.TestCase):
#Does NOT test derivation, grafting and other operations.
    def setUp(self):
        tree1 = BiColouredTree.basetree(black)
        forest1 = Forest([tree1, tree1])
        self.tree = BiColouredTree(white, forest1)
