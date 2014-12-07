import unittest
import trees
from trees.ButcherTrees import ButcherTree, ButcherEmptyTree
from trees.functions import alpha, F, order, number_of_children, density, symmetry
from forest import Forest
from series.Bseries import BseriesRule
from forest.linearCombination import LinearCombination
from forest.differentiation import differentiate

class simple_series(unittest.TestCase):
    def test_zero_series(self):
        rule1 = BseriesRule()
        tree1 = ButcherTree.basetree()
        self.assertEqual(0, rule1(tree1))

    def test_sum_series(self):
        thesum = LinearCombination()
        thesum += ButcherTree.basetree()
        rule1 = BseriesRule(thesum)
        self.assertEqual(0, rule1(ButcherEmptyTree()))
        self.assertEqual(1, rule1(ButcherTree.basetree()))

    def test_RK_series(self):
        import rungekutta.methods
        rule1 = BseriesRule(rungekutta.methods.RKeuler.phi)
        self.assertEqual(1, rule1(trees.ButcherTrees.ButcherEmptyTree()))
        self.assertEqual(1, rule1(ButcherTree.basetree()))
        tree2 = ButcherTree.basetree()
        forest2 = Forest([tree2])
        tree3 = ButcherTree(forest2)
        result = rule1(tree3)
        self.assertEqual(0, result)
