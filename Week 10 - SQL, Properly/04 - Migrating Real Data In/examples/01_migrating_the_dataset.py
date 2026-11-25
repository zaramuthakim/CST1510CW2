"""
MIGRATING A REAL DATASET INTO SQLITE
========================================
Week 8's data, properly stored - with pandas doing the heavy lifting.
Run:  python 01_migrating_the_dataset.py
"""

import sqlite3
import os
import pandas as pd
import requests
from io import StringIO

DB = "example7.db"
if os.path.exists(DB):
    os.remove(DB)

# --- 1. Load a real dataset the way Week 8 taught -----------------------

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
text = requests.get(url, timeout=10).text
df = pd.read_csv(StringIO(text))
print(df.head())


# --- 2. DataFrame.to_sql() - the whole migration, one line -----------

with sqlite3.connect(DB) as conn:
    df.to_sql("tips", conn, if_exists="replace", index=False)

print("migrated", len(df), "rows")


# --- 3. Querying it back out - as a DataFrame again, with pd.read_sql -----

with sqlite3.connect(DB) as conn:
    result = pd.read_sql("SELECT * FROM tips WHERE tip > 5", conn)
print(result)


# --- 4. Or as plain rows, sqlite3 style, if you don't need pandas here ---

with sqlite3.connect(DB) as conn:
    rows = conn.execute("SELECT COUNT(*) FROM tips").fetchone()
print("total rows in the table:", rows[0])


# --- 5. Same idea, three fields ---------------------------------------------
# The tips.csv migration above already IS the AI / Data Science version.

incident_lines = ["10.0.0.5,high", "10.0.0.9,low"]                              # Cyber Security
incidents_df = pd.DataFrame(
    [line.split(",") for line in incident_lines], columns=["ip", "severity"]
)
with sqlite3.connect(DB) as conn:
    incidents_df.to_sql("incidents", conn, if_exists="replace", index=False)
    print(pd.read_sql("SELECT * FROM incidents WHERE severity = 'high'", conn))

ticket_lines = ["fix printer,open", "reset password,closed"]                     # IT
tickets_df = pd.DataFrame(
    [line.split(",") for line in ticket_lines], columns=["summary", "status"]
)
with sqlite3.connect(DB) as conn:
    tickets_df.to_sql("tickets", conn, if_exists="replace", index=False)
    print(pd.read_sql("SELECT * FROM tickets WHERE status = 'open'", conn))


# --- TRY IT ------------------------------------------------------------------
# 1. Migrate a different dataset (your own, or Week 8's fallback) into a
#    new table using to_sql().
# 2. Query it back with pd.read_sql() using a WHERE condition of your own.
# 3. Explain, in one sentence, what if_exists="replace" does, and why you
#    would sometimes want if_exists="append" instead.
