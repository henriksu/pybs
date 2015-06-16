from fractions import Fraction
from math import factorial

from pybs.utils import memoized2 as memoized, LinearCombination
from pybs.unordered_tree import leaf
from pybs.combinations import \
    empty_tree, \
    split, \
    subtrees, \
    antipode_ck, \
    tree_commutator as tree_commutator
from pybs.series import \
    BseriesRule, \
    VectorfieldRule, \
    ForestRule, \
    tree_tuples_of_order
# TODO: Include Sphinx in installation?


def hf_composition(a):
    r"""The composition :math:`a b`,
    where :math:`b` is the B-series representing
    the vector field corresponding to the exact solution.

    That is :math:`b = \delta_{\circ}`.
    """  # TODO: include some trees in the sphinx docs.
    if a(empty_tree) != 1:
        raise ValueError(
            'Composition can only be performed on consistent B-series.')

    def new_rule(tree):
        if tree == empty_tree:
            return 0
        else:
            result = 1
            for subtree, multiplicity in tree.items():
                result *= a(subtree) ** multiplicity
            return result
    return BseriesRule(new_rule)


def lie_derivative(c, b, truncate=False):
    """The Lie-derivative of ``c`` with respect to ``b`` as
    a new :class:`series.Bseries.BseriesRule`.
   """
    if b(empty_tree) != 0:
        raise ValueError(
            'The second argument does not satisfy b(ButcherEmptyTree()) == 0.')

    @memoized
    def new_rule(tree):
        result = 0
        if tree == empty_tree:
            return result
        pairs = split(tree, truncate)
        for pair, multiplicity in pairs.items():
            result += multiplicity * b(pair[0]) * c(pair[1])
        return result
    return VectorfieldRule(new_rule)


def modified_equation(a, quadratic_vectorfield=False):
    """The modified equation. Mostely equivalent to :func:`log`."""
    if a(empty_tree) != 1 or a(leaf) != 1:  # TODO: Check last condition.
        raise ValueError(
            'Can not calculate the modified equation for this BseriesRule.')

    @memoized
    def new_rule(tree):
        if tree == empty_tree:
            return 0
        result = a(tree)
        c = new_rule  # This is a BseriesRule. Caution: Recursive!
        for j in range(2, tree.order() + 1):
            c = lie_derivative(c, new_rule, True)  # TODO: Is this memoized?
            result -= Fraction(c(tree), factorial(j))
        return result
    result = VectorfieldRule(new_rule)
    if quadratic_vectorfield:
        result = remove_non_binary(result)
    return result


def log(a, quadratic_vectorfield=False):
    """The logarithm.

    If ``a`` is the B-series rule for a numerical method,
    it returns the rule for the modified equation.

    .. note::
       Much slower than :func:`modified_equation`.
    """
    if a(empty_tree) != 1:
        raise ValueError(
            'Can not calculate the logarithm for this rule.')

    @memoized
    def new_rule(tree):
        if tree == empty_tree:
            return 0
        a_2 = remove_empty_tree(a)
        result = a_2(tree)
        b = a_2
        for n in range(2, tree.order() + 1):
            b = composition(b, a_2)
            result += ((-1)**(n+1)) * Fraction(b(tree), n)
        return result
    result = VectorfieldRule(new_rule)
    if quadratic_vectorfield:
        result = remove_non_binary(result)
    return result


def exp(a, quadratic_vectorfield=False):
    """The exponential.

    If ``a`` is the rule for the B-serie of some modified equation,
    it returns the B-series rule for the numerical method.
    """
    if a(empty_tree) != 0:
        raise ValueError(
            'Can not calculate the exponential for this rule.')

    @memoized
    def new_rule(tree):
        if tree == empty_tree:
            return 1
        result = a(tree)
        b = a
        for n in range(2, tree.order() + 1):
            b = composition(b, a)
            result += Fraction(b(tree), factorial(n))
        return result
    result = BseriesRule(new_rule)
    if quadratic_vectorfield:
        result = remove_non_binary(result)
    return result


