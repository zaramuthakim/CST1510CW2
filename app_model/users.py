from pathlib import Path
import sqlite3
import bcrypt
"""User registration, login, and database operations."""

def generate_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def is_valid_hash(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def add_user(conn, username, password_hash, role="user"):
    conn.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role),
    )
    conn.commit()

def get_user(conn, username):
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()

def get_all_users(conn):
    return conn.execute("SELECT * FROM users").fetchall()

def update_role(conn, username, new_role):
    conn.execute(
        "UPDATE users SET role = ? WHERE username = ?", (new_role, username)
    )
    conn.commit()

def delete_user(conn, username):
    conn.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()

def register_user(conn, username, password):
    username = username.strip()
    if not username:
        return False, "Username cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    try:
        add_user(conn, username, generate_hash(password))
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    return True, "Registered. You can log in now."

def login_user(conn, username, password):
    user = get_user(conn, username.strip())
    if user is not None and is_valid_hash(password, user[2]):
        return True, "Welcome back!"
    return False, "Wrong username or password."

def migrate_users_file(conn, path):
    path = Path(path)
    if not path.exists():
        return 0
    added = 0
    with path.open("r") as file:
        for line in file:
            name, password_hash = line.strip().split(",", 1)
            if get_user(conn, name) is None:
                add_user(conn, name, password_hash)
                added += 1
    return added
