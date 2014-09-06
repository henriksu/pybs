# This Python file uses the following encoding: utf-8
import collections
import functools
import weakref

# Copied from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}#weakref.WeakKeyDictionary()
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


# Following is due to Mike Graham (I exchanged dict for Counter and added elements)
# Found at
#http://stackoverflow.com/questions/2703599/what-would-be-a-frozen-dict
class FrozenCounter(collections.Mapping):
    """Don't forget the docstrings!!"""
    #__slots__ = ('_d','_hash') # Sannsynligvis meningsløs hvis Mapping ikke har __slots__.
    def __init__(self, *args, **kwargs):
        object.__setattr__(self, '_d', collections.Counter(*args, **kwargs))
        object.__setattr__(self, '_hash', None)

# TODO: block setattr and delattr...
    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]
    
    def elements(self):
        for value, multiplicity in self.iteritems():
            for i in xrange(multiplicity): #  TODO: How to repeat yield without for?
                yield value

    def __eq__(self, other): #  TODO: Check that this is a good implementation.
        if self is other:
            return True
        elif isinstance(other, FrozenCounter):
            return self._d == other._d
        elif isinstance(other, collections.Counter):
            return self._d == other
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
            for pair in self.iteritems():
                result ^= hash(pair)
            object.__setattr__(self, '_hash', result)
        return self._hash
#         if self._hash is None:
#             FrozenCounter.__setattr__(self, '_hash', 0)
#             for pair in self.iteritems():
#                 FrozenCounter.__setattr__(self, '_hash', self._hash ^ hash(pair))
#         return self._hash




# By Eyal Lotem and Yair Chuchem, 2007,
# http://code.activestate.com/recipes/528879-weak-key-and-value-dictionary/
class WeakKeyValueDict(object):
    """
    A dict in which items are removed whenever either key or value are
    garbage-collected.
    """
    def __init__(self, *args, **kw):
        init_dict = dict(*args, **kw)
        
        self._d = weakref.WeakKeyDictionary(
            (key, self._create_value(key, value))
            for key, value in init_dict.iteritems())

    def _create_value(self, key, value):
        key_weakref = weakref.ref(key)
        def value_collected(wr):
            del self[key_weakref()]
        return weakref.ref(value, value_collected)

    def __getitem__(self, key):
        return self._d[key]()
    
    def __setitem__(self, key, value):
        self._d[key] = self._create_value(key, value)

    def __delitem__(self, key):
        del self._d[key]

    def __len__(self):
        return len(self._d)

    def __cmp__(self, other):
        try:
            other_iteritems = other.iteritems
        except AttributeError:
            return NotImplemented
        return cmp(sorted(self.iteritems()),
                   sorted(other_iteritems()))

    def __hash__(self):
        raise TypeError("%s objects not hashable" % (self.__class__.__name__,))

    def __contains__(self, key):
        return key in self._d

    def __iter__(self):
        return self.iterkeys()

    def iterkeys(self):
        return self._d.iterkeys()

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        for value in self._d.itervalues():
            yield value()

    def values(self):
        return list(self.itervalues())
    
    def iteritems(self):
        for key in self._d:
            yield self._d[key]()

    def items(self):
        return list(self.iteritems())

    def update(self, other):
        for key, value in other.iteritems():
            self[key] = value

    def __repr__(self):
        return repr(self._d)

    def clear(self):
        self._d.clear()

    def copy(self):
        return WeakKeyValueDict(self)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def has_key(self, key):
        return key in self

    def pop(self, key, *args):
        if args:
            return self._pop_with_default(key, *args)
        return self._pop(key)

    def _pop(self, key):
        return self._d.pop(key)()
    
    def _pop_with_default(self, key, default):
        if key in self:
            return self._d.pop(key)
        return default

    def popitem(self):
        key, value = self._d.popitem()
        return key, value()

    def setdefault(self, key, default):
        if key in self:
            return self[key]
        self[key] = default
        return default

