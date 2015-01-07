# This Python file uses the following encoding: utf-8
from pybs.trees import AbstractTreeLike, AbstractUnorderedRootedTree, AbstractNotTree
from pybs.combinations import FrozenForest
from pybs.utils import memoized


class AbstractLabeledTreeLike(AbstractTreeLike):
    __slots__ = ()


class AbstractLabeledTree(AbstractUnorderedRootedTree, AbstractLabeledTreeLike):
    __slots__ = ('label',) # Move to AbstractLabeledTreeLike
    
    def __init__(self, label, forest=FrozenForest()):
        #  TODO: Typecheck
        object.__setattr__(self, 'label',label)
        AbstractUnorderedRootedTree.__init__(self, forest)

    def __str__(self):
        if FrozenForest.__len__(self):
            return '[' + ','.join([str(elem) for elem in self.elements()]) + ']' + self.variable_label(self.label)
        else:
            return self.node_sign(self.label)

    def __eq__(self, other):
        if self is other:
            return True #  Is this necessary, or is it done automatically?
        elif isinstance(other, type(self)):
            return FrozenForest.__eq__(self, other) and self.label == other.label
        return False # TODO: return not implemented (error) ?

    def __ne__(self, other):
        if self is other:
            return False
        return FrozenForest.__ne__(self, other) or self.label != other.label
        #  TODO: Is it true that two trees evaluate equal iff (with large probability) their hash are equal?

    def __hash__(self):
        return hash((FrozenForest.__hash__(self), self.label))

    @classmethod
    def emptytree(cls, label):
        return NotImplementedError # TODO: THINK return cls.emptytree(label)

    @classmethod
    def basetree(cls, colour):
        return NotImplementedError# TODO: return cls(colour, FrozenForest())

    @classmethod
    def basetrees(cls):
        return NotImplementedError #TODO: FrozenForest([cls.basetree(black), cls.basetree(white)])

    def m_label(self, label):
        try:
            tmp = [item[1] for item in self.items() if item[0].label == label]
        except AttributeError:
            tmp = []
        result = 0 # TODO: Use python
        for pair in tmp:
            result += pair[1]
        return result

    def F(self):
        return NotImplementedError # TODO: generalize.
    def D(self, label): # is it right to include label?
        return NotImplementedError # TODO:


class AbstractLabeledNotTree(AbstractNotTree, AbstractLabeledTreeLike):
    __slots__ = ()

    @property
    def D(self):
        return NotImplementedError# TODO: something like: return type(self).tree(self.label)
