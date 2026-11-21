# Week 9: Register and log in

**This week your project gains:** `auth.py`. Users register and log in from the terminal. Passwords are hashed with bcrypt and stored in `DATA/users.txt`.

```
CST1510_CW2/
  fetch_data.py       (Week 8)
  auth.py             (new)
  DATA/raw.csv
  DATA/users.txt      (created by registering; not uploaded to GitHub)
```

Students keep working in the same `CST1510_CW2` repository and commit at the end of the lab.

---

## Workshop

| Do |
|---|
| **Demo:** run `python auth.py` in `DEMO/project/`, register, log in, then open `DATA/users.txt` |
| Topic: `01 - Why Hash, Not Encrypt/` (hashing versus encrypting) |
| Topic: `02 - bcrypt in Python/` (`hashpw`, `checkpw`, salt, cost) |
| Topic: `03 - Register and Login/` (register and log in with a text file) |
| Topic: `04 - Keeping Secrets Out of Code/` (environment variables, `.gitignore`; needed again in Week 12) |

## Lab

Everything is in `LAB/W09_Lab.ipynb`: hash a password, check a password, write `generate_hash` and `is_valid_hash`, store users in a text file, then build `auth.py`.

## Folder

| | |
|---|---|
| `DEMO/project/` | the instructor's working example after this week |
| `LAB/` | the step-by-step notebook |
| `0x - topic folders` | walkthrough + examples |
