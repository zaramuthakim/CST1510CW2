"""schema.py - creates the tables."""


def create_pet_table(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pets (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)")
    conn.commit()
