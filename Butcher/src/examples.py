from trees.ButcherTrees import ButcherTree, D
from forest import FrozenForest

print 'The first tree is: ButcherTree() =', ButcherTree()
#print 'And the empty tree is: ButcherNotTree() =', ButcherNotTree()
#print 'And since ButcherNotTree().F =', ButcherNotTree().F, 'we have ButcherNotTree.D =', str(ButcherNotTree().D) + '. Note: The result is a "FrozenForest" containing one "' + str(ButcherTree.basetree()) + '".'
print 'These two first trees can be accessed through ButcherTree.emptytree() =', ButcherTree.emptytree(), 'and ButcherTree.basetree() =', str(ButcherTree.basetree()) + '.'
print 'So far, new trees can be made:'
print '    1. by taking the derivative of existing trees.'
print '    Ex.: D(ButcherTree.basetree()) =', D(ButcherTree.basetree()), 'Note: The derivative always returns a "FrozenForest".'
print '    2. by specifying the forest of child trees to the constructor.'
print '    Ex.: ButcherTree(FrozenForest([ButcherTree.basetree(), ButcherTree.basetree()])) = ', ButcherTree(FrozenForest([ButcherTree.basetree(), ButcherTree.basetree()]))
print 'It is also possible to derivate all the trees in a FrozenForest. Starting at the empty tree,'
print 'the n-th derivative is the FrozenForest of all trees of order n. Complete with alpha as the multiplicity (check this claim):'
forest_of_trees_of_order_1 = D(ButcherTree.emptytree())
print 'forest_of_trees_of_order_1 = ButcherTree.emptytree().D =', forest_of_trees_of_order_1
forest_of_trees_of_order_2 = D(forest_of_trees_of_order_1)
print 'forest_of_trees_of_order_2 = forest_of_trees_of_order_1.D() =', forest_of_trees_of_order_2
forest_of_trees_of_order_3 = forest_of_trees_of_order_2.D()
print 'forest_of_trees_of_order_3 = forest_of_trees_of_order_2.D() =', forest_of_trees_of_order_3
forest_of_trees_of_order_4 = forest_of_trees_of_order_3.D()
print 'forest_of_trees_of_order_4 = forest_of_trees_of_order_3.D() =', forest_of_trees_of_order_4
forest_of_trees_of_order_5 = forest_of_trees_of_order_4.D()
print 'forest_of_trees_of_order_5 = forest_of_trees_of_order_4.D() =', forest_of_trees_of_order_5
print
print 'Further each ButcherTree-object provides some useful properties:'
tmp = ButcherTree(FrozenForest([ButcherTree.basetree()]))
t = ButcherTree(FrozenForest([tmp, ButcherTree.basetree()])); del tmp
print 'let t =', str(t) + ', then:'
print 't.order = t.order =', t.order
print 't.numer_of_children = t.m =', t.m
print 't.density = t.gamma =', t.gamma
print 't.symmetry = t.sigma =', t.sigma
print 't.alpha =', t.alpha
print 't.F = <<' + t.F + '>> (A string)'
print 't.D =', t.D
print 't.multiplicities() =', t.multiplicities(),  '(Mostly for internal use)'
print
from rungekutta.methods import RKmidpoint
print 'One useful application is implemented,'
print 'finding the order of an RK method.'
print 'Ex.: The midpoint rule:'
print 'RKmidpoint.printMe():'
RKmidpoint.printMe()
print 'RKmidpoint.order =', RKmidpoint.order


