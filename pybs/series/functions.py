from math import factorial
from fractions import Fraction
from itertools import count, islice
from functools import partial

from pybs.utils import memoized
from pybs.trees import ButcherTree, ButcherEmptyTree, order
from pybs.combinations import split, treeGenerator, trees_of_order


def equal_up_to_order(a, b, max_order=None):
    for tree in treeGenerator():
        if max_order and order(tree) > max_order:
            return max_order
        elif not a(tree) == b(tree):
            return order(tree) - 1


def hf_composition(baseRule):
    if baseRule(ButcherEmptyTree()) != 1:
        raise ValueError(
            'Composition can only be performed on consistent B-series.')

    def newRule(tree):
        if isinstance(tree, ButcherEmptyTree):
            return 0
        else:
            result = 1
            for subtree, multiplicity in tree.items():
                result *= baseRule(subtree) ** multiplicity
            return result
    return newRule


def lieDerivative(c, b, truncate=False):
    if b(ButcherEmptyTree()) != 0:
        raise ValueError(
            'The second argument does not satisfy b(ButcherEmptyTree()) == 0.')

    def newRule(tree):
        result = 0
        if tree == ButcherEmptyTree():
            return result
        pairs = split(tree, truncate)
        for pair, multiplicity in pairs.items():
            result += multiplicity * c(pair[0]) * b(pair[1])
        return result
    return newRule


def modifiedEquation(a):
    if a(ButcherEmptyTree()) != 1 or a(ButcherTree.basetree()) != 1:
        raise ValueError(
            'Can not calculate the modified equation for this BseriesRule.')

    @memoized
    def newRule(tree):
        if tree == ButcherEmptyTree():
            return 0
        elif tree == ButcherTree.basetree():
            return 1
        result = a(tree)
        c = newRule  # This is a BseriesRule. Caution: Recursive!
        for j in range(2, order(tree) + 1):
            c = lieDerivative(c, newRule, True)
            result -= Fraction(c(tree), factorial(j))
        return result
    return newRule


def symplectic_up_to_order(a, max_order=None):
    orders = count(start=2)
    if max_order:
        orders = islice(orders, max_order)
    _sympCond = partial(_symplecticityCondition, a)
    for order in orders:
        max_check_order = order / 2  # Intentional truncation in division.
        for order1 in islice(count(1), max_check_order):
            order2 = order - order1
            for tree1 in trees_of_order(order1):
                for tree2 in trees_of_order(order2):
                    if not _sympCond(tree1, tree2):
                        return order - 1
    return max_order


def _symplecticityCondition(a, tree1, tree2):
    'Symmetric function in tree1, tree2.'
    return a(tree1 * tree2) + a(tree2 * tree1) == a(tree1) * a(tree2)

if __name__ == '__main__':
    exact = BseriesRule('exact')
    modified = modifiedEquation(exact)
#    from forest.differentiation import TreeGenerator
    for tree in treeGenerator():
        if order(tree) > 8:
            break
        #print tree
        print modified(tree)
    print 'Finished'
