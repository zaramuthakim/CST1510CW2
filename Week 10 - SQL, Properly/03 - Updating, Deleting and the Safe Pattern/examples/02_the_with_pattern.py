"""
THE CLEAN, SAFE PATTERN
==========================
`with` auto-commits on success and auto-rolls-back if an error is raised.
Run:  python 02_the_with_pattern.py
"""

import sqlite3
import os

DB = "example6.db"
if os.path.exists(DB):
    os.remove(DB)

# --- 1. Without `with` - you must remember commit() and close() ---------

conn = sqlite3.connect(DB)
conn.execute("CREATE TABLE devices (id INTEGER PRIMARY KEY, name TEXT, ip TEXT UNIQUE)")
conn.execute("INSERT INTO devices (name, ip) VALUES (?, ?)", ("Router-A", "10.0.0.1"))
conn.commit()     # easy to forget - your changes silently vanish without this
conn.close()       # easy to forget - the connection stays open


# --- 2. With `with` - commit and close happen for you ---------------------

with sqlite3.connect(DB) as conn:
    conn.execute(
        "INSERT INTO devices (name, ip) VALUES (?, ?)",
        ("Firewall-1", "10.0.0.10"),
    )
    # commit happens automatically here, when the block ends normally


# --- 3. And it rolls back automatically if something goes wrong -------
# ip is UNIQUE - inserting the same one twice raises an error INSIDE the
# block. Nothing from this failed block gets committed.

try:
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO devices (name, ip) VALUES (?, ?)", ("Duplicate", "10.0.0.10"))
except sqlite3.IntegrityError as e:
    print("Insert failed, nothing was committed:", e)


# --- 4. row_factory - getting dict-like rows back, not bare tuples --------

with sqlite3.connect(DB) as conn:
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM devices WHERE name = ?", ("Router-A",)).fetchone()
    print(row["name"], row["ip"])     # by column name, not position


# --- TRY IT ------------------------------------------------------------------
# 1. Rewrite one of Topic 2's inserts to use the `with` pattern instead of
#    calling commit() manually.
# 2. Trigger the UNIQUE constraint on purpose and catch the resulting error.
# 3. Explain, in one sentence, what "leaving connections open" (a common
#    mistake) actually risks in a real, long-running application.
