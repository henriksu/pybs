from math import factorial
from fractions import Fraction

from src.trees import ButcherTree, ButcherEmptyTree, density, order, isTall, isBinary, number_of_children
from src.combinations import LinearCombination, split, TreeGenerator


class BseriesRule(object):
    def __init__(self, arg = None, a = 0):
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
        'Directly from Owren'
        if isTall(tree):
            return 2 ** (1-order(tree))
        else:
            return 0

    def _AVF(self, tree):
        'Directly from Owren'
        if order(tree) == 1:
            return 1
        elif not isBinary(tree):
            return 0
        else:
            if number_of_children(tree) == 1:
                return self._AVF(tree.child)/2.0 # TODO: tree.child FINNES IKKE
            elif number_of_children(tree) == 2:
                alpha = Fraction(2*self.a + 1, 4)
                return alpha * self._AVF(tree.childOne) * self._AVF(tree.childTwo)
                
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
    if a(ButcherEmptyTree())!= 1 or a(ButcherTree.basetree()) !=1:
        raise ValueError
    mainResult = BseriesRule()
    def newRule(tree):
        if tree == ButcherEmptyTree():
            return 0
        elif tree == ButcherTree.basetree():
            return 1
        result = a(tree)
        c = mainResult # This is a BseriesRule. Caution: Recursive!
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
    for tree in TreeGenerator(ButcherTree):
        if order(tree) > 7:
            break
        print tree
        print modified(tree)
    print 'Finished'