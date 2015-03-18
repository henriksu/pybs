from math import factorial
from fractions import Fraction
from itertools import count, islice
from functools import partial

from numpy.linalg import lstsq
from scipy import sparse
from scipy.sparse.linalg import lsqr
import numpy as np

from pybs.utils import \
    memoized
from pybs.unordered_tree import \
    leaf, \
    number_of_trees_of_order, \
    number_of_tree_pairs_of_total_order as m,\
    the_trees, \
    tree_generator, \
    trees_of_order
from pybs.combinations import \
    empty_tree, \
    LinearCombination, \
    split, \
    subtrees, antipode_ck, \
    symp_split, \
    treeCommutator as tree_commutator
from pybs.series.Bseries import \
    BseriesRule, \
    exponential, \
    ForestRule, \
    VectorfieldRule


def equal_up_to_order(a, b, max_order=None):
    if not a(empty_tree) == b(empty_tree):
        return None
    for tree in tree_generator():
        if max_order and tree.order() > max_order:
            return max_order
        elif not a(tree) == b(tree):
            return tree.order() - 1


def convergence_order(a):
    # exponential = B-series of the exact solution.
    return equal_up_to_order(a, exponential)


def symmetric_up_to_order(a, max_order=None):
    #  TODO: make memoization use "best so far" to improve on it later.
    # Use some weak dict.
    # Prepare it to work with "quadratic tree generator"?
    # Will need new tree generator.
    b = adjoint(a)
    return equal_up_to_order(a, b, max_order)
    # TODO: check convergence order and exploit it. efficiency.


def conjugate_to_symplectic(a, max_order=float("inf")):
    conv_order = convergence_order(a)  # Known minimum.
    # Methods of order 2 are always conjugate to symplectic up to order 3:
    first_order_checked = conv_order + 1 + (conv_order == 2)
    # TODO: Find out why max order is 2*convergence_order. Simplification?
    max_order = min(max_order, 2*conv_order)
    orders = xrange(first_order_checked, max_order+1)

    # FOllowing is slow and abandoned,
    # because it usually checks too far.
    # symmetry_order = symmetric_up_to_order(a, max_order)
    _alpha = modified_equation(a)

    def alpha(u, v):
        return _alpha(u.butcher_product(v)) - _alpha(v.butcher_product(u))
    for order in orders:
        if symmetric_up_to_order(a, order) == order and order % 2 == 0:
            continue
        A = conjugate_symplecticity_matrix(order)
        b = [alpha(u, v) for u, v in tree_pairs_of_order(order)]
        # lstsq "wants" NumPy-matrices, but eats Python-lists OK.
        res = lstsq(A, b)[1]  # square of 2-norm in a 1x1 matrix/ndarray.
        if res > 10.0**(-14):  # TODO: Choose a good tolerance.
            return order - 1
    return max_order


def conjugate_symplecticity_matrix(order):
    "An m_(order) by m_(order-1) matrix of integers. \
    Independent of the method under consideration."
    A = []
    list_of_pairs1 = tree_pairs_of_order(order)
    list_of_pairs2 = tree_pairs_of_order(order-1)
    for pair in list_of_pairs1:
        tmp = [0] * m(order-1)  # TODO: vector of m_(order-1) zeros.
        for tree, multiplicity in symp_split(pair[0]).items():
            try:
                # TODO: Not sure it will help to sort them,
                # due to the way duplication of pairs is avoided.
                the_number = list_of_pairs2.index((tree, pair[1]))
            except ValueError:
                the_number = list_of_pairs2.index((pair[1], tree))
            tmp[the_number] += multiplicity

        for tree, multiplicity in symp_split(pair[1]).items():
            try:
                the_number = list_of_pairs2.index((pair[0], tree))
            except ValueError:
                the_number = list_of_pairs2.index((tree, pair[0]))
            tmp[the_number] += multiplicity

        A.append(tmp)
    return A


