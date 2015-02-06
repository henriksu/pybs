from itertools import product
from pybs.utils import Multiset as Multiset, memoized
from pybs.trees import ButcherTree, ButcherEmptyTree, order
from pybs.combinations import LinearCombination, Forest, FrozenForest


@memoized
def graft(base, other):
    result = LinearCombination()
    if isinstance(base, ButcherEmptyTree):
        result += other
        return result  # Just to make sure it is Lincomb.
    elif isinstance(other, ButcherEmptyTree):
        result += base
        return result
    result += base * other  # Grafting onto the root.
    for subtree, multiplicity1 in base.items():
        amputated_tree = base.sub(subtree)  # Removing one instance of subtree.
        replacements = graft(subtree, other)
        for replacement, multiplicity2 in replacements.items():
            multiset_of_new_children = amputated_tree.add(replacement)
            new_tree = type(base)(multiset_of_new_children)
            result += new_tree * (multiplicity1 * multiplicity2)
    return result


def split(tree, truncate=False):
    if tree == ButcherEmptyTree():
        raise ValueError('Can not split the empty tree')
    result = _split(tree)
    if not truncate:
        result[(ButcherEmptyTree(), tree)] = 1
    return result


def _split(tree):
    result = Multiset()
    for childtree, multiplicity in tree.items():
        amputated_tree = tree.sub(childtree)
        result[(type(tree)(amputated_tree), childtree)] = multiplicity
        childSplits = _split(childtree)
        for pair, multiplicity2 in childSplits.items():
            multiset_of_new_children = amputated_tree.add(pair[0])
            new_tree = type(tree)(multiset_of_new_children)
            new_pair = (new_tree, pair[1])
            result[new_pair] = multiplicity * multiplicity2
    return result


def subtrees(tree):
    if tree == ButcherEmptyTree():
        raise ValueError('Can not split the empty tree')
    result = Multiset()

    result[(ButcherEmptyTree(), FrozenForest((tree,)))] = 1
    tmp = [subtrees(sub_tree) for sub_tree in tree.elements()]
    if tmp:
        for item in product(*tmp):  # iterator over all combinations.
            to_be_grafted, cuttings = zip(*item)
            new_forest_of_cuttings = \
                reduce(Forest.inplace_multiset_sum, cuttings, Forest())
            result.inplace_add((ButcherTree(to_be_grafted), FrozenForest(new_forest_of_cuttings)))
    else:
        result[(tree, FrozenForest())] = 1
    return result
        # TODO: Is there a missing multiplicity?


def differentiate(thing):
    if isinstance(thing, LinearCombination):
        result = LinearCombination()
        for tree, factor in thing.iteritems():
            result += treeD(tree) * factor
    elif isinstance(thing, ButcherTree):
        result = treeD(thing)
    elif isinstance(thing, ButcherEmptyTree):
        result = LinearCombination()
        result += ButcherTree.basetree()
    return result


def treeD(tree):
    return graft(tree, ButcherTree.basetree())


def linCombCommutator(op1, op2, max_order=None):
    if isinstance(op1, ButcherTree) or isinstance(op1, ButcherEmptyTree):
        tmp = LinearCombination()
        tmp += op1
        op1 = tmp
    if isinstance(op2, ButcherTree) or isinstance(op2, ButcherEmptyTree):
        tmp = LinearCombination()
        tmp += op2
        op2 = tmp
    result = LinearCombination()
    for tree1, factor1 in op1.items():
        for tree2, factor2 in op2.items():
            if (not max_order) or order(tree1) + order(tree2) <= max_order:
                result += (factor1 * factor2) * treeCommutator(tree1, tree2)
    return result


def treeCommutator(op1, op2):
    return graft(op1, op2) - graft(op2, op1)


def treeGenerator():
    'Yields all trees, including empty tree, by increasing order.'
    theSum = LinearCombination(ButcherEmptyTree())
    while True:
        for tree in theSum:
            yield tree
        theSum = differentiate(theSum)


def trees_of_order(n):
    theSum = LinearCombination(ButcherEmptyTree())
    for i in xrange(n):
        theSum = differentiate(theSum)
    for tree in theSum:
        yield tree
