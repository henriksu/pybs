from fractions import Fraction

from pybs.combinations.forests import empty_tree


def _zero(tree):
    return 0


def _unit(tree):
    if tree == empty_tree():
        return 1
    else:
        return 0


def _exact(tree):
    if tree == empty_tree():
        return 1
    return Fraction(1, tree.density())


def _kahan(tree):
    'Directly from Owren'  # TODO: Test
    if tree.is_Tall():
        return 2 ** (1-tree.order())
    else:
        return 0


def _AVF(self, tree, a):
    'Directly from Owren'  # TODO: Test
    if tree.order() == 1:
        return 1
    elif not tree.is_Binary():
        return 0
    else:
        if tree.number_of_children() == 1:
            return _AVF(tree.keys()[0], a)/2.0
        elif tree.number_of_children() == 2:
            alpha = Fraction(2*a + 1, 4)
            return alpha * _AVF(tree.keys()[0], a) * \
                _AVF(tree.keys()[1], a)

exponential = _exact
zero = _zero
