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
        """Initiate a tree from arguments.

        Possible arguments include strings of the format ``[[],[]]``,
        another :class:`UnorderedTree` and a list/tuple of trees.
        """
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

    multiplicities = ClonableMultiset.values

    def __str__(self):
        """Return a string representation of the format ``[[],[]]``.
        """
        return '[' + \
            ','.join([str(elem) for elem in self.elements()]) + ']'

    def _planar_forest_str(self):
        """Return string for package planar forest.

        Slightly different string representation, e.g. ``b[b,b]``.
        """
        if self:
            return 'b[' + ','.join([elem._planar_forest_str() for elem in
                                    sorted(self.elements())]) + ']'
        else:
            return 'b'

    def _repr_svg_(self):
        """Needed to make IPython draw trees.
        """
        # TODO: Implement properly. Rename tikz()?
        the_string = self._planar_forest_str()
        forest_thing = generate_forest(the_string)
        tikz_string = str(forest_thing)
        tikz_string = """\
        \\tikzstyle planar forest=[scale=0.17, sibling distance=0, \
        level distance=0, semithick]
        \\tikzstyle planar forest node=[scale=0.28, \
        shape=circle, semithick, draw]
        \\tikzstyle b=[style=planar forest node, fill=black]
        """ + tikz_string
        svg_data = tikz2svg(tikz_string)
        return svg_data

    def butcher_product(self, other):
        r"""Return the Butcher product
        :math:`self \circ other`

        The Butcher product is formed by adding ``other`` to
        the multiset of children of self.
        """
        if isinstance(other, type(self)):
            with self.clone() as result:
                result.inplace_add(other)
            return result
        else:
            raise TypeError

    def __eq__(self, other):
        """Check if two UnorderedTrees are equal.

        Done by checking that other is indeed an Unordered tree,
        and the test equality as ClonableMultisets.
        """
        if isinstance(other, UnorderedTree):
            return ClonableMultiset.__eq__(self, other)
        else:
            return NotImplemented

    def __cmp__(self, other):
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
        """Return the total number of vertexes in a tree."""
        result = 1
        for elem, mult in self.items():
            result += mult * elem.order()
        return result

    def number_of_children(self):
        """Return number of children of the root.

        Multiplicities included. To find the number of different child trees
        see ClonableMultiset.no_uniques().
        """
        return sum(self.multiplicities())

    def density(self):
        r"""Return the density, :math:`\gamma`, of a tree.
        """
        result = self.order()
        for elem, mult in self.iteritems():
            result *= elem.density() ** mult
        return result

    def symmetry(self):
        r"""Return the symmetry, :math:`\sigma`, of a tree.
        """
        def _subtree_contribution((tree, multiplicity)):
            return tree.symmetry() ** multiplicity * \
                factorial(multiplicity)
        return reduce(__mul__,
                      map(_subtree_contribution, self.items()), 1)

    def alpha(self):
        r"""Return the :math:`\alpha` of a tree.
        """
        return factorial(self.order()) / \
            (self.symmetry() * self.density())
        # Will always come out integer.

    def F(self):
        """Return elementary differential as a string.

        The returned string is not really suitable for further calculations.
        """
        result = 'f' + "'" * self.number_of_children()
        if self.number_of_children() == 1:
            result += self.keys()[0].F()
        elif self.number_of_children() > 1:
            result += '(' + ','.join([elem.F() for elem in self.elements()]) \
                + ')'
        return result

    def is_binary(self):
        """Check if the :class:`UnorderedTree` is a binary tree."""
        if self.number_of_children() > 2:
            return False
        for subtree in self:
            if not subtree.is_binary():
                return False
        return True

    def is_tall(self):
        """Check if the :class:`UnorderedTree` is a tall tree."""
        if self.number_of_children() > 1:
            return False
        for subtree in self:
            if not subtree.is_tall():
                return False
        return True

    def is_bushy(self):
        """Check if the :class:`UnorderedTree` is a bushy tree."""
        if self == leaf:
            return True
        elif self.keys() == [leaf]:
            return True
        else:
            return False

    def _is_symmetric(self):
        """Used to check if free trees are symmetric."""
        if len(self._ms) == 1:
            for tree in self:
                if tree._is_symmetric():
                    return True
                else:
                    return False
        else:
            return False

    def get_free_tree(self):
        """Return the FreeTree representative of `self`.

        Note that the returned object is not necessarily complete in
        the sense that it knows about all rooted trees it represents.
        To make sure the rooted tree is complete, call
        ``the_trees[self.order()].free_trees()``.
        """
        if self in the_trees[self.order()]._free_dict:
            return the_trees[self.order()]._free_dict[self]
        else:
            half_order = Fraction(self.order(), 2)
            for childtree in self:
                if childtree.order() > half_order:
                    # Shift towards childtree.
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
                    if childtree < amputated_tree:
                        shifted_tree = childtree.butcher_product(
                            amputated_tree)
                        free_tree = shifted_tree.get_free_tree()
                        free_tree._rooted_trees[self] = -1
                    elif childtree == amputated_tree:
                        free_tree = FreeTree(self, superfluous=True)
                    else:  # non-superfluous
                        free_tree = FreeTree(self, superfluous=False)
                    the_trees[self.order()]._free_dict[self] = free_tree
                    return free_tree
            free_tree = FreeTree(representative=self, superfluous=False)
            # Only odd ordered trees.
            the_trees[self.order()]._free_dict[self] = free_tree
            return free_tree


