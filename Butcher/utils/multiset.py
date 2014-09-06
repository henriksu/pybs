# This Python file uses the following encoding: utf-8
from itertools import repeat as _repeat, chain as _chain, starmap as _starmap
from itertools import imap as _imap
import heapq as _heapq
from operator import itemgetter as _itemgetter, eq as _eq, __add__
from collections import Mapping as _Mapping
from copy import copy

# This is based heavily on Collections' Counter, But note that
# 1. It has slots.
# 2. Values are ALWAYS natural numbers.
class Multiset(dict):
    __slots__ = ('_fast_setitem',)
    def __init__(self, iterable=None, *args, **kwds):
        self._fast_setitem = super(Multiset, self).__setitem__
        super(Multiset, self).__init__()
        self.inplace_multiset_sum(iterable, **kwds)

    def __missing__(self, key): #  Do I really want this behaviour? I do.
        return 0

    def __setitem__(self, key, value):
        if isinstance(value, int):
            if value > 0:
                self._fast_setitem(key, value)
            elif value == 0:
                if key in self:
                    del self[key] # ELSE just leave it. Don't want it in the dict anyways...
            else:
                raise ValueError('Multiset cannot have negative values: ' + str(key) + ': ' + str(value))
        else:
            raise TypeError(
                'bad operand type for Multiset.inplace_multiset_sum(). Values must be of type int, not: ' + str(type(value)))

    # TODO: Do I really need this behaviour?
    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            super(Multiset, self).__delitem__(elem)

    def most_common(self, n=None):
        if n is None:
            return sorted(self.iteritems(), key=_itemgetter(1), reverse=True)
        return _heapq.nlargest(n, self.iteritems(), key=_itemgetter(1))

    def elements(self):
        'Iterator returning each element as many times as its multiplicity.'
        return _chain.from_iterable(_starmap(_repeat, self.iteritems()))

    def inplace_multiset_sum(self, iterable=None, **kwds):
        'Inplace multiset sum' # TODO: Remane?
        if iterable is not None:
            if isinstance(iterable, (Multiset, FrozenMultiset)): # TODO: Consider an AbstractMultiset class.
                # TODO: Use set addition/union whatever here ?
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self._fast_setitem(elem, self_get(elem, 0) + count)
                else:
                    super(Multiset, self).update(iterable) # fast path when counter is empty
            elif isinstance(iterable, _Mapping):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                            self[elem] = self_get(elem, 0) + count
                else:
                    for elem, count in iterable.iteritems():
                        self[elem] = count
            else:
                self_get = self.get
                for elem in iterable:
                    self._fast_setitem(elem, self_get(elem, 0) + 1)
        if kwds:
            self.inplace_multiset_sum(kwds)

    def inplace_add(self, elem):
        'Fast inplace increment/addition of element.'
        self._fast_setitem(elem, self.get(elem, 0) + 1)

    def add(self, elem):
        result = copy(self)
        result._fast_setitem(elem, result.get(elem, 0) + 1)
        return result

    def inplace_multiset_difference(self, iterable=None, **kwds):
        'Inplace multiset difference. Not truncated.'
        if iterable is not None:
            self_get = self.get
            if isinstance(iterable, (Multiset, FrozenMultiset)):
                # TODO: Use multiset minus or whatever here? or else merge with next elif.
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) - count
            elif isinstance(iterable, _Mapping):
                for elem, count in iterable.items():
                    self[elem] = self_get(elem, 0) - count
            else:
                for elem in iterable:
                    oldcount = self_get(elem, 0)
                    if oldcount > 1:
                        self._fast_setitem(elem, oldcount - 1)
                    elif oldcount == 1:
                        del self[elem]
                    else:
                        raise ValueError('Multiset cannot have negative values: ' + str(elem) + ': -1')
        if kwds:
            self.inplace_multiset_difference(kwds)

    def scalar_mul(self, n):
        if isinstance(n, int):
            return type(self)(dict(((key, n*value) for (key, value) in self.iteritems()))) #  TODO: This is a nasty workaround.
        else:
            return NotImplemented
    def multiset_sum(self, other): #  Old name: __add__
        'Multiset sum. Returns new instance.'
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            result._fast_setitem(elem, count + other[elem])
        for elem, count in other.items():
            if elem not in self:
                result._fast_setitem(elem, count)
        return result

    def multiset_difference(self, other):#  Old name: __sub__
        'Zero truncated multiset difference. Returns new instance.'
        # TODO: Choose the not-truncated?
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result._fast_setitem(elem, newcount)
        return result

    def __or__(self, other):
        'Multiset union' # TODO: Correctly assosciated to "|". Rename?
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            other_count = other[elem]
            result._fast_setitem(
                elem, other_count if count < other_count else count)
        for elem, count in other.items():
            if elem not in self:
                result._fast_setitem(elem, count)
        return result

    def __and__(self, other):
        'Multiset intersection' # TODO: Correctly assosciated to "&". Rename?
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = count if count < other_count else other_count
            if newcount > 0:
                result._fast_setitem(elem, newcount)
        return result

    def __len__(self):
        'Cardinality. Sum of multiplicities.'
        return reduce(__add__, self.values(), 0)

    def no_uniques(self):
        'Number of different elements in the multiset.'
        return dict.__len__(self)

    def copy(self):
        return self.__class__(self)

    def __reduce__(self): #  Good for pickling.
        return self.__class__, (dict(self),)


    def __repr__(self): #  TODO: Do something like this in my classes too!
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)


    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Multiset.fromkeys() is undefined.  Use Multiset(iterable) instead.')


