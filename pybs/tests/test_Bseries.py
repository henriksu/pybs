import unittest

from pybs.unordered_tree import UnorderedTree, leaf, tree_generator
from pybs.combinations import Forest, LinearCombination, empty_tree
from pybs.combinations.linearCombination import make_rule
from pybs.series.Bseries import zero, exponential
from pybs.combinations import Forest, differentiate as D, graft, treeCommutator, split
from pybs.series import hf_composition, modified_equation, composition_ssa
from pybs.rungekutta.methods import RKeuler, RKimplicitEuler, RKimplicitMidpoint,\
    RKimplicitTrapezoidal

from itertools import islice
from pybs.series.functions import equal_up_to_order


class simple_series(unittest.TestCase):
    def test_zero_series(self):
        rule1 = zero
        tree1 = leaf()
        self.assertEqual(0, rule1(tree1))

    def test_sum_series(self):
        thesum = LinearCombination()
        thesum += leaf()
        rule1 = make_rule(thesum)
        self.assertEqual(0, rule1(empty_tree()))
        self.assertEqual(1, rule1(leaf()))

    def test_RK_series(self):
        import pybs.rungekutta.methods
        rule1 = pybs.rungekutta.methods.RKeuler.phi()
        self.assertEqual(1, rule1(empty_tree()))
        self.assertEqual(1, rule1(leaf()))
        tree2 = leaf()
        forest2 = Forest([tree2])
        tree3 = UnorderedTree(forest2)
        result = rule1(tree3)
        self.assertEqual(0, result)

    def test_modified(self):
        a = exponential
        c = modified_equation(a)
        n = 10
        self.assertEqual(c(empty_tree()), 0)
        computed = list(c(tree) for tree in islice(tree_generator(), 0, n))
        expected = [1] + [0]*(n-1)
        self.assertEqual(computed, expected)

    def test_composition(self):
        "It is known that the explicit and implicit Euler methods are adjoint.\
        Furthermore, the composition implicit o explicit = trapezoidal,\
        and explicit o implicit = implicit midpoint.\
        This verifies the coproduct."
        max_order = 5
        explicit_euler = RKeuler.phi()
        implicit_euler = RKimplicitEuler.phi()
        implicit_midpoint = RKimplicitMidpoint.phi()
        implicit_trapezoidal = RKimplicitTrapezoidal.phi()
        result1 = composition_ssa(explicit_euler, implicit_euler)
        tmp = equal_up_to_order(result1, implicit_trapezoidal, max_order)
        self.assertEqual(tmp, max_order)
        result2 = composition_ssa(implicit_euler, explicit_euler)
        tmp = equal_up_to_order(result2, implicit_midpoint, max_order)
        self.assertEqual(tmp, max_order)

    def test_memoization(self):
        """
        Performing a split has an influence on the modified equation computation?
        """
        tmp = UnorderedTree(Forest([leaf()]))
        t = UnorderedTree(Forest([tmp, leaf()]))
        split(t)
        a = exponential
        c = modified_equation(a)