class FreeTree(object):
    """FreeTree-objects represent free trees.

    They are based around the rooted tree representative and
    a dictionary of rooted trees that are equivalent as free trees.
    """
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
        self._rooted_trees = {self.representative: 1}
        # key = euivalent tree,
        # value = binary kappa relative the representative.
        # Gets strange error message from _rooted_trees if key is not in it...
        self.complete = False  # False signifies incomplete OR unknown.
        self._symmetric = None
    # TODO: implement member check?
    # TODO: implement a complete_me(self)
    # TODO: inherit comparison and order from the representative. Implement!

    def __eq__(self, other):
        """FreeTree-objects are considered equal iff their representatives are equal.
        """
        return self.representative == other.representative

    def __ne__(self, other):
        return self.representative != other.representative

    def __str__(self):
        """Return a string reresentative of the free tree.

        This is just the string representative of its
        rooted tree representative.
        """
        return str(self.representative)

    def __cmp__(self, other):
        """Ordering based on ordering of representative.

        """
        if not isinstance(other, type(self)):
            return NotImplemented
        if self is other:
            return 0
        else:
            return self.representative.__cmp__(other.representative)

    def order(self):
        """Return the order of the free tree.

        The order of a free tree is the same as the order of all
        the rooted trees it represents.
        """
        return self.representative.order()

    def is_symmetric(self):
        """Return true if any of its rooted trees are symmetric.
        """
        if self._symmetric is not None:
            return self._symmetric
        else:
            if not the_trees[self.order()]._free_trees_are_complete:
                    the_trees[self.order()].free_trees(False)
                    # Complete them for symmetry check.
                    # TODO: Make is_symmetric() force completion of free_tree.
            for tree in self._rooted_trees:
                if tree._is_symmetric():
                    self._symmetric = True
                    return True
            else:  # This else-clause is on the for-loop.
                self._symmetric = False
                return False


class Trees(object):
    """Class to memoize trees and provide some useful functions.

    One instance, called ``the_trees``, is made as the module is loaded.
    There is no need to make more.

    Main purpose is to be a dictionary of  :class:`TreeOrder` objects.
    The TreeOrder object for trees of order `n` is accessed as
    ``the_trees[n]``.
    If the TreeOrder object does not exist, it will be made by
    the ``the_trees`` object and returned.
    """
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
        r"""Return a tree's index in :math:`T` or :math:`FT`.

        The index starts at 1 and respects to the total ordering.
        If the tree object is a FreeTree,
        the index is only over the free trees.
        """
        order = tree.order()
        if isinstance(tree, UnorderedTree):
            return number_of_trees_up_to_order(order) + \
                self[order].index(tree) + 1
        elif isinstance(tree, FreeTree):
            return self[order].number_of_free_trees_up_to_order() + \
                self[order].index(tree) + 1

    def non_superfluous_index(self, tree):
        """Return the index of a non-superfluous FreeTree.

        Similar to the above, except that only non-superfluous
        trees are given indexes.
        """
        if tree.superfluous:
            raise ValueError
        order = tree.order()
        return self[order].number_of_non_superfluous_trees_up_to_order() + \
            self[order].non_superfluous_index(tree) + 1

the_trees = Trees()


