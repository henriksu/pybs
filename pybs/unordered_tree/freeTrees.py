from fractions import Fraction
from pybs.utils import memoized


class FreeTree(object):
    def __init__(self, representative, superfluous=None):
        # TODO: check that representative IS indeed a representative.
        if superfluous is None:
            # TODO: Make sure the free tree is completed.
            representative = get_free_tree(representative)
            self.representative = representative.representative
            self.superfluous = representative.superfluous
        else:
            self.representative = representative
            self.superfluous = superfluous
        # TODO: representative.free_tree() = self ?!?
        # TODO: are any properties like symmetry shared by all equivalent trees?
        self.rooted_trees = {self.representative: 1}  # key = euivalent tree, value = binary cappa kappa relative the representative.
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
        elif tree.order() % 2 == 0 and childtree.order() == half_order:
            amputated_tree = tree.sub(childtree)
            if childtree < amputated_tree:  # TODO: Check that this corresponds to Muruas convention.
                shifted_tree = childtree.butcher_product(amputated_tree)
                free_tree = get_free_tree(shifted_tree)
                free_tree.rooted_trees[tree] = -1
                return free_tree
            elif childtree == amputated_tree:
                return FreeTree(tree, superfluous=True)
            else:  # non-superfluous
                return FreeTree(tree, superfluous=False)
    return FreeTree(representative=tree, superfluous=False)  # Only odd ordered trees.
    # TODO: collect the partition.


def partition_into_free_trees(list_of_trees):
    result = set()
    for tree in list_of_trees:
        free_tree = result.add(get_free_tree(tree))
    for free_tree in result:
        free_tree.complete = True  # TODO: consider wheter or not this is OK.
    return result
