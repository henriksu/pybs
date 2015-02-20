# This Python file uses the following encoding: utf-8
from pybs.utils import ClonableMultiset


class Forest(ClonableMultiset):
    __slots__ = ()
    multiplicities = ClonableMultiset.values
    # TODO: Alias. "Correct" way of doing it?

    def __init__(self, arg=0):
        if arg and isinstance(arg, ClonableMultiset):
            ClonableMultiset.__init__(self, arg._ms)
        else:
            ClonableMultiset.__init__(self, arg)

    def __str__(self):
        return '(' + ', '.join([str(tree) + '^' + str(self[tree])
                                for tree in self]) + ')'

    def __mul__(self, other):
        return self.multiset_sum(other)

    def order(self):
        result = 0
        for tree, multiplicity in self:
            result += tree.order() * multiplicity
        return result

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return ClonableMultiset.__eq__(self, other)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return ClonableMultiset.__ne__(self, other)
        return NotImplemented

    def number_of_trees(self):
        return self.cardinality()
    # __bool__, __iter__,  is inherited from multiset.


def empty_tree():
    return Forest()