class FrozenMultiset(object):
    __slots__ = ('_ms','_hash')
    def __init__(self, *args, **kwargs):
        object.__setattr__(self, '_ms', Multiset(*args, **kwargs))
        object.__setattr__(self, '_hash', None)

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, FrozenMultiset):
            return self._ms == other._ms
        elif isinstance(other, Multiset):
            return self._ms == other
        else:
            return NotImplemented
        
    def __ne__(self, other):
        if self is other:
            return False
        elif isinstance(other, FrozenMultiset):
            return self._ms != other._ms
        elif isinstance(other, Multiset):
            return self._ms != other
        else:
            return NotImplemented

    def most_common(self, n=None):
        return self._ms.most_common(n)

    def __setattr__(self, *args, **kwargs):
        pass

    def __delattr__(self, *args, **kwargs):
        pass

    def __iter__(self):
        return iter(self._ms)
    
    def iteritems(self):
        return self._ms.iteritems()

    def __len__(self):
        return len(self._ms)

    def __getitem__(self, key):
        return self._ms[key]
    
    def keys(self):
        return self._ms.keys()

    def values(self):
        return self._ms.values()
    
    def items(self):
        return self._ms.items()
    
    def elements(self):
        return self._ms.elements()


    def multiset_difference(self, other): #  Old name: __sub__
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result._fast_setitem(elem, newcount)
        return result

    def sub(self, elem):
        result = copy(self._ms)
        if elem in result:
            count = result.get(elem, 0)
            if count > 1:
                result._fast_setitem(elem, count - 1)
            elif count == 1:
                del result[elem]
            else:
                raise ValueError
            return result
                

    def __hash__(self):
        # It would have been simpler and maybe more obvious to 
        # use hash(tuple(sorted(self._d.iteritems()))) from this discussion
        # so far, but this solution is O(n). I don't know what kind of 
        # n we are going to run into, but sometimes it's hard to resist the 
        # urge to optimize when it will gain improved algorithmic performance.
        if self._hash is None:
            result = 0
            for pair in self._ms.iteritems():
                result ^= hash(pair)
            object.__setattr__(self, '_hash', result)
        return self._hash
#         if self._hash is None:
#             FrozenCounter.__setattr__(self, '_hash', 0)
#             for pair in self.iteritems():
#                 FrozenCounter.__setattr__(self, '_hash', self._hash ^ hash(pair))
#         return self._hash
    def __repr__(self): #  TODO: Do something like this in my classes too!
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)




if __name__ == '__main__':
    a = Multiset({'a':1, 'b':4})
    print a
    b = FrozenMultiset(a)
    print b
    for elem in a.elements():
        print elem
    for elem in b.elements():
        print elem
    pass
    1+1
    print 1
    
    
    
    
    