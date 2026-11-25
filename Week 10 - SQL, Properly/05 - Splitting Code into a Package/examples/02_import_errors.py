"""
THE IMPORT ERRORS YOU WILL MEET
==================================
Python looks for the packages you import in the folder that holds the script
you run. This file sits NEXT TO the tiny_app folder's parent, not next to
tiny_app itself, so the import fails on purpose.

Run:  python 02_import_errors.py
Then copy this file into 01_a_tiny_package and run it again from there.
"""

import sys
from pathlib import Path

print("Python is looking for packages in:", sys.path[0])

try:
    from tiny_app.pets import add_pet
    print("Import worked: tiny_app was found next to this script.")
except ModuleNotFoundError as error:
    print("ModuleNotFoundError:", error)
    print("-> tiny_app is not in that folder. Move the script next to the tiny_app folder.")

package = Path(__file__).parent / "01_a_tiny_package" / "tiny_app"
print("tiny_app/__init__.py exists:", (package / "__init__.py").exists())
print("(Without __init__.py some tools do not treat the folder as a package: always create it.)")
