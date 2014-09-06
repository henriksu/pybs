# This Python file uses the following encoding: utf-8
from math import factorial
from operator import __mul__
from utils import memoized
from utils.multiset import Multiset, FrozenMultiset
from forest import Forest, FrozenForest
# TODO: Implement the cache miss super fast memoization.


class AbstractTreeLike(object):
    __slots__ = ('__weakref__',)
    def __setattr__(self, *args):
        raise AttributeError
    def __delattr__(self, *args):
        raise AttributeError


class AbstractUnorderedRootedTree(FrozenMultiset, AbstractTreeLike):
    __slots__ = ()
    def __init__(self, forest=FrozenMultiset()):
        FrozenMultiset.__init__(self, forest)
        
    multiplicities = FrozenMultiset.values #  Alias. "Correct" way of doing it?
    
    @property
    @memoized
    def order(self):
        result = 1
        for elem, mult in self.items():
            result += mult * elem.order
        return result

    @property
    @memoized
    def m(self):
        'Number of children.'
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
            new_tree = self * other
            result.inplace_add(new_tree)
            for subtree, multiplicity1 in self.items():
                amputated_forest = self.sub(subtree)
                forest_of_replacements = subtree.graft(other)
                for sub_diff, multiplicity2 in forest_of_replacements.items():
                    multiset_of_new_children = amputated_forest.add(sub_diff)
                    new_tree2 = type(self)(multiset_of_new_children)
                    result.inplace_multiset_sum({new_tree2: multiplicity1 * multiplicity2})
            return result

    @classmethod
    def basetrees(cls):
        raise NotImplementedError
    
    def alpha(self):
        raise NotImplementedError #  TODO: Implement me.

    def __mul__(self, other):
        new_self = Multiset(self)
        new_self.inplace_add(other)
        return type(self)(new_self)



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
