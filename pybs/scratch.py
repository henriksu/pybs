from pybs.utils import number_of_trees_of_order
from pybs.trees import ButcherTree, ButcherEmptyTree, F, order, \
    number_of_children, density, symmetry, alpha
from pybs.combinations import Forest, differentiate as D, graft, treeCommutator, split, treeGenerator
from pybs.series import hf_composition, modified_equation, symplectic_up_to_order
import pybs.rungekutta.methods
from itertools import islice
from sage.structure.list_clone import ClonableElement
from sage.structure.parent import Parent
tmp = pybs.rungekutta.methods.RKimplicitMidpoint
a = tmp.phi

#print symplectic_up_to_order(a, 10)


class A(ClonableElement):
    def foo(self):
        return 'Hello World'


b = ClonableElement(parent=Parent())
b._is_immutable()
