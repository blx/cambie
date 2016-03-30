import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from .prelude import partial


def _bar(bins, weights):
    """Returns a pyplot bar graph of `weights` labeled by `bins`."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bar = ax.bar(left=bins,
                 height=weights)
    ax.set_xlim(left=0, right=24)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 1.0))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%02.f'))
    ax.tick_params(color='black',
                   direction='out',
                   length=5)
    return fig

def trips_by_hour(db):
    """Returns a histogram of Compass taps by hour."""
    data = db.cursor().execute("""select cast(substr(t."time", 0, 3) as int) hour, count(*) n
                                  from "trip" t
                                  join "location" l on t."location" = l."location"
                                  group by hour
                                  order by hour asc""")
    bins, weights = zip(*data)
    fig = _bar(bins, weights)
    fig.axes[0].set_xlabel('Time of day')
    fig.axes[0].set_ylabel('Tap-in count')
    return fig

