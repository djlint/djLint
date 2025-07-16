"""Djlint test config."""

from __future__ import annotations

import difflib
import shutil
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner
from colorama import Fore, Style

from djlint import main as djlint
from djlint.settings import Config

if TYPE_CHECKING:
    import os
    from collections.abc import Iterator, Mapping
    from typing import TextIO

    from typing_extensions import Any

    from djlint.types import LintError


@pytest.fixture
def runner() -> CliRunner:
    """Click runner for djlint tests."""
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

    color = {"-": Fore.YELLOW, "+": Fore.GREEN, "@": Style.BRIGHT + Fore.BLUE}

    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * source_width} {source_text} {'─' * source_width}{Style.RESET_ALL}"
    )
    print()
    print(source)
    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * expected_width} {expected_text} {'─' * expected_width}{Style.RESET_ALL}"
    )
    print()
    print(expected)
    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * actual_width} {actual_text} {'─' * actual_width}{Style.RESET_ALL}"
    )
    print()
    print(actual)
    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * diff_width} {diff_text} {'─' * diff_width}{Style.RESET_ALL}"
    )
    print()
    for diff in tuple(
        difflib.unified_diff(expected.split("\n"), actual.split("\n"))
    )[2:]:
        print(f"{color.get(diff[:1], Style.RESET_ALL)}{diff}{Style.RESET_ALL}")


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
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * source_width} {source_text} {'─' * source_width}{Style.RESET_ALL}"
    )
    print()
    print(source)
    print()

    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * expected_width} {expected_text} {'─' * expected_width}{Style.RESET_ALL}"
    )
    print()
    for x in expected:
        print(
            f"{Fore.RED}{Style.BRIGHT}{x['code']}{Style.RESET_ALL} {x['line']} {x['match']}"
        )
        print(f"     {x['message']}")
        print()

    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * actual_width} {actual_text} {'─' * actual_width}{Style.RESET_ALL}"
    )
    print()

    for x in actual:
        print(
            f"{Fore.RED}{Style.BRIGHT}{x['code']}{Style.RESET_ALL} {x['line']} {x['match']}"
        )
        print(f"     {x['message']}")
        print()
    if not actual:
        print(f"{Fore.YELLOW}No codes found.{Style.RESET_ALL}")
        print()

    else:
        print(f"{Fore.YELLOW}{actual}{Style.RESET_ALL}")
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
