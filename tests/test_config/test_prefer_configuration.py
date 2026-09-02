"""Test prefer_configuration.

uv run pytest tests/test_config/test_prefer_configuration.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.settings import Config

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A project whose own file and named file set the same thing."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "pyproject.toml").write_text(
        '[tool.djlint]\nprofile = "jinja"\nindent = 2\n', encoding="utf-8"
    )
    (tmp_path / "global.djlintrc").write_text(
        '{"indent": 8, "extend_exclude": "sub"}', encoding="utf-8"
    )
    (tmp_path / "page.html").write_text("<div></div>", encoding="utf-8")
    return tmp_path


def test_the_project_file_wins_by_default(project: Path) -> None:
    """The named file is a global one, so the project's own file wins."""
    config = Config(
        str(project / "page.html"), configuration=project / "global.djlintrc"
    )

    assert config.indent_size == 2


def test_the_named_file_wins_when_asked(project: Path) -> None:
    config = Config(
        str(project / "page.html"),
        configuration=project / "global.djlintrc",
        prefer_configuration=True,
    )

    assert config.indent_size == 8


def test_a_setting_only_the_project_file_has_still_applies(
    project: Path,
) -> None:
    """Preferring the named file layers it over the project's, not past it."""
    config = Config(
        str(project / "page.html"),
        configuration=project / "global.djlintrc",
        prefer_configuration=True,
    )

    assert config.profile == "jinja"


def test_a_setting_only_the_named_file_has_still_applies(project: Path) -> None:
    config = Config(
        str(project / "page.html"), configuration=project / "global.djlintrc"
    )

    assert "sub" in config.exclude


def test_the_flag_alone_changes_nothing(project: Path) -> None:
    """With no file named, there is nothing to prefer."""
    plain = Config(str(project / "page.html"))
    preferred = Config(str(project / "page.html"), prefer_configuration=True)

    assert plain.indent_size == preferred.indent_size == 2
