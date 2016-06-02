#!/usr/bin/env python2

from .argh import Command, Argh
from .cambie import load_trips, geocode_locations, plot_trips_by_hour
from .util import connect

_db = lambda env: connect(env['db'])

commands = {
    'load_trips':    Command(load_trips, deps={'db': _db}, args=[['csv_files', {'nargs': '+', 'metavar': 'csvfile'}]]),
    'geocode_stops': Command(geocode_locations, deps={'db': _db}),
    'plot_trips':    Command(plot_trips_by_hour, deps={'db': _db}),
}

cli = Argh('cambie', commands)


if __name__ == '__main__':
    from . import env

    cli(env)
