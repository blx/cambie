#!/usr/bin/env python

# Loads CSVs of your travel history exported from TransLink BC's
# Compass Card site into a SQLite database.

from __future__ import print_function

import glob
import csv
import sqlite3
from datetime import datetime

def connect(dbpath):
    return sqlite3.connect(dbpath)

def create_table(db):
    db.execute("""create table compass (
                  "datetime" int,
                  "location" text,
                  "transaction" text,
                  "product" text,
                  "amount" int)""")

def ingest_csv(db, csvpath):
    parseDateTime = lambda s: datetime.strptime(s, "%b-%d-%Y %I:%M %p")

    def rows():
        with open(csvpath) as f:
            reader = csv.reader(f)
            reader.next()
            for row in reader:
                row[0] = parseDateTime(row[0])
                yield row

    cur = db.cursor()
    cur.executemany("insert into compass values (?, ?, ?, ?, ?)",
                    rows())
    db.commit()

def all_trips(db):
    cur = db.cursor()
    return cur.execute("""select * from compass
                          where "transaction" != "Missing Tap out"
                          order by datetime""")


if __name__ == "__main__":
    db = connect("compass.sqlite3")
    create_table(db)

    for csvf in glob.iglob("data/*.csv"):
        print("Ingesting %s" % csvf)
        ingest_csv(db, csvf)
