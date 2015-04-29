from fractions import Fraction
from itertools import islice
import unittest

from pybs.utils import LinearCombination
from pybs.unordered_tree import \
    UnorderedTree, \
    leaf, \
    number_of_tree_pairs_of_total_order as m, \
    tree_generator
from pybs.combinations import \
    Forest, \
    empty_tree, \
    split
from pybs.series import \
    BseriesRule, \
    modified_equation, \
    composition_ssa, \
    inverse, \
    adjoint, \
    stepsize_adjustment, \
    conjugate,\
    conjugate_by_commutator, \
    exp, \
    log, \
\
    equal_up_to_order, \
    convergence_order, \
    symmetric_up_to_order, \
    symplectic_up_to_order, \
    conjugate_to_symplectic, \
    energy_preserving_upto_order, \
    hamiltonian_up_to_order, \
    new_hamiltonian_up_to_order, \
\
    zero, \
    exponential, \
    unit, \
    _kahan, \
    unit_field, \
    AVF
from pybs.series.checks import \
    tree_pairs_of_order, \
    _conjugate_symplecticity_matrix

from pybs.rungekutta.methods import \
    RKeuler, \
    RKimplicitEuler, \
    RKimplicitMidpoint,\
    RKimplicitTrapezoidal, \
    RKmidpoint, \
    RKrunge1, \
    RKrunge2, \
    RK4, \
    RK38rule, \
    RKlobattoIIIA4, \
    RKlobattoIIIB4, \
    RKcashKarp


