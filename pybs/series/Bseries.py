from fractions import Fraction

from pybs.combinations import empty_tree, LinearCombination, Forest
from pybs.unordered_tree import UnorderedTree, leaf


class BseriesRule(object):
    def __init__(self, arg=None, quadratic_vectorfield=False):
        if arg is None:
            self._call = lambda x: 0
        elif isinstance(arg, LinearCombination):
            self._call = lambda tree: arg[tree]  # TODO: Check that there are no non-trees.
        elif callable(arg):
            self._call = arg

            self.quadratic_vectorfield = quadratic_vectorfield

    def __call__(self, arg):
        if isinstance(arg, UnorderedTree) or arg == empty_tree():
            return self._call(arg)
        elif isinstance(arg, Forest):
            result = 1
            for tree, multiplicity in arg.items():
                result *= self._call(tree) ** multiplicity
                # TODO: Use reduce() or something?
            return result
        elif isinstance(arg, LinearCombination):
            result = 0
            for elem, multiplicity in arg.items():
                result += self(elem) * multiplicity
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
    if tree == empty_tree():
        return 1
    if tree.is_tall():
        return Fraction(1, (2 ** (tree.order()-1)) * tree.symmetry())
    else:
        return 0


def _AVF(tree, a):
    'Directly from Owren'  # TODO: Test
    if tree.order() == 1:
        return 1
    elif not tree.is_binary():
        return 0
    else:
        if tree.number_of_children() == 1:
            return _AVF(tree.keys()[0], a)/2.0
        elif tree.number_of_children() == 2:
            alpha = Fraction(2*a + 1, 4)
            return alpha * _AVF(tree.keys()[0], a) * \
                _AVF(tree.keys()[1], a)


def _unit_field(tree):
    if tree == leaf():
        return 1
    return 0

exponential = BseriesRule(_exact)
zero = BseriesRule(_zero)
unit = BseriesRule(_unit)
unit_field = BseriesRule(_unit_field)
