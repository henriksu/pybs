from fractions import Fraction
from pybs.utils import memoized


class FreeTree(object):
    def __init__(self, representative):
        # TODO: check that representative IS indeed a representative.
        self.representative = representative
        # TODO: representative.free_tree() = self ?!?
        # TODO: are any properties like symmetry shared by all equivalent trees?
        self.superfluous = _free_tree_is_superfluous(representative)  # TODO: Postpone this untill asked?
        self.rooted_trees = {representative: 1}  # key = euivalent tree, value = binary cappa kappa relative the representative.
        # Gets strange error message from rooted_trees if key is not in it... THROW something.
        self.complete = False  # False signifies incomplete OR unknown.
    # TODO: implement member check?
    # TODO: implement a complete_me(self)
    # TODO: inherit comparison and order from the representative. Implement!
    def __str__(self):
        return str(self.representative)


# TODO: Use weakDict in memoized. Or make it a property on the UnorderedTree.
@memoized
def get_free_tree(tree):
    half_order = Fraction(tree.order(), 2)
    for childtree in tree:
        if childtree.order() > half_order:
            amputated_tree = tree.sub(childtree)
            shifted_tree = childtree.butcher_product(amputated_tree)
            free_tree = get_free_tree(shifted_tree)
            free_tree.rooted_trees[tree] = -free_tree.rooted_trees[shifted_tree]
            return free_tree
    return FreeTree(representative=tree)
    # TODO: collect the partition and decide superfuousness.


def _free_tree_is_superfluous(tree):
    # The assumption of being free-tree-representatie is important!
    if tree.order() % 2 == 1:
        return False  # Odd ordered trees are non-superflous.
    half_order = tree.order() / 2  # TODO: divide/% only once.
    for childtree in tree:
        if childtree.order() == half_order:
            if tree.sub(childtree) == childtree:
                return True
            else:
                return False  # No other possibility will arise.
    return False


def partition_into_free_trees(list_of_trees):
    result = set()
    for tree in list_of_trees:
        free_tree = result.add(get_free_tree(tree))
    for free_tree in result:
        free_tree.complete = True  # TODO: consider wheter or not this is OK.
    return result