class simple_series(unittest.TestCase):
    def test_zero_series(self):
        rule1 = zero
        tree1 = leaf
        self.assertEqual(0, rule1(tree1))

    def test_sum_series(self):
        thesum = LinearCombination()
        thesum += leaf
        rule1 = BseriesRule(thesum)
        self.assertEqual(0, rule1(empty_tree))
        self.assertEqual(1, rule1(leaf))

    def test_RK_series(self):
        import pybs.rungekutta.methods
        rule1 = pybs.rungekutta.methods.RKeuler.phi()
        self.assertEqual(1, rule1(empty_tree))
        self.assertEqual(1, rule1(leaf))
        tree2 = leaf
        forest2 = Forest([tree2])
        tree3 = UnorderedTree(forest2)
        result = rule1(tree3)
        self.assertEqual(0, result)

    def test_modified(self):
        a = exponential
        c = modified_equation(a)
        n = 10
        self.assertEqual(c(empty_tree), 0)
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
        Performing a split has an influence on
        the modified equation computation?
        """
        tmp = UnorderedTree(Forest([leaf]))
        t = UnorderedTree(Forest([tmp, leaf]))
        split(t)
        a = exponential
        c = modified_equation(a)
        c

    def test_symplectic(self):
        max_order = 7
        euler = RKeuler.phi()
        self.assertEqual(symplectic_up_to_order(
            euler, max_order), 1)
        # ==order
        impl_euler = RKimplicitEuler.phi()
        self.assertEqual(symplectic_up_to_order(
            impl_euler, max_order), 1)
        # ==order
        midpoint = RKmidpoint.phi()
        self.assertEqual(symplectic_up_to_order(
            midpoint, max_order), 2)
        # ==order
        impl_midpoint = RKimplicitMidpoint.phi()
        self.assertEqual(symplectic_up_to_order(
            impl_midpoint, max_order), max_order)
        # hamiltonian
        impl_trap = RKimplicitTrapezoidal.phi()
        self.assertEqual(symplectic_up_to_order(
            impl_trap, max_order), 2)
        # ==order
        runge1 = RKrunge1.phi()
        self.assertEqual(symplectic_up_to_order(
            runge1, max_order), 3)
        # == order + 1
        runge2 = RKrunge2.phi()
        self.assertEqual(symplectic_up_to_order(
            runge2, max_order), 2)
        # ==order
        rk4 = RK4.phi()
        self.assertEqual(symplectic_up_to_order(
            rk4, max_order), 4)
        # ==order
        rk38 = RK38rule.phi()
        self.assertEqual(symplectic_up_to_order(
            rk38, max_order), 4)
        # ==order
        lobattoIIIA4 = RKlobattoIIIA4.phi()
        self.assertEqual(symplectic_up_to_order(
            lobattoIIIA4, max_order), 4)
        # ==order
        lobattoIIIB4 = RKlobattoIIIB4.phi()
        self.assertEqual(symplectic_up_to_order(
            lobattoIIIB4, max_order), 4)
        # ==order
        cashKarp = RKcashKarp.phi()
        self.assertEqual(symplectic_up_to_order(
            cashKarp, max_order), 5)
        # ==order
        # exponential
        self.assertEqual(symplectic_up_to_order(
            exponential, max_order), max_order)
        # hamiltonian

    @unittest.skip
    def test_hamiltonian(self):
        max_order = 7
        euler = RKeuler.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(euler), max_order), 1)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(euler), max_order), 1)  # ==order
        impl_euler = RKimplicitEuler.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(impl_euler), max_order), 1)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(impl_euler), max_order), 1)  # ==order
        midpoint = RKmidpoint.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(midpoint), max_order), 2)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(midpoint), max_order), 2)  # ==order
        impl_midpoint = RKimplicitMidpoint.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(impl_midpoint), max_order), max_order)
        # hamiltonian
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(impl_midpoint), max_order), max_order)
        # hamiltonian
        impl_trap = RKimplicitTrapezoidal.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(impl_trap), max_order), 2)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(impl_trap), max_order), 2)  # ==order
        runge2 = RKrunge2.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(runge2), max_order), 2)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(runge2), max_order), 2)  # ==order
        runge1 = RKrunge1.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(runge1), max_order), 3)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(runge1), max_order), 3)  # ==order
        rk4 = RK4.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(rk4), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(rk4), max_order), 4)  # ==order
        rk38 = RK38rule.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(rk38), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(rk38), max_order), 4)  # ==order
        lobattoIIIA4 = RKlobattoIIIA4.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(lobattoIIIA4), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(lobattoIIIA4), max_order), 4)  # ==order
        lobattoIIIB4 = RKlobattoIIIB4.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(lobattoIIIB4), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(lobattoIIIB4), max_order), 4)  # ==order
        cashKarp = RKcashKarp.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(cashKarp), max_order), 5)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(cashKarp), max_order), 5)  # ==order
        # exponential
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(exponential), max_order), max_order)
        # hamiltonian
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(exponential), max_order), max_order)
        # hamiltonian
        runge1 = RKrunge1.phi()
        self.assertEqual(hamiltonian_up_to_order(
            modified_equation(runge1), max_order), 3)  # == order + 1
        self.assertEqual(new_hamiltonian_up_to_order(
            modified_equation(runge1), max_order), 3)  # == order + 1

#    @unittest.skip
    def test_hamiltonian_2(self):
        max_order = 7
        euler = RKeuler.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(euler), max_order), 1)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(euler), max_order), 1)  # ==order
        impl_euler = RKimplicitEuler.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(impl_euler), max_order), 1)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(impl_euler), max_order), 1)  # ==order
        midpoint = RKmidpoint.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(midpoint), max_order), 2)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(midpoint), max_order), 2)  # ==order
        impl_midpoint = RKimplicitMidpoint.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(impl_midpoint), max_order), max_order)
        # hamiltonian
        self.assertEqual(new_hamiltonian_up_to_order(
            log(impl_midpoint), max_order), max_order)
        # hamiltonian
        impl_trap = RKimplicitTrapezoidal.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(impl_trap), max_order), 2)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(impl_trap), max_order), 2)  # ==order
        runge2 = RKrunge2.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(runge2), max_order), 2)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(runge2), max_order), 2)  # ==order
        runge1 = RKrunge1.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(runge1), max_order), 3)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(runge1), max_order), 3)  # ==order
        rk4 = RK4.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(rk4), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(rk4), max_order), 4)  # ==order
        rk38 = RK38rule.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(rk38), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(rk38), max_order), 4)  # ==order
        lobattoIIIA4 = RKlobattoIIIA4.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(lobattoIIIA4), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(lobattoIIIA4), max_order), 4)  # ==order
        lobattoIIIB4 = RKlobattoIIIB4.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(lobattoIIIB4), max_order), 4)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(lobattoIIIB4), max_order), 4)  # ==order
        cashKarp = RKcashKarp.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(cashKarp), max_order), 5)  # ==order
        self.assertEqual(new_hamiltonian_up_to_order(
            log(cashKarp), max_order), 5)  # ==order
        # exponential
        self.assertEqual(hamiltonian_up_to_order(
            log(exponential), max_order), max_order)
        # hamiltonian
        self.assertEqual(new_hamiltonian_up_to_order(
            log(exponential), max_order), max_order)
        # hamiltonian
        runge1 = RKrunge1.phi()
        self.assertEqual(hamiltonian_up_to_order(
            log(runge1), max_order), 3)  # == order + 1
        self.assertEqual(new_hamiltonian_up_to_order(
            log(runge1), max_order), 3)  # == order + 1


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


class test_conjugate_to_symplectic(unittest.TestCase):
    def test_pairs(self):
        result = len(tree_pairs_of_order(0))
        expected = m(0)
        self.assertEqual(expected, result)
        result = len(tree_pairs_of_order(1))
        expected = m(1)
        self.assertEqual(expected, result)
        result = len(tree_pairs_of_order(2))
        expected = m(2)
        self.assertEqual(expected, result)
        result = len(tree_pairs_of_order(3))
        expected = m(3)
        self.assertEqual(expected, result)
        result = len(tree_pairs_of_order(4))
        expected = m(4)
        self.assertEqual(expected, result)
        result = len(tree_pairs_of_order(5))
        expected = m(5)
        self.assertEqual(expected, result)
        result = len(tree_pairs_of_order(6))
        expected = m(6)
        self.assertEqual(expected, result)
#         result = len(tree_pairs_of_order(7))
#         expected = m(7)
#         self.assertEqual(expected, result)
#         result = len(tree_pairs_of_order(8))
#         expected = m(8)
#         self.assertEqual(expected, result)
#         result = len(tree_pairs_of_order(9))
#         expected = m(9)
#         self.assertEqual(expected, result)
#         result = len(tree_pairs_of_order(10))
#         expected = m(10)
#         self.assertEqual(expected, result)
#         result = len(tree_pairs_of_order(11))
#         expected = m(11)
#         self.assertEqual(expected, result)
#         result = len(tree_pairs_of_order(12))
#         expected = m(12)
#         self.assertEqual(expected, result)

    def test_matrix(self):
        A = _conjugate_symplecticity_matrix(0)
        self.assertEqual(0, len(A))

        A = _conjugate_symplecticity_matrix(1)
        self.assertEqual(0, len(A))

        A = _conjugate_symplecticity_matrix(2)
        self.assertEqual(1, len(A))
        self.assertEqual(0, len(A[0]))

        A = _conjugate_symplecticity_matrix(3)
        self.assertEqual(1, len(A))
        self.assertEqual(1, len(A[0]))

        A = _conjugate_symplecticity_matrix(4)
        self.assertEqual(3, len(A))
        self.assertEqual(1, len(A[0]))

        A = _conjugate_symplecticity_matrix(5)
        self.assertEqual(6, len(A))
        self.assertEqual(3, len(A[0]))

        A = _conjugate_symplecticity_matrix(6)
        self.assertEqual(16, len(A))
        self.assertEqual(6, len(A[0]))

        A = _conjugate_symplecticity_matrix(7)
        self.assertEqual(37, len(A))
        self.assertEqual(16, len(A[0]))

    def test_it(self):
        method = RKimplicitMidpoint.phi()
        result = conjugate_to_symplectic(method)
        self.assertEqual(4, result)

        method = RKlobattoIIIA4.phi()
        result = conjugate_to_symplectic(method)
        self.assertEqual(6, result)

        method = RKlobattoIIIB4.phi()
        result = conjugate_to_symplectic(method)
        self.assertEqual(4, result)

        method = BseriesRule(_kahan, quadratic_vectorfield=True)
        # TODO: Treat quadratic f more professionally!
        result = conjugate_to_symplectic(method)
        self.assertEqual(4, result)


class test_modified_(unittest.TestCase):
    def test(self):
        modified = modified_equation(exponential)
        result = equal_up_to_order(modified, unit_field, 8)
        self.assertEqual(8, result)


class test_exp_log(unittest.TestCase):
    def setUp(self):
        self.max_order = 5

    def test_log_explicit_euler(self):
        a = RKeuler.phi()
        alpha_1 = modified_equation(a)
        alpha_2 = log(a)
        result = equal_up_to_order(alpha_1, alpha_2, self.max_order)
        self.assertEqual(self.max_order, result)

    def test_exp_explicit_euler(self):
        a = RKeuler.phi()
        alpha_1 = log(a)
        a_1 = exp(alpha_1)
        result = equal_up_to_order(a, a_1, self.max_order)
        self.assertEqual(self.max_order, result)

        alpha_2 = modified_equation(a)
        result = equal_up_to_order(alpha_1, alpha_2, self.max_order)
        self.assertEqual(self.max_order, result)

        a_2 = exp(alpha_2)
        result = equal_up_to_order(a, a_2, self.max_order)
        self.assertEqual(self.max_order, result)


class test_energy_preserving_up_to_order(unittest.TestCase):
    def test_exact(self):
        max_order = 5
        a = exponential
        b = modified_equation(a)
        result = energy_preserving_upto_order(b, max_order)
        self.assertEqual(max_order, result)

    def test_forward_euler(self):
        a = RKeuler.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(1, result)  # = order

    def test_implicit_euler(self):
        a = RKimplicitEuler.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(1, result)  # = order

    def test_midpoint(self):
        a = RKmidpoint.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(2, result)  # = order

    def test_implicit_midpoint(self):
        a = RKimplicitMidpoint.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(2, result)  # = order

    def test_implicit_trapezoidal(self):
        a = RKimplicitTrapezoidal.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(2, result)  # = order

    def test_runge1(self):
        a = RKrunge1.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(2, result)  # = order

    def test_runge2(self):
        a = RKrunge2.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(2, result)  # = order

    def test_rk4(self):
        a = RK4.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(4, result)  # = order

    def test_rk38(self):
        a = RK38rule.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(4, result)  # = order

    def test_RKlobattoIIIA4(self):
        a = RKlobattoIIIA4.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(4, result)  # = order

    def test_RKlobattoIIIB4(self):
        a = RKlobattoIIIB4.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(4, result)  # = order

    def test_RKcashKarp(self):
        a = RKcashKarp.phi()
        b = modified_equation(a)
        result = energy_preserving_upto_order(b)
        self.assertEqual(5, result)  # = order

    def test_avf(self):
        max_order = 5
        a = AVF
        b = modified_equation(a)
        result1 = convergence_order(a)
        self.assertEqual(2, result1)
        result2 = symplectic_up_to_order(a)
        self.assertEqual(2, result2)
        result3 = conjugate_to_symplectic(a)
        self.assertEqual(4, result3)
        result4 = symmetric_up_to_order(a, max_order)
        self.assertEqual(max_order, result4)
        result5 = energy_preserving_upto_order(b, max_order)
        self.assertEqual(max_order, result5)  # = energy preserving


class test_conjugate(unittest.TestCase):
    def test_no_1(self):
        max_order = 5
        trapezoidal = RKimplicitTrapezoidal.phi()
        imp_midpoint = RKimplicitMidpoint.phi()
        half_imp_euler = stepsize_adjustment(RKimplicitEuler.phi(),
                                             Fraction(1, 2))
#        half_exp_euler = stepsize_adjustment(RKeuler.phi(),\
#                                             Fraction(1, 2))
        the_conjugate = conjugate(imp_midpoint, half_imp_euler)
        equal_up_to_order(trapezoidal, the_conjugate, max_order)

    def test_no_2(self):
        max_order = 5
        trapezoidal = RKimplicitTrapezoidal.phi()
        imp_midpoint = RKimplicitMidpoint.phi()
        half_imp_euler = stepsize_adjustment(RKimplicitEuler.phi(),
                                             Fraction(1, 2))
#        half_exp_euler = stepsize_adjustment(RKeuler.phi(),\
#                                             Fraction(1, 2))
        the_conjugate = conjugate_by_commutator(imp_midpoint, half_imp_euler)
        equal_up_to_order(trapezoidal, the_conjugate, max_order)
