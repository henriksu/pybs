# This Python file uses the following encoding: utf-8
import math

import src.utils
import src.utils.multiset as multiset
from src.utils.miscellaneous import memoized as memoized
import src.trees as trees
import src.forest as forest

#class ButcherTreeLike(trees.AbstractTreeLike):
#    __slots__= ()


class ButcherTree(trees.AbstractUnorderedRootedTree):
    __slots__ = ()

    @classmethod
    def basetree(cls):
        return cls(multiset.FrozenMultiset())

#    @classmethod
#    def basetrees(cls):
#        return cls(multiset.FrozenMultiset())

    def __str__(self):
        if multiset.FrozenMultiset.__len__(self): #  if Non-empty
            return '[' + ','.join([str(elem) for elem in self.elements()]) + ']'
        else:
            return '[]' #TODO: Remove IF.

    @classmethod
    def emptytree(cls):
        return forest.FrozenForest() # TODO: USeful default/choice?
#     def __eq__(self,other):
#         if self is other:
#             return True #  Is this necessary, or is it done automatically?
#         if isinstance(other, type(self)):
#             return self.childtrees == other.childtrees
#         return False

#     def __ne__(self, other):
#         if self is other:
#             return False
#         return self.childtrees != other.childtrees
#         #  TODO: Is it true that two trees evaluate equal iff (with large probability) their hash are equal?


@memoized
def alpha(tree):
    return math.factorial(trees.order(tree)) / (trees.symmetry(tree) * trees.density(tree)) #  Will always come out integer.

def F(tree): #  Elementary differential.
    #if tree == ButcherTree.emptytree:
    #   return 'y'
    result = 'f' + "'" * trees.number_of_children(tree)
    if trees.number_of_children(tree) == 1:
        result += F(tree.keys()[0])
    elif trees.number_of_children(tree) > 1:
        result += '(' + ','.join([F(elem) for elem in tree.elements()]) + ')'
    return result



#class ButcherNotTree(trees.AbstractNotTree, ButcherTreeLike):
#    __slots__ = ()
#    D = forest.FrozenForest([ButcherTree()])

# TODO: FIX THIS
#ButcherTree.emptytree = ButcherNotTree