def tree_pairs_of_order(order):
    "Returns a list of tuples of functions. \
    Each tuple considered as an unordered pair is returned exactly once."
    result = []
    max_order = order / 2  # Intentional truncation in division.
    for order1 in range(1, max_order + 1):
        order2 = order - order1
        # Sorting is important for reproducability.
        for tree1 in trees_of_order(order1, sort=True):
            for tree2 in trees_of_order(order2, sort=True):
                if (order1 != order2) or \
                   ((order1 == order2) and (tree2, tree1) not in result):
                    result.append((tree1, tree2))
    return result


def hf_composition(baseRule):
    if baseRule(empty_tree) != 1:
        raise ValueError(
            'Composition can only be performed on consistent B-series.')

    def new_rule(tree):
        if tree == empty_tree:
            return 0
        else:
            result = 1
            for subtree, multiplicity in tree.items():
                result *= baseRule(subtree) ** multiplicity
            return result
    return BseriesRule(new_rule)


def lie_derivative(c, b, truncate=False):
    if b(empty_tree) != 0:
        raise ValueError(
            'The second argument does not satisfy b(ButcherEmptyTree()) == 0.')

    @memoized
    def new_rule(tree):
        result = 0
        if tree == empty_tree:
            return result
        pairs = split(tree, truncate)
        for pair, multiplicity in pairs.items():
            result += multiplicity * b(pair[0]) * c(pair[1])
        return result
    return BseriesRule(new_rule)


def modified_equation(a):
    if a(empty_tree) != 1 or a(leaf) != 1:  # TODO: Check last condition.
        raise ValueError(
            'Can not calculate the modified equation for this BseriesRule.')

    @memoized
    def new_rule(tree):
        if tree == empty_tree:
            return 0
        result = a(tree)
        c = new_rule  # This is a BseriesRule. Caution: Recursive!
        for j in range(2, tree.order() + 1):
            c = lie_derivative(c, new_rule, True)  # TODO: Is this memoized?
            result -= Fraction(c(tree), factorial(j))
        return result
    result = BseriesRule(new_rule)
    if a.quadratic_vectorfield:
        result = remove_non_binary(result)
    return result


def log(a):
    if a(empty_tree) != 1:
        raise ValueError(
            'Can not calculate the logarithm for this BseriesRule.')

    @memoized
    def new_rule(tree):
        if tree == empty_tree:
            return 0
        a_2 = remove_empty_tree(a)
        result = a_2(tree)
        b = a_2
        for n in range(2, tree.order() + 1):
            b = composition(b, a_2)
#            c = stepsize_adjustment(b, Fraction(1, n))  # TODO: Remove.
            result += ((-1)**(n+1)) * Fraction(b(tree), n)
        return result
    return VectorfieldRule(new_rule)  # TODO: is VectorfieldRUle always right??
#    result = BseriesRule(new_rule)
#    if a.quadratic_vectorfield:
#        result = remove_non_binary(result)
#    return result


def exp(a):
    if a(empty_tree) != 0:
        raise ValueError(
            'Can not calculate the exponential for this BseriesRule.')

    @memoized
    def new_rule(tree):
        if tree == empty_tree:
            return 1
        result = a(tree)
        b = a
        for n in range(2, tree.order() + 1):
            b = composition(b, a)
            result += Fraction(b(tree), factorial(n))
        return result
    result = BseriesRule(new_rule)
    if a.quadratic_vectorfield:
        result = remove_non_binary(result)
    return result


def remove_non_binary(a):
    base_rule = a._call
    et = empty_tree

    def new_rule(tree):
        if tree == et or tree.is_binary():
            return base_rule(tree)
        else:
            return 0
    return BseriesRule(new_rule)


def remove_empty_tree(a):
    base_rule = a._call
    et = empty_tree

    def new_rule(tree):
        if tree == et:
            return 0
        else:
            return base_rule(tree)
    return BseriesRule(new_rule)


