from enum import Enum  # TODO: Note dependency on enum34 in the installation.
from operator import __add__ as _add
from itertools import imap as _imap

from pybs.utils import memoized
from pybs.unordered_tree import leaf

treeType = Enum('treeType', 'ordinary binary symmetric')
tree_pool = dict()
tree_pool[treeType.ordinary] = dict()  # TODO: Implement
tree_pool[treeType.binary] = dict()  # TODO: Implement
tree_pool[treeType.symmetric] = dict()  # NEEDED? TODO: Implement


#class TreeType(object):
#    # TODO: memoize me?
#    def __init__(self, name='ordinary'):
#        pass


class TreeOrder(object):  # TODO: Find an enum type.
    def __init__(self, order, tree_type=treeType.ordinary):
        self.order = order
        self.tree_type = tree_type
        self.trees = None
        self.free_trees = None
        self.tree_generator  # TODO: Needed?


def tree_generator(sort=False):
    'Yields all trees by increasing order.'
    oldSet = set([leaf])
    while True:
        for tree in oldSet:
            yield tree
        newSet = set()
        for tree in oldSet:
            newSet.update(_graft_leaf(tree))
        if sort:
            oldSet = sorted(newSet)
        else:
            oldSet = newSet


def trees_of_order(order, sort=False, tree_type=treeType.ordinary):
    oldSet = set([leaf])
    for _ in range(order-1):
        oldSet = _graft_leaf_on_set(oldSet)
    if sort:
        oldSet = sorted(oldSet)
    for tree in oldSet:
        yield tree


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
