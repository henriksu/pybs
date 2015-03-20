from pybs.rungekutta.methods import RKeuler, RKimplicitEuler
from pybs.unordered_tree import tree_generator
from pybs.series import series_commutator

a = RKimplicitEuler.phi()
for tree in tree_generator():
    if tree.order() == 5:
        break
    print tree, a(tree)

b = RKeuler.phi()
c = series_commutator(a, b)
for tree in tree_generator(sort=True):
    if tree.order() == 6:
        break
    print tree, c(tree)
