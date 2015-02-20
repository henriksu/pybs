import unittest
from pybs import unordered_tree


class simple_tree(unittest.TestCase):
    def test_generator(self):
        print "Hello World!"
        gen = unordered_tree.tree_generator(sort=True)
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()

    def test_graded_component(self):
        print "graded component"
        gen = unordered_tree.trees_of_order(4, True)
        for tree in gen:
            print tree
