import unittest

from pybs.trees import ButcherTree, ButcherEmptyTree
from pybs.combinations import Forest, LinearCombination
from pybs.combinations.linearCombination import make_rule
from pybs.series.Bseries import zero, exponential
from pybs.combinations import Forest, differentiate as D, graft, treeCommutator, split, treeGenerator
from pybs.series import hf_composition, modifiedEquation

from itertools import islice


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

    def test_modified(self):
        a = exponential
        c = modifiedEquation(a)
        n = 10
        computed = list(c(tree) for tree in islice(treeGenerator(), 0, n))
        expected = [0,1] + [0]*(n-2)
        self.assertEqual(computed, expected)

    def test_memoization(self):
        """
        Performing a split has an influence on the modified equation computation?
        """
        tmp = ButcherTree(Forest([ButcherTree.basetree()]))
        t = ButcherTree(Forest([tmp, ButcherTree.basetree()]))
        split(t)
        a = exponential
        c = modifiedEquation(a)

