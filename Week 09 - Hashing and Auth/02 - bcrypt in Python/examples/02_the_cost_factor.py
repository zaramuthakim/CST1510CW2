"""
THE COST FACTOR
==================
bcrypt is slow ON PURPOSE. Measuring exactly how slow, and why that is a
feature, not a bug.
Run:  python 02_the_cost_factor.py
"""

import bcrypt
import time

# --- 1. gensalt() takes a "rounds" argument - the cost factor ------------
# Each increase doubles the work. Higher = slower = safer against
# brute-force, at the cost of a slower login for everyone, including you.

password = b"a-password-to-time"

for rounds in (10, 12, 14):
    start = time.perf_counter()
    bcrypt.hashpw(password, bcrypt.gensalt(rounds=rounds))
    elapsed = time.perf_counter() - start
    print(f"cost factor {rounds}: {elapsed:.3f} seconds")


# --- 2. Why this matters to a legitimate user vs an attacker ---------------
# A 0.4-second delay is imperceptible when YOU log in once.
# An attacker trying a million passwords pays that delay a million times -
# turning "seconds" into days.

attempts = 1_000_000
seconds_per_hash = 0.4     # a typical cost-factor-12 timing
total_seconds = attempts * seconds_per_hash
print(f"{attempts:,} attempts at cost 12 would take about "
      f"{total_seconds / 60 / 60 / 24:.1f} days")


# --- 3. The default is already a reasonable choice -------------------------
# bcrypt.gensalt() with no argument uses a sensible default (12 in this
# version) - you do not need to tune this yourself unless you have a
# specific reason to.

print(bcrypt.gensalt())     # the cost factor is encoded right there, e.g. $2b$12$...


# --- TRY IT ------------------------------------------------------------------
# 1. Time cost factor 8 as well, alongside 10, 12 and 14. How much faster
#    is it?
# 2. Explain, in one sentence, why doubling the cost factor's number does
#    not just double the time - it roughly doubles it per +1, so the growth
#    is much steeper than it looks.
# 3. Given your own timing for cost 12, estimate how long 10 million
#    attempts would take.
