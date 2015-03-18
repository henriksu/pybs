# TODO: Is this useful??
def partition_into_free_trees(list_of_trees):
    result = set()
    for tree in list_of_trees:
        result.add(tree.get_free_tree())
    return result
