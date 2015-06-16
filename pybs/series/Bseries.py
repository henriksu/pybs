from fractions import Fraction

from pybs.utils import LinearCombination
from pybs.combinations import empty_tree, Forest
from pybs.unordered_tree import UnorderedTree, leaf


class BseriesRule(object):
    """Objects of this class are B-series rules for numerical methods.

    They treat forests as characters of the Hopf algebra.
    For other B-series rules use :Class:`VectorfieldRule`
    or :class:`ForestRule`."""
    def __init__(self, arg=None):
        if arg is None:
            self._call = lambda x: 0
        elif isinstance(arg, LinearCombination):
            self._call = lambda tree: arg[tree]  # TODO: Check that there are no non-trees.
        elif callable(arg):
            self._call = arg

    def __call__(self, arg):
        if isinstance(arg, UnorderedTree) or arg == empty_tree:
            return self._call(arg)
        elif isinstance(arg, Forest):
            result = 1
            for tree, multiplicity in arg.items():
                result *= self._call(tree) ** multiplicity
                # TODO: Use reduce() or something?
            return result
#            else:
#                return 0
        elif isinstance(arg, LinearCombination):
            result = 0
            for elem, multiplicity in arg.items():
                result += self(elem) * multiplicity
            return result


class VectorfieldRule(object):
    """Objects of this class are B-series rules that correspond to modified
    equations.

    That means they act on forests as infinitesimal characters.
    """
    def __init__(self, arg=None):
        if arg is None:
            self._call = lambda x: 0
        elif isinstance(arg, LinearCombination):
            self._call = lambda tree: arg[tree]  # TODO: Check that this is reasonable.
        elif callable(arg):
            self._call = arg

    def __call__(self, arg):
        if isinstance(arg, UnorderedTree) or arg == empty_tree:
            return self._call(arg)
        elif isinstance(arg, Forest):
            if arg.number_of_trees() == 1:  # TODO: Do nicer.
                for elem in arg:
                    return self._call(elem)
            else:
                return 0
        elif isinstance(arg, LinearCombination):
            result = 0
            for elem, multiplicity in arg.items():
                result += self(elem) * multiplicity
            return result


class ForestRule(object):
    """General rule with arbitrary behavior for forest.

    Use this if the two others are unsuitable.
    """
#  Results on forests are not deducable from results on trees.
    def __init__(self, arg=None):
        if arg is None:
            self._call = lambda x: 0
        elif isinstance(arg, LinearCombination):
            self._call = lambda forest: arg[forest]
        elif callable(arg):
            self._call = arg

    def __call__(self, arg):
        if isinstance(arg, (UnorderedTree, Forest)):
            return self._call(arg)
        elif isinstance(arg, LinearCombination):
            result = 0
            for elem, multiplicity in arg.items():
                result += self(elem) * multiplicity
            return result


def _unit(tree):
    if tree == empty_tree:
        return 1
    else:
        return 0


def _exact(tree):
    if tree == empty_tree:
        return 1
    return Fraction(1, tree.density())


def _kahan(tree):
    if tree == empty_tree:
        return 1
    if tree.is_tall():
        return Fraction(1, (2 ** (tree.order()-1)) * tree.symmetry())
    else:
        return 0  # TODO: Necessary??


def _AVF_old(a, tree):
    if tree == empty_tree:
        return 1
    if tree == leaf:
        return 1
    elif not tree.is_binary():
        return 0
    else:
        if tree.number_of_children() == 1:
            return Fraction(_AVF(a, tree.keys()[0]), 2)
        elif tree.number_of_children() == 2:
            alpha = Fraction(2*a + 1, 4)
            if len(tree._ms) == 2:
                return alpha * _AVF(a, tree.keys()[0]) * \
                    _AVF(a, tree.keys()[1])
            else:
                return alpha * _AVF(a, tree.keys()[0]) ** 2


def _AVF(tree):
    "According to `Energy-Preserving Runge-Kutta Methods`, Celledoni et al."
    if tree == empty_tree:
        return 1
    if tree == leaf:
        return 1
    else:
        result = Fraction(1, tree.number_of_children() + 1)
        for child_tree, multiplicity in tree.items():
            result *= _AVF(child_tree) ** multiplicity
        return result


def _unit_field(tree):
    if tree == leaf:
        return 1
    return 0

exponential = BseriesRule(_exact)
unit = BseriesRule(_unit)
unit_field = VectorfieldRule(_unit_field)
AVF = BseriesRule(_AVF)
