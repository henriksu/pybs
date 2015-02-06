# This Python file uses the following encoding: utf-8
from operator import itemgetter
from itertools import ifilter
from functools import total_ordering

from pybs.utils import FrozenMultiset as FrozenMultiset, Multiset as Multiset
from abstractTrees import \
    AbstractUnorderedRootedTree as AbstractUnorderedRootedTree
# class ButcherTreeLike(trees.AbstractTreeLike):
#     __slots__= ()


@total_ordering
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
        elif isinstance(arg, Multiset):  # Catching ButcherTree(Forest).
            object.__setattr__(self, '_ms', Multiset(arg))
            object.__setattr__(self, '_hash', None)
        else:
            # arg is iterable. Cleaning ButcherEmptyTree.
            arg = ifilter(lambda x: isinstance(x, ButcherTree), arg)
            object.__setattr__(self, '_ms', Multiset(arg))
            object.__setattr__(self, '_hash', None)

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

    def __lt__(self, other):
        'Ordering due to P.Leone (2000) PhD thesis.'
        from functions import order, number_of_children
        if self == other:
            return False  # Quicker, and necessary for the empty tree.
        elif order(self) < order(other):
            return True
        elif order(self) > order(other):
            return False
        elif number_of_children(self) < number_of_children(other):
            return True
        elif number_of_children(self) > number_of_children(other):
            return False
        else:
            list_a = self.items()
            list_a.sort(key=itemgetter(0))
            list_b = other.items()
            list_b.sort(key=itemgetter(0))
            for (a, b) in zip(list_a, list_b):
                if a != b:
                    if a[0] < b[0]:
                        return True
                    elif a[0] > b[0]:
                        return False
                    elif a[1] < b[1]:
                        return False
                    else:
                        # by now a[1] > b[1] (They cant be equal since
                        # the tuples are unequal)
                        return True
#                else:
#                    pass


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
