"""
MIGRATING WEEK 9's USERS FILE
================================
The flat file from last week, moved into a proper table - the exact upgrade
the lab's load_data.py makes.
Run:  python 02_migrating_the_users_file.py
"""

import sqlite3
import os
import bcrypt

DB = "example8.db"
USERS_FILE = "old_users.txt"
if os.path.exists(DB):
    os.remove(DB)
if os.path.exists(USERS_FILE):
    os.remove(USERS_FILE)

# --- 1. Recreate last week's flat file, so there is something to migrate ---

def register_flat(username, password, path=USERS_FILE):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    with open(path, "a") as f:
        f.write(f"{username},{hashed.decode('utf-8')}\n")

register_flat("alice", "correct-horse-battery-staple")
register_flat("bob", "another-real-password")


# --- 2. Create the users table -----------------------------------------

with sqlite3.connect(DB) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)


# --- 3. Read the flat file, insert each line as a row --------------------
# Week 7's parsing, Week 9's file, Week 10's storage - all three weeks in
# four lines.

with sqlite3.connect(DB) as conn:
    with open(USERS_FILE) as f:
        for line in f:
            username, password_hash = line.strip().split(",", 1)
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )


# --- 4. Confirm the migration, and that login still works the same way -----

with sqlite3.connect(DB) as conn:
    for row in conn.execute("SELECT username FROM users"):
        print(row[0])

    stored = conn.execute(
        "SELECT password_hash FROM users WHERE username = ?", ("alice",)
    ).fetchone()[0]
    print(bcrypt.checkpw(b"correct-horse-battery-staple", stored.encode("utf-8")))   # True


# --- TRY IT ------------------------------------------------------------------
# 1. Register a third user into the flat file, then migrate it too.
# 2. After migrating, delete old_users.txt - the database is now the single
#    source of truth. Confirm login still works using only the database.
# 3. Explain, in one sentence, why the UNIQUE constraint on username matters
#    even more now than it did for the flat file.
