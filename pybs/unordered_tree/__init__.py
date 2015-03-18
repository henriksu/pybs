from enum import Enum  # TODO: Note dependency on enum34 in the installation.

treeType = Enum('treeType', 'ordinary binary symmetric')


from pybs.unordered_tree.functions import \
    number_of_trees_of_order, \
    number_of_trees_up_to_order, \
    number_of_tree_pairs_of_total_order
# from pybs.unordered_tree.freeTrees import ?
from pybs.unordered_tree.unordered_tree import \
    UnorderedTree, \
    leaf, \
    the_trees, \
    tree_generator, \
    trees_of_order, \
    FreeTree
