import gc
from pybs.utils.miscellaneous import WeakKeyValueDict


class MyThing(object):
    store = WeakKeyValueDict()  # TODO: Weakdict.
    # This is slightly sketchy since inheriting my thing does not result in new stores being allocated.
    # As a consequence IF a given tree and a given forest compares equal, only one of them will be stored.

    def __init__(self, flavor):
        self.flavor = flavor

    def __hash__(self):
        return hash(self.flavor)

    def __eq__(self, other):
        return self.flavor == other.flavor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self in self.store:
            result = self.store[self]
            reference_list = gc.get_referrers(self)
            for reference in reference_list:
                reference = result
        else:
            self.store[self] = self
            return self


with MyThing('salt') as a:
    c = 1+1
with MyThing('salt') as b:
    c = 1+1
with MyThing('a') as c:
    c.flavor = 'b'

del c
for thing in MyThing.store:
    print thing.flavor
