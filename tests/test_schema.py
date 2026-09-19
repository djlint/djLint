"""Test that the published json schema still describes djLint's options.

uv run pytest tests/test_schema.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from djlint.settings import _PROFILES, _QUOTE_STYLES  # noqa: PLC2701

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
    assert _schema()["additionalProperties"] is False


def test_the_schema_offers_the_values_djlint_accepts() -> None:
    """The schema and djLint agree on what a value may be.

    A value missing here is one an editor calls a mistake; one too many is
    a value it offers that djLint then refuses.
    """
    properties = _schema()["properties"]

    assert properties["profile"]["enum"] == sorted(_PROFILES)
    assert properties["quote_style"]["enum"] == sorted(_QUOTE_STYLES)
