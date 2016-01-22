#!/usr/bin/env python2

"""Loads CSVs of your travel history exported from TransLink BC's
Compass Card site into an SQLite database."""

from __future__ import print_function

from functools import partial
import time
import glob
import re
import csv
import sqlite3
from datetime import datetime

import credentials as creds
import translink_geocode as translink

CSV_DIR = "data"
get_stop = partial(translink.get_stop, creds.API_KEY)

def connect(dbpath):
    def _sqlite_regexp(pattern, s):
        # SQLite in its infinite generosity defines the "regexp" keyword
        # but leaves its implementation up to the user.
        return re.search(pattern, s) is not None

    db = sqlite3.connect(dbpath)
    db.create_function("REGEXP", 2, _sqlite_regexp)
    return db

DDL = {
    'trip':       """create table trip (
                       "datetime" int,
                       "location" text,    -- like "50268" or "Waterfront Stn"
                       "transaction" text,
                       "product" text,
                       "amount" int)""",
    'location':   """create table location (
                       "id" integer primary key,
                       "location" text,    -- like "50187"
                       "name" text,        -- like "WB W HASTINGS ST FS ABBOTT ST"
                       "lat" decimal,
                       "long" decimal)""",
    'route':      """create table route (
                       "id" integer primary key,
                       "name" text)        -- like "009" """,
    'route_stop': """create table route_stop (
                       "route_id" integer,
                       "location_id" integer,
                       foreign key("route_id") references route("id"),
                       foreign key("location_id") references location("id"))"""
}

def geocode_locations(db):
    cur = db.cursor()
    cur.execute("""select distinct(location) from trip
                   where location regexp '[0-9]+'""")
    locs = [row[0] for row in cur]

    for i, loc in enumerate(locs):
        geo = get_stop(loc)
        result = [loc, geo['Name'].rstrip('- '), geo['Latitude'], geo['Longitude']]
        cur.execute("""insert into location ("location", "name", "lat", "long")
                       values (?, ?, ?, ?)""",
                    result)
        print('Geocoded %s (%s) to %0.6f, %0.6f' % result)

        # TransLink limits API calls to 100/minute
        if (i + 1) % 100 == 0:
            t = 50
            print('... Sleeping %d seconds to keep TransLink API happy ...' % t)
            time.sleep(t)

    db.commit()

def ingest_csv(db, csvpath):
    "Loads trip history from CSV into SQLite."
    parse_datetime = lambda s: datetime.strptime(s, "%b-%d-%Y %I:%M %p")

    def rows():
        with open(csvpath) as f:
            reader = csv.reader(f)
            reader.next()
            for row in reader:
                row[0] = parse_datetime(row[0])
                yield row

    cur = db.cursor()
    cur.executemany("insert into trip values (?, ?, ?, ?, ?)",
                    rows())
    db.commit()

def all_trips(db):
    cur = db.cursor()
    for row in cur.execute("""select * from trip
                              where "transaction" != "Missing Tap out"
                              order by datetime"""):
        yield row


if __name__ == "__main__":
    db = connect("compass.sqlite3")
    db.execute(DDL['trip'])

    for csvf in glob.iglob(CSV_DIR + "/*.csv"):
        print("Ingesting trip history from %s" % csvf)
        ingest_csv(db, csvf)
