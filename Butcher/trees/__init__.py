# This Python file uses the following encoding: utf-8
from math import factorial
from operator import __mul__
from utils import memoized
from forest import Forest, FrozenForest
# TODO: Implement the cache miss super fast memoization.


class AbstractTreeLike(object):
    __slots__ = ('__weakref__',) #  Immutability
    def __setattr__(self, *args):
        raise AttributeError
    def __delattr__(self, *args):
        raise AttributeError


class AbstractUnorderedRootedTree(FrozenForest, AbstractTreeLike):
    __slots__ = () #  Making each instance more memory efficient.
    #  In addition __slots__ will cause an error if new instance variables are added.
    #  This is a good thing to detect deviation from the mathematical tree.
    def __init__(self, forest=FrozenForest()):
        FrozenForest.__init__(self, forest)

    @property
    @memoized
    def order(self):
        result = 1
        for elem, mult in self.items(): #  Rename "elem" to "tree" or "subtree".
            result += mult * elem.order
        return result

    @property
    @memoized
    def m(self): #  Number of children.
        return sum(self.multiplicities())

    @property
    @memoized
    def gamma(self):
        result = self.order
        for elem in self:
            result *= elem.gamma ** self[elem]
        return result

    @property
    @memoized
    def sigma(self):
        return reduce(__mul__, map(self._subtree_contribution, self.items()), 1)

    @staticmethod
    def _subtree_contribution((tree, multiplicity)):
        return tree.sigma ** multiplicity * factorial(multiplicity)

    @property
    def norm(self): #  Alias TODO: Norm is defined for infinitytrees. Make sure this does not crash.
        return self.order
    
    @property
    def number_of_children(self): #  Alias
        return self.m
    @property
    def density(self): #  Alias
        return self.gamma
    
    @property
    def symmetry(self): #  Alias
        return self.sigma

    def graft(self,other):
            result = Forest()
            new_forest = self + other
            new_tree = type(self)(new_forest) #  Not good. TODO:
            result.update((new_tree,))
            for subtree in self:
                amputated_forest = self - subtree
                forest_of_replacements = subtree.graft(other)
                for sub_diff in forest_of_replacements:
                    # Not good TODO:
                    result.update({type(self)(amputated_forest + sub_diff): forest_of_replacements[sub_diff] * self[subtree]})
            return result

    @classmethod
    def basetrees(cls):
        raise NotImplementedError
    
    def alpha(self):
        raise NotImplementedError #  TODO: Implement me. Find definition.



class AbstractNotTree(AbstractTreeLike):
    __slots__ = ()
    def graft(self, other):# TODO: Sjekk at jeg ikke prøver å pode to ikke-trær
        return FrozenForest((other,))

    def __str__(self):
        return 'Ø'

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __ne__(self, other):
        return not isinstance(other, type(self))

    def __hash__(self):
        return 0

    # Should these really be defined ???
    F = 'y'
    order = 0
    multiplicities = []
    m = number_of_children = 0
    gamma = density = 1
    sigma = symmetry = 1
    alpha = 1

def TreeGenerator(treetype):
    forest = FrozenForest([treetype.basetrees()])
    while True:
        for tree in forest:
            yield tree
        forest = forest.D()

    
    
# La str() gi ut LaTeX-kode? Trenger sikkert flere forskjellige output-formater.
# The way in which Frozen counter will have to be updated is not too different from strings.

#    memoization_dict = dict #WeakKeyDictionary
#    tree_pool = dict() #  WeakKeyValueDict. Could be a set, if one could retreive an element from a set.
    #m_mem = memoization_dict()

#     def __new__(cls, *args, **kw):
#         new_tree = super(AbstractUnorderedRootedTree, cls).__new__(cls) # TODO: Get AbstractUnorderedRootedTree out of this line.
#         new_tree.__init__(*args, **kw)
#         if new_tree in cls.tree_pool:
#             return cls.tree_pool[new_tree]
#         else:
#             cls.tree_pool[new_tree] = new_tree
#             return new_tree


if __name__ == "__main__":
    pass
