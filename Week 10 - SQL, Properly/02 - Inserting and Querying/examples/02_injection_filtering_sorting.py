"""
SQL INJECTION, FILTERING AND SORTING
========================================
Why ? placeholders are not optional, plus WHERE, AND/OR, ORDER BY, LIMIT.
Run:  python 02_injection_filtering_sorting.py
"""

import sqlite3
import os

DB = "example4.db"
if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
conn.executemany(
    "INSERT INTO users (name, role) VALUES (?, ?)",
    [("alice", "admin"), ("bob", "user"), ("carol", "user")],
)
conn.commit()

# --- 1. The vulnerability - building SQL by joining strings ------------
# NEVER do this with a value that came from a user:

name = "bob"
unsafe_query = f"SELECT * FROM users WHERE name = '{name}'"
print(unsafe_query)


# --- 2. What happens if "name" is actually an attack ----------------------

malicious_input = "' OR '1'='1"
unsafe_query = f"SELECT * FROM users WHERE name = '{malicious_input}'"
print(unsafe_query)
print(conn.execute(unsafe_query).fetchall())     # returns EVERY row - the WHERE did nothing


# --- 3. The fix - ? placeholders treat the value as DATA, never as CODE ---

safe_result = conn.execute("SELECT * FROM users WHERE name = ?", (malicious_input,)).fetchall()
print(safe_result)     # empty - there is no user actually named that whole string


# --- 4. WHERE, AND, ORDER BY, LIMIT --------------------------------------

print(conn.execute("SELECT name FROM users WHERE role = ?", ("user",)).fetchall())
print(conn.execute("SELECT name FROM users WHERE role = ? AND name != ?", ("user", "bob")).fetchall())
print(conn.execute("SELECT name FROM users ORDER BY name DESC").fetchall())
print(conn.execute("SELECT name FROM users ORDER BY id LIMIT 2").fetchall())


# --- TRY IT ------------------------------------------------------------------
# 1. Write a query that finds every "admin" role user, using a placeholder.
# 2. Sort users by name, ascending, and print just the first result.
# 3. Explain, in one sentence, why "' OR '1'='1" breaks the unsafe query but
#    not the safe one.
