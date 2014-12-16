from math import factorial
from fractions import Fraction

from src.trees import ButcherTree, ButcherEmptyTree, order
from src.combinations import split, treeGenerator
from Bseries import BseriesRule


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
    result = BseriesRule()

    def newRule(tree):
        if isinstance(tree, ButcherEmptyTree):
            return 0
        else:
            result = 1
            for subtree, multiplicity in tree.items():
                result *= baseRule(subtree) ** multiplicity
            return result
    result._call = newRule
    return result


def lieDerivative(c, b, truncate=False):
    if b(ButcherEmptyTree()) != 0:
        raise ValueError(
            'The second argument does not satisfy b(ButcherEmptyTree()) == 0.')
    result = BseriesRule()

    def newRule(tree):
        result = 0
        if tree == ButcherEmptyTree():
            return result
        pairs = split(tree, truncate)
        for pair, multiplicity in pairs.items():
            result += multiplicity * c(pair[0]) * b(pair[1])
        return result
    result._call = newRule
    return result


def modifiedEquation(a):
    if a(ButcherEmptyTree()) != 1 or a(ButcherTree.basetree()) != 1:
        raise ValueError(
            'Can not calculate the modified equation for this BseriesRule.')
    finalRule = BseriesRule()

    def newRule(tree):
        if tree == ButcherEmptyTree():
            return 0
        elif tree == ButcherTree.basetree():
            return 1
        result = a(tree)
        c = finalRule  # This is a BseriesRule. Caution: Recursive!
        for j in range(2, order(tree) + 1):
            c = lieDerivative(c, finalRule, True)
            result -= Fraction(c(tree), factorial(j))
        return result
    finalRule._call = newRule
    return finalRule

if __name__ == '__main__':
    exact = BseriesRule('exact')
    modified = modifiedEquation(exact)
#    from forest.differentiation import TreeGenerator
    for tree in treeGenerator():
        if order(tree) > 7:
            break
        print tree
        print modified(tree)
    print 'Finished'
