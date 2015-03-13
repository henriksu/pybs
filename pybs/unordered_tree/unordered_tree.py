from operator import itemgetter, __mul__
from math import factorial
from copy import copy
from itertools import ifilter


from pybs.utils import ClonableMultiset


class UnorderedTree(ClonableMultiset):
    # __slots__ = ('__weakref__',)

    def __init__(self, arg=0):
        if isinstance(arg, basestring):
            if not (arg[0] == '[' and arg[-1] == ']'):
                raise ValueError('Invalid string')
            elif arg == '[]':
                ClonableMultiset.__init__(self)
            else:
                arg = arg[1:-1].split(',')
                childtrees = []
                for elem in arg:
                    childtrees.append(UnorderedTree(elem))
                ClonableMultiset.__init__(self, childtrees)
        elif arg == 0:
            ClonableMultiset.__init__(self)
        elif isinstance(arg, ClonableMultiset):
            object.__setattr__(self, '_ms', copy(arg._ms))
            object.__setattr__(self, '_hash', None)
            self.set_immutable()
        elif isinstance(arg, dict):
            object.__setattr__(self, '_ms', copy(arg))
            object.__setattr__(self, '_hash', None)
            self.set_immutable()
        else:
            arg = ifilter(lambda x: isinstance(x, UnorderedTree), arg)
            ClonableMultiset.__init__(self, arg)

    def __bool__(self):
        return False

    multiplicities = ClonableMultiset.values

#    def __iter__(self):
#        return self.elements()

    def __str__(self):
        if self:  # if Non-empty
            return '[' + \
                ','.join([str(elem) for elem in self.elements()]) + ']'
        else:
            return '[]'  # TODO: Remove IF.

    def latex(self):
        return str(self)

    def butcher_product(self, other):
        if isinstance(other, type(self)):
            with self.clone() as result:
                result.inplace_add(other)
            return result
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, UnorderedTree):
            return ClonableMultiset.__eq__(self, other)
        else:
            return NotImplemented

    def __cmp__(self, other):  # lt
        'Ordering due to P.Leone (2000) PhD thesis.'
        if not isinstance(other, type(self)):
            return NotImplemented
        if ClonableMultiset.__eq__(self, other):
            return 0
        elif self.order() < other.order():
            return -1
        elif self.order() > other.order():
            return 1
        elif self.number_of_children() < other.number_of_children():
            return -1
        elif self.number_of_children() > other.number_of_children():
            return 1
        else:
            list_a = self.items()
            list_a.sort(key=itemgetter(0))
            list_b = other.items()
            list_b.sort(key=itemgetter(0))
            for (a, b) in zip(list_a, list_b):
                if a != b:
                    if a[0] < b[0]:
                        return -1
                    elif a[0] > b[0]:
                        return 1
                    elif a[1] < b[1]:
                        return 1
                    else:
                        # by now a[1] > b[1] (They cant be equal since
                        # the tuples are unequal)
                        return -1

    def order(self):
        result = 1
        for elem, mult in self.items():
            result += mult * elem.order()
        return result

    def number_of_children(self):
        'Number of children.'
        return sum(self.multiplicities())

    def density(self):
        result = self.order()
        for elem, mult in self.iteritems():
            result *= elem.density() ** mult
        return result

    def symmetry(self):
        def _subtree_contribution((tree, multiplicity)):
            return tree.symmetry() ** multiplicity * \
                factorial(multiplicity)
        return reduce(__mul__,
                      map(_subtree_contribution, self.items()), 1)

    def alpha(self):
        return factorial(self.order()) / \
            (self.symmetry() * self.density())
    # Will always come out integer.

    def F(self):
        'Elementary differential.'
        result = 'f' + "'" * self.number_of_children()
        if self.number_of_children() == 1:
            result += self.keys()[0].F()
        elif self.number_of_children() > 1:
            result += '(' + ','.join([elem.F() for elem in self.elements()]) \
                + ')'
        return result

    def is_binary(self):
        if self.number_of_children() > 2:
            return False
        for subtree in self:
            if not subtree.is_binary():
                return False
        return True

    def is_tall(self):
        if self.number_of_children() > 1:
            return False
        for subtree in self:
            if not subtree.is_tall():
                return False
        return True

    def is_bushy(self):
        if self == leaf:
            return True
        elif self.keys() == [leaf]:
            return True
        else:
            return False


leaf = UnorderedTree()
