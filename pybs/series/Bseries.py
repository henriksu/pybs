from fractions import Fraction

from pybs.combinations import empty_tree, LinearCombination, Forest
from pybs.unordered_tree import UnorderedTree


class BseriesRule(object):
    def __init__(self, arg=None, a=0):
        if arg is None:
            self._call = lambda x: 0
        elif isinstance(arg, LinearCombination):
            self._call = lambda tree: arg[tree]  # TODO: Check that there are no non-trees.
        elif callable(arg):
            self._call = arg

    def __call__(self, arg):
        if isinstance(arg, UnorderedTree) or arg == empty_tree():
            return self._call(arg)
        elif isinstance(arg, Forest):
            result = 1
            for tree, multiplicity in arg.items():
                result *= self._call(tree) ** multiplicity
                # TODO: Use reduce() or something?
            return result


def _zero(tree):
    return 0


def _unit(tree):
    if tree == empty_tree():
        return 1
    else:
        return 0


def _exact(tree):
    if tree == empty_tree():
        return 1
    return Fraction(1, tree.density())


def _kahan(tree):
    'Directly from Owren'  # TODO: Test
    if tree.is_Tall():
        return 2 ** (1-tree.order())
    else:
        return 0


def _AVF(self, tree, a):
    'Directly from Owren'  # TODO: Test
    if tree.order() == 1:
        return 1
    elif not tree.is_Binary():
        return 0
    else:
        if tree.number_of_children() == 1:
            return _AVF(tree.keys()[0], a)/2.0
        elif tree.number_of_children() == 2:
            alpha = Fraction(2*a + 1, 4)
            return alpha * _AVF(tree.keys()[0], a) * \
                _AVF(tree.keys()[1], a)

exponential = BseriesRule(_exact)
zero = BseriesRule(_zero)
