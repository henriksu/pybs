from operator import itemgetter
import math
import operator
import sage.all
from sage.combinat.abstract_tree import AbstractClonableTree
# from sage.combinat.rooted_tree import *
from pybs.utils import ClonableMultiset

from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.parent import Parent
from sage.categories.sets_cat import Sets
from sage.categories.sets_with_grading import SetsWithGrading
from sage.sets.disjoint_union_enumerated_sets import \
    DisjointUnionEnumeratedSets
from sage.sets.non_negative_integers import NonNegativeIntegers


class UnorderedTree(ClonableMultiset):
    # __slots__ = ('__weakref__',)

    def __init__(self, parent, iterable=0, *args, **kwargs):
        ClonableMultiset.__init__(self, parent, iterable, *args, **kwargs)

    def is_empty(self):
        return False

    multiplicities = ClonableMultiset.values

    def __iter__(self):
        return self.elements()

    def __str__(self):
        if self:  # if Non-empty
            return '[' + \
                ','.join([str(elem) for elem in self.elements()]) + ']'
        else:
            return '[]'  # TODO: Remove IF.

    def _latex_(self):
        return str(self)

    def butcherproduct(self, other):
        if isinstance(other, type(self)):
            with self.clone() as result:
                result.inplace_add(other)
            return result
        else:
            raise TypeError

    def __cmp__(self, other):  # lt
        'Ordering due to P.Leone (2000) PhD thesis.'
        if self == other:
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
    grade = order  # Used by ...

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
                math.factorial(multiplicity)
        return reduce(operator.__mul__,
                      map(_subtree_contribution, self.items()), 1)

    def alpha(self):
        return math.factorial(self.order()) / \
            (self.symmetry() * self.density())
    # Will always come out integer.

    def F(self):
        'Elementary differential.'
        result = 'f' + "'" * self.number_of_children()
        if self.number_of_children() == 1:
            result += self.keys()[0].F()
        elif self.number_of_children() > 1:
            result += '(' + ','.join([elem.F() for elem in self.elements()]) + ')'
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
        if self == UnorderedTrees().leaf():
            return True
        elif self.keys() == [UnorderedTrees().leaf()]:
            return True
        else:
            return False

    # iter(T) itererer over barna.
    # T.parent().labeled_trees() er "oensket".
    # T.depth()
    # T.node_number() Tilsvarer "order".
    # T.subtrees() generator rekursivt over alle traer. (ikke kejnt for meg)
    # T.tree_factorial()
    # T.to/from_hexacode() kanskje?

    # T.to_poset(root_to_leaf=False)
    # T.to_undirected_graph()
    # T.grade() = order(T)


class UnorderedTrees(UniqueRepresentation, Parent):
    Element = UnorderedTree

    def __init__(self):
        Parent.__init__(self, category=SetsWithGrading())

    def _element_constructor_(self, *args, **keywords):
        return self.element_class(self, *args, **keywords)

    def leaf(self):
        return self.element_class(self)

#    def generating_series(self):
#        pass  # TODO: Do I need it?

    def tree_generator(self, sort=False):
        'Yields all trees by increasing order.'
        oldSet = set([self.leaf()])
        while True:
            for tree in oldSet:
                yield tree
            newSet = set()
            for tree in oldSet:
                newSet.update(self.graft_leaf(tree))
            if sort:
                oldSet = sorted(newSet)
            else:
                oldSet = newSet

    def graft_leaf_on_set(self, oldSet):
        newSet = set()
        for tree in oldSet:
            newSet.update(self.graft_leaf(tree))
        oldSet = newSet
        return oldSet

    def graft_leaf(self, tree):
        result = set()
        result.add(tree.butcherproduct(self.leaf()))
        for subtree in tree.keys():
            amputated_tree = tree.sub(subtree)
            replacements = self.graft_leaf(subtree)
            for replacement in replacements:
                with amputated_tree.clone() as tmp:
                    tmp.inplace_add(replacement)
                result.add(tmp)
        return result

    def graded_component(self, grade, sort=False):
        oldSet = set([self.leaf()])
        for _ in range(grade-1):
            oldSet = self.graft_leaf_on_set(oldSet)
        if sort:
            oldSet = sorted(oldSet)
        for tree in oldSet:
            yield tree


class UnorderedTrees_all(DisjointUnionEnumeratedSets, UnorderedTrees):

    def __init__(self):
        pass
    # labeled_tree)() ?????
    # WSunlabaled_trees()


class UnorderedTrees_size(UnorderedTrees):
    def __init__(self, ):
        pass
    # .cardinality() og .element_class() er de viktigste nye.
