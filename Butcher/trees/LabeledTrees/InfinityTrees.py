# This Python file uses the following encoding: utf-8
from itertools import count
from trees.LabeledTrees import AbstractLabeledTreeLike, AbstractLabeledTree, AbstractLabeledNotTree
from forest import FrozenForest
#from utils import memoized


class InfinityTreeLike(AbstractLabeledTreeLike):
    __slots__ = ()


class InfinityTree(AbstractLabeledTree, InfinityTreeLike):
    def __init__(self, label, forest=FrozenForest()):
        AbstractLabeledTree.__init__(self, label, forest)

    @classmethod
    def variable_label(cls, label):
        str(label)

    @classmethod
    def node_sign(cls, label):
        return '(' + cls.variable_label(label) + ')'

    @classmethod
    def emptytree(cls, colour):
        return InfinityNotTree(colour)

    @classmethod
    def basetrees(cls):
        for i in count(1):
            yield InfinityTree(i)

    def F(self):
        raise NotImplementedError

    def D(self):
        raise NotImplementedError

class InfinityNotTree(AbstractLabeledNotTree, InfinityTreeLike):
    __slots__ = ()
    
    def m_label(self, label):
        return 0






