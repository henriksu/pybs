#!/usr/bin/env sage -python #  TODO: Add to all files.
# This Python file uses the following encoding: utf-8
import cProfile as profile
import pstats
from sage.all import *

from forest import Forest
from trees.ButcherTrees import ButcherTree

def make_all_trees_up_to_order(n=11):
    basetree = ButcherTree(Forest())
    base_forest = Forest([basetree])
    result = [len(base_forest)]
    for i in xrange(n):
        base_forest = base_forest.D()
        result.append(len(base_forest))

profile.run('make_all_trees_up_to_order()', filename='MinKuleFil')
p = pstats.Stats('MinKuleFil')
#p.strip_dirs()
p.sort_stats('cumtime')
p.print_stats()
pass