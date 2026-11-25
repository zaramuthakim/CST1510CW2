"""
CONNECTING AND CREATING TABLES
=================================
The whole database is one file - no server, nothing to install.
Run:  python 01_connect_and_create.py
"""

import sqlite3
import os

DB = "example.db"
if os.path.exists(DB):
    os.remove(DB)

# --- 1. Connecting opens the file, or creates it if it does not exist -----

conn = sqlite3.connect(DB)
print(type(conn))


# --- 2. A cursor runs SQL and holds the results ---------------------------

cursor = conn.cursor()


# --- 3. CREATE TABLE - defining the shape -----------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id     INTEGER PRIMARY KEY,
        name   TEXT    NOT NULL,
        ip     TEXT    UNIQUE NOT NULL,
        active INTEGER DEFAULT 1
    )
""")
conn.commit()     # nothing is saved until you commit

# IF NOT EXISTS -> no error if it's already there
# PRIMARY KEY   -> unique row identifier, auto-numbered
# NOT NULL      -> value is required
# UNIQUE        -> no two rows can match
# DEFAULT       -> value used if none given


# --- 4. Always close when done, or use `with` (Topic 3 shows why) -------

conn.close()


# --- 5. An in-memory database - useful for testing, disappears after -----

temp = sqlite3.connect(":memory:")
temp.execute("CREATE TABLE scratch (x INTEGER)")
print("in-memory table created, gone the moment the program ends")


# --- 6. Same idea, three fields ---------------------------------------------
# The devices table above already IS the IT version - one row per tracked
# server. Same shape, two more domains.

conn = sqlite3.connect(DB)
conn.execute("""
    CREATE TABLE IF NOT EXISTS datasets (                -- AI / Data Science
        id     INTEGER PRIMARY KEY,
        name   TEXT NOT NULL,
        rows   INTEGER
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS incidents (                -- Cyber Security
        id       INTEGER PRIMARY KEY,
        ip       TEXT NOT NULL,
        severity TEXT
    )
""")
conn.commit()
conn.close()
print("datasets and incidents tables created, one row per dataset / per event")


# --- TRY IT ------------------------------------------------------------------
# 1. Create a table called "notes" with columns id (primary key) and
#    text (not null).
# 2. Run the same CREATE TABLE statement twice in a row - confirm IF NOT
#    EXISTS means the second run does not error.
# 3. Explain, in one sentence, why nothing is saved until conn.commit().
