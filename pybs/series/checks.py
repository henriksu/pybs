from fractions import Fraction
from itertools import count, islice
from functools import partial

from numpy.linalg import lstsq
from scipy import sparse
from scipy.sparse.linalg import lsqr
import numpy as np

from pybs.utils import memoized
from pybs.combinations import empty_tree, symp_split
from pybs.unordered_tree import \
    tree_generator, \
    number_of_tree_pairs_of_total_order as m, \
    trees_of_order, \
    leaf, \
    the_trees, \
    number_of_trees_of_order
from pybs.series import exponential, adjoint, modified_equation


def equal_up_to_order(a, b, max_order=None):
    '''Checks that 'a' and 'b' give the exact same answer for all trees.
    Returns n equals the largest order for which this is true.

    More details'''
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
                # TODO: I think some trees are repeated! Merge with the other similar case.
                if (order1 != order2) or \
                   ((order1 == order2) and (tree2, tree1) not in result):
                    result.append((tree1, tree2))
    return result


def symplectic_up_to_order(a, max_order=None):
    # TODO: Find convergence order and check only from there upwards.
    if a(empty_tree) != 1:
        return None
    orders = count(start=2)
    if max_order:
        orders = islice(orders, max_order - 1)
    _symp_cond = partial(_symplecticity_condition, a)
    for order in orders:
        if not satisfied_for_tree_pairs_of_order(_symp_cond, order):
            return order - 1
    return max_order


def hamiltonian_up_to_order(a, max_order=None):
    # TODO: Check convergence order (equal to 01000...)
    # and check only from there upwards.
    if a(empty_tree) != 0 or a(leaf) == 0:
        return None  # TODO: Throw some kind of exception
    orders = count(start=2)
    if max_order:
        orders = islice(orders, max_order - 1)
    _ham_cond = partial(_hamilton_condition, a)
    for order in orders:
        if not satisfied_for_tree_pairs_of_order(_ham_cond, order):
            return order - 1
    return max_order


def satisfied_for_tree_pairs_of_order(condition, order):
    max_check_order = order / 2  # Intentional truncation in division.
    for order1 in range(1, max_check_order + 1):
        order2 = order - order1
        for tree1 in trees_of_order(order1):
            for tree2 in trees_of_order(order2):
                if not condition(tree1, tree2):
                    return False
    return True


def _symplecticity_condition(a, tree1, tree2):
    'Symmetric function in tree1, tree2.'
    return a(tree1.butcher_product(tree2)) + a(tree2.butcher_product(tree1)) \
        == a(tree1) * a(tree2)


def _hamilton_condition(a, tree1, tree2):
    'Symmetric function in tree1, tree2.'
    # TODO: extract the sum into another function?
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
    '''returns a matrix whose columns form a basis for \
    Hamiltonian B-series of "order".

    Details.
    '''
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
    # TODO: Celledoni's PPT says trees are repeated in the basis?!?
    # Perhaps it includes symmetry coefficient?


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
        return False  # Suspecting: Happens if iteration hits exact solution.
    # res[1] = 0: x=0, special case for trivial solution.
    # res[1] = 1: Found (approx) solution to Ax = b.
    # res[1] = 2: Not in colspan, lst.sq. approximation was found.
    return res[1] != 1 and (res[1] == 2 or res[3] > 10.0**(-10))
