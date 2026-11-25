"""pets.py - everything about pets. Every function receives the connection."""


def add_pet(conn, name, age):
    cur = conn.cursor()
    cur.execute("INSERT INTO pets (name, age) VALUES (?, ?)", (name, age))
    conn.commit()


def get_all_pets(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pets")
    return cur.fetchall()
