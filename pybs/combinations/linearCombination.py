from numbers import Number


class LinearCombination(dict):
    __slots__ = ('_fast_setitem',)

    def __init__(self, iterable=None, *args, **kwds):
        self._fast_setitem = super(LinearCombination, self).__setitem__
        super(LinearCombination, self).__init__()
        self.__iadd__(iterable)

    def __str__(self):
        return ' + '.join([str(self[element]) + '*' +
                           str(element) for element in self])

    def __missing__(self, key):
        return 0

    def __setitem__(self, key, value):
        if isinstance(value, Number):
            if value == 0:
                if key in self:
                    del self[key]
            else:
                self._fast_setitem(key, value)
        else:
            raise TypeError(
                'bad operand type. Values must be of type Number, not: ' +
                str(type(value)))

    def __delitem__(self, elem):
        'Like dict.__delitem__() ' + \
            'but does not raise KeyError for missing values.'
        if elem in self:
            super(LinearCombination, self).__delitem__(elem)

    def __iadd__(self, other):
        'Inplace vector addition'
        self_get = self.get
        if isinstance(other, LinearCombination):
            if self:
                for elem, count in other.iteritems():
                    self._fast_setitem(elem, self_get(elem, 0) + count)
            else:
                super(LinearCombination, self).update(other)
        elif other is not None:  # WHY condition?
            self._fast_setitem(other, self_get(other, 0) + 1)
        return self

    def __add__(self, other):
        result = self.copy()
        result += other
        return result

    def __isub__(self, other):
        'Inplace vector subtraction.'
        self_get = self.get
        if isinstance(other, LinearCombination):
            for elem, count in other.items():
                self[elem] = self_get(elem, 0) - count
        else:
            self._fast_setitem(other, self_get(other, 0) - 1)
        return self

    def __sub__(self, other):
        result = self.copy()
        result -= other
        return result

    def __mul__(self, other):
        'Scalar multiplication.'
        if isinstance(other, Number):
            result = LinearCombination()
            for key, value in self.iteritems():
                result[key] = value * other
            return result
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def dimensions(self):
        'Number of different elements in the multiset.'
        return dict.__len__(self)

    def copy(self):
        result = LinearCombination()
        result += self
        return result

#    def __reduce__(self): #  Good for pickling.
#        return self.__class__, (dict(self),)

    def __repr__(self):  # TODO: Do something like this in my classes too!
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)
