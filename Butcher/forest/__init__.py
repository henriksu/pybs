# This Python file uses the following encoding: utf-8
#from collections import Counter
#from utils import FrozenCounter
from utils.multiset import Multiset as Multiset, FrozenMultiset as FrozenMultiset
from copy import copy

class AbstractForest(object):
    __slots__ = ()

    def __str__(self):
        return '(' + ', '.join([str(tree) + '^' + str(self[tree]) for tree in self]) + ')'

    def __add__(self, other): # Slow backup.
        new_self = Forest(self) # TODO: This line will cause problems with FrozenMultiset.
        new_self.update((other,))
        return type(self)(new_self)

    def __mul__(self, other):
        if isinstance(other, int):
            return type(self)(dict(((key, other*value) for (key, value) in self.iteritems()))) #  TODO: This is a nasty workaround.
        else:
            raise NotImplementedError #  TODO: Throw what python wants in such cases

    def __sub__(self, other): # TODO: Do these calculations on multisets, not forest...
        new_self = Forest(self)
        new_self.subtract((other,))
        if new_self[other] == 0:
            del new_self[other]
        return type(self)(new_self)

    def D(self):
        result = Forest()
        for tree, multiplicity in self.iteritems():
            result.update(tree.D * multiplicity)
        return result


class Forest(Multiset, AbstractForest):
    __slots__ = ()
    multiplicities = Multiset.values #  Alias. "Correct" way of doing it?

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], FrozenMultiset):
            Multiset.__init__(self, args[0]._ms)
        else:
            Multiset.__init__(self, *args, **kwargs)

    def __add__(self, other):
        new_self = Forest(self) # TODO: This line will cause problems with FrozenMultiset.
        new_self.update((other,))
        return new_self



class FrozenForest(FrozenMultiset, AbstractForest): #  In effect a frozen Multiset with some tree specific functions.
    __slots__ = ()
    multiplicities = FrozenMultiset.values #  Alias. "Correct" way of doing it?

    def __add__(self, other):
        new_self = Forest(self) # TODO: This line will cause problems with FrozenMultiset.
        new_self.update((other,))
        return FrozenForest(new_self)


if __name__ == '__main__':
    a = FrozenForest({'a':1, 'b':2})
    pass