"""
INSERT AND SELECT
====================
Adding rows, and getting them back.   Run:  python 01_insert_and_select.py
"""

import sqlite3
import os

DB = "example3.db"
if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
conn.execute("""
    CREATE TABLE devices (
        id     INTEGER PRIMARY KEY,
        name   TEXT NOT NULL,
        ip     TEXT UNIQUE NOT NULL,
        type   TEXT
    )
""")
conn.commit()

# --- 1. ? placeholders - never build SQL by joining strings -----------

conn.execute(
    "INSERT INTO devices (name, ip, type) VALUES (?, ?, ?)",
    ("Router-A", "10.0.0.1", "router"),
)
conn.commit()


# --- 2. executemany() - inserting several rows at once ---------------

rows = [
    ("Switch-1", "10.0.0.2", "switch"),
    ("AP-Lobby", "10.0.0.3", "access point"),
]
conn.executemany(
    "INSERT INTO devices (name, ip, type) VALUES (?, ?, ?)", rows
)
conn.commit()


# --- 3. SELECT * - fetchall() gives every row, as a list of tuples ------

for row in conn.execute("SELECT * FROM devices").fetchall():
    print(row)


# --- 4. fetchone() - a single row, or None ------------------------------

one = conn.execute("SELECT name, ip FROM devices WHERE id = ?", (1,)).fetchone()
print(one)

missing = conn.execute("SELECT name FROM devices WHERE id = ?", (999,)).fetchone()
print(missing)     # None - no crash, just nothing found


# --- 5. Iterating the cursor directly, without fetchall() ----------------

for name, ip in conn.execute("SELECT name, ip FROM devices"):
    print(f"{name} -> {ip}")


# --- 6. Same idea, three fields ---------------------------------------------

conn.execute("CREATE TABLE cleaned_rows (label TEXT, value REAL)")             # AI / Data Science
for label, value in [("R-001", 87.0), ("R-002", 120.0)]:
    conn.execute("INSERT INTO cleaned_rows VALUES (?, ?)", (label, value))
conn.commit()

conn.execute("CREATE TABLE incidents (ip TEXT, severity TEXT)")                # Cyber Security
conn.execute("INSERT INTO incidents VALUES (?, ?)", ("10.0.0.5", "high"))
conn.commit()
print(conn.execute("SELECT * FROM incidents WHERE severity = ?", ("high",)).fetchall())

print(conn.execute(                                                             # IT
    "SELECT * FROM devices WHERE type = ? AND id >= ?", ("router", 1)
).fetchall())


# --- TRY IT ------------------------------------------------------------------
# 1. Insert a device of your own, then SELECT it back by its ip.
# 2. Use executemany() to insert 3 devices at once.
# 3. Explain, in one sentence, why "?" placeholders are used instead of
#    f-string-ing the values directly into the SQL.