def remove_non_binary(a):
    """Sets the value at all non-binary trees to zero.

    Used for quadratic vector fields."""
    base_rule = a._call

    def new_rule(tree):
        if tree == empty_tree or tree.is_binary():
            return base_rule(tree)
        else:
            return 0
    return type(a)(new_rule)


def remove_empty_tree(a):
    """Returns :math:`a - I`.

    Used by :func:`log`."""
    base_rule = a._call
    et = empty_tree

    def new_rule(tree):
        if tree == et:
            return 0
        else:
            return base_rule(tree)
    return type(a)(new_rule)


def composition_ssa(a, b):
    """Same as :func:`composition`, except that it
    halves the stepsize afterwards.

    Equivalent to ``stepsize_adjustment(composition(a,b),Fraction(1, 2))``.
    """
    if a(empty_tree) != 1:
        raise ValueError(
            'Composition can only be performed on consistent B-series.')

    @memoized
    def new_rule(tree):
        sub_trees = subtrees(tree)
        result = 0
        for pair, multiplicity in sub_trees.items():
            result += a(pair[0]) * b(pair[1]) * multiplicity
        return Fraction(result, 2**tree.order())

    return BseriesRule(new_rule)
    # TODO: account for ForestRule.


def stepsize_adjustment(a, A):
    """Corresponds to letting h -> A h."""
    base_rule = a._call

    def new_rule(tree):
        return A**tree.order() * base_rule(tree)
    return BseriesRule(new_rule)


def composition(a, b):
    r"""Composition of methods, b after a.

    Return the composition :math:`a \circ b`.
    The returned object is a :class:`BseriesRule` if
    :math:`a(\emptyset) = 1` and a :class:`ForestRule`
    otherwise.
    """
    @memoized
    def new_rule(arg):  # arg is tree or forest.
        result = 0
        for pair, multiplicity in subtrees(arg).items():
            result += a(pair[0]) * b(pair[1]) * multiplicity
        return result
    if a(empty_tree) != 1:
        return ForestRule(new_rule)
    else:
        return BseriesRule(new_rule)


def inverse(a):
    r"""Return the inverse of *a* in the Butcher group.

    The returned BseriesRule is calculated as
    :math:`\left(a \circ S\right)(\tau)`,
    where :math:`S` denotes the antipode.
    """
    # TODO: Test that a is of the right kind.
    @memoized
    def new_rule(tree):
        return a(antipode_ck(tree))
    return BseriesRule(new_rule)


def conjugate(a, c):
    """The conjugate of ``a`` with change of coordinates ``c``.

    Calculated with compositions and inverse."""
    return composition(inverse(c), composition(a, c))


def conjugate_by_commutator(a, c):
    """The conjugate of ``a`` with change of coordinates ``c``.

    Calculated using the commutator.
    """
    def new_rule(tree):
        if tree == empty_tree:
            return 0
        tmp = a
        result = 0
        for n in range(tree.order() + 1):
            result += Fraction((-1)**n, factorial(n)) * tmp(tree)
            tmp = series_commutator(c, tmp)
        return result
    return BseriesRule(new_rule)


def adjoint(a):
    """The adjoint is the inverse with reversed time step.

    Returns a BseriesRule.
    """
    def new_rule(tree):
        return (-1)**tree.order() * inverse(a)(tree)
    return BseriesRule(new_rule)
# TODO: Adjoint of a modified equation p. 324 HLW.


def series_commutator(a, b):
    """Corresponds to tree commutator, just for series."""
    # TODO: TEST ME!

    def new_rule(tree):
        order = tree.order()
        if order in new_rule.orders:
            return new_rule.storage[tree] * tree.symmetry()
            # TODO: Move the correction by symmetry to initialisation.
        else:
            result = LinearCombination()
            for tree1, tree2 in tree_tuples_of_order(order):
                result += \
                    Fraction(a(tree1) * b(tree2),
                             tree1.symmetry() * tree2.symmetry()) * \
                    tree_commutator(tree1, tree2)
            new_rule.orders.add(order)
            new_rule.storage += result
            return new_rule.storage[tree] * tree.symmetry()
    new_rule.storage = LinearCombination()
    new_rule.orders = set((0,))  # the coefficient of the empty tree is always 0.
    return BseriesRule(new_rule)
