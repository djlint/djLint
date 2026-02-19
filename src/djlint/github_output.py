"""Build djLint GitHub workflow command output."""

from __future__ import annotations

from typing import TYPE_CHECKING

from click import echo

from djlint.output import build_relative_path

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

    from djlint.settings import Config
    from djlint.types import LintError, ProcessResult


def escape_data(data: str) -> str:
    """Escape data for GitHub Actions."""
    return data.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def escape_property(data: str) -> str:
    """Escape property for GitHub Actions."""
    return (
        data.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
        .replace(":", "%3A")
        .replace(",", "%2C")
    )


def print_github_output(
    config: Config, file_errors: Iterable[ProcessResult], _file_count: int
) -> int:
    """Print results as GitHub workflow commands."""
    lint_error_count = 0
    format_error_count = 0

    for error in sorted(
        file_errors,
        key=lambda x: next(iter(next(iter(x.values())))),  # type: ignore[call-overload]
    ):
        if error.get("format_message") and not config.stdin:
            format_error_count += print_format_errors(
                error["format_message"], config
            )
        if error.get("lint_message"):
            lint_error_count += print_lint_errors(error["lint_message"], config)

    return lint_error_count + format_error_count


def print_lint_errors(
    error: Mapping[str, Iterable[LintError]], config: Config
) -> int:
    """Print lint errors in GitHub format."""
    errors = sorted(
        next(iter(error.values())),
        key=lambda x: tuple(int(i) for i in x["line"].split(":")),
    )
    if not errors:
        return 0

    filename = escape_property(
        build_relative_path(next(iter(error)), config.project_root)
    )

    for message_dict in errors:
        line = escape_property(message_dict["line"].split(":")[0])
        level = "error" if message_dict["code"].startswith("E") else "warning"
        message = escape_data(
            f"{message_dict['code']} {message_dict['message']}"
        )
        echo(f"::{level} file={filename},line={line}::{message}")

    return len(errors)


def print_format_errors(
    errors: Mapping[str, Sequence[str]], config: Config
) -> int:
    """Print format errors in GitHub format."""
    if not errors:
        return 0

    filename = escape_property(
        build_relative_path(next(iter(errors)), config.project_root)
    )
    if bool(next(iter(errors.values()))):
        echo(f"::error file={filename}::Formatting changes required")

    return sum(1 for v in errors.values() if v)
