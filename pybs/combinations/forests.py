# This Python file uses the following encoding: utf-8
from pybs.utils import ClonableMultiset


class Forest(ClonableMultiset):
    """Objects of this class represent forests.

    Forests are initialized by a list of trees.
    Furthermore, multiplication of two forests, ``*``, is overloaded to
    give a new forest containing all the trees of the two original forests.
    """
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
        """The order of the forest.

        The order of a forest is defined to be the sum of the order of
        the member trees, multiplicities included.
        """
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
        "Return *k*, the number of **distinct** trees."
        return self.cardinality()
    # __bool__, __iter__,  is inherited from multiset.


#: Shortand for the empty forest.
#: It is also known as the "empty tree" and
#: denoted :math:`\emptyset` in writing.
empty_tree = Forest()
