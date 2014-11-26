# This Python file uses the following encoding: utf-8
from src.utils.multiset import Multiset as Multiset, FrozenMultiset as FrozenMultiset


class AbstractForest(object):
    __slots__ = ()

    def __str__(self):
        return '(' + ', '.join([str(tree) + '^' + str(self[tree]) for tree in self]) + ')'

#     def D(self):
#         result = Forest()
#         for tree, multiplicity in self.iteritems():
#             result.inplace_multiset_sum( tree.D.scalar_mul(multiplicity) )
#         return result


class Forest(AbstractForest, Multiset):
    __slots__ = ()
    multiplicities = Multiset.values #  Alias. "Correct" way of doing it?

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], FrozenMultiset):
            Multiset.__init__(self, args[0]._ms)
        else:
            Multiset.__init__(self, *args, **kwargs)


class FrozenForest(AbstractForest, FrozenMultiset):
    __slots__ = ()
    multiplicities = FrozenMultiset.values

if __name__ == '__main__':
    a = FrozenForest({'a':1, 'b':2})
    pass