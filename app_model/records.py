import pandas as pd
"""Database operations for the records table."""

TABLE = "records"

def load_csv(conn, csv_path):
    df = pd.read_csv(csv_path)
    df.to_sql(TABLE, conn, if_exists="replace", index=False)
    return len(df)

def get_columns(conn):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE} LIMIT 0")
    return [column[0] for column in cur.description]

def get_all_records(conn):
    return pd.read_sql(f"SELECT rowid AS row_id, * FROM {TABLE}", conn)

def count_records(conn):
    return conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]

def _check_column(conn, column):
    if column not in get_columns(conn):
        raise ValueError(f"Unknown column: {column}")

def search_records(conn, column, text):
    _check_column(conn, column)
    sql = f"SELECT rowid AS row_id, * FROM {TABLE} WHERE {column} LIKE ?"
    return pd.read_sql(sql, conn, params=(f"%{text}%",))

def add_record(conn, values):
    for column in values:
        _check_column(conn, column)
    names = ", ".join(values)
    marks = ", ".join("?" for _ in values)
    conn.execute(
        f"INSERT INTO {TABLE} ({names}) VALUES ({marks})",
        tuple(values.values()),
    )
    conn.commit()

def update_record(conn, row_id, column, value):
    _check_column(conn, column)
    cur = conn.execute(
        f"UPDATE {TABLE} SET {column} = ? WHERE rowid = ?", (value, row_id)
    )
    conn.commit()
    return cur.rowcount

def delete_record(conn, row_id):
    cur = conn.execute(f"DELETE FROM {TABLE} WHERE rowid = ?", (row_id,))
    conn.commit()
    return cur.rowcount
