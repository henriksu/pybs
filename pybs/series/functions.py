from pybs.unordered_tree import trees_of_order


def tree_pairs_of_order(order, sort=False):
    "Returns a list of tuples of functions. \
    Each tuple considered as an unordered pair is returned exactly once."
    result = []
    max_order = order / 2  # Intentional truncation in division.
    for order1 in range(1, max_order + 1):
        order2 = order - order1
        # Sorting is important for reproducability.
        for tree1 in trees_of_order(order1, sort):
            for tree2 in trees_of_order(order2, sort):
                # TODO: I think some trees are repeated! Merge with the other similar case.
                if (order1 != order2) or \
                   ((order1 == order2) and (tree2, tree1) not in result):
                    result.append((tree1, tree2))
    return result


def tree_tuples_of_order(order):
    """Unsorted list of tuples such that the sum of the
    orders of the two trees in a tuple is *order*.
    """
    for order1 in range(1, order):
        order2 = order - order1
        for tree1 in trees_of_order(order1):
            for tree2 in trees_of_order(order2):
                yield (tree1, tree2)
