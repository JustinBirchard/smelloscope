# __init__.py
#* Smelloscope Version 1.3
#* file last updated 12/2/22
"""Loads smello.toml into memory
"""

import pathlib
import tomli

path = pathlib.Path(__file__).parent / "smello.toml"
with path.open(mode="rb") as fp:
    smello = tomli.load(fp)
