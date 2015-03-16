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
        'Ordering based on ordering of representative.'
        if not isinstance(other, type(self)):
            return NotImplemented
        if self is other:
            return 0
        else:
            return self.representative.__cmp__(other.representative)

    def order(self):
        return self.representative.order()



# TODO: Is this useful??
def partition_into_free_trees(list_of_trees):
    result = set()
    for tree in list_of_trees:
        result.add(tree.get_free_tree())
    return result
