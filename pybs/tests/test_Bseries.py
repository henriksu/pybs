import unittest

from pybs.unordered_tree import UnorderedTree, leaf, tree_generator
from pybs.combinations import Forest, LinearCombination, empty_tree
from pybs.series.Bseries import zero, exponential, BseriesRule
from pybs.combinations import Forest, differentiate as D, graft, treeCommutator, split
from pybs.series import hf_composition, modified_equation, composition_ssa
from pybs.rungekutta.methods import RKeuler, RKimplicitEuler, RKimplicitMidpoint,\
    RKimplicitTrapezoidal, RKmidpoint, RKrunge1, RKrunge2, RK4, \
    RK38rule, RKlobattoIIIA4, RKlobattoIIIB4, RKcashKarp

from itertools import islice
from pybs.series.functions import equal_up_to_order, symplectic_up_to_order, hamiltonian_up_to_order


class simple_series(unittest.TestCase):
    def test_zero_series(self):
        rule1 = zero
        tree1 = leaf()
        self.assertEqual(0, rule1(tree1))

    def test_sum_series(self):
        thesum = LinearCombination()
        thesum += leaf()
        rule1 = BseriesRule(thesum)
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

    def test_symplectic(self):
        max_order = 7
        euler = RKeuler.phi()
        print "euler: ", symplectic_up_to_order(euler, max_order), " ", RKeuler.order
        impl_euler = RKimplicitEuler.phi()
        print "implicit euler: ", symplectic_up_to_order(impl_euler, max_order), " ", RKimplicitEuler.order
        midpoint = RKmidpoint.phi()
        print "midpoint: ", symplectic_up_to_order(midpoint, max_order), " ", RKmidpoint.order
        impl_midpoint = RKimplicitMidpoint.phi()
        print "implicit midpoint: ", symplectic_up_to_order(impl_midpoint, max_order), " ", RKimplicitMidpoint.order  # symplectic all the way? Yes
        impl_trap = RKimplicitTrapezoidal.phi()
        print "implicit trapezoidal: ", symplectic_up_to_order(impl_trap, max_order), " ", RKimplicitTrapezoidal.order
        runge1 = RKrunge1.phi()
        print "runge1: ", symplectic_up_to_order(runge1, max_order), " ", RKrunge1.order
        runge2 = RKrunge2.phi()
        print "runge2: ", symplectic_up_to_order(runge2, max_order), " ", RKrunge2.order
        rk4 = RK4.phi()
        print "RK4: ", symplectic_up_to_order(rk4, max_order), " ", RK4.order
        rk38 = RK38rule.phi()
        print "RK38rule: ", symplectic_up_to_order(rk38, max_order), " ", RK38rule.order
        lobattoIIIA4 = RKlobattoIIIA4.phi()
        print "lobattoIIIA4: ", symplectic_up_to_order(lobattoIIIA4, max_order), " ", RKlobattoIIIA4.order
        lobattoIIIB4 = RKlobattoIIIB4.phi()
        print "lobattoIIIB4: ", symplectic_up_to_order(lobattoIIIB4, max_order), " ", RKlobattoIIIB4.order
        cashKarp = RKcashKarp.phi()
        print "cashKarp: ", symplectic_up_to_order(cashKarp, max_order), " ", RKcashKarp.order
        # exponential
        print "exact: ", symplectic_up_to_order(exponential, max_order)
        self.assertTrue(False)

    def test_hamiltonian(self):
        max_order = 7
        euler = RKeuler.phi()
        print "euler: ", hamiltonian_up_to_order(euler, max_order), " ", RKeuler.order
        impl_euler = RKimplicitEuler.phi()
        print "implicit euler: ", hamiltonian_up_to_order(impl_euler, max_order), " ", RKimplicitEuler.order
        midpoint = RKmidpoint.phi()
        print "midpoint: ", hamiltonian_up_to_order(midpoint, max_order), " ", RKmidpoint.order
        impl_midpoint = RKimplicitMidpoint.phi()
        print "implicit midpoint: ", hamiltonian_up_to_order(impl_midpoint, max_order), " ", RKimplicitMidpoint.order  # hamiltonian all the way? Yes
        impl_trap = RKimplicitTrapezoidal.phi()
        print "implicit trapezoidal: ", hamiltonian_up_to_order(impl_trap, max_order), " ", RKimplicitTrapezoidal.order
        runge1 = RKrunge1.phi()
        print "runge1: ", hamiltonian_up_to_order(runge1, max_order), " ", RKrunge1.order
        runge2 = RKrunge2.phi()
        print "runge2: ", hamiltonian_up_to_order(runge2, max_order), " ", RKrunge2.order
        rk4 = RK4.phi()
        print "RK4: ", hamiltonian_up_to_order(rk4, max_order), " ", RK4.order
        rk38 = RK38rule.phi()
        print "RK38rule: ", hamiltonian_up_to_order(rk38, max_order), " ", RK38rule.order
        lobattoIIIA4 = RKlobattoIIIA4.phi()
        print "lobattoIIIA4: ", hamiltonian_up_to_order(lobattoIIIA4, max_order), " ", RKlobattoIIIA4.order
        lobattoIIIB4 = RKlobattoIIIB4.phi()
        print "lobattoIIIB4: ", hamiltonian_up_to_order(lobattoIIIB4, max_order), " ", RKlobattoIIIB4.order
        cashKarp = RKcashKarp.phi()
        print "cashKarp: ", hamiltonian_up_to_order(cashKarp, max_order), " ", RKcashKarp.order
        # exponential
        print "exact: ", hamiltonian_up_to_order(exponential, max_order)
        self.assertTrue(False)
