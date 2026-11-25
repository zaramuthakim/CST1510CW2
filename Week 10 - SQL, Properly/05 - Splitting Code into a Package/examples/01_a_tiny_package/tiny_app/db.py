"""db.py - the ONE place that knows how to connect."""

import sqlite3


def connect_database(path=":memory:"):
    return sqlite3.connect(path)