def composition_ssa(a, b):
    if a(empty_tree) != 1:
        raise ValueError(
            'Composition can only be performed on consistent B-series.')

    def subRule(pair):
        return a(pair[0]) * b(pair[1])

    @memoized
    def new_rule(tree):
        sub_trees = subtrees(tree)
        result = 0
        for pair, multiplicity in sub_trees.items():
            result += subRule(pair) * multiplicity
        return Fraction(result, 2 ** tree.order())

    return BseriesRule(new_rule)
    # TODO: account for ForestRule.


def stepsize_adjustment(a, A):
    base_rule = a._call

    def new_rule(tree):
        return A**tree.order() * base_rule(tree)
    return BseriesRule(new_rule)


def composition(a, b):
    @memoized
    def new_rule(arg):  # arg is tree or forest.
        result = 0
        for pair, multiplicity in subtrees(arg).items():
            result += a(pair[0]) * b(pair[1]) * multiplicity
        return result
    if a(empty_tree) != 1:
        return ForestRule(new_rule)
    else:
        return BseriesRule(new_rule)


def inverse(a):
    "The inverse of 'a' in the Butcher group."
    def new_rule(tree):
        return a(antipode_ck(tree))
    return BseriesRule(new_rule)


def conjugate(a, c):
    "The conjugate of 'a' with change of coordinates 'c'."
    return BseriesRule(composition(inverse(c), composition(a, c)))


def adjoint(a):
    "The adjoint is the inverse with reversed time step."
    b = inverse(a)

    def new_rule(tree):
        return (-1)**tree.order() * b(tree)
    return BseriesRule(new_rule)


def series_commutator(a, b):
    # TODO: TEST ME!
    orders = set((0,))  # the coefficient of the empty tree is always 0.
    storage = LinearCombination()

    def new_rule(tree):
        order = tree.order()
        if order in orders:
            return storage[tree]
        else:
            result = LinearCombination()
            for order1 in range(1, order):
                order2 = order - order1
                for tree1 in trees_of_order(order1):
                    for tree2 in trees_of_order(order2):
                        result += (a(tree1) * b(tree2)) * \
                            tree_commutator(tree1, tree2)
            orders.add(order)
            storage += result
    return BseriesRule(new_rule)


def symplectic_up_to_order(a, max_order=None):
    # TODO: Find convergence order and check only from there upwards.
    if a(empty_tree) != 1:
        return None
    orders = count(start=2)
    if max_order:
        orders = islice(orders, max_order - 1)
    _symp_cond = partial(_symplecticity_condition, a)
    for order in orders:
        max_check_order = order / 2  # Intentional truncation in division.
        for order1 in range(1, max_check_order + 1):
            order2 = order - order1
            for tree1 in trees_of_order(order1):
                for tree2 in trees_of_order(order2):
                    if not _symp_cond(tree1, tree2):
                        return order - 1
    return max_order


def _symplecticity_condition(a, tree1, tree2):
    'Symmetric function in tree1, tree2.'
    return a(tree1.butcher_product(tree2)) + a(tree2.butcher_product(tree1)) \
        == a(tree1) * a(tree2)


# DANGER: NOT TESTED
def hamiltonian_up_to_order(a, max_order=None):
    # TODO: Check convergence order (equal to 01000...)
    # and check only from there upwards.
    if a(empty_tree) != 0 or a(leaf) == 0:
        return None  # Not hamiltonian at all.
    orders = count(start=2)
    if max_order:
        orders = islice(orders, max_order - 1)
    _ham_cond = partial(_hamilton_condition, a)
    for order in orders:
        max_check_order = order / 2  # Intentional truncation in division.
        for order1 in range(1, max_check_order + 1):
            order2 = order - order1
            for tree1 in trees_of_order(order1):
                for tree2 in trees_of_order(order2):
                    if not _ham_cond(tree1, tree2):
                        return order - 1
    return max_order


def _hamilton_condition(a, tree1, tree2):
    return a(tree1.butcher_product(tree2)) + \
        a(tree2.butcher_product(tree1)) == 0


