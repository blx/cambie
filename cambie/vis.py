import matplotlib.pyplot as plt


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
    bins, weights = zip(*data)
    return _hist(bins, weights)
