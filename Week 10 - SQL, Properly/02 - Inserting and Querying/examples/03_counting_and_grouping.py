"""
COUNTING AND GROUPING
=========================
COUNT, AVG, MAX and GROUP BY answer questions about a whole table at once,
for example "how many rows are there in each category?". LIKE searches for part of a word.
Run:  python 03_counting_and_grouping.py
"""

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE games (title TEXT, genre TEXT, year INTEGER, rating REAL)")
conn.executemany(
    "INSERT INTO games VALUES (?, ?, ?, ?)",
    [
        ("Hollow Knight", "Platformer", 2017, 9.1),
        ("Celeste", "Platformer", 2018, 8.9),
        ("Portal 2", "Puzzle", 2011, 9.5),
        ("Tetris", "Puzzle", 1984, 9.0),
        ("Hades", "Roguelike", 2020, 9.3),
    ],
)

# 1. One number for the whole table
print(conn.execute("SELECT COUNT(*), AVG(rating), MAX(rating) FROM games").fetchone())

# 2. One row per group
query = """
    SELECT genre, COUNT(*) AS how_many, AVG(rating) AS average_rating
    FROM games
    GROUP BY genre
    ORDER BY how_many DESC
"""
for row in conn.execute(query):
    print(row)

# 3. Searching for part of a word (% means "anything")
print(conn.execute("SELECT title FROM games WHERE title LIKE ?", ("%e%",)).fetchall())


# --- TRY IT ------------------------------------------------------------------
# 1. Show the highest rating in each genre (use MAX(rating)).
# 2. Count only the games released after 2015.
