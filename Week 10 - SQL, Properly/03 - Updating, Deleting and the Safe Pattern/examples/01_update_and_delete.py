"""
UPDATE AND DELETE
====================
Changing and removing rows - and the one mistake that affects EVERY row.
Run:  python 01_update_and_delete.py
"""

import sqlite3
import os

DB = "example5.db"
if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
conn.execute("CREATE TABLE devices (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, active INTEGER DEFAULT 1)")
conn.executemany(
    "INSERT INTO devices (name, ip) VALUES (?, ?)",
    [("Router-A", "10.0.0.1"), ("Switch-1", "10.0.0.2"), ("AP-Lobby", "10.0.0.3")],
)
conn.commit()

# --- 1. UPDATE - changing existing rows -------------------------------

conn.execute("UPDATE devices SET ip = ? WHERE id = ?", ("10.0.0.254", 1))
conn.commit()
print(conn.execute("SELECT name, ip FROM devices WHERE id = 1").fetchone())


# --- 2. rowcount - how many rows actually changed ------------------------

cursor = conn.execute("UPDATE devices SET active = 0 WHERE name = ?", ("AP-Lobby",))
conn.commit()
print(cursor.rowcount)     # 1 - exactly one row matched


# --- 3. DELETE - removing rows --------------------------------------

conn.execute("DELETE FROM devices WHERE active = 0")
conn.commit()
print(conn.execute("SELECT name FROM devices").fetchall())     # AP-Lobby is gone


# --- 4. THE mistake: UPDATE or DELETE with no WHERE ------------------
# This changes or removes EVERY row in the table. Always double check the
# WHERE clause before running one of these - especially with real data.

# conn.execute("DELETE FROM devices")
# -> wipes the WHOLE table, no confirmation, no undo

# Safer habit: run the matching SELECT first, and check what comes back,
# before running the UPDATE/DELETE with the same WHERE clause.
print(conn.execute("SELECT * FROM devices WHERE active = 0").fetchall())     # check first
# only if that looks right:
# conn.execute("DELETE FROM devices WHERE active = 0")


# --- 5. Same idea, three fields ---------------------------------------------

conn.execute("CREATE TABLE readings (id INTEGER PRIMARY KEY, value REAL)")
conn.execute("INSERT INTO readings (value) VALUES (999.0)")
conn.commit()
conn.execute("UPDATE readings SET value = ? WHERE id = ?", (23.7, 1))          # AI / Data Science
conn.commit()
print(conn.execute("SELECT * FROM readings WHERE id = 1").fetchone())

conn.execute("CREATE TABLE incidents (id INTEGER PRIMARY KEY, resolved INTEGER DEFAULT 0)")
conn.execute("INSERT INTO incidents (resolved) VALUES (0)")
conn.commit()
conn.execute("UPDATE incidents SET resolved = 1 WHERE id = ?", (1,))           # Cyber Security
conn.commit()
print(conn.execute("SELECT * FROM incidents WHERE id = 1").fetchone())

conn.execute("DELETE FROM devices WHERE id = ?", (2,))                         # IT - by id, never a blanket delete
conn.commit()
print(conn.execute("SELECT id, name FROM devices").fetchall())


# --- TRY IT ------------------------------------------------------------------
# 1. Update one device's name, then confirm the change with a SELECT.
# 2. Delete one device by id, and print cursor.rowcount to confirm exactly
#    one row was removed.
# 3. Explain, in one sentence, why running the matching SELECT first is a
#    good habit before every UPDATE/DELETE.
