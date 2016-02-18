from operator import itemgetter

import matplotlib.pyplot as plt

from .libclj import juxtmap, comp, first, second


def _hist(bins, weights):
    """Returns a pyplot histogram of `weights` labeled by `bins`."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    hist = ax.hist(bins,
                   len(bins) - 1,
                   weights=weights)
    return fig

def trips_by_hour(db):
    """Returns a histogram of Compass taps by hour."""
    data = db.cursor().execute("""select cast(substr(t."time", 0, 3) as int) hour, count(*) n
                                  from "trip" t
                                  join "location" l on t."location" = l."location"
                                  group by hour
                                  order by n desc""")
    bins, weights = juxtmap([first, second],
                            data)

    return _hist(bins, weights)
