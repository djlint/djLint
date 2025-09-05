"""Test precedence between djlint.toml and .djlint.toml.

Tests that djlint.toml takes precedence over .djlint.toml when both exist.

"""

from __future__ import annotations

from pathlib import Path

from djlint.settings import Config


def test_djlint_toml_precedence() -> None:
    """Test that djlint.toml takes precedence over .djlint.toml."""
    config = Config(str(Path(__file__).parent / "blank.html"))

    # Should use values from djlint.toml, not .djlint.toml
    assert config.indent == 4 * " "  # From djlint.toml
    assert config.profile == "html"  # From djlint.toml
    # These should not be "django" and 2 spaces from .djlint.toml