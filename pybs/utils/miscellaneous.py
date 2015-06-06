# This Python file uses the following encoding: utf-8
from collections import \
    Hashable as _Hashable
from functools import partial as _partial, wraps


# Copied from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}  # weakref.WeakKeyDictionary()

    def __call__(self, *args):
        if not isinstance(args, _Hashable):
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
        return _partial(self.__call__, obj)


def memoized2(func):
    """Slightly different memoization.

    Does not confuse autodoc the way other decorators do.
    """
    @wraps(func)
    def wrapper(*args):
        if args in wrapper.cache:
            return wrapper.cache[args]
        else:
            value = func(*args)
            wrapper.cache[args] = value
            return value
    wrapper.cache = {}
    return wrapper
