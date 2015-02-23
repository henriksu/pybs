from itertools import product
from pybs.utils import ClonableMultiset as Multiset, memoized
from pybs.unordered_tree import UnorderedTree, leaf
from pybs.combinations import LinearCombination, Forest as Forest
from pybs.combinations import Forest as FrozenForest  # TODO: NASTY HACK
from pybs.combinations import empty_tree


@memoized
def graft(base, other):
    result = LinearCombination()
    if base == empty_tree():
        result += other
        return result  # Just to make sure it is Lincomb.
    elif other == empty_tree():
        result += base
        return result
    else:
        result += base.butcher_product(other)
        for subtree, multiplicity1 in base.items():
            amputated_tree = base.sub(subtree)
            replacements = graft(subtree, other)
            for replacement, multiplicity2 in replacements.items():
#                multiset_of_new_children = amputated_tree.add(replacement)
#                new_tree = type(base)(multiset_of_new_children)
                new_tree = amputated_tree.add(replacement)
                #result2 = LinearCombination()
                #result2[new_tree] = multiplicity1 * multiplicity2
                result[new_tree] += multiplicity1 * multiplicity2
        return result


def split(tree, truncate=False):
    "Splits a tree."
    result = _split(tree)
    if not truncate:
        result[(empty_tree(), tree)] = 1
    return result


def _split(tree):
    result = LinearCombination()
    for childtree, multiplicity in tree.items():
        amputated_tree = tree.sub(childtree)
        result[(amputated_tree, childtree)] = multiplicity
        childSplits = _split(childtree)
        for pair, multiplicity2 in childSplits.items():
            new_tree = amputated_tree.add(pair[0])
            new_pair = (new_tree, pair[1])
            result[new_pair] = multiplicity * multiplicity2
    return result


def subtrees(tree):  # HCK comporudct.
    result = LinearCombination()  # changed from Multiset()
    if tree == empty_tree():
        result += (empty_tree(), empty_tree())
        return result  # TODO: IS THIS NECESSARY?
    result[(Forest((tree,)), empty_tree())] = 1
    tmp = [subtrees(child_tree) for child_tree in tree.elements()]  # TODO: more efficient looping.
    if tmp:
        for item in product(*tmp):  # iterator over all combinations.
            cuttings, to_be_grafted = zip(*item)
            with Forest().clone() as forest_of_cuttings:
                for forest in cuttings:
                    forest_of_cuttings.inplace_multiset_sum(forest)
                #reduce(Forest.inplace_multiset_sum, cuttings, forest_of_cuttings)
            result += (forest_of_cuttings, UnorderedTree(to_be_grafted))
    else:
        result[(empty_tree(), tree)] = 1
    return result
        # TODO: Is there a missing multiplicity?


def differentiate(thing):
    if isinstance(thing, LinearCombination):
        result = LinearCombination()
        for tree, factor in thing.iteritems():
            result += treeD(tree) * factor
    elif isinstance(thing, UnorderedTree):
        result = treeD(thing)
    elif thing == empty_tree():
        result = LinearCombination()
        result += leaf()
    return result


def treeD(tree):
    return graft(tree, leaf())


def linCombCommutator(op1, op2, max_order=None):
    if isinstance(op1, UnorderedTree) or op1 == empty_tree():
        tmp = LinearCombination()
        tmp += op1
        op1 = tmp
    if isinstance(op2, UnorderedTree) or op2 == empty_tree():
        tmp = LinearCombination()
        tmp += op2
        op2 = tmp
    result = LinearCombination()
    for tree1, factor1 in op1.items():
        for tree2, factor2 in op2.items():
            if (not max_order) or tree1.order() + tree2.order() <= max_order:
                result += (factor1 * factor2) * treeCommutator(tree1, tree2)
    return result


def treeCommutator(op1, op2):
    return graft(op1, op2) - graft(op2, op1)
