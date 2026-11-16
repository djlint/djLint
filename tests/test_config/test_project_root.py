"""Test which folder's configuration djLint reads.

uv run pytest tests/test_config/test_project_root.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from click import UsageError

from djlint.settings import Config, _warn_once, find_project_root  # noqa: PLC2701

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(autouse=True)
def _fresh_warnings() -> None:
    _warn_once.cache_clear()


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    (tmp_path / "djlint.toml").write_text("indent = 2\n", encoding="utf-8")
    return tmp_path


def test_a_package_without_djlint_settings_takes_the_repository_s(repository: Path) -> None:
    package = repository / "packages" / "web"
    package.mkdir(parents=True)
    (package / "pyproject.toml").write_text('[project]\nname = "web"\n', encoding="utf-8")

    assert find_project_root(package) == repository
    assert Config(str(package)).indent_size == 2


def test_a_package_with_djlint_settings_takes_its_own(repository: Path) -> None:
    package = repository / "web"
    package.mkdir()
    (package / "pyproject.toml").write_text("[tool.djlint]\nindent = 3\n", encoding="utf-8")

    assert find_project_root(package) == package
    assert Config(str(package)).indent_size == 3


def test_a_package_with_a_djlint_file_takes_its_own(repository: Path) -> None:
    package = repository / "web"
    package.mkdir()
    (package / ".djlintrc").write_text('{"indent": 3}', encoding="utf-8")

    assert find_project_root(package) == package
    assert Config(str(package)).indent_size == 3


def test_a_package_with_its_own_rules_is_a_project(repository: Path) -> None:
    package = repository / "web"
    package.mkdir()
    (package / "pyproject.toml").write_text('[project]\nname = "web"\n', encoding="utf-8")
    (package / ".djlint_rules.yaml").write_text(
        "- rule:\n    name: X001\n    message: x\n    patterns: ['x']\n", encoding="utf-8"
    )

    assert find_project_root(package) == package
    assert "X001" in {entry["rule"]["name"] for entry in Config(str(package)).linter_rules}


@pytest.mark.parametrize("value", ["false", '""', "[]"])
def test_djlint_settings_that_are_no_table_stop_the_search(repository: Path, value: str) -> None:
    package = repository / "web"
    package.mkdir()
    (package / "pyproject.toml").write_text(f"[tool]\ndjlint = {value}\n", encoding="utf-8")

    assert find_project_root(package) == package
    with pytest.raises(UsageError, match="its djLint settings are not a table"):
        Config(str(package))


def test_an_empty_djlint_table_is_passed_by(repository: Path) -> None:
    package = repository / "web"
    package.mkdir()
    (package / "pyproject.toml").write_text("[tool.djlint]\n", encoding="utf-8")

    assert find_project_root(package) == repository


def test_the_search_stops_at_the_root_of_a_repository(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text("indent = 2\n", encoding="utf-8")
    checkout = tmp_path / "checkout"
    (checkout / ".git").mkdir(parents=True)

    assert find_project_root(checkout) == checkout
    assert Config(str(checkout)).indent_size == 4


def test_an_unreadable_pyproject_stops_the_search(repository: Path) -> None:
    package = repository / "web"
    package.mkdir()
    (package / "pyproject.toml").write_text("[tool.djlint\n", encoding="utf-8")

    assert find_project_root(package) == package
    with pytest.raises(UsageError, match=r"Could not read pyproject.toml"):
        Config(str(package))


def test_a_djlint_file_beside_pyproject_settings_is_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.djlint]\nindent = 3\n", encoding="utf-8")
    (tmp_path / "djlint.toml").write_text("indent = 2\n", encoding="utf-8")

    assert Config(str(tmp_path)).indent_size == 3
    assert capsys.readouterr().err == (
        "Warning: djlint.toml is not read, as [tool.djlint] in pyproject.toml comes first.\n"
    )


def test_a_djlintrc_beside_djlint_toml_is_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "web"\n', encoding="utf-8")
    (tmp_path / "djlint.toml").write_text("indent = 2\n", encoding="utf-8")
    (tmp_path / ".djlintrc").write_text('{"indent": 3}', encoding="utf-8")

    assert Config(str(tmp_path)).indent_size == 2
    assert capsys.readouterr().err == (
        "Warning: .djlintrc is not read, as djlint.toml comes first.\n"
    )


def test_the_nearest_editorconfig_wins_and_the_ones_above_fill_in(repository: Path) -> None:
    (repository / "djlint.toml").unlink()
    (repository / ".editorconfig").write_text(
        "[*]\nindent_size = 3\nmax_line_length = 90\n", encoding="utf-8"
    )
    package = repository / "web"
    package.mkdir()
    (package / ".editorconfig").write_text("[*.html]\nindent_size = 2\n", encoding="utf-8")

    config = Config(str(package))

    assert (config.indent_size, config.max_line_length) == (2, 90)


def test_an_editorconfig_with_root_ends_the_search(repository: Path) -> None:
    (repository / "djlint.toml").unlink()
    (repository / ".editorconfig").write_text("[*]\nmax_line_length = 90\n", encoding="utf-8")
    package = repository / "web"
    package.mkdir()
    (package / ".editorconfig").write_text(
        "root = true\n\n[*]\nindent_size = 2\n", encoding="utf-8"
    )

    config = Config(str(package))

    assert (config.indent_size, config.max_line_length) == (2, 120)


def test_unset_in_an_editorconfig_drops_what_one_above_gives(repository: Path) -> None:
    (repository / "djlint.toml").unlink()
    (repository / ".editorconfig").write_text("[*]\nindent_size = 3\n", encoding="utf-8")
    package = repository / "web"
    package.mkdir()
    (package / ".editorconfig").write_text("[*]\nindent_size = unset\n", encoding="utf-8")

    assert Config(str(package)).indent_size == 4
