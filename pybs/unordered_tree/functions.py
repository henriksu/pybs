from operator import __add__ as _add
from itertools import imap as _imap

from pybs.utils import memoized


@memoized
def number_of_trees_of_order(n):
    if n < 2:
        return n
    result = 0
    for k in range(1, n):
        result += k * number_of_trees_of_order(k) * _s(n-1, k)
    return result / (n - 1)


@memoized
def _s(n, k):
    result = 0
    for j in range(1, n/k + 1):
        result += number_of_trees_of_order(n+1-j*k)
    return result
# Joe Riel (joer(AT)san.rr.com), Jun 23 2008


def number_of_trees_up_to_order(n):
    '''Number of _trees up to, not including order n.'''
    return reduce(_add, _imap(number_of_trees_of_order, xrange(n)), 0)


def number_of_tree_pairs_of_total_order(n):
    "Needed for conjugate symplectic check. Known as m_n. \
    Taken from Hairer et al. \
    On Conjugate symplecticity of B-series integrators"
    # TODO: Implement general formula instead of table lookup.
    table = [0, 0, 1, 1, 3, 6, 16, 37, 96, 239, 622, 1607, 4235]
    return table[n]
