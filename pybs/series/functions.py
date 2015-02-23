from math import factorial
from fractions import Fraction
from itertools import count, islice
from functools import partial

from pybs.utils import memoized
from pybs.unordered_tree import tree_generator, trees_of_order, leaf
from pybs.combinations import split, empty_tree
from pybs.series.Bseries import exponential


def equal_up_to_order(a, b, max_order=None):
    if not a(empty_tree()) == b(empty_tree()):
        return 0
    for tree in tree_generator():
        if max_order and tree.order() > max_order:
            return max_order
        elif not a(tree) == b(tree):
            return tree.order() - 1


def hf_composition(baseRule):
    if baseRule(empty_tree()) != 1:
        raise ValueError(
            'Composition can only be performed on consistent B-series.')

    def newRule(tree):
        if tree == empty_tree():
            return 0
        else:
            result = 1
            for subtree, multiplicity in tree.items():
                result *= baseRule(subtree) ** multiplicity
            return result
    return newRule


def lie_derivative(c, b, truncate=False):
    if b(empty_tree()) != 0:
        raise ValueError(
            'The second argument does not satisfy b(ButcherEmptyTree()) == 0.')

    def newRule(tree):
        result = 0
        if tree == empty_tree():
            return result
        pairs = split(tree, truncate)
        for pair, multiplicity in pairs.items():
            result += multiplicity * c(pair[0]) * b(pair[1])
        return result
    return newRule


def modified_equation(a):
    if a(empty_tree()) != 1 or a(leaf()) != 1:
        raise ValueError(
            'Can not calculate the modified equation for this BseriesRule.')

    @memoized
    def newRule(tree):
        if tree == empty_tree():
            return 0
        elif tree == leaf():
            return 1
        result = a(tree)
        c = newRule  # This is a BseriesRule. Caution: Recursive!
        for j in range(2, tree.order() + 1):
            c = lie_derivative(c, newRule, True)
            result -= Fraction(c(tree), factorial(j))
        return result
    return newRule


def symplectic_up_to_order(a, max_order=None):
    orders = count(start=2)
    if max_order:
        orders = islice(orders, max_order)
    _sympCond = partial(_symplecticity_condition, a)
    for order in orders:
        max_check_order = order / 2  # Intentional truncation in division.
        for order1 in islice(count(1), max_check_order):
            order2 = order - order1
            for tree1 in trees_of_order(order1):
                for tree2 in trees_of_order(order2):
                    if not _sympCond(tree1, tree2):
                        return order - 1
    return max_order


def _symplecticity_condition(a, tree1, tree2):
    'Symmetric function in tree1, tree2.'
    return a(tree1.butcher_product(tree2)) + a(tree2.butcher_product(tree1)) \
        == a(tree1) * a(tree2)

if __name__ == '__main__':
    modified = modified_equation(exponential)
#    from forest.differentiation import TreeGenerator
    print modified(empty_tree())
    for tree in tree_generator():
        if tree.order() > 8:
            break
        #print tree
        print modified(tree)
    print 'Finished'
