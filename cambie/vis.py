import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from .prelude import *


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
    ax.grid(True)
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

def _directions_by_hour(db, hour):
    if not 0 <= hour <= 23:
        raise IndexError('Hour must be within [0, 23]')

    time_lo = '%02d:30' % ((hour - 1) % 24)
    time_hi = '%02d:29' % hour

    if hour != 0:
        cond = "tm between (?) and (?)"
    else:
        cond = "tm >= (?) or tm <= (?)"

    data = db.cursor().execute("""
        select
            coalesce(sum(case when substr(z.name, 0, 3) == 'WB' then z.n end), 0) n_WB,
            coalesce(sum(case when substr(z.name, 0, 3) == 'EB' then z.n end), 0) n_EB,
            coalesce(sum(case when substr(z.name, 0, 3) == 'NB' then z.n end), 0) n_NB,
            coalesce(sum(case when substr(z.name, 0, 3) == 'SB' then z.n end), 0) n_SB,
            coalesce(sum(case when substr(z.name, 0, 4) == 'UBC' then z.n end), 0) n_UBC,
            coalesce(sum(case when z.name is null then z.n else 0 end), 0) n_skytrain
        from (
            select t."location", l."name", substr(t."time", 0, 6) tm, count(*) n
            from "trip" t
            left outer join "location" l on t."location" = l."location"
            where
                (t."transaction" like 'Tap in%'
                 or t."transaction" like 'Transfer at%')
                and """ + cond + """
            group by t."location"
            order by n desc
        ) z""", [time_lo, time_hi])
    return data

def directions_by_hour(db):
    hours = list(range(0, 24))
    dirs = map(comp(first,
                    list,  # realize all the Cursors
                    partial(_directions_by_hour, db)),
               hours)
    return _bar(hours, dirs)
