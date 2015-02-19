import unittest
from pybs import unordered_tree

Tree = unordered_tree.UnorderedTrees()


class simple_tree(unittest.TestCase):
    def test_generator(self):
        print "Hello World!"
        gen = Tree.tree_generator(sort=True)
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()
        print gen.next()

    def test_graded_component(self):
        print "graded component"
        gen = Tree.graded_component(4, True)
        for tree in gen:
            print tree
