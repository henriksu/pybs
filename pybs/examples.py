from pybs.utils import number_of_trees_of_order
from pybs.trees import ButcherTree, ButcherEmptyTree, F, order, \
    number_of_children, density, symmetry, alpha
from pybs.combinations import Forest, differentiate as D, graft, treeCommutator, split, treeGenerator
from pybs.series import BseriesRule, hf_composition, modifiedEquation

print 'The first tree is: ButcherTree() =', ButcherTree()
print 'And the empty tree is: ButcherEmptyTree() =', ButcherEmptyTree()
print 'And since F(ButcherEmptyTree()) =', F(ButcherEmptyTree()), ', we have D(ButcherEmptyTree) =', str(D(ButcherEmptyTree())) + '. Note: The result is a "LinearCombination" containing one "' + str(ButcherTree.basetree()) + '".'
print 'These two first trees can be accessed through ButcherTree.emptytree() =', ButcherTree.emptytree(), 'and ButcherTree.basetree() =', str(ButcherTree.basetree()) + '.'
print 'Some methods for constructing new trees are:'
print '    1. by specifying the forest of child trees to the constructor.'
tree = ButcherTree(Forest([ButcherTree.basetree(), ButcherTree.basetree()]))
print '    Ex.: tree = ButcherTree(Forest([ButcherTree.basetree(), ButcherTree.basetree()])) = ', tree
print '    2. by grafting one tree onto another:'
print '    Ex.: graft(tree, ButcherTree.basetree()) = ', graft(tree, ButcherTree.basetree())
print '    3. by taking the derivative of existing trees.'
print '    Ex.: D(ButcherTree.basetree()) =', D(ButcherTree.basetree())

print 'It is also possible to take the derivative of all the trees in a LinearCOmbination. Starting at the empty tree,'
print 'the n-th derivative is a LinearCombination of all trees of order n, complete with alpha as the multiplicity:'
trees_of_order_1 = D(ButcherTree.emptytree())
print 'trees_of_order_1 = D(ButcherTree.emptytree()) =', trees_of_order_1
trees_of_order_2 = D(trees_of_order_1)
print 'trees_of_order_2 = D(trees_of_order_1) =', trees_of_order_2
trees_of_order_3 = D(trees_of_order_2)
print 'trees_of_order_3 = D(trees_of_order_2) =', trees_of_order_3
trees_of_order_4 = D(trees_of_order_3)
print 'trees_of_order_4 = D(trees_of_order_3) =', trees_of_order_4
trees_of_order_5 = D(trees_of_order_4)
print 'trees_of_order_5 = D(trees_of_order_4) =', trees_of_order_5
print 'The number of trees of a given order can be calculated'
print 'without constructing all the trees: number_of_trees_of_order(30) = ', number_of_trees_of_order(30)
print
print 'Some functions on trees:'
tmp = ButcherTree(Forest([ButcherTree.basetree()]))
t = ButcherTree(Forest([tmp, ButcherTree.basetree()])); del tmp
print 'let t =', str(t) + ', then:'
print 'order(t) = ', order(t)
print 'number_of_children(t) = ', number_of_children(t)
print 'density(t) = ', density(t)
print 'symmetry(t) = ', symmetry(t)
print 'alpha(t) =', alpha(t)
print 'F(t) = "' + F(t) + '" (A string)'
print 't.multiplicities() =', t.multiplicities(),  '(A, list)'
print
print 'Tree commutator: treeCommutator(t, ButcherTree.basetree()) = ', treeCommutator(t, ButcherTree.basetree())
print 'Splitting: split(tree) = ', split(tree)
print
print 'B-series:'
a = BseriesRule('exact')
print "Let a = BseriesRule('exact')"
b = hf_composition(a)
print "Then b = hf_composition(a) gives:"
b = hf_composition(a)
tmp = treeGenerator()
tmp_tree = tmp.next()
print tmp_tree, ', b = ', b(tmp_tree)
tmp_tree = tmp.next()
print tmp_tree, ', b = ', b(tmp_tree)
tmp_tree = tmp.next()
print tmp_tree, ', b = ', b(tmp_tree)
tmp_tree = tmp.next()
print tmp_tree, ', b = ', b(tmp_tree)

c = modifiedEquation(a)
print 'If c = modifiedEquation(a), one gets the B series corresponding to the original equation:'
tmp = treeGenerator()
tmp_tree = tmp.next()
print tmp_tree, ', c = ', c(tmp_tree)
tmp_tree = tmp.next()
print tmp_tree, ', c = ', c(tmp_tree)
tmp_tree = tmp.next()
print tmp_tree, ', c = ', c(tmp_tree)
tmp_tree = tmp.next()
print tmp_tree, ', c = ', c(tmp_tree), '(c is zero for all other trees...)'
print
from pybs.rungekutta.methods import RKmidpoint # A small collection of Butcher tableaus.
print 'And last, but not least, finding the order of an RK method.'
print 'Ex.: The midpoint rule:'
print 'RKmidpoint.printMe():'
RKmidpoint.printMe()
print 'RKmidpoint.order =', RKmidpoint.order
