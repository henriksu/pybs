from fractions import Fraction
from math import factorial

from pybs.utils import memoized
from pybs.unordered_tree import leaf, trees_of_order
from pybs.combinations import \
    empty_tree, \
    split, \
    subtrees, \
    antipode_ck, \
    LinearCombination, \
    treeCommutator as tree_commutator
from pybs.series import BseriesRule, VectorfieldRule, ForestRule
# TODO: Include Sphinx in installation?

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
