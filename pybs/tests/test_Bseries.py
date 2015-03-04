import unittest

from pybs.unordered_tree import UnorderedTree, leaf, tree_generator
from pybs.combinations import Forest, LinearCombination, empty_tree
from pybs.series.Bseries import zero, exponential, unit, BseriesRule
from pybs.combinations import Forest, differentiate as D, graft, treeCommutator, split
from pybs.series import hf_composition, modified_equation, composition_ssa, inverse, adjoint
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
        self.assertEqual(symplectic_up_to_order(euler, max_order), 1)  # ==order
        impl_euler = RKimplicitEuler.phi()
        self.assertEqual(symplectic_up_to_order(impl_euler, max_order), 1)  # ==order
        midpoint = RKmidpoint.phi()
        self.assertEqual(symplectic_up_to_order(midpoint, max_order), 2)  # ==order
        impl_midpoint = RKimplicitMidpoint.phi()
        self.assertEqual(symplectic_up_to_order(impl_midpoint, max_order), max_order)  # hamiltonian
        impl_trap = RKimplicitTrapezoidal.phi()
        self.assertEqual(symplectic_up_to_order(impl_trap, max_order), 2)  # ==order
        runge1 = RKrunge1.phi()
        self.assertEqual(symplectic_up_to_order(runge1, max_order), 3)  # == order + 1
        runge2 = RKrunge2.phi()
        self.assertEqual(symplectic_up_to_order(runge2, max_order), 2)  # ==order
        rk4 = RK4.phi()
        self.assertEqual(symplectic_up_to_order(rk4, max_order), 4)  # ==order
        rk38 = RK38rule.phi()
        self.assertEqual(symplectic_up_to_order(rk38, max_order), 4)  # ==order
        lobattoIIIA4 = RKlobattoIIIA4.phi()
        self.assertEqual(symplectic_up_to_order(lobattoIIIA4, max_order), 4)  # ==order
        lobattoIIIB4 = RKlobattoIIIB4.phi()
        self.assertEqual(symplectic_up_to_order(lobattoIIIB4, max_order), 4)  # ==order
        cashKarp = RKcashKarp.phi()
        self.assertEqual(symplectic_up_to_order(cashKarp, max_order), 5)  # ==order
        # exponential
        self.assertEqual(symplectic_up_to_order(exponential, max_order), max_order)  # hamiltonian

    @unittest.skip
    def test_hamiltonian(self):
        max_order = 7
        euler = RKeuler.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(euler), max_order), 1)  # ==order
        impl_euler = RKimplicitEuler.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(impl_euler), max_order), 1)  # ==order
        midpoint = RKmidpoint.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(midpoint), max_order), 2)  # ==order
        impl_midpoint = RKimplicitMidpoint.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(impl_midpoint), max_order), max_order)  # hamiltonian
        impl_trap = RKimplicitTrapezoidal.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(impl_trap), max_order), 2)  # ==order
        runge1 = RKrunge1.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(runge1), max_order), 3)  # == order + 1
        runge2 = RKrunge2.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(runge2), max_order), 2)  # ==order
        rk4 = RK4.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(rk4), max_order), 4)  # ==order
        rk38 = RK38rule.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(rk38), max_order), 4)  # ==order
        lobattoIIIA4 = RKlobattoIIIA4.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(lobattoIIIA4), max_order), 4)  # ==order
        lobattoIIIB4 = RKlobattoIIIB4.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(lobattoIIIB4), max_order), 4)  # ==order
        cashKarp = RKcashKarp.phi()
        self.assertEqual(hamiltonian_up_to_order(modified_equation(cashKarp), max_order), 5)  # ==order
        # exponential
        self.assertEqual(hamiltonian_up_to_order(modified_equation(exponential), max_order), max_order)  # hamiltonian


class inverse_series(unittest.TestCase):
    def setUp(self):
        self.max_order = 5

    def test_exact(self):
        a = exponential
        b = inverse(a)
        c = composition_ssa(a, b)
        result = equal_up_to_order(c, unit, self.max_order)
        self.assertEqual(result, self.max_order)
        c = composition_ssa(b, a)
        result = equal_up_to_order(c, unit, self.max_order)
        self.assertEqual(result, self.max_order)

    def test_explicit_euler(self):
        a = RKeuler.phi()
        b = inverse(a)
        c = composition_ssa(a, b)
        result = equal_up_to_order(c, unit, self.max_order)
        self.assertEqual(result, self.max_order)
        c = composition_ssa(b, a)
        result = equal_up_to_order(c, unit, self.max_order)
        self.assertEqual(result, self.max_order)

    def test_cash_karp(self):
        a = RKcashKarp.phi()
        b = inverse(a)
        c = composition_ssa(a, b)
        result = equal_up_to_order(c, unit, self.max_order)
        self.assertEqual(result, self.max_order)
        c = composition_ssa(b, a)
        result = equal_up_to_order(c, unit, self.max_order)
        self.assertEqual(result, self.max_order)


class adjoint_series(unittest.TestCase):
    def setUp(self):
        self.max_order = 5

    def test_exact(self):
        # symmetric
        a = exponential
        b = adjoint(a)
        result = equal_up_to_order(a, b, self.max_order)
        self.assertEqual(result, self.max_order)

    def test_implicit_midpoint(self):
        # symmetric
        a = RKimplicitMidpoint.phi()
        b = adjoint(a)
        result = equal_up_to_order(a, b, self.max_order)
        self.assertEqual(result, self.max_order)

    def test_lobattoA(self):
        # symmetric
        a = RKlobattoIIIA4.phi()
        b = adjoint(a)
        result = equal_up_to_order(a, b, self.max_order)
        self.assertEqual(result, self.max_order)

    def test_lobattoB(self):
        # symmetric
        a = RKlobattoIIIB4.phi()
        b = adjoint(a)
        result = equal_up_to_order(a, b, self.max_order)
        self.assertEqual(result, self.max_order)

    def test_explicit_euler(self):
        a = RKeuler.phi()
        b = adjoint(a)
        result = equal_up_to_order(b, RKimplicitEuler.phi(), self.max_order)
        self.assertEqual(result, self.max_order)

    def test_implicit_euler(self):
        a = RKimplicitEuler.phi()
        b = adjoint(a)
        result = equal_up_to_order(b, RKeuler.phi(), self.max_order)
        self.assertEqual(result, self.max_order)
