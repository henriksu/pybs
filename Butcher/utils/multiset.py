# This Python file uses the following encoding: utf-8
from itertools import repeat as _repeat, chain as _chain, starmap as _starmap
from itertools import imap as _imap
import heapq as _heapq
from operator import itemgetter as _itemgetter, eq as _eq
from collections import Mapping as _Mapping


# This is based heavily on Collections' Counter, But note that
# 1. It has slots.
# 2. Values are ALWAYS natural numbers.
class Multiset(dict):
    __slots__ = ('_fast_setitem',)
    def __init__(self, iterable=None, *args, **kwds):
        self._fast_setitem = super(Multiset, self).__setitem__
        super(Multiset, self).__init__()
        self.update(iterable, **kwds)


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
                'bad operand type for Multiset.update(). Values must be of type int, not: ' + str(type(value)))

    def most_common(self, n=None):
        if n is None:
            return sorted(self.iteritems(), key=_itemgetter(1), reverse=True)
        return _heapq.nlargest(n, self.iteritems(), key=_itemgetter(1))

    #The functions "__missing__"(make sure keyErrer is raised. Is not implemented...
    def elements(self):
        return _chain.from_iterable(_starmap(_repeat, self.iteritems()))


    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Multiset.fromkeys() is undefined.  Use Multiset(iterable) instead.')

    def update(self, iterable=None, **kwds):
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
            self.update(kwds)

    def subtract(self, iterable=None, **kwds):
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
            self.subtract(kwds)

    def copy(self):
        return self.__class__(self)

    def __reduce__(self): #  Good for pickling.
        return self.__class__, (dict(self),)

    # TODO: Do I really need this behaviour?
    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            super(Multiset, self).__delitem__(elem)

    def __repr__(self): #  TODO: Do something like this in my classes too!
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    def __add__(self, other):
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            result._fast_setitem(elem, count + other[elem])
        for elem, count in other.items():
            if elem not in self:
                result._fast_setitem(elem, count)
        return result

    def __sub__(self, other):
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result._fast_setitem(elem, newcount)
        return result

    def __or__(self, other):
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
        if not isinstance(other, (Multiset, FrozenMultiset)):
            return NotImplemented
        result = Multiset()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = count if count < other_count else other_count
            if newcount > 0:
                result._fast_setitem(elem, newcount)
        return result


class FrozenMultiset(object):
    __slots__ = ('_ms','_hash')
    def __init__(self, *args, **kwargs):
        object.__setattr__(self, '_ms', Multiset(*args, **kwargs))
        object.__setattr__(self, '_hash', None)

    def __repr__(self): #  TODO: Do something like this in my classes too!
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    def most_common(self, n=None):
        return self._ms.most_common(n)

    def __setattr__(self, *args, **kwargs):
        pass

    def __delattr__(self, *args, **kwargs):
        pass

# TODO: DO I need it? DOes it block function calls?
#     def __getattr__(self, *args, **kwargs):
#         pass

# TODO: block setattr and delattr...
    def __iter__(self):
        return iter(self._ms)

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
        return self._ms.elements() #  TODO: Can I return the iterator itself?
#         for value, multiplicity in self.iteritems():
#             for i in xrange(multiplicity): #  TODO: How to repeat yield without for?
#                 yield value

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
    
    
    
    
    