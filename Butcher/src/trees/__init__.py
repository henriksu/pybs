# This Python file uses the following encoding: utf-8
import math
import operator
from numbers import Number

import src.utils
from src.utils.miscellaneous import memoized as memoized
import forest as forest
# TODO: Implement the cache miss super fast memoization.

class AbstractUnorderedRootedTree(src.utils.multiset.FrozenMultiset):
    __slots__ = ('__weakref__',)

    def __setattr__(self, *args):
        raise AttributeError

    def __delattr__(self, *args):
        raise AttributeError

    def __init__(self, forest=src.utils.multiset.FrozenMultiset()):
        src.utils.multiset.FrozenMultiset.__init__(self, forest)
        
    multiplicities = src.utils.multiset.FrozenMultiset.values #  Alias. "Correct" way of doing it?
 
    @staticmethod
    def _subtree_contribution((tree, multiplicity)):
        return symmetry(tree) ** multiplicity * math.factorial(multiplicity)

    @classmethod
    def basetrees(cls):
        raise NotImplementedError
    
    def alpha(self):
        raise NotImplementedError #  TODO: Implement me.

    def __mul__(self, other):
        if isinstance(other, type(self)):
            new_self = src.utils.multiset.Multiset(self)
            new_self.inplace_add(other)
            return type(self)(new_self)
        elif isinstance(other, Number):
            from forest.linearCombination import LinearCombination # TODO: Nasty work around
            tmp = LinearCombination()
            tmp[self] = other
            return tmp

   
@memoized
def order(tree):
    result = 1
    for elem, mult in tree.items():
        result += mult * order(elem)
    return result

@memoized
def number_of_children(tree):
    'Number of children.'
    return sum(tree.multiplicities())

@memoized
def density(tree):
    result = order(tree)
    for elem in tree:
        result *= density(elem) ** tree[elem]
    return result

@memoized
def symmetry(tree):
    return reduce(operator.__mul__, map(tree._subtree_contribution, tree.items()), 1)



def TreeGenerator(treetype):
    theForest = forest.FrozenForest([treetype.basetrees()])
    while True:
        for tree in theForest:
            yield tree
        theForest = theForest.D()

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