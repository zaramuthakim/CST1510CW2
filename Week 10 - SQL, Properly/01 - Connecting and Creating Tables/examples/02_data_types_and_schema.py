"""
DATA TYPES AND SCHEMA DESIGN
================================
SQLite keeps types simple - which is convenient, and a trap if you are not
careful.
Run:  python 02_data_types_and_schema.py
"""

import sqlite3
import os

DB = "example2.db"
if os.path.exists(DB):
    os.remove(DB)

# --- 1. Five storage classes - that's genuinely all of them ---------------
# INTEGER, REAL, TEXT, BLOB, NULL. No separate DATE type - store dates as
# TEXT, in ISO format (YYYY-MM-DD), so they sort correctly as text too.

conn = sqlite3.connect(DB)
conn.execute("""
    CREATE TABLE readings (
        id        INTEGER PRIMARY KEY,
        sensor    TEXT    NOT NULL,
        value     REAL    NOT NULL,
        recorded  TEXT    NOT NULL,
        raw_bytes BLOB
    )
""")
conn.commit()


# --- 2. SQLite is flexible about types - it will not stop you being wrong --

conn.execute("INSERT INTO readings (sensor, value, recorded) VALUES (?, ?, ?)",
             ("temp-01", "not-a-number", "2026-09-08"))     # SQLite allows this!
conn.commit()

row = conn.execute("SELECT value FROM readings").fetchone()
print(row)             # ('not-a-number',) - stored as-is, no error
print(type(row[0]))     # str, even though the column is REAL


# --- 3. This means YOUR code has to enforce the discipline SQLite won't ----
# Convert and validate before you INSERT - do not rely on the schema to
# catch a bad value for you.

def safe_insert(conn, sensor, value, recorded):
    """Insert a reading, converting value to float first - fails loudly if it can't."""
    value = float(value)     # raises ValueError here, not silently later
    conn.execute("INSERT INTO readings (sensor, value, recorded) VALUES (?, ?, ?)",
                 (sensor, value, recorded))
    conn.commit()

safe_insert(conn, "temp-02", "23.7", "2026-09-08")     # fine - converts cleanly
print(conn.execute("SELECT sensor, value FROM readings WHERE sensor = 'temp-02'").fetchone())


# --- TRY IT ------------------------------------------------------------------
# 1. Try inserting a genuinely non-numeric string as a "REAL" value through
#    safe_insert and confirm it raises ValueError instead of silently storing it.
# 2. Design a schema (as a CREATE TABLE statement) for a table of log
#    entries: id, timestamp (TEXT), level (TEXT), message (TEXT).
# 3. Explain, in one sentence, why storing dates as ISO-format TEXT lets
#    them still sort correctly.
