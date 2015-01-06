# This Python file uses the following encoding: utf-8
from trees.LabeledTrees import AbstractLabeledTreeLike, AbstractLabeledTree, AbstractLabeledNotTree
from forest import FrozenForest
#from forest import FrozenForest
#from utils import memoized


class AbstractColouredTreeLike(AbstractLabeledTreeLike):
    __slots__ = ()

    @property
    def colour(self):
        return self.label


class AbstractColouredTree(AbstractLabeledTree, AbstractColouredTreeLike):
    __slots__ = ()
    def __init__(self, colour, forest=FrozenForest()):
        AbstractLabeledTree.__init__(self, colour, forest)

class AbstractColouredNotTree(AbstractLabeledNotTree, AbstractColouredTreeLike):
    __slots__ = ('label',)
    def __init__(self, colour):
        object.__setattr__(self,'label', colour)

    def __str__(self):
        return 'Ø' + self.variable_label(self.label)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.label == other.label
        return False

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.label != other.label
        return True

    def __hash__(self):
        return hash(self.label)

    @property
    def F(self):
        return self.variable_label(self.label)




