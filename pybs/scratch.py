from pybs.utils import number_of_trees_of_order
from pybs.trees import ButcherTree, ButcherEmptyTree, F, order, \
    number_of_children, density, symmetry, alpha
from pybs.combinations import Forest, differentiate as D, graft, treeCommutator, split, treeGenerator
from pybs.series import hf_composition, modifiedEquation, symplectic_up_to_order
import pybs.rungekutta.methods
from itertools import islice
tmp = pybs.rungekutta.methods.RKimplicitMidpoint
a = tmp.phi

print symplectic_up_to_order(a, 10)
