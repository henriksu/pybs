from copy import copy
from itertools import repeat as _repeat, chain as _chain, starmap as _starmap
import heapq as _heapq
from collections import Mapping as _Mapping
from operator import itemgetter as _itemgetter, __add__ as _add

from clonable import Clonable


class ClonableMultiset(Clonable):
    __slots__ = ('_ms',)

    def __init__(self, iterable=0, *args, **kwargs):
        """Make a new ClonableMultiset.

        If an argument is given, it is added to the new instance using
        ``inplace_multiset_sum``.
        The result is immutable.
        """
        Clonable.__init__(self)
        Clonable.__setattr__(self, '_ms', dict())
        self.inplace_multiset_sum(iterable, **kwargs)
        self.set_immutable()

    def check(self):
        pass

    def __copy__(self):
        """Return a shallow mutable copy of self."""
        result = self.__class__(self)
        result._set_mutable()
        return result

    def __nonzero__(self):
        """Return true if set is not empty.

        Used to determine boolean value."""
        return bool(self._ms)

    def __setitem__(self, key, value):
        self._require_mutable()
        if isinstance(value, int):
            if value > 0:
                self._ms[key] = value
            elif value == 0:
                if key in self:
                    del self[key]
                # ELSE just leave it. Don't want it in the dict anyways...
            else:
                raise ValueError(
                    'ClonableMultiset cannot have negative values: ' +
                    str(key) + ': ' + str(value))
        else:
            raise TypeError(
                'bad operand type for ' +
                'ClonableMultiset.inplace_multiset_sum(). ' +
                'Values must be of type int, not: ' + str(type(value)))

    def __getitem__(self, key):
        try:
            return self._ms[key]
        except KeyError:
            return 0

    def __delitem__(self, elem):
        'Like dict.__delitem__() ' + \
            'but does not raise KeyError for missing values.'
        self._require_mutable()
        if elem in self._ms:
            del self._ms[elem]

    def inplace_multiset_sum(self, iterable=0, **kwds):
        """Updates :math:`A` to :math:`A \uplus B`."""
        self._require_mutable()
        if iterable is not 0:
            self_get = self._ms.get
            if isinstance(iterable, ClonableMultiset):
                if self:
                    for elem, count in iterable.iteritems():
                        self._ms[elem] = self_get(elem, 0) + count
                else:
                    self._ms.update(iterable)
                    # Fast path when counter is empty
            elif isinstance(iterable, _Mapping):
                if self:
                    for elem, count in iterable.iteritems():
                            self[elem] = self_get(elem, 0) + count
                else:
                    for elem, count in iterable.iteritems():
                        self[elem] = count
            else:
                for elem in iterable:
                    self._ms[elem] = self_get(elem, 0) + 1
        if kwds:
            self.inplace_multiset_sum(kwds)

    def inplace_add(self, elem):
        """"Add `elem` to `self` with multiplicity 1.

        If elem is already in A its multiplicity is increased by one.
        """
        self._require_mutable()
        self._ms[elem] = self._ms.get(elem, 0) + 1

    def add(self, elem):
        """Same as above, except the result is returned as a new instance of
        ClonableMultiset."""
        with self.clone() as result:
            result._ms[elem] = result._ms.get(elem, 0) + 1
        return result

    def inplace_multiset_difference(self, iterable=None, **kwds):
        """Update :math:`A` to :math:`A \setminus B`.

        Raises an exception if the multiplicity of an element in B is larger
        than the multiplicity of the same element in A.
        This is non-standard behavior for mathematical multisets, but a sound
        check when they are used for trees.
        """
        self._require_mutable()
        if iterable is not None:
            self_get = self._ms.get
            if isinstance(iterable, ClonableMultiset):
                # TODO: Use multiset minus or whatever here?
                # or else merge with next elif.
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) - count
            elif isinstance(iterable, _Mapping):
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) - count
            else:
                for elem in iterable:
                    oldcount = self_get(elem, 0)
                    if oldcount > 1:
                        self._ms[elem] = oldcount - 1
                    elif oldcount == 1:
                        del self._ms[elem]
                    else:
                        raise ValueError(
                            'ClonableMultiset cannot have negative values: ' +
                            str(elem) + ': -1')
        if kwds:
            self.inplace_multiset_difference(kwds)

    def scalar_mul(self, n):
        r"""Returns :math:`n \bigotimes A` as a new instance.

        That is a multiset where the multiplicities are scaled by `n`.
        """
        if isinstance(n, int):
            with self.clone() as result:
                for key in self.iterkeys():
                    result[key] *= n
            return result
