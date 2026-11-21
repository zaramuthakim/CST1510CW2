"""
WHAT HASHING ACTUALLY DOES
=============================
Using Python's built-in hashlib just to see the shape of it - real password
hashing is Topic 2's job (bcrypt), not this module.
Run:  python 01_what_hashing_actually_does.py
"""

import hashlib

# --- 1. A hash is a fixed-size fingerprint of some input --------------

print(hashlib.sha256(b"password123").hexdigest())
print(hashlib.sha256(b"a much longer piece of text entirely").hexdigest())
# both outputs are the same LENGTH, however long the input was


# --- 2. It is deterministic - same input, same output, every time ------

print(hashlib.sha256(b"password123").hexdigest() == hashlib.sha256(b"password123").hexdigest())   # True


# --- 3. The avalanche effect - one character changes everything -----------

print(hashlib.sha256(b"password123").hexdigest())
print(hashlib.sha256(b"password124").hexdigest())     # one digit different -
                                                          # completely different hash


# --- 4. One-way - you cannot reverse a hash back to the input -----------
# There is no "unhash()" function. Verifying a password means hashing what
# was TYPED and comparing the two hashes - never decrypting anything.

typed_password = "password123"
stored_hash = hashlib.sha256(b"password123").hexdigest()

print(hashlib.sha256(typed_password.encode()).hexdigest() == stored_hash)   # True - a match,
                                                                                # found by hashing
                                                                                # again, not decrypting


# --- 5. Same idea, three fields ---------------------------------------------

file_a = b"survey_2026 contents..."                                # AI / Data Science
file_b = b"survey_2026 contents..."
same_file = hashlib.sha256(file_a).hexdigest() == hashlib.sha256(file_b).hexdigest()
print("files identical:", same_file)

rainbow_table = {hashlib.sha256(p.encode()).hexdigest(): p             # Cyber Security
                  for p in ["123456", "password", "qwerty"]}
leaked_hash = hashlib.sha256(b"password").hexdigest()
print("cracked via rainbow table:", rainbow_table.get(leaked_hash))

published_hash = hashlib.sha256(b"installer bytes...").hexdigest()     # IT
downloaded_file = b"installer bytes..."
print("download untampered:", hashlib.sha256(downloaded_file).hexdigest() == published_hash)


# --- TRY IT ------------------------------------------------------------------
# 1. Hash your own name and a friend's name - confirm the outputs are
#    completely different lengths of... wait, are they? Check.
# 2. Change one character in a string and see how much of the hash changes.
# 3. Explain, in one sentence, why "verify by hashing again and comparing"
#    is different from "decrypt and compare".
