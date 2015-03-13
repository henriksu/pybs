from enum import Enum  # TODO: Note dependency on enum34 in the installation.
from operator import __add__ as _add
from itertools import imap as _imap, count as _count

from pybs.utils import memoized
from pybs.unordered_tree import leaf

treeType = Enum('treeType', 'ordinary binary symmetric')
tree_pool = dict()
tree_pool[treeType.ordinary] = dict()  # TODO: Implement
tree_pool[treeType.binary] = dict()  # TODO: Implement


#class TreeType(object):
#    # TODO: memoize me?
#    def __init__(self, name='ordinary'):
#        pass


class TreeOrder(object):  # TODO: Find an enum type.
    def __init__(self, order, tree_type=treeType.ordinary):
        self.order = order
        self.tree_type = tree_type
        self.trees = None
        self.trees_are_sorted = False
        self.free_trees = None
        #self.tree_generator  # TODO: Needed?

    def __hash__(self):  # It appears immutable.
        return hash((hash(self.order), hash(self.tree_type)))

    def __eq__(self, other):
        return self.order == other.order and self.tree_type == other.tree_type

    def trees_of_order(self, sort=False):
        if self.trees is not None:
            if not sort:
                return self.trees
            else:  # sort=True
                if self.trees_are_sorted:
                    return self.trees
                else:  # sorting required.
                    self.trees = sorted(self.trees)
                    self.trees_are_sorted = True
                    return self.trees
        else:  # Must generate the trees.
            if self.order == 1:
                self.trees = (leaf,)
                self.trees_are_sorted = True
                return self.trees
            else:
                try:
                    previous_trees = tree_pool[self.tree_type][self.order-1].trees_of_order()
                except KeyError:
                    tree_order = TreeOrder(self.order-1, self.tree_type)
                    tree_pool[self.tree_type][self.order-1] = tree_order
                    previous_trees = tree_order.trees_of_order()
            self.trees = set()
            for tree in previous_trees:
                self.trees.update(_graft_leaf(tree))
            if sort:
                self.trees = tuple(sorted(self.trees))  # Tuple to protect from mutability.
                self.trees_are_sorted = True
            else:  # Freeze the set
                self.trees = frozenset(self.trees)  # Modest protection from alteration.
            return self.trees


def tree_generator(sort=False, tree_type=treeType.ordinary):
    if tree_type == treeType.ordinary:
        return ordinary_tree_generator(sort)


def ordinary_tree_generator(sort):
    'Yields all trees by increasing order.'
    for order in _count(1):
        try:
            tree_order = tree_pool[treeType.ordinary][order]
            for tree in tree_order.trees_of_order(sort):
                yield tree
        except KeyError:  # TreeOrder didn't exist.
            tree_order = TreeOrder(order, treeType.ordinary)
            tree_pool[treeType.ordinary][order] = tree_order
            for tree in tree_order.trees_of_order(sort):
                yield tree


def trees_of_order(order, sort=False, tree_type=treeType.ordinary):
    try:
        return tree_pool[tree_type][order].trees_of_order(sort)
    except KeyError:
        tree_order = TreeOrder(order, treeType.ordinary)
        tree_pool[treeType.ordinary][order] = tree_order
        return tree_order.trees_of_order(sort)


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


@memoized
def number_of_trees_of_order(n):
    if n < 2:
        return n
    result = 0
    for k in range(1, n):
        result += k * number_of_trees_of_order(k) * _s(n-1, k)
    return result / (n - 1)


@memoized
def _s(n, k):
    result = 0
    for j in range(1, n/k + 1):
        result += number_of_trees_of_order(n+1-j*k)
    return result
# Joe Riel (joer(AT)san.rr.com), Jun 23 2008


def number_of_tree_pairs_of_total_order(n):
    "Needed for conjugate symplectic check. Known as m_n. \
    Taken from Hairer et al. \
    On Conjugate symplecticity of B-series integrators"
    # TODO: Implement general formula instead of table lookup.
    table = [0, 0, 1, 1, 3, 6, 16, 37, 96, 239, 622, 1607, 4235]
    return table[n]


def number_of_trees_up_to_order(n):
    '''Number of trees up to and including order n.'''
    return reduce(_add, _imap(number_of_trees_of_order, xrange(n + 1)), 0)
