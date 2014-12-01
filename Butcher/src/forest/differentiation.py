from linearCombination import LinearCombination
from trees.ButcherTrees import ButcherTree as ButcherTree

def graft(base, other):
    result = LinearCombination()
    result += base * other # Grafting onto the root.
    for subtree, multiplicity1 in base.items():
        amputated_tree = base.sub(subtree) # Removing one instance of subtree.
        replacements = graft(subtree, other)
        for replacement, multiplicity2 in replacements.items():
            multiset_of_new_children = amputated_tree.add(replacement)
            new_tree = type(base)(multiset_of_new_children)
            result += new_tree * (multiplicity1 * multiplicity2)
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

def TreeGenerator(treetype):
    theSum = LinearCombination(treetype.basetree())
    while True:
        for tree in theSum:
            yield tree
        theSum = differentiate(theSum)
