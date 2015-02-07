from copy import copy
from itertools import repeat as _repeat, chain as _chain, starmap as _starmap
import heapq as _heapq
from sage.structure.list_clone import ClonableElement
from collections import Mapping as _Mapping
from operator import itemgetter as _itemgetter, __add__ as _add
from sage.misc.latex import latex
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.categories.sets_cat import Sets
from sage.categories.objects import Objects
from sage.categories.sets_with_partial_maps import SetsWithPartialMaps


class ClonableMultiset(ClonableElement):
    __slots__ = ('_ms', '_parent')

    def __init__(self, parent, iterable=0, *args, **kwargs):
        # ClonableElement.__init__(self, parent=Parent())
        ClonableElement.__setattr__(self, '_parent', parent)
        ClonableElement.__setattr__(self, '_ms', dict())
        self.inplace_multiset_sum(iterable, **kwargs)
        self.set_immutable()

    def check(self):
        pass

    def __copy__(self):
        result = self._parent(self._ms)
        result._set_mutable()
        return result

    def __nonzero__(self):
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
        'Inplace multiset sum'
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
        'Fast inplace increment/addition of element.'
        self._require_mutable()
        self._ms[elem] = self._ms.get(elem, 0) + 1

    def add(self, elem):
        with self.clone() as result:
            result._ms[elem] = result._ms.get(elem, 0) + 1
        return result

    def inplace_multiset_difference(self, iterable=None, **kwds):
        'Inplace multiset difference. Not truncated.'
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
        'Multiset sum. Returns new instance.'
        if isinstance(other, ClonableMultiset):
            with self.clone() as result:
                for elem, count in other.items():
                    result._ms[elem] = result._ms.get(elem, 0) + count
            return result
        else:
            return NotImplemented

    def multiset_difference(self, other):  # Old name: __sub__
        'Zero truncated multiset difference. Returns new instance.'
        # TODO: Choose the not-truncated?
        if isinstance(other, ClonableMultiset):
            with self._parent().clone() as result:
                for elem, count in self.items():
                    newcount = count - other[elem]
                    if newcount > 0:
                        result._ms[elem] = newcount
            return result
        else:
            return NotImplemented

    def __or__(self, other):
        'Multiset union'  # TODO: Correctly assosciated to "|". Rename?
        if isinstance(other, ClonableMultiset):
            with self._parent().clone() as result:
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
        'Multiset intersection'  # TODO: Correctly associated to "&". Rename?
        if isinstance(other, ClonableMultiset):
            with self._parent().clone() as result:
                for elem, count in self.items():
                    other_count = other[elem]
                    newcount = count if count < other_count else other_count
                    if newcount > 0:
                        result._ms[elem] = newcount
            return result
        else:
            return NotImplemented

    def cardinality(self):
        'Cardinality. Sum of multiplicities.'
        return reduce(_add, self._ms.values(), 0)

    def no_uniques(self):
        'Number of different elements in the multiset.'
        return len(self._ms)

    def most_common(self, n=None):
        if n is None:
            return sorted(self.iteritems(), key=_itemgetter(1), reverse=True)
        return _heapq.nlargest(n, self.iteritems(), key=_itemgetter(1))

    def elements(self):
        'Iterator returning each element as many times as its multiplicity.'
        return _chain.from_iterable(_starmap(_repeat, self._ms.iteritems()))

    def _eq_(self, other):
        if self is other:
            return True
        elif isinstance(other, ClonableMultiset):
            return self._ms == other._ms
        else:
            return NotImplemented

    def _ne_(self, other):
        if self is other:
            return False
        elif isinstance(other, ClonableMultiset):
            return self._ms != other._ms
        else:
            return NotImplemented

    def __setattr__(self, *args, **kwargs):
        raise AttributeError

    def __delattr__(self, *args, **kwargs):
        pass

    def __iter__(self):
        return iter(self._ms)

    def iteritems(self):
        return self._ms.iteritems()

    def iterkeys(self):
        return self._ms.iterkeys()

    def keys(self):
        return self._ms.keys()

    def values(self):
        return self._ms.values()

    def items(self):
        return self._ms.items()

    def sub(self, elem):
        with self.clone() as result:
            if elem in result:
                count = result.get(elem, 0)
                if count > 1:
                    result._fast_setitem(elem, count - 1)
                elif count == 1:
                    del result[elem]
                else:
                    raise ValueError
            return result

    def _hash_(self):
        # It would have been simpler and maybe more obvious to
        # use hash(tuple(sorted(self._d.iteritems()))) from this discussion
        # so far, but this solution is O(n). I don't know what kind of
        # n we are going to run into, but sometimes it's hard to resist the
        # urge to optimize when it will gain improved algorithmic performance.
        result = 0
        for pair in self._ms.iteritems():
            result ^= hash(pair)
        return result

    def _repr_(self):  # TODO: Do something like this in my classes too!
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    def _latex_(self):
        if not self:
            return '\\emptyset'
        else:
            results = []
            for elem, mult in self.most_common():
                tmp = latex(elem) + '^{' + latex(mult) + '}'
                results.append(tmp)
            return '\\left[' +\
                ', '.join(results) +\
                '\\right]'


class ClonableMultisets(UniqueRepresentation, Parent):
    def __init__(self):
        Parent.__init__(self, category=Sets())#Objects())#SetsWithPartialMaps())
        # TODO: Is this the right choice?

    def _element_constructor_(self, *args, **keywords):
        return self.element_class(self, *args, **keywords)

    Element = ClonableMultiset
