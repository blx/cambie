import sqlite3
import csv
import re

def _sqlite_regexp(pattern, s):
    # SQLite in its infinite generosity defines the "regexp" keyword
    # but leaves its implementation up to the user.
    return re.search(pattern, s) is not None

def connect(dbpath):
    db = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES)
    db.create_function("REGEXP", 2, _sqlite_regexp)
    return db

def create_table_once(db, ddl):
    try:
        db.execute(ddl)
    except sqlite3.OperationalError:
        pass

def csv_rows(csvpath, skip_rows=1):
    "Returns a generator of rows (lists of fields) parsed from CSV at csvpath."
    with open(csvpath) as f:
        reader = csv.reader(f)
        if skip_rows:
            for _ in xrange(skip_rows):
                reader.next()
        for row in reader:
            yield row