#            return type(self)(dict(((key, n*value)
#                                    for (key, value) in self.iteritems())))
            # TODO: This is a nasty workaround.
        else:
            return NotImplemented

    def multiset_sum(self, other):  # Old name: __add__
        """Return :math:`A \uplus B` as a new instance."""
        if isinstance(other, ClonableMultiset):
            with self.clone() as result:
                for elem, count in other.items():
                    result._ms[elem] = result._ms.get(elem, 0) + count
            return result
        else:
            return NotImplemented

    def multiset_difference(self, other):  # Old name: __sub__
        """Return :math:`A \setminus B` as a new instance.

        .. note:: Does allow a multiplicity in B to be larger than the
           corresponding multiplicity in A,
           the multiplicity of the element in question is 0.
        """
        # TODO: Choose the not-truncated?
        if isinstance(other, ClonableMultiset):
            with self.__class__().clone() as result:
                for elem, count in self.items():
                    newcount = count - other[elem]
                    if newcount > 0:
                        result._ms[elem] = newcount
            return result
        else:
            return NotImplemented

    def __or__(self, other):
        """Return the multiset union :math:`A \cup B` as a new instance.

        This is the same syntax as set union in Python (``|``).
        """
        # TODO: Correctly assosciated to "|". Rename?
        if isinstance(other, ClonableMultiset):
            with self.__class__().clone() as result:
                for elem, count in self.items():
                    other_count = other[elem]
                    result._ms[elem] = \
                        other_count if count < other_count else count
                for elem, count in other.items():
                    if elem not in self:
                        result._ms[elem] = count
            return result
        else:
            return NotImplemented

    def __and__(self, other):
        """"Return the multiset intersection :math:`A \cap B` as a new instance.

        This is the same syntax as set intersection in Python (``&``)."""
        # TODO: Correctly associated to "&". Rename?
        if isinstance(other, ClonableMultiset):
            with self.__class__().clone() as result:
                for elem, count in self.items():
                    other_count = other[elem]
                    newcount = count if count < other_count else other_count
                    if newcount > 0:
                        result._ms[elem] = newcount
            return result
        else:
            return NotImplemented

    def cardinality(self):
        """Return sum of multiplicities."""
        return reduce(_add, self._ms.values(), 0)

    def no_uniques(self):
        """Number of different elements in the multiset."""
        return len(self._ms)

    def most_common(self, n=None):
        """Return the `n` most common elements.
        """
        if n is None:
            return sorted(self.iteritems(), key=_itemgetter(1), reverse=True)
        return _heapq.nlargest(n, self.iteritems(), key=_itemgetter(1))

    def elements(self):
        'Iterator returning each element as many times as its multiplicity.'
        return _chain.from_iterable(_starmap(_repeat, self._ms.iteritems()))

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, ClonableMultiset):
            return self._ms == other._ms
        else:
            return NotImplemented

    def __ne__(self, other):
        if self is other:
            return False
        elif isinstance(other, ClonableMultiset):
            return self._ms != other._ms
        else:
            return NotImplemented

    def __setattr__(self, *args, **kwargs):
        raise AttributeError

    def __delattr__(self, *args, **kwargs):
        raise AttributeError

    def __iter__(self):
        return iter(self._ms)

    def iteritems(self):
        """Return iterator over (key,value)-pairs."""
        return self._ms.iteritems()

    def iterkeys(self):
        """Return iterator over keys."""
        return self._ms.iterkeys()

    def keys(self):
        """Return list of keys (elements)."""
        return self._ms.keys()

    def values(self):
        """Return list of values (multiplicities)"""
        return self._ms.values()

    def items(self):
        """Return list of (key,value)-pairs."""
        return self._ms.items()

    def sub(self, elem):
        with self.clone() as result:
            if elem in result:
                count = result[elem]
                if count > 1:
                    result._ms[elem] -= 1#fast_setitem(elem, count - 1)
                elif count == 1:
                    del result[elem]
                else:
                    raise ValueError
            return result

    def __contains__(self, elem):
        """Return True if elem is in self."""
        return elem in self._ms

    def __bool__(self):
        return bool(self._ms)

    def _hash_(self):
        """Return hash value for multiset.

        Only called if immutable.
        """
        # It would have been simpler and maybe more obvious to
        # use hash(tuple(sorted(self._d.iteritems()))) from this discussion
        # so far, but this solution is O(n). I don't know what kind of
        # n we are going to run into, but sometimes it's hard to resist the
        # urge to optimize when it will gain improved algorithmic performance.
        result = 0
        for pair in self._ms.iteritems():
            result ^= hash(pair)
        return result

    def __repr__(self):
        """Return a string representative of the ClonableMultiset-object."""
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)
