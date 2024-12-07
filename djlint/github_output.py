"""Build djLint GitHub workflow command output."""

from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
from click import echo

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence
    from djlint.settings import Config
    from djlint.types import LintError, ProcessResult


def print_github_output(
    config: Config, file_errors: Iterable[ProcessResult], file_count: int
) -> int:
    """Print results as GitHub workflow commands."""
    lint_error_count = 0
    format_error_count = 0

    for error in sorted(
        file_errors,
        key=lambda x: next(iter(next(iter(x.values())))),
    ):
        if error.get("format_message") and not config.stdin:
            format_error_count += print_format_errors(error["format_message"], config)
        if error.get("lint_message"):
            lint_error_count += print_lint_errors(error["lint_message"], config)

    return lint_error_count + format_error_count


def print_lint_errors(error: Mapping[str, Iterable[LintError]], config: Config) -> int:
    """Print lint errors in GitHub format."""
    errors = sorted(
        next(iter(error.values())),
        key=lambda x: tuple(int(i) for i in x["line"].split(":")),
    )
    if not errors:
        return 0

    filename = build_relative_path(next(iter(error)), config.project_root)

    for message_dict in errors:
        line = message_dict["line"].split(":")[0]
        level = "error" if message_dict["code"].startswith("E") else "warning"
        echo(
            f"::{level} file={filename},line={line}::{message_dict['code']} {message_dict['message']}"
        )

    return len(errors)


def print_format_errors(errors: Mapping[str, Sequence[str]], config: Config) -> int:
    """Print format errors in GitHub format."""
    if not errors:
        return 0

    filename = build_relative_path(next(iter(errors)), config.project_root)
    if bool(next(iter(errors.values()))):
        echo(f"::error file={filename}::Formatting changes required")

    return sum(1 for v in errors.values() if v)


def build_relative_path(url: str, project_root: Path) -> str:
    """Get path relative to project."""
    url_path = Path(url)
    if project_root != url_path and project_root in url_path.parents:
        return str(url_path.relative_to(project_root))
    return url
