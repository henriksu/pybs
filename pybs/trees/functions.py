import math
import operator

from pybs.utils import memoized as memoized
from pybs.trees import ButcherTree, ButcherEmptyTree


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
def density(self):
    if isinstance(self, ButcherEmptyTree):
        return 1
    result = order(self)
    for elem in self:
        result *= density(elem) ** self[elem]
    return result


@memoized
def symmetry(self):
    def _subtree_contribution((self, multiplicity)):
        return symmetry(self) ** multiplicity * math.factorial(multiplicity)
    return reduce(operator.__mul__, map(_subtree_contribution, self.items()),
                  1)


@memoized
def alpha(self):
    return math.factorial(order(self)) / (symmetry(self) * density(self))
    # Will always come out integer.


def F(self):
    'Elementary differential.'
    if isinstance(self, ButcherEmptyTree):
        return 'y'
    result = 'f' + "'" * number_of_children(self)
    if number_of_children(self) == 1:
        result += F(self.keys()[0])
    elif number_of_children(self) > 1:
        result += '(' + ','.join([F(elem) for elem in self.elements()]) + ')'
    return result


@memoized
def isBinary(self):
    if isinstance(self, ButcherEmptyTree):
        return True
    if number_of_children(self) > 2:
        return False
    for subtree in self:
        if not isBinary(subtree):
            return False
    return True


@memoized
def isTall(self):
    if isinstance(self, ButcherEmptyTree):
        return True
    if number_of_children(self) > 1:
        return False
    for subtree in self:
        if not isTall(subtree):
            return False
    return True


def isBushy(self):
    if self == ButcherEmptyTree or self == ButcherTree.basetree():
        return True
    elif self.keys() == [ButcherTree.basetree()]:
        return True
    else:
        return False
