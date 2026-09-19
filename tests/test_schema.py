"""Test that the published json schema still describes djLint's options.

uv run pytest tests/test_schema.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any

_SCHEMA = Path("docs/src/static/schema/djlint.json")
_SETTINGS = Path("src/djlint/settings.py")
_CONFIG_KEY_PATTERN = re.compile(
    r"""(?:djlint_settings\.get|setting_int)\(\s*["']([\w-]+)["']"""
)


def _schema() -> dict[str, Any]:
    schema: dict[str, Any] = json.loads(_SCHEMA.read_text(encoding="utf-8"))
    return schema


def _configured_keys() -> set[str]:
    """Every key djLint reads out of a configuration file."""
    return set(
        _CONFIG_KEY_PATTERN.findall(_SETTINGS.read_text(encoding="utf-8"))
    )


def test_the_schema_covers_every_configuration_option() -> None:
    """An option missing here is one an editor calls a mistake."""
    keys = _configured_keys()

    assert keys
    assert set(_schema()["properties"]) - {"$schema"} == keys


def test_every_schema_property_says_what_it_does() -> None:
    assert [
        name
        for name, entry in _schema()["properties"].items()
        if not entry.get("description")
    ] == []


def test_the_schema_turns_away_what_djlint_would() -> None:
    schema = _schema()

    assert schema["additionalProperties"] is False
    assert schema["properties"]["quote_style"]["enum"] == ["double", "single"]
