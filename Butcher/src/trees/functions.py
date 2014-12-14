import math
import operator

from src.utils import memoized as memoized
from src.trees import ButcherTree, ButcherEmptyTree


@memoized
def order(tree):
    result = 1
    if tree == ButcherEmptyTree():
        return 0
    for elem, mult in tree.items():
        result += mult * order(elem)
    return result


@memoized
def number_of_children(tree):
    'Number of children.'
    if isinstance(tree, ButcherEmptyTree):
        return 0
    return sum(tree.multiplicities())


@memoized
def density(tree):
    if isinstance(tree, ButcherEmptyTree):
        return 1
    result = order(tree)
    for elem in tree:
        result *= density(elem) ** tree[elem]
    return result


@memoized
def symmetry(tree):
    def _subtree_contribution((tree, multiplicity)):
        return symmetry(tree) ** multiplicity * math.factorial(multiplicity)
    return reduce(operator.__mul__, map(_subtree_contribution, tree.items()),
                  1)


@memoized
def alpha(tree):
    return math.factorial(order(tree)) / (symmetry(tree) * density(tree))
    # Will always come out integer.


def F(tree):
    'Elementary differential.'
    if isinstance(tree, ButcherEmptyTree):
        return 'y'
    result = 'f' + "'" * number_of_children(tree)
    if number_of_children(tree) == 1:
        result += F(tree.keys()[0])
    elif number_of_children(tree) > 1:
        result += '(' + ','.join([F(elem) for elem in tree.elements()]) + ')'
    return result


def isBinary(tree):
    if isinstance(tree, ButcherEmptyTree):
        return True
    if number_of_children(tree) > 2:
        return False
    for subtree in tree:
        if not isBinary(subtree):
            return False
    return True


def isTall(tree):
    if isinstance(tree, ButcherEmptyTree):
        return True
    if number_of_children(tree) > 1:
        return False
    for subtree in tree:
        if not isTall(subtree):
            return False
    return True


def isBushy(tree):
    if tree == ButcherEmptyTree or tree == ButcherTree.basetree():
        return True
    elif tree.keys() == [ButcherTree.basetree()]:
        return True
    else:
        return False
