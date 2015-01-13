from fractions import Fraction

from pybs.trees import ButcherEmptyTree, density, order, \
    isTall, isBinary, number_of_children
from pybs.combinations import LinearCombination


def _zero(tree):
    return 0

def _unit(tree):
    if isinstance(tree, ButcherEmptyTree):
        return 1
    else:
        return 0

def _exact(tree):
    return Fraction(1, density(tree))

def _kahan(tree):
    'Directly from Owren'  # TODO: Test
    if isTall(tree):
        return 2 ** (1-order(tree))
    else:
        return 0

def _AVF(self, tree, a):
    'Directly from Owren'  # TODO: Test
    if order(tree) == 1:
        return 1
    elif not isBinary(tree):
        return 0
    else:
        if number_of_children(tree) == 1:
            return _AVF(tree.keys()[0], a)/2.0
        elif number_of_children(tree) == 2:
            alpha = Fraction(2*a + 1, 4)
            return alpha * _AVF(tree.keys()[0], a) * \
                _AVF(tree.keys()[1], a)

exponential = _exact
zero = _zero
