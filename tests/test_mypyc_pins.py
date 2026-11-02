"""Test that the binary wheels are compiled against the locked versions.

The mypyc build hook installs its own dependencies, so it pins them to the
versions in uv.lock, which the tests run with. For mypy that also keeps the
license test_third_party_licenses checks the one the wheels ship.

uv run pytest tests/test_mypyc_pins.py
"""

from __future__ import annotations

import tomllib
from pathlib import Path


def test_mypyc_dependencies_match_the_lock() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    hook = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["hooks"]["mypyc"]
    lock = tomllib.loads(Path("uv.lock").read_text(encoding="utf-8"))
    locked = {package["name"]: package["version"] for package in lock["package"]}

    for requirement in hook["dependencies"]:
        name, sep, version = requirement.partition("==")
        assert sep, f"pin {requirement} in the mypyc build hook"
        if name in locked:
            assert version == locked[name], (
                f"the mypyc build hook pins {requirement}, uv.lock has {locked[name]}"
            )
