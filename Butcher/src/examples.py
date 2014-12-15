from src.trees import ButcherTree, ButcherEmptyTree, F, order, number_of_children, density, symmetry, alpha
from src.combinations import Forest, FrozenForest, differentiate as D
import src.rungekutta

print 'The first tree is: ButcherTree() =', ButcherTree()
print 'And the empty tree is: ButcherNotTree() =', ButcherEmptyTree()
print 'And since F(ButcherEmptyTree()) =', F(ButcherEmptyTree()), ', we have D(ButcherEmptyTree) =', str(D(ButcherEmptyTree())) + '. Note: The result is a "LinearCombination" containing one "' + str(ButcherTree.basetree()) + '".'
print 'These two first trees can be accessed through ButcherTree.emptytree() =', ButcherTree.emptytree(), 'and ButcherTree.basetree() =', str(ButcherTree.basetree()) + '.'
print 'So far, new trees can be made:'
print '    1. by taking the derivative of existing trees.'
print '    Ex.: D(ButcherTree.basetree()) =', D(ButcherTree.basetree()), 'Note: The derivative always returns a "LinearCombination".'
print '    2. by specifying the forest of child trees to the constructor.'
print '    Ex.: ButcherTree(Forest([ButcherTree.basetree(), ButcherTree.basetree()])) = ', ButcherTree(Forest([ButcherTree.basetree(), ButcherTree.basetree()]))
print 'It is also possible to take the derivative of all the trees in a LinearCOmbination. Starting at the empty tree,'
print 'the n-th derivative is a LinearCombination of all trees of order n, Complete with alpha as the multiplicity:'
forest_of_trees_of_order_1 = D(ButcherTree.emptytree())
print 'forest_of_trees_of_order_1 = D(ButcherTree.emptytree()) =', forest_of_trees_of_order_1
forest_of_trees_of_order_2 = D(forest_of_trees_of_order_1)
print 'forest_of_trees_of_order_2 = D(forest_of_trees_of_order_1) =', forest_of_trees_of_order_2
forest_of_trees_of_order_3 = D(forest_of_trees_of_order_2)
print 'forest_of_trees_of_order_3 = D(forest_of_trees_of_order_2) =', forest_of_trees_of_order_3
forest_of_trees_of_order_4 = D(forest_of_trees_of_order_3)
print 'forest_of_trees_of_order_4 = D(forest_of_trees_of_order_3) =', forest_of_trees_of_order_4
forest_of_trees_of_order_5 = D(forest_of_trees_of_order_4)
print 'forest_of_trees_of_order_5 = D(forest_of_trees_of_order_4) =', forest_of_trees_of_order_5
print
print 'Further each ButcherTree-object provides some useful properties:'
tmp = ButcherTree(Forest([ButcherTree.basetree()]))
t = ButcherTree(Forest([tmp, ButcherTree.basetree()])); del tmp
print 'let t =', str(t) + ', then:'
print 'order(t) = ', order(t)
print 'number_of_children(t) = ', number_of_children(t)
print 'density(t) = ', density(t)
print 'symmetry(t) = ', symmetry(t)
print 'alpha(t) =', alpha(t)
print 'F(t) = <<' + F(t) + '>> (A string)'
print 'D(t) =', D(t)
print 't.multiplicities() =', t.multiplicities(),  '(Mostly for internal use)'
print
from src.rungekutta.methods import RKmidpoint
print 'One useful application is implemented,'
print 'finding the order of an RK method.'
print 'Ex.: The midpoint rule:'
print 'RKmidpoint.printMe():'
RKmidpoint.printMe()
print 'RKmidpoint.order =', RKmidpoint.order


