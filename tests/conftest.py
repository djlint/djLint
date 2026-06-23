"""Djlint test config."""

from __future__ import annotations

import difflib
import shutil
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest
from click import style
from click.testing import CliRunner

from djlint import main as djlint
from djlint.settings import Config

if TYPE_CHECKING:
    import os
    from collections.abc import Iterator, Mapping
    from typing import TextIO

    from typing_extensions import Any

    from djlint.types import LintError


@pytest.fixture
def runner(monkeypatch: pytest.MonkeyPatch) -> CliRunner:
    """Click runner for djlint tests."""
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    return CliRunner()


@pytest.fixture
def tmp_file() -> Iterator[tempfile._TemporaryFileWrapper[bytes]]:
    """Create a temp file for formatting."""
    tmp = tempfile.NamedTemporaryFile(delete=False)  # noqa: SIM115
    try:
        with tmp:
            yield tmp
    finally:
        Path(tmp.name).unlink(missing_ok=True)


def printer(expected: str, source: str, actual: str) -> None:
    width, _ = shutil.get_terminal_size()

    expected_text = "Expected"
    actual_text = "Actual"
    diff_text = "Diff"
    source_text = "Source"

    expected_width = (width - len(expected_text) - 2) // 2
    actual_width = (width - len(actual_text) - 2) // 2
    diff_width = (width - len(diff_text) - 2) // 2
    source_width = (width - len(source_text) - 2) // 2

    colors: dict[str, dict[str, Any]] = {
        "-": {"fg": "yellow"},
        "+": {"fg": "green"},
        "@": {"fg": "blue", "bold": True},
    }

    print()
    print(
        style(
            f"{'─' * source_width} {source_text} {'─' * source_width}",
            fg="blue",
            bold=True,
        )
    )
    print()
    print(source)
    print()
    print(
        style(
            f"{'─' * expected_width} {expected_text} {'─' * expected_width}",
            fg="blue",
            bold=True,
        )
    )
    print()
    print(expected)
    print()
    print(
        style(
            f"{'─' * actual_width} {actual_text} {'─' * actual_width}",
            fg="blue",
            bold=True,
        )
    )
    print()
    print(actual)
    print()
    print(
        style(
            f"{'─' * diff_width} {diff_text} {'─' * diff_width}",
            fg="blue",
            bold=True,
        )
    )
    print()
    for diff in tuple(
        difflib.unified_diff(expected.split("\n"), actual.split("\n"))
    )[2:]:
        print(style(diff, **colors.get(diff[:1], {})))


def lint_printer(
    source: str, expected: list[LintError], actual: list[LintError]
) -> None:
    width, _ = shutil.get_terminal_size()

    expected_text = "Expected Rules"
    actual_text = "Actual"
    source_text = "Source"

    expected_width = (width - len(expected_text) - 2) // 2
    actual_width = (width - len(actual_text) - 2) // 2
    source_width = (width - len(source_text) - 2) // 2

    print()
    print(
        style(
            f"{'─' * source_width} {source_text} {'─' * source_width}",
            fg="blue",
            bold=True,
        )
    )
    print()
    print(source)
    print()

    print(
        style(
            f"{'─' * expected_width} {expected_text} {'─' * expected_width}",
            fg="blue",
            bold=True,
        )
    )
    print()
    for x in expected:
        print(
            f"{style(x['code'], fg='red', bold=True)} {x['line']} {x['match']}"
        )
        print(f"     {x['message']}")
        print()

    print(
        style(
            f"{'─' * actual_width} {actual_text} {'─' * actual_width}",
            fg="blue",
            bold=True,
        )
    )
    print()

    for x in actual:
        print(
            f"{style(x['code'], fg='red', bold=True)} {x['line']} {x['match']}"
        )
        print(f"     {x['message']}")
        print()
    if not actual:
        print(style("No codes found.", fg="yellow"))
        print()

    else:
        print(style(str(actual), fg="yellow"))
        print()


def write_to_file(the_file: str | os.PathLike[str], the_text: bytes) -> None:
    """Shortcode for write some bytes to a file."""
    Path(the_file).write_bytes(the_text)


def reformat(
    the_file: TextIO, runner: CliRunner, the_text: bytes, profile: str = "html"
) -> SimpleNamespace:
    write_to_file(the_file.name, the_text)
    result = runner.invoke(
        djlint, (the_file.name, "--profile", profile, "--reformat")
    )
    return SimpleNamespace(
        text=Path(the_file.name).read_text(encoding="utf-8"),
        exit_code=result.exit_code,
    )


def config_builder(args: Mapping[str, Any] | None = None) -> Config:
    if args:
        return Config("dummy/source.html", **args)
    return Config("dummy/source.html")


@pytest.fixture
def basic_config() -> Config:
    """Return a config object with default basic options."""
    return Config("dummy/source.html")


@pytest.fixture
def django_config() -> Config:
    """Return a config object with django profile."""
    return Config("dummy/source.html", profile="django")


@pytest.fixture
def jinja_config() -> Config:
    """Return a config object with jinja."""
    return Config("dummy/source.html", profile="jinja")


@pytest.fixture
def handlebars_config() -> Config:
    """Return a config object with handlebars."""
    return Config("dummy/source.html", profile="handlebars")


@pytest.fixture
def nunjucks_config() -> Config:
    """Return a config object with nunjucks."""
    return Config("dummy/source.html", profile="nunjucks")
