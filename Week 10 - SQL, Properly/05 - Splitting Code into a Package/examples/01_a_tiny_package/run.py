"""
A TINY PACKAGE
================
Three small files in a folder called tiny_app (plus an empty __init__.py),
used by this one script.

Run it from INSIDE this folder:   python run.py
"""

from tiny_app.db import connect_database
from tiny_app.pets import add_pet, get_all_pets
from tiny_app.schema import create_pet_table

conn = connect_database()          # one connection, made in one place
create_pet_table(conn)             # ...and handed to each function that needs it

add_pet(conn, "Rex", 4)
add_pet(conn, "Mia", 2)
print(get_all_pets(conn))

conn.close()
