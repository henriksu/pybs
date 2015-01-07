# This Python file uses the following encoding: utf-8
from pybs.utils import FrozenMultiset as FrozenMultiset
from abstractTrees import \
    AbstractUnorderedRootedTree as AbstractUnorderedRootedTree
# class ButcherTreeLike(trees.AbstractTreeLike):
#     __slots__= ()


class ButcherTree(AbstractUnorderedRootedTree):
    __slots__ = ()

    def __init__(self, arg=None):
        if isinstance(arg, basestring):
            # make '' be the empty tree in the factory.
            if arg == '[]':
                AbstractUnorderedRootedTree.__init__(self)
            elif not (arg[0] == '[' and arg[-1] == ']'):
                raise ValueError('Invalid string')
            else:
                arg = arg[1:-1].split(',')
                childtrees = []
                for elem in arg:
                    childtrees.append(ButcherTree(elem))
                AbstractUnorderedRootedTree.__init__(self, childtrees)
        elif arg is None:
            AbstractUnorderedRootedTree.__init__(self)
        else:
            AbstractUnorderedRootedTree.__init__(self, arg)

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
