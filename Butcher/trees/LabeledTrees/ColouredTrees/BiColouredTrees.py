# This Python file uses the following encoding: utf-8
from trees.LabeledTrees.ColouredTrees import AbstractColouredTreeLike, AbstractColouredTree, AbstractColouredNotTree
from forest import FrozenForest
from trees import memoized


black = object()
white = object()
variable = {black: 'y', white: 'z'}
node_sign= {black: '*', white: 'o'}

class BiColouredTreeLike(AbstractColouredTreeLike):
    #WAY TO INHERIT FROM TWO CLASSES WITH NONEMPTY __slots__
    __slots__ = ()#  ('variable', 'black', 'white')

    @classmethod
    def variable_label(cls, colour):
        return variable[colour]


class BiColouredTree(AbstractColouredTree, BiColouredTreeLike): #  Black-White trees
    __slots__ = ()
    # p. 68. Gamma is defined to be same as for mono-coloured trees.

    def __init__(self, colour, forest=FrozenForest()):
        AbstractColouredTree.__init__(self, colour, forest)

    @classmethod
    def node_sign(cls, colour):
        return node_sign[colour]
    


    @classmethod
    def emptytree(cls, label):
        return BiColouredNotTree(label)

    @classmethod
    def basetree(cls, label):
        return cls(label, FrozenForest())
    
    @classmethod
    def basetrees(cls):
        return FrozenForest([cls.basetree(black), cls.basetree(white)])

    @property
    @memoized
    def m_black(self):
        try:
            tmp = [item[1] for item in self.items() if item[0].label == black]
        except AttributeError:
            tmp = []
        result = 0 #  TODO: USe python.
        for pair in tmp:
            result += pair #  pair[1]
        return result

    @property
    def m_white(self):
        return self.m - self.m_black

    @property    
    def F(self): #  Elementary differential.
#         if self == BiColouredTree.emptytree(black):
#             return 'y'
#         elif self == BiColouredTree.emptytree(white):
#             return 'z'
        if self.label == black:
            result = 'f'
        else:
            result = 'g'
        if self.m > 0:
            result += '_'
            result += variable[black] * self.m_black
            result += variable[white] * self.m_white
        if self.m == 1:
            result += self.keys()[0].F
        elif self.m > 1:
            result += '(' + ','.join([elem.F for elem in self.elements()]) + ')'
        return result

    @property
    def D(self, label):
        return self.graft(BiColouredTree.basetree(label)) #  TODO: Will this make sense for taking the derivative of either empty tree?


class BiColouredNotTree(AbstractColouredNotTree, BiColouredTreeLike):
    __slots__ = ()
    def __init__(self, colour):
        AbstractColouredNotTree.__init__(self, colour) # TODO: Do I really need to specify which super init to call?

    @property
    def D(self):
        return BiColouredTree(self.label)
    
    m_black = m_white = 0

BiColouredTree.emptytree = BiColouredNotTree
black
white
