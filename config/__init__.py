# __init__.py

import pathlib
import tomli

path = pathlib.Path(__file__).parent / "smello.toml"
with path.open(mode="rb") as fp:
    smello = tomli.load(fp)
