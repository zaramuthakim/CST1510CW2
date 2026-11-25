"""
ROWID AND TABLE INFO
========================
Every SQLite table has a hidden number for each row called rowid. It is a simple way to
refer to one row when you edit or delete it. PRAGMA table_info lists the columns of a table,
which lets a program check a column name before it uses it in a query.
Run:  python 03_rowid_and_table_info.py
"""

import sqlite3

import pandas as pd

conn = sqlite3.connect(":memory:")
pd.DataFrame({"name": ["Ana", "Ben", "Cy"], "score": [7, 9, 4]}).to_sql("results", conn, index=False)

# 1. rowid is there even though we never created it
print(pd.read_sql("SELECT rowid AS row_id, * FROM results", conn))

# 2. Change one row, using its rowid
conn.execute("UPDATE results SET score = ? WHERE rowid = ?", (10, 2))
print(conn.execute("SELECT name, score FROM results WHERE rowid = 2").fetchone())

# 3. The columns of the table
info = pd.read_sql("PRAGMA table_info(results)", conn)
columns = list(info["name"])
print(columns)

# 4. A ? placeholder can protect a value but not a column name,
#    so check the name against the real list first.
wanted = "score; DROP TABLE results"
print(wanted in columns)


# --- TRY IT ------------------------------------------------------------------
# 1. Delete the row with rowid 3 and print the table again.
# 2. Write a function that raises ValueError if a column name is not in the table.
