from linearCombination import LinearCombination
from trees.ButcherTrees import ButcherTree as ButcherTree

def graft(base,other):
    result = LinearCombination()
    new_tree = base * other
    result += new_tree
    for subtree, multiplicity1 in base.items():
        amputated_tree = base.sub(subtree)
        sum_of_replacements = graft(subtree, other)
        for sub_diff, multiplicity2 in sum_of_replacements.items():
            multiset_of_new_children = amputated_tree.add(sub_diff)
            new_tree2 = type(base)(multiset_of_new_children)
            result += new_tree2 * (multiplicity1 * multiplicity2)
    return result

def differentiate(thing):
    if isinstance(thing, LinearCombination):
        result = LinearCombination()
        for tree, factor in thing.iteritems():
            result += treeD(tree) * factor
    elif isinstance(thing, ButcherTree):
        result = treeD(thing)
    return result

def treeD(tree):
    return graft(tree, ButcherTree.basetree())
