# This Python file uses the following encoding: utf-8
import operator
import numpy as np

from src.combinations import TreeGenerator
from src.utils import memoized as memoized
from src.trees import ButcherTree, ButcherEmptyTree, density, order
#  Note the use of dtype=object. It allows for exact algebra.
#  However it is much slower since _np will call Python code.

class RK_method(object):
    def __init__(self, number_of_trees_of_order, b):
        self.number_of_trees_of_order = number_of_trees_of_order #  np array
        self.b = b #  np array
        self._s = self.b.size #  "number_of_trees_of_order" is _s x _s. TODO: Check that number_of_trees_of_order is same.

    def printMe(self): # Simple thing. Look into prettyPrint
        print 'number_of_trees_of_order ='
        print self.number_of_trees_of_order
        print 'b =', self.b

    @property
    @memoized
    def order(self):
        for tree in TreeGenerator(ButcherTree):
            #print tree
            if not self.phi(tree) * density(tree) == 1:
                return order(tree) - 1

    def phi(self, tree): #  elementary weight
        if isinstance(tree, ButcherEmptyTree):
            return 1 # We havent even allowed for non-consistent RK-methods.
        return np.dot(self.b, self.g_vector(tree))[0]

    @memoized
    def g_vector(self, tree):
        g_vector = np.ones((self._s,1), dtype=object)
        def u_vector((subtree, multiplicity)):
            return np.dot(self.number_of_trees_of_order,self.g_vector(subtree)) ** multiplicity
        return reduce(operator.__mul__, map(u_vector, tree.items()), g_vector)
