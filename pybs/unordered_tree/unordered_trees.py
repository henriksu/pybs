from operator import itemgetter, __mul__
from math import factorial
from fractions import Fraction
from copy import copy
from itertools import ifilter, count as _count

from pybs.utils import ClonableMultiset, generate_forest, tikz2svg
from pybs.unordered_tree import treeType, number_of_trees_up_to_order


class UnorderedTree(ClonableMultiset):
    r"""Class whose elements represents unabeled, unordered rooted trees.

    A tree is represented as a multiset of *child trees*.
    That is, the internal organization closely resemples the
    notation :math:`\tau = [\tau_1^{m_1}, \dots, \tau_k^{m_k}]`
    known from the literature.
    """
    # __slots__ = ('__weakref__',)

    def __init__(self, arg=0):
        if isinstance(arg, basestring):
            if not (arg[0] == '[' and arg[-1] == ']'):
                raise ValueError('Invalid string')
            elif arg == '[]':
                ClonableMultiset.__init__(self)
            else:
                arg = arg[1:-1]
                count = 0
                list_of_children = []
                start = 0
                stop = 0
                for char in arg:
                    if char == ',' and count == 0:
                        list_of_children.append(UnorderedTree(arg[start:stop]))
                        start = stop + 1
                        stop = start
                    else:
                        stop += 1
                        if char == '[':
                            count += 1
                        elif char == ']':
                            count -= 1
                list_of_children.append(UnorderedTree(arg[start:stop]))
                ClonableMultiset.__init__(self, list_of_children)
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
        # TODO: Chek. SHouldnt it be "True"?
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

    def _planar_forest_str(self):
        if self:
            return 'b[' + ','.join([elem._planar_forest_str() for elem in sorted(self.elements())]) + ']'
        else:
            return 'b'

    def _repr_svg_(self):  # TODO: REMOVE THE l IN THE NAME!
        # TODO: Implement properly. Rename tikz()?
        the_string = self._planar_forest_str()
        forest_thing = generate_forest(the_string)
        tikz_string = str(forest_thing)
        tikz_string = """\
        \\tikzstyle planar forest=[scale=0.17, sibling distance=0, level distance=0, semithick]
        \\tikzstyle planar forest node=[scale=0.28, shape=circle, semithick, draw]
        \\tikzstyle b=[style=planar forest node, fill=black]
        """ + tikz_string
        svg_data = tikz2svg(tikz_string)
        return svg_data

