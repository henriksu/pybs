class Clonable(object):
    __slots__ = ('_is_immutable', '_hash')

    def __init__(self):
        Clonable.__setattr__(self, '_is_immutable', False)
        Clonable.__setattr__(self, '_hash', None)

    def _require_mutable(self):
        if self._is_immutable:
            raise ValueError

    def is_mutable(self):
        return not self._is_immutable

    def is_immutable(self):
        return self._is_immutable

    def set_immutable(self):
        Clonable.__setattr__(self, '_is_immutable', True)

    def _set_mutable(self):
        Clonable.__setattr__(self, '_is_immutable', False)

    def __hash__(self):
        if self._hash is None:
            if not self._is_immutable:
                raise ValueError
            else:
                Clonable.__setattr__(self, '_hash', self._hash_())
        return self._hash

    def clone(self):
        return self.__copy__()

    def __enter__(self):
        self._require_mutable()
        return self

    def __exit__(self, typ, value, tracback):
        self.set_immutable()
        return False
