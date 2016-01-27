from numbers import Number


class LinearCombination(dict):
    """Class to represent linear combinations of arbitrary elements.
    """
    __slots__ = ('_fast_setitem',)

    def __init__(self, iterable=None, *args, **kwds):
        self._fast_setitem = super(LinearCombination, self).__setitem__
        super(LinearCombination, self).__init__()
        self.__iadd__(iterable)

    def __str__(self):
        return ' + '.join([str(self[element]) + '*' +
                           str(element) for element in self])

    def __missing__(self, key):
        """Called if an element is not in the :class:`LinearCombination`.

        If an element is not in the :class:`LinearCombination`,
        its coefficient is 0.
        """
        return 0

    def __setitem__(self, key, value):
        """Called when coefficients are set as e.g. ``linComb[elem]=4``.

        Ensures the coefficient is a ``Number``, and
        that the key is deleted if the coefficient is 0.
        """
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
        """Like dict.__delitem__() \
        but does not raise KeyError for missing values.
        """
        if elem in self:
            super(LinearCombination, self).__delitem__(elem)

    def __iadd__(self, other):
        """Overload inplace addition (``self += other``).

        If `other` is a :class:`LinearCombination`,
        they are added as vectors, if not
        other is assumed to be an element and is bumped by 1."""
        self_get = self.get
        if isinstance(other, LinearCombination):
            if self:
                for elem, count in other.items():
                    self._fast_setitem(elem, self_get(elem, 0) + count)
            else:
                super(LinearCombination, self).update(other)
        elif other is not None:  # WHY condition?
            self._fast_setitem(other, self_get(other, 0) + 1)
        return self

    def __add__(self, other):
        """Overload addition (``self + other``).

        Same rule as above if `other` is not :class:`LinearCombination`.
        """
        result = self.copy()
        result += other
        return result

    def __isub__(self, other):
        """Overload inplace subtraction (``self -= other``).

        Same rule as above if `other` is not :class:`LinearCombination`.
        """
        self_get = self.get
        if isinstance(other, LinearCombination):
            for elem, count in other.items():
                self[elem] = self_get(elem, 0) - count
        else:
            self._fast_setitem(other, self_get(other, 0) - 1)
        return self

    def __sub__(self, other):
        """Overload subtraction (``self - other``).

        Same rule as above if `other` is not :class:`LinearCombination`.
        """
        result = self.copy()
        result -= other
        return result

    def __mul__(self, other):
        """Overload multiplication, used for scalar multiplication (``self * num``).
        """
        if isinstance(other, Number):
            result = LinearCombination()
            for key, value in self.items():
                result[key] = value * other
            return result
        else:
            return NotImplemented

    def __rmul__(self, other):
        """Overload multiplication to deal with scalar multiplication \
        from the right (``num * self``).
        """
        return self * other

    def dimensions(self):
        """Number of different elements in the multiset."""
        return dict.__len__(self)

    def copy(self):
        """Return an identical :class:`LinearCombination`."""
        result = LinearCombination()
        result += self
        return result

#    def __reduce__(self): #  Good for pickling.
#        return self.__class__, (dict(self),)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)
