# This Python file uses the following encoding: utf-8
import operator
import numpy as np

import trees
import forest.differentiation as differentiation
from trees.functions import density, order
import src.utils.miscellaneous
from trees.ButcherTrees import ButcherTree, ButcherEmptyTree
#  Note the use of dtype=object. It allows for exact algebra.
#  However it is much slower since numpy will call Python code.

class RK_method(object):
    def __init__(self, a, b):
        self.a = a #  np array
        self.b = b #  np array
        self.s = self.b.size #  "a" is s x s. TODO: Check that a is same.

    def printMe(self): # Simple thing. Look into prettyPrint
        print 'a ='
        print self.a
        print 'b =', self.b

    @property
    @src.utils.miscellaneous.memoized
    def order(self):
        for tree in differentiation.TreeGenerator(ButcherTree):
            #print tree
            if not self.phi(tree) * density(tree) == 1:
                return order(tree) - 1

    def phi(self, tree): #  elementary weight
        if isinstance(tree, trees.ButcherTrees.ButcherEmptyTree):
            return 1 # We havent even allowed for non-consistent RK-methods.
        return np.dot(self.b, self.g_vector(tree))[0]

    @src.utils.miscellaneous.memoized
    def g_vector(self, tree):
        g_vector = np.ones((self.s,1), dtype=object)
        def u_vector((subtree, multiplicity)):
            return np.dot(self.a,self.g_vector(subtree)) ** multiplicity
        return reduce(operator.__mul__, map(u_vector, tree.items()), g_vector)


if __name__ == "__main__":
    pass


    #print 'phi of basetree: ', RKeuler.phi('*')
    #print 'phi of second-order tree: ', RKeuler.phi('[*]')
    #print 'phi of ', '[*,*]', ': ', RKeuler.phi('[*,*]')
