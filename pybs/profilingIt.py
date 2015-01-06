# This Python file uses the following encoding: utf-8
import cProfile as profile
import pstats


from pybs.trees import ButcherEmptyTree
from pybs.combinations import LinearCombination, differentiate as D


def make_all_trees_up_to_order(n=11):
    theSum = LinearCombination(ButcherEmptyTree())
    for i in xrange(n):
        theSum = D(theSum)

profile.run('make_all_trees_up_to_order()', filename='MinKuleFil')
p = pstats.Stats('MinKuleFil')
# p.strip_dirs()
p.sort_stats('cumtime')
p.print_stats()
pass
