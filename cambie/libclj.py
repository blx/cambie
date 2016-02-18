try:
    basestring
except NameError:
    # python3; ensure we get a list out of zip
    __zip = zip
    def zip(*colls):
        return list(__zip(*colls))

from operator import itemgetter

__all__ = ('identity', 'first', 'second', 'comp', 'juxt', 'juxtmap')


def identity(x):
    """Returns its argument."""
    return x

first = itemgetter(0)
second = itemgetter(1)

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
    
def juxt(*fns):
    """Returns the juxtaposition of the `fns`.
    juxt *fns :: *(a -> b_i) -> (a -> [b_0, b_1, ...b_n])"""

    if not fns:
        raise TypeError('juxt requires at least 1 argument')

    def _juxted(*a, **kw):
        return [f(*a, **kw) for f in fns]
    return _juxted

def juxtmap(fns, *colls):
    """Returns [f(coll1, coll2, ...)[0],
                f(coll1, coll2, ...)[1],
                ...].
    Traverses the colls simultaneously and only once."""
    return zip(*map(juxt(*fns), *colls))
