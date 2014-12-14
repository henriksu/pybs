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
        raise ValueError
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


def lieDerivative(c, b, truncated=False):
    if b(ButcherEmptyTree()) != 0:
        raise ValueError
    result = BseriesRule()

    def newRule(tree):
        result = 0
        if tree == ButcherEmptyTree():
            return result
        pairs = split(tree, truncated)
        for pair, multiplicity in pairs.items():
            result += multiplicity * c(pair[0]) * b(pair[1])
        return result
    result._call = newRule
    return result


def modifiedEquation(a):
    if a(ButcherEmptyTree()) != 1 or a(ButcherTree.basetree()) != 1:
        raise ValueError
    mainResult = BseriesRule()

    def newRule(tree):
        if tree == ButcherEmptyTree():
            return 0
        elif tree == ButcherTree.basetree():
            return 1
        result = a(tree)
        c = mainResult  # This is a BseriesRule. Caution: Recursive!
        for j in range(2, order(tree) + 1):
            c = lieDerivative(c, mainResult, True)
            result -= Fraction(c(tree), factorial(j))
        return result
    mainResult._call = newRule
    return mainResult

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
