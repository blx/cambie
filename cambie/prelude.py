try:
    # Python 2
    basestring
    __PY3 = False

    mapv = map
    from itertools import imap as map
    reduce = reduce
    items = dict.iteritems

except NameError:
    # Python 3; ensure we get lists instead of generators
    __PY3 = True

    def mapv(f, *colls):
        return list(map(f, *colls))
    map = map
    from functools import reduce
    items = dict.items

from functools import partial

# Internal imports
from itertools import chain, islice
from operator import itemgetter

__all__ = ('identity', 'first', 'second', 'merge', 'comp', 'thread', 'juxt', 'items',
           'reduce', 'partial', 'map', 'mapv', 'take', 'rest', 'drop')


def identity(x):
    """Returns its argument."""
    return x

first = itemgetter(0)
second = itemgetter(1)

def take(n, coll):
    return islice(coll, 0, n)

def rest(coll):
    return islice(coll, 1, None)

def drop(n, coll):
    return islice(coll, n, None)

def merge(*dicts):
    """Returns the dict obtained by shallowing merging the `dicts` left-to-right.
    merge :: {}
    merge *dicts :: *{} -> {}"""
    return dict(chain(*(items(d) for d in dicts if d)))

def comp(*fns):
    """Returns the right-to-left composition of the `fns`.
    comp :: identity
    comp fn :: (a -> b) -> (a -> b)
    comp *fns :: (b_n -> c), *(b_i -> b_i+1), (*a -> b_0) -> (*a -> c)"""

    if not fns:
        return identity

    # This is ugly but faster than the standard reduce() version
    def _comped(*a, **kw):
        x = fns[-1](*a, **kw)
        for f in fns[-2::-1]:
            x = f(x)
        return x
    return _comped

def thread(x, *fns):
    """Threads `x` left-to-right through the `fns`, returning the final result.
    thread x :: a -> a
    thread x, *fns :: a_0, *(a_i -> a_i+1) -> a_n"""
    for f in fns:
        x = f(x)
    return x
    
def juxt(*fns):
    """Returns the juxtaposition of the `fns`.
    juxt *fns :: *(a -> b_i) -> (a -> [b_0, b_1, ...b_n])"""

    if not fns:
        raise TypeError('juxt requires at least 1 argument')

    def _juxted(*a, **kw):
        return [f(*a, **kw) for f in fns]
    return _juxted
