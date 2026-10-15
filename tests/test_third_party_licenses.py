"""Test that LICENSE-THIRD-PARTY carries the current mypyc runtime license.

The binary wheels are compiled with mypyc, which builds its runtime into
them, so they must ship mypy's license.

uv run pytest tests/test_third_party_licenses.py
"""

from __future__ import annotations

from importlib.metadata import distribution
from pathlib import Path


def test_mypy_license_is_current() -> None:
    mypy_license = distribution("mypy").read_text("licenses/LICENSE")
    assert mypy_license is not None

    shipped = Path("LICENSE-THIRD-PARTY").read_text(encoding="utf-8")

    assert mypy_license.strip() in shipped, (
        "mypy's license changed: replace its text in LICENSE-THIRD-PARTY"
    )
