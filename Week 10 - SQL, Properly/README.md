# Week 10: Move to a database

**This week your project gains:** a SQLite database (`DATA/app.db`) for the users and the API data, and the code moves into a package called `app_model`.

```
CST1510_CW2/
  fetch_data.py       (Week 8)
  load_data.py        (new) copies users.txt and raw.csv into the database
  app_model/          (new)
    __init__.py  db.py  schema.py  users.py  records.py
  DATA/raw.csv  DATA/app.db
```

`auth.py` from Week 9 is replaced by `app_model/users.py`. The two hash functions are copied across unchanged.

---

## Workshop

| Do |
|---|
| **Demo:** run `python load_data.py` in `DEMO/project/` and watch 500 rows land in a table |
| Topic: `01 - Connecting and Creating Tables/` (`connect`, `CREATE TABLE`, types) |
| Topic: `02 - Inserting and Querying/` (`INSERT`, `SELECT`, `WHERE`, injection, `COUNT` and `GROUP BY`) |
| Topic: `03 - Updating, Deleting and the Safe Pattern/` (`UPDATE`, `DELETE`, `with`) |
| Topic: `04 - Migrating Real Data In/` (CSV files into tables with pandas, `rowid`, `read_sql`) |
| Topic: `05 - Splitting Code into a Package/` (modules, `__init__.py`, imports; needed for the `app_model` package) |

## Lab

Do `LAB/W10_SQL_Basics.ipynb` first (plain SQL, no Python). Then `LAB/W10_Lab.ipynb`:

| Part | |
|---|---|
| Steps 1 to 3 | `sqlite3` in Python, `?` placeholders, functions that take `conn` |
| Step 4 | pandas: `to_sql` and `read_sql` |
| Step 5 | build the `app_model` package: `db.py`, `schema.py`, `users.py`, `records.py` |
| Steps 6 to 8 | `load_data.py`, check everything, keep the database private, commit |

## Folder

| | |
|---|---|
| `DEMO/project/` | the instructor's working example after this week |
| `LAB/` | the step-by-step notebooks |
| `0x - topic folders` | walkthrough + examples |
