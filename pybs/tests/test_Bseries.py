import unittest

from pybs.trees import ButcherTree, ButcherEmptyTree
from pybs.combinations import Forest, LinearCombination
from pybs.combinations.linearCombination import make_rule
from pybs.series.Bseries import zero


class simple_series(unittest.TestCase):
    def test_zero_series(self):
        rule1 = zero
        tree1 = ButcherTree.basetree()
        self.assertEqual(0, rule1(tree1))

    def test_sum_series(self):
        thesum = LinearCombination()
        thesum += ButcherTree.basetree()
        rule1 = make_rule(thesum)
        self.assertEqual(0, rule1(ButcherEmptyTree()))
        self.assertEqual(1, rule1(ButcherTree.basetree()))

    def test_RK_series(self):
        import pybs.rungekutta.methods
        rule1 = pybs.rungekutta.methods.RKeuler.phi
        self.assertEqual(1, rule1(ButcherEmptyTree()))
        self.assertEqual(1, rule1(ButcherTree.basetree()))
        tree2 = ButcherTree.basetree()
        forest2 = Forest([tree2])
        tree3 = ButcherTree(forest2)
        result = rule1(tree3)
        self.assertEqual(0, result)