class TreeOrder(object):  # TODO: Find an enum type.
    """A TreeOrder object provides all the trees of a given order.

    It keeps a set or list of the rooted trees,
    the free trees and the non-superluous free trees of a given order.
    The purpose is mainly memoization.
    """
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

#    def __hash__(self):  # OK, since ti does appears immutable to the outside.
#        return hash((hash(self.order), hash(self.tree_type)))
#
#    def __eq__(self, other):
#        return self.order == other.order and self.tree_type == other.tree_type

    def trees(self, sort=False):
        """Return the rooted trees of the order.

        The trees are generated only the first time they are asked for,
        and they are sorted only the first time they are needed sorted.
        This is thus a slightly intricate memoization function.
        The `sort` argument in the following two
        functions serve the same purpose.
        """
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
                self._trees = tuple(sorted(self._trees))
                self._trees_are_sorted = True
            else:  # Freeze the set
                self._trees = frozenset(self._trees)
            return self._trees

    def free_trees(self, sort=False):
        """Return the free trees of the order.

        Similar to ``trees()``. Note that the FreeTree objects are guaranteed
        to know the complete set of rooted trees they represent.
        """
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

    def non_superfluous_trees(self, sort=False):
        """Return the non-superfluous free trees of the order.

        Similar to ``trees()``.
        """
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

    def number_of_free_trees_up_to_order(self):
        """Return the number of free trees up to, but not including the order.

        Calculated by counting.
        """
        if self.order == 1:
            return 0
        else:
            return the_trees[self.order-1].number_of_free_trees_up_to_order() + \
                len(the_trees[self.order-1].free_trees())

    def number_of_non_superfluous_trees_up_to_order(self):
        """Return the number of non-superfluous free trees up to,
        but not including the order.

        Calculated by counting.
        """
        if self.order == 1:
            return 0
        else:
            return the_trees[self.order-1].number_of_non_superfluous_trees_up_to_order() + \
                len(the_trees[self.order-1].non_superfluous_trees())

    def index(self, tree):
        """Return the index of a tree in the order.

        The index starts at zero for the smallest tree of the order.
        If the tree is a FreeTree, the index only counts free trees.
        """
        if isinstance(tree, UnorderedTree):
            return self.trees(True).index(tree)
        elif isinstance(tree, FreeTree):
            return self.free_trees(True).index(tree)

    def non_superfluous_index(self, tree):
        """Return the index of a non-superfluous free tree in the order.

        Just as the ``index()``-method.
        """
        # It's your problem if you enter a rooted tree.
        return self.non_superfluous_trees(True).index(tree)

    def tree_with_index(self, index):
        """Reurn the UnorderedTree with `index` within the order.

        The index starts at zero.
        """
        return self.trees(True)[index]

    def free_tree_with_index(self, index):
        """Reurn the FreeTree with `index` within the order.

        The index starts at zero.
        """
        return self.free_trees(True)[index]

    def non_superfluous_tree_with_index(self, index):
        """Reurn the `index`-th non-superfuous free tree within the order.

        The index starts at zero.
        """
        return self.non_superfluous_trees(True)[index]


leaf = UnorderedTree()


def tree_generator(sort=False, tree_type=treeType.ordinary):
    """Return a generator for all the trees.

    If `sort` is true, the trees are returned in sorted order;
    if not they are returned order by order but otherwise arbitrarily.
    """
    # TODO: Implement tree type.
    if tree_type == treeType.ordinary:
        return _ordinary_tree_generator(sort)


def _ordinary_tree_generator(sort=False):
    """Yields all unordered trees by increasing order.
    """
    for order in _count(1):
            for tree in the_trees[order].trees(sort):
                yield tree


def trees_of_order(order, sort=False, tree_type=treeType.ordinary):
    # Kept for backward compatibility
    return the_trees[order].trees(sort)


def _graft_leaf_on_set(oldSet):
    # Unused.
    newSet = set()
    for tree in oldSet:
        newSet.update(_graft_leaf(tree))
    oldSet = newSet
    return oldSet


def _graft_leaf(tree):
    """Return a set of all trees made by grafting a leaf node on `tree`

    This is the function used to construct all trees of a given order.
    It is **not** the grafting product, since multiplicity is ignored.
    """
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


def partition_into_free_trees(list_of_trees):
    """Return a set of all the free trees from `list_of_trees`.
    """
    result = set()
    for tree in list_of_trees:
        result.add(tree.get_free_tree())
    return result
