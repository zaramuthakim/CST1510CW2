from pathlib import Path
import sqlite3
"""Database connection helpers."""

DB_PATH = Path(__file__).parent.parent / "DATA" / "app.db"

def connect_database(path=DB_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path)
