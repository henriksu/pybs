# This Python file uses the following encoding: utf-8
from math import factorial

from utils import memoized
from utils.multiset import FrozenMultiset
from trees import FrozenForest, \
    AbstractTreeLike, AbstractUnorderedRootedTree, AbstractNotTree



class ButcherTreeLike(AbstractTreeLike):
    __slots__= ()


class ButcherTree(AbstractUnorderedRootedTree, ButcherTreeLike):
    __slots__ = ()

    @classmethod
    def basetree(cls):
        return cls(FrozenMultiset())

    @classmethod
    def basetrees(cls):
        return cls(FrozenMultiset())

    def __str__(self):
        if FrozenMultiset.__len__(self): #  if Non-empty
            return '[' + ','.join([str(elem) for elem in self.elements()]) + ']'
        else:
            return '*'

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

    @property
    @memoized
    def alpha(self):
        return factorial(self.order) / (self.sigma * self.gamma) #  Will always come out integer.

    @property    
    def F(self): #  Elementary differential.
        #if self == ButcherTree.emptytree:
        #   return 'y'
        result = 'f' + "'" * self.m
        if self.m == 1:
            result += self.keys()[0].F
        elif self.m > 1:
            result += '(' + ','.join([elem.F for elem in self.elements()]) + ')'
        return result

    @property #  Does this really need/ought to be a property? Memoized? NO to the last. For a moderate tree, the forest will be huge.
    def D(self): #  Derivate once more. Perhaps generalize to grafting
        return self.graft(ButcherTree.basetree())


class ButcherNotTree(AbstractNotTree, ButcherTreeLike):
    __slots__ = ()
    D = FrozenForest([ButcherTree()])


ButcherTree.emptytree = ButcherNotTree
