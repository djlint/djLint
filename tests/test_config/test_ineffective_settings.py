"""Test the warnings about settings that do nothing.

uv run pytest tests/test_config/test_ineffective_settings.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.settings import Config, _warn_once  # noqa: PLC2701

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(autouse=True)
def _fresh_warnings() -> None:
    _warn_once.cache_clear()


def test_max_blank_lines_with_preserve_blank_lines(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    Config(str(tmp_path), preserve_blank_lines=True, max_blank_lines=1)

    assert "max_blank_lines has no effect with preserve_blank_lines" in capsys.readouterr().err


def test_max_blank_lines_from_a_config_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / ".djlintrc").write_text(
        '{"preserve_blank_lines": true, "max_blank_lines": 2}', encoding="utf-8"
    )

    Config(str(tmp_path))

    assert "max_blank_lines has no effect" in capsys.readouterr().err


def test_the_default_max_blank_lines_is_not_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    Config(str(tmp_path), preserve_blank_lines=True)

    assert not capsys.readouterr().err


def test_prefer_configuration_without_configuration(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    Config(str(tmp_path), prefer_configuration=True)

    assert "--prefer-configuration has no effect without --configuration" in (
        capsys.readouterr().err
    )


def test_a_warning_is_shown_once_per_run(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    for _ in range(3):
        Config(str(tmp_path), preserve_blank_lines=True, max_blank_lines=1)

    assert capsys.readouterr().err.count("max_blank_lines has no effect") == 1