#    def _repr_latex_(self):
#        the_string = self._planar_forest_str()
#        forest_thing = generate_forest(the_string)
#        tikz_string = str(forest_thing)
#        tikz_string = """\
#        \\tikzstyle planar forest=[scale=0.17, sibling distance=0, level distance=0, semithick]
#        \\tikzstyle planar forest node=[scale=0.28, shape=circle, semithick, draw]
#        \\tikzstyle b=[style=planar forest node, fill=black]
#        """ + tikz_string
#        return '$' + tikz_string + '$'

    def butcher_product(self, other):
        r"""Return the Butcher product
        :math:`self \diamond other`

        The Butcher product is formed by adding *other* to
        the multiset of children of self.
        """
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
        r"""Ordering due to P.Leone (2000) PhD thesis.

        This is a total ordering.
        For most purposes it is just used to define a suitable bijection
        between :math:`T` and :math:`\mathbb{N}`.
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        if self is other or ClonableMultiset.__eq__(self, other):
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

    def _is_symmetric(self):
        if len(self._ms) == 1:
            for tree in self:
                if tree._is_symmetric():
                    return True
                else:
                    return False
        else:
            return False

    def get_free_tree(self):
        if self in the_trees[self.order()]._free_dict:
            return the_trees[self.order()]._free_dict[self]
        else:
            half_order = Fraction(self.order(), 2)
            for childtree in self:
                if childtree.order() > half_order:
                    amputated_tree = self.sub(childtree)
                    shifted_tree = childtree.butcher_product(amputated_tree)
                    free_tree = shifted_tree.get_free_tree()
                    free_tree._rooted_trees[self] = \
                        -free_tree._rooted_trees[shifted_tree]
                    the_trees[self.order()]._free_dict[self] = \
                        free_tree
                    return free_tree
                elif self.order() % 2 == 0 and childtree.order() == half_order:
                    amputated_tree = self.sub(childtree)
                    if childtree < amputated_tree:  # TODO: Check that this corresponds to Muruas convention.
                        shifted_tree = childtree.butcher_product(amputated_tree)
                        free_tree = shifted_tree.get_free_tree()
                        free_tree._rooted_trees[self] = -1
                        the_trees[self.order()]._free_dict[self] = free_tree
                        return free_tree
                    elif childtree == amputated_tree:
                        free_tree = FreeTree(self, superfluous=True)
                        the_trees[self.order()]._free_dict[self] = free_tree
                        return free_tree
                    else:  # non-superfluous
                        free_tree = FreeTree(self, superfluous=False)
                        the_trees[self.order()]._free_dict[self] = free_tree
                        return free_tree
            free_tree = FreeTree(representative=self, superfluous=False)  # Only odd ordered trees.
            the_trees[self.order()]._free_dict[self] = free_tree
            return free_tree

leaf = UnorderedTree()


class Trees(object):
    def __init__(self):
        self._orders = dict()

    def __getitem__(self, order):
        try:
            return self._orders[order]
        except KeyError:
            tree_order = TreeOrder(order, treeType.ordinary)
            self._orders[order] = tree_order
            return tree_order

    def __setitem__(self):
        pass

    def index(self, tree):
        'One indexed total indexing respecting the order.'
        order = tree.order()
        if isinstance(tree, UnorderedTree):
            return number_of_trees_up_to_order(order) + \
                self[order].index(tree) + 1
        elif isinstance(tree, FreeTree):
            return self[order].number_of_free_trees_up_to_order() + \
                self[order].index(tree) + 1

    def non_superfluous_index(self, tree):
        if tree.superfluous:
            raise ValueError
        order = tree.order()
        return self[order].number_of_non_superfluous_trees_up_to_order() + \
            self[order].non_superfluous_index(tree) + 1

the_trees = Trees()


class TreeOrder(object):  # TODO: Find an enum type.
    def __init__(self, order, tree_type=treeType.ordinary):
        self.order = order
        self.tree_type = tree_type
        self._trees = None
        self._trees_are_sorted = False
        self._free_trees = None
        self._free_trees_are_sorted = False
        self._free_trees_are_complete = False
        self._non_superfluous_trees = None
        self._non_superfluous_trees_are_sorted = False
        self._free_dict = dict()
        #self.tree_generator  # TODO: Needed?

    def __hash__(self):  # It appears immutable.
        return hash((hash(self.order), hash(self.tree_type)))

    def __eq__(self, other):
        return self.order == other.order and self.tree_type == other.tree_type

    def trees(self, sort=False):
        if self._trees is not None:
            if not sort:
                return self._trees
            else:  # sort=True
                if self._trees_are_sorted:
                    return self._trees
                else:  # sorting required.
                    self._trees = tuple(sorted(self._trees))
                    self._trees_are_sorted = True
                    return self._trees
        else:  # Must generate the _trees.
            if self.order == 1:
                self._trees = (leaf,)
                self._trees_are_sorted = True
                return self._trees
            else:
                try:
                    previous_trees = the_trees[self.order-1].trees()
                except KeyError:
                    tree_order = TreeOrder(self.order-1, self.tree_type)
                    the_trees[self.order-1] = tree_order
                    previous_trees = tree_order.trees()
            self._trees = set()
            for tree in previous_trees:
                self._trees.update(_graft_leaf(tree))
            if sort:
                self._trees = tuple(sorted(self._trees))  # Tuple to protect from mutability.
                self._trees_are_sorted = True
            else:  # Freeze the set
                self._trees = frozenset(self._trees)  # Modest protection from alteration.
            return self._trees

    def free_trees(self, sort=False):
        # Always use ordinary _trees.
        if self._free_trees_are_complete:
            if (not sort) or self._free_trees_are_sorted:
                return self._free_trees
            else:
                self._free_trees = tuple(sorted(self._free_trees))
                self._free_trees_are_sorted = True
                return self._free_trees
        else:
            self._free_trees = set()
            for t in the_trees[self.order].trees():
                self._free_trees.add(t.get_free_tree())
            self._free_trees_are_complete = True
            if sort:
                self._free_trees = tuple(sorted(self._free_trees))
                self._free_trees_are_sorted = True
            else:
                self._free_trees = frozenset(self._free_trees)
            return self._free_trees

    def number_of_free_trees_up_to_order(self):
        if self.order == 1:
            return 0
        else:
            return the_trees[self.order-1].number_of_free_trees_up_to_order() + \
                len(the_trees[self.order-1].free_trees())

    def non_superfluous_trees(self, sort=False):
        if self._non_superfluous_trees is not None:
            if (not sort) or self._non_superfluous_trees_are_sorted:
                return self._non_superfluous_trees
            else:
                self._non_superfluous_trees = \
                    tuple(sorted(self._non_superfluous_trees))
                self._non_superfluous_trees_are_sorted = True
                return self._non_superfluous_trees
        else:
            self._non_superfluous_trees = \
                filter(lambda free_tree: not free_tree.superfluous,
                       self.free_trees(sort))
            if sort:
                self._non_superfluous_trees = \
                    tuple(sorted(self._non_superfluous_trees))
                self._non_superfluous_trees_are_sorted = True
            else:
                self._non_superfluous_trees = \
                    frozenset(self._non_superfluous_trees)
            return self._non_superfluous_trees

    def number_of_non_superfluous_trees_up_to_order(self):
        if self.order == 1:
            return 0
        else:
            return the_trees[self.order-1].number_of_non_superfluous_trees_up_to_order() + \
                len(the_trees[self.order-1].non_superfluous_trees())

    def index(self, tree):
        'Zero indexed within the order.'
        if isinstance(tree, UnorderedTree):
            return self.trees(True).index(tree)
        elif isinstance(tree, FreeTree):
            return self.free_trees(True).index(tree)

    def non_superfluous_index(self, tree):
        # It's your problem if you enter a rooted tree.
        return self.non_superfluous_trees(True).index(tree)

    def tree_with_index(self, index):
        return self.trees(True)[index]

    def free_tree_with_index(self, index):
        return self.free_trees(True)[index]

    def non_superfluous_tree_with_index(self, index):
        return self.non_superfluous_trees(True)[index]


def tree_generator(sort=False, tree_type=treeType.ordinary):
    if tree_type == treeType.ordinary:
        return _ordinary_tree_generator(sort)


def _ordinary_tree_generator(sort):
    'Yields all _trees by increasing order.'
    for order in _count(1):
        try:
            tree_order = the_trees[order]
            for tree in tree_order.trees(sort):
                yield tree
        except KeyError:  # TreeOrder didn't exist.
            tree_order = TreeOrder(order, treeType.ordinary)
            the_trees[order] = tree_order
            for tree in tree_order.trees(sort):
                yield tree


def trees_of_order(order, sort=False, tree_type=treeType.ordinary):
        return the_trees[order].trees(sort)


def _graft_leaf_on_set(oldSet):
    newSet = set()
    for tree in oldSet:
        newSet.update(_graft_leaf(tree))
    oldSet = newSet
    return oldSet


def _graft_leaf(tree):
    result = set()
    result.add(tree.butcher_product(leaf))
    for subtree in tree.keys():
        amputated_tree = tree.sub(subtree)
        replacements = _graft_leaf(subtree)
        for replacement in replacements:
            with amputated_tree.clone() as tmp:
                tmp.inplace_add(replacement)
            result.add(tmp)
    return result


class FreeTree(object):
    def __init__(self, representative, superfluous=None):
        # TODO: check that representative IS indeed a representative.
        if superfluous is None:
            # TODO: Make sure the free tree is completed.
            representative = representative.get_free_tree()
            self.representative = representative.representative
            self.superfluous = representative.superfluous
        else:
            self.representative = representative
            self.superfluous = superfluous
        # TODO: representative.free_tree() = self ?!?
        # TODO: are any properties like symmetry shared by all equivalent trees?
        self._rooted_trees = {self.representative: 1}  # key = euivalent tree, value = binary cappa kappa relative the representative.
        # Gets strange error message from _rooted_trees if key is not in it... THROW something.
        self.complete = False  # False signifies incomplete OR unknown.
        self._symmetric = None
    # TODO: implement member check?
    # TODO: implement a complete_me(self)
    # TODO: inherit comparison and order from the representative. Implement!

    def __eq__(self, other):
        return self.representative == other.representative

    def __ne__(self, other):
        return self.representative != other.representative

    def __str__(self):
        return str(self.representative)

    def __cmp__(self, other):
        """Ordering based on ordering of representative.

        This is the same as Murua's definition 8 in
        "Formal series and numerical integrators, Part I:
        Systems of ODEs and symplectic integrators",
        except the representative and order conditions are not the same.
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        if self is other:
            return 0
        else:
            return self.representative.__cmp__(other.representative)

    def order(self):
        return self.representative.order()

    def is_symmetric(self):
        if self._symmetric is not None:
            return self._symmetric
        else:
            if not the_trees[self.order()]._free_trees_are_complete:
                    the_trees[self.order()].free_trees(False)  # Complete them for symmetry check.
                    # TODO: Make is_symmetric() force completion of free_tree.
            for tree in self._rooted_trees:
                if tree._is_symmetric():
                    self._symmetric = True
                    return True
            else:  # This else-clause is on the for-loop.
                self._symmetric = False
                return False