def new_hamiltonian_up_to_order(a, max_order=None):
    if a(empty_tree) != 0 or a(leaf) == 0:
        return None  # Not vectorfield at all. TODO: exception.
    orders = count(start=2)  # TODO: start at 2 ? why not? no conditions?
    if max_order:
        orders = islice(orders, max_order - 1)
    for order in orders:
        A = hamiltonian_matrix(order)
        b = np.asarray(map(a, trees_of_order(order, sort=True)),
                       dtype=np.float64)
#        b = b.transpose()
        # lstsq "wants" NumPy-matrices, but eats Python-lists OK.
        if not np.any(b):
            continue  # b is zero vector, no need to check further.
        if order == 2:
            return 1
        if not_in_colspan(A, b):
            return order - 1
    return max_order


@memoized
def hamiltonian_matrix(order):
    nsft = the_trees[order].non_superfluous_trees(sort=True)
    m = number_of_trees_of_order(order)
    n = len(nsft)
    result = sparse.lil_matrix((m, n), dtype=np.int8)
    for free_tree in nsft:
        j = the_trees[order].non_superfluous_index(free_tree)
        for tree, sign in free_tree._rooted_trees.items():
            # TODO: dont acces private.
            i = the_trees[order].index(tree)
            result[i, j] = sign
    return result


def energy_preserving_upto_order(a, max_order=None):
    "Input: vector field/Lie ALGEBRA element"
    if a(empty_tree) != 0 or a(leaf) == 0:
        return None  # Not vectorfield at all. TODO: exception.
    orders = count(start=2)  # TODO: start at 2 ? why not 1? no conditions?
    if max_order:
        orders = islice(orders, max_order - 1)
    for order in orders:
        if not is_energy_preserving_of_order(a, order):
            return order - 1
    return max_order


def is_energy_preserving_of_order(a, order):
    forbidden_trees, interesting_trees = _get_tree_sets(order)
    for tree in forbidden_trees:
        if a(tree) != 0:
            return False
    for free_tree, collection in interesting_trees.items():
        collection = sorted(collection)
        A = get_energy_matrix(free_tree, collection)
        b = np.asarray(map(a, collection), dtype=np.float64)
        if not_in_colspan(A, b):
            return False
    return True


# @memoized TODO: Find a way of hashing input.
def get_energy_matrix(free_tree, collection):
    # collection = sorted(collection)
    le = len(collection)
    A = sparse.lil_matrix((le, le-1), dtype=np.int64)
    A[0, :] = Fraction(-collection[0].symmetry(),
                       free_tree._rooted_trees[
                       leaf.butcher_product(collection[0])])
    for tree in collection[1:]:
        i = collection.index(tree)
        A[i, i-1] = Fraction(tree.symmetry(),
                             free_tree._rooted_trees[
                             leaf.butcher_product(tree)])
    return A
    # TODO: avoid performing BP twice.


@memoized
def _get_tree_sets(order):
    # uninteresting_trees = set()  # Energy preservation does not care.
    forbidden_trees = set()  # Never found in energy preserving series.
    interesting_trees = dict()  # included in a non trivial basis vector.
    for tree in the_trees[order].trees():
        free_tree = leaf.butcher_product(tree).get_free_tree()
        if free_tree.superfluous:  # a) in FCM, Celledoni et al.
            pass  # Don't store them
            # uninteresting_trees.add(tree)
        elif free_tree.is_symmetric():  # b)
            forbidden_trees.add(tree)
        elif free_tree in interesting_trees:
            interesting_trees[free_tree].add(tree)
        else:
            interesting_trees[free_tree] = set((tree,))
    return forbidden_trees, interesting_trees


def not_in_colspan(A, b):
    try:
        res = lsqr(A, b)
    except ZeroDivisionError:
        print "ZeroDivisionError ignored."
        return False  # TODO: File BUG report.
    # res[1] = 0: x=0, special case for trivial solution.
    # res[1] = 1: Found (approx) solution to Ax = b.
    # res[1] = 2: Not in colspan, lst.sq. approximation was found.
#    return res[1] != 1 and (res[1] == 2 or res[3] > 10.0**(-5))
    return res[1] != 1 and (res[1] == 2 or res[3] > 10.0**(-10))
