"""
ENVIRONMENT VARIABLES
========================
Where a real secret lives - not in your code, not in your repository.
Run:  python 01_environment_variables.py
"""

import os

# --- 1. A hard-coded secret is a mistake, not just bad style --------------
# If this line is ever committed to a public GitHub repo, the secret is
# compromised the moment it is pushed - deleting it later does not help,
# it is already in the commit history forever.

# BAD - never do this:
# API_KEY = "sk-abc123realsecretvalue"


# --- 2. Environment variables live outside your code entirely -----------
# Set one in your terminal before running the script:
#     export MY_API_KEY="sk-abc123realsecretvalue"     (macOS/Linux)
#     setx MY_API_KEY "sk-abc123realsecretvalue"         (Windows)

api_key = os.environ.get("MY_API_KEY")
print(api_key)     # None if it was never set - that is expected here


# --- 3. A sensible default, and a clear message when it's missing --------

api_key = os.environ.get("MY_API_KEY", "not set")
if api_key == "not set":
    print("MY_API_KEY is not set - set it before running this for real.")
else:
    print("Key loaded (not printed here on purpose).")


# --- 4. os.environ works the same way for anything secret ----------------
# Not just API keys - database passwords, tokens, anything that must never
# appear in a file you might commit.


# --- 5. When a variable is required, raise instead of defaulting ---------
# A default like "not set" is fine for something optional. When the program
# genuinely cannot continue without it, raise a clear error instead of
# letting it fail later with a confusing message.

def require_env(name):
    """Return the named environment variable, or raise a clear error if it is missing."""
    value = os.environ.get(name)
    if value is None:
        raise RuntimeError(f"{name} is not set. Set it before running this.")
    return value

try:
    require_env("MY_API_KEY")
except RuntimeError as e:
    print("Caught it:", e)


# --- 6. Same idea, three fields ---------------------------------------------

kaggle_token = os.environ.get("KAGGLE_TOKEN", "not set")            # AI / Data Science
print("Kaggle token loaded:", kaggle_token != "not set")

threat_intel_key = os.environ.get("THREAT_INTEL_KEY", "not set")     # Cyber Security
print("threat-intel key loaded:", threat_intel_key != "not set")

monitoring_token = os.environ.get("MONITORING_TOKEN", "not set")     # IT
print("monitoring token loaded:", monitoring_token != "not set")


# --- TRY IT ------------------------------------------------------------------
# 1. In your terminal, set an environment variable and read it back with
#    os.environ.get().
# 2. Call require_env() on a variable you know IS set (e.g. "HOME" or "PATH")
#    and check it returns the value instead of raising.
# 3. Explain, in one sentence, why deleting a secret from your code AFTER
#    committing it does not actually fix the leak.
