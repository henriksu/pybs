# This Python file uses the following encoding: utf-8
from numbers import Number

from pybs.utils import Multiset as Multiset, FrozenMultiset as FrozenMultiset
# TODO: Implement the cache miss super fast memoization.


class AbstractUnorderedRootedTree(FrozenMultiset):
    __slots__ = ('__weakref__',)

    def __setattr__(self, *args):
        raise AttributeError

    def __delattr__(self, *args):
        raise AttributeError

    def __init__(self, forest=FrozenMultiset()):
        FrozenMultiset.__init__(self, forest)

    multiplicities = FrozenMultiset.values  # Alias. "Correct" way of doing it?

    @classmethod
    def basetrees(cls):
        raise NotImplementedError

    def alpha(self):
        raise NotImplementedError  # TODO: Implement me.

    def __mul__(self, other):
        if isinstance(other, type(self)):
            new_self = Multiset(self)
            new_self.inplace_add(other)
            return type(self)(new_self)
        elif isinstance(other, Number):
            from pybs.utils.linearCombination import LinearCombination
            # TODO: Nasty work around
            tmp = LinearCombination()
            tmp[self] = other
            return tmp


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
