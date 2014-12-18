# This Python file uses the following encoding: utf-8
from src.utils import FrozenMultiset as FrozenMultiset
from abstractTrees import \
    AbstractUnorderedRootedTree as AbstractUnorderedRootedTree
# class ButcherTreeLike(trees.AbstractTreeLike):
#     __slots__= ()


class ButcherTree(AbstractUnorderedRootedTree):
    __slots__ = ()

    @classmethod
    def basetree(cls):
        return cls(FrozenMultiset())

#    @classmethod
#    def basetrees(cls):
#        return cls(multiset.FrozenMultiset())

    def __str__(self):
        if FrozenMultiset.__len__(self):  # if Non-empty
            return '[' + \
                ','.join([str(elem) for elem in self.elements()]) + ']'
        else:
            return '[]'  # TODO: Remove IF.

    @classmethod
    def emptytree(cls):
        return ButcherEmptyTree()
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
#         #  TODO: Is it true that two trees evaluate equal iff
#                  (with large probability) their hash are equal?


class ButcherEmptyTree(object):
    def __eq__(self, other):
        if isinstance(other, ButcherEmptyTree):
            return True
        else:
            return False

    def __str__(self):
        return 'Ø'

    def __repr__(self):
        return 'ButcherEmptyTree()'
# TODO: FIX THIS
# ButcherTree.emptytree = ButcherEmptyTree
