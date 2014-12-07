import operator
from fractions import Fraction
from forest.linearCombination import LinearCombination
from trees.ButcherTrees import ButcherTree, ButcherEmptyTree
from trees.functions import density

class BseriesRule(object):
    def __init__(self, arg = None):
        if arg is None:
            self._call = lambda x: 0
        elif arg == 'unit':
            self._call = self._unit
        elif arg == 'exact':
            self.call = self._exact
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

def hf_composition(baseRule):
    if baseRule(ButcherEmptyTree) != 1:
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