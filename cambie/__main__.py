#!/usr/bin/env python2

"""Loads CSVs of your travel history exported from TransLink BC's
Compass Card site into an SQLite database."""

from __future__ import print_function

from functools import partial
from itertools import imap
import time
from datetime import datetime

from . import credentials as creds
from .util import csv_rows, connect, create_table_once
from . import translink_geocode as translink

CSV_DIR = 'data'
DB = 'compass.sqlite3'

info = print
get_bus_stop = partial(translink.get_stop, creds.API_KEY)

DDL = {
    'trip':       """create table "trip" (
                       "id" int primary key,
                       "datetime" text,
                       "date" text,
                       "time" text,
                       "location" text,    -- like "50268" or "Waterfront Stn"
                       "transaction" text,
                       "product" text,
                       "amount" int,
                       unique("date", "time", "location", "transaction"))""",
    'location':   """create table "location" (
                       "id" int primary key,
                       "location" text,    -- like "50187"
                       "name" text,        -- like "WB W HASTINGS ST FS ABBOTT ST"
                       "lat" decimal,
                       "long" decimal)""",
    'route':      """create table "route" (
                       "id" int primary key,
                       "name" text)        -- like "009" """,
    'route_stop': """create table "route_stop" (
                       "route_id" int,
                       "location_id" int,
                       foreign key("route_id") references route("id"),
                       foreign key("location_id") references location("id"))"""
}

def geocode_locations(db):
    "Adds geo-information to db for all trips that haven't yet been geocoded."
    create_table_once(db, DDL['location'])

    cur = db.cursor()
    cur.execute("""select distinct(t."location") from "trip" t
                   left outer join "location" l on l."location" = t."location"
                   where l."location" is null
                   and t."location" regexp '[0-9]+'""")
    locs = [row[0] for row in cur]

    for i, loc in enumerate(locs):
        geo = get_bus_stop(loc)
        result = (loc, geo['Name'].rstrip('- '), geo['Latitude'], geo['Longitude'])
        cur.execute("""insert into "location" ("location", "name", "lat", "long")
                       values (?, ?, ?, ?)""",
                    result)
        info('Geocoded %s (%s) to %0.6f, %0.6f' % result)

        # TransLink limits API calls to 100/minute
        if (i + 1) % 100 == 0:
            t = 50
            info('... Sleeping %d seconds to keep TransLink API happy ...' % t)
            time.sleep(t)

    db.commit()

def ingest_csv(db, csvpath):
    """Loads trip history from CSV into SQLite. Note: idempotent but unintelligent:
    if you pass in a CSV that's already been ingested, the DB will be unchanged
    but we'll still traverse the entire file."""
    def parse_datetime(s):
        dt = datetime.strptime(s, "%b-%d-%Y %I:%M %p")
        # Split into date (2016-02-15) and time (09:31) components for sqlite.
        # (Compass card datetime resolution is in minutes)
        return [str(dt), str(dt.date()), str(dt.time())[:5]]

    def rowfn(row):
        row = parse_datetime(row[0]) + row[1:]
        return row

    cur = db.cursor()
    # Insert if new; skip and ignore constraint violation if already exists
    cur.executemany("""insert or ignore into trip
                       ("datetime", "date", "time", "location", "transaction", "product", "amount")
                       values (?, ?, ?, ?, ?, ?)""",
                    imap(rowfn, csv_rows(csvpath)))
    db.commit()

def all_trips(db):
    cur = db.cursor()
    for row in cur.execute("""select * from "trip"
                              where "transaction" != 'Missing Tap out'
                              order by datetime"""):
        yield row

def load_trips(db, csv_dir):
    import glob
    import os

    create_table_once(db, DDL['trip'])

    for csvf in glob.iglob(os.path.join(csv_dir, '*.csv')):
        info('Ingesting trip history from %s' % csvf)
        ingest_csv(db, csvf)

if __name__ == '__main__':
    import argparse

    def cmd(fn, args=None):
        """Wrapper function to supply DB connection and appropriate arguments
        to subcommands."""
        return lambda ns: fn(connect(DB),
                             **{k: getattr(ns, k)
                                for k in args or []})

    argparser = argparse.ArgumentParser(prog='cambie')
    cmds = argparser.add_subparsers()

    cmd_load_trips = cmds.add_parser('load_trips')
    cmd_load_trips.add_argument('csv_dir')
    cmd_load_trips.set_defaults(func=cmd(load_trips, ['csv_dir']))

    cmd_geocode_stops = cmds.add_parser('geocode_stops')
    cmd_geocode_stops.set_defaults(func=cmd(geocode_locations))

    args = argparser.parse_args()

    args.func(args)
