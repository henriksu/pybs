from fractions import Fraction

from pybs.trees import ButcherEmptyTree, density, order, \
    isTall, isBinary, number_of_children
from pybs.combinations import LinearCombination


class BseriesRule(object):
    def __init__(self, arg=None, a=0):
        if arg is None:
            self._call = lambda x: 0
        elif arg == 'unit':
            self._call = self._unit
        elif arg == 'exact':
            self._call = self._exact
        elif arg == 'kahan':
            self._call = self._kahan
        elif arg == 'AVF' or arg == 'average vector field':
            self.a = a
            self._call = self._AVF
        elif isinstance(arg, LinearCombination):
            self._call = lambda tree: arg[tree]
        elif callable(arg):
            self._call = arg

    def __call__(self, tree):
        return self._call(tree)

    def _unit(self, tree):
        if isinstance(tree, ButcherEmptyTree):
            return 1
        else:
            return 0

    def _exact(self, tree):
        return Fraction(1, density(tree))

    def _kahan(self, tree):
        'Directly from Owren'  # TODO: Test
        if isTall(tree):
            return 2 ** (1-order(tree))
        else:
            return 0

    def _AVF(self, tree):
        'Directly from Owren'  # TODO: Test
        if order(tree) == 1:
            return 1
        elif not isBinary(tree):
            return 0
        else:
            if number_of_children(tree) == 1:
                return self._AVF(tree.keys()[0])/2.0
            elif number_of_children(tree) == 2:
                alpha = Fraction(2*self.a + 1, 4)
                return alpha * self._AVF(tree.keys()[0]) * \
                    self._AVF(tree.keys()[1])
