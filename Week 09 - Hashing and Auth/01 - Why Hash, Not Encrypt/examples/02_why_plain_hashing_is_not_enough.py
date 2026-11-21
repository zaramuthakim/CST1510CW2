"""
WHY PLAIN HASHING IS NOT ENOUGH
===================================
A small, honest demonstration of a rainbow-table-style attack - and why
bcrypt (Topic 2) fixes exactly this.
Run:  python 02_why_plain_hashing_is_not_enough.py
"""

import hashlib

# --- 1. Build a "rainbow table" of common passwords -------------------
# An attacker does this once, in advance - for millions of common passwords.

common_passwords = ["123456", "password", "qwerty", "admin", "letmein"]
rainbow_table = {hashlib.sha256(p.encode()).hexdigest(): p for p in common_passwords}


# --- 2. A "stolen" database of plain sha256 hashes, no salt -----------

stolen_hashes = {
    "alice": hashlib.sha256(b"qwerty").hexdigest(),
    "bob": hashlib.sha256(b"Tr0ub4dor&3xotic").hexdigest(),   # a genuinely strong password
}


# --- 3. The attack - just a dictionary lookup, instant --------------------

for username, stolen_hash in stolen_hashes.items():
    if stolen_hash in rainbow_table:
        print(f"{username}: CRACKED instantly -> {rainbow_table[stolen_hash]}")
    else:
        print(f"{username}: not in the table - safe from THIS attack")


# --- 4. Salting defeats this completely --------------------------------
# Add something random and unique, per user, before hashing. Now the
# pre-computed table is useless - it was built for the password ALONE.

import secrets

salt_alice = secrets.token_hex(8)
salted_hash = hashlib.sha256((salt_alice + "qwerty").encode()).hexdigest()

print(salted_hash in rainbow_table)     # False - the table has no idea about this salt


# --- 5. This is exactly what bcrypt does for you automatically -----------
# bcrypt generates and stores the salt as part of the hash itself - you
# never manage it by hand. Topic 2 shows the real functions.


# --- TRY IT ------------------------------------------------------------------
# 1. Add "letmein123" to stolen_hashes and check whether it is in the table.
# 2. Explain why bob's strong password was already safe from THIS particular
#    attack, even without a salt.
# 3. Explain, in one sentence, why the salt has to be different for every
#    user, not the same for everyone.
