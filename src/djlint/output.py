"""Build djLint console output."""

from __future__ import annotations

import shutil
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

import regex as re
from click import echo, style

if TYPE_CHECKING:
    from collections.abc import Collection, Iterable, Mapping, Sequence
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError, ProcessResult


_OUTPUT_WHITESPACE_PATTERN: Final = re.compile(
    r"\s{2,}|\n", cache_pattern=False
)


def report_on_stderr(config: Config, /) -> bool:
    """Whether the report has to keep off stdout.

    In stdin mode stdout carries the file back to whatever piped it in, so a
    report written there ends up inside the buffer the editor saves.
    """
    return config.stdin and (config.reformat or config.check)


def first_filename(result: ProcessResult) -> str:
    """The file a worker's result is about, for ordering the report."""
    messages = result.get("lint_message") or result.get("format_message") or {}
    return next(iter(messages), "")


def finding_position(finding: LintError) -> tuple[int, int]:
    """Line and column of a finding, for ordering a file's report."""
    line, column = finding["line"].split(":")
    return int(line), int(column)


def print_output(
    config: Config, file_errors: Sequence[ProcessResult], file_count: int
) -> int:
    """Print results to console."""
    file_quantity = build_quantity(file_count)
    lint_error_count = 0
    format_error_count = 0
    print_blanks = not config.stdin and not config.quiet

    if print_blanks:
        echo()

    for error in sorted(file_errors, key=first_filename):
        if error.get("format_message"):
            if config.stdin and config.check:
                format_error_count += count_format_errors(
                    error["format_message"]
                )
            elif not config.stdin:
                format_error_count += build_check_output(
                    error["format_message"], config
                )

        if error.get("lint_message"):
            lint_error_count += build_output(error["lint_message"], config)

    if config.statistics and config.lint:
        build_stats_output(
            tuple(x.get("lint_message") for x in file_errors), config
        )

    tense_message = (
        build_quantity(format_error_count) + " would be"
        if config.check
        else build_quantity_tense(format_error_count)
    )
    reformat_success_message = f"{tense_message} updated."

    error_case = "error" if lint_error_count == 1 else "errors"
    lint_success_message = (
        f"Linted {file_quantity}, found {lint_error_count} {error_case}."
    )

    if print_blanks:
        echo()

    if (
        not config.quiet
        and not config.stdin
        and (config.reformat or config.check)
    ):
        echo(
            style(
                reformat_success_message,
                fg="red" if format_error_count > 0 else "blue",
                bold=format_error_count > 0,
            )
        )

    if config.lint and not config.quiet:
        echo(
            style(
                lint_success_message,
                fg="red" if lint_error_count > 0 else "blue",
                bold=lint_error_count > 0,
            ),
            err=report_on_stderr(config),
        )

    if print_blanks:
        echo()

    return lint_error_count + format_error_count


def build_relative_path(url: str, project_root: Path) -> str:
    """Get path relative to project."""
    url_path = Path(url)
    if project_root != url_path and project_root in url_path.parents:
        return str(url_path.relative_to(project_root))

    return url


def build_output(
    error: Mapping[str, Iterable[LintError]], config: Config
) -> int:
    """Build output for file errors."""
    errors = sorted(next(iter(error.values())), key=finding_position)

    if not errors:
        return 0

    err = report_on_stderr(config)
    filename = build_relative_path(next(iter(error)), config.project_root)

    if "{filename}" not in config.linter_output_format and not config.stdin:  # noqa: RUF027
        width, _ = shutil.get_terminal_size()
        echo(
            style(f"\n{filename}\n", fg="green", bold=True)
            + style("─" * (width - 1), dim=True)
        )

    for message_dict in errors:
        line = style(message_dict["line"], fg="blue")
        code = style(
            message_dict["code"],
            fg="red" if message_dict["code"][:1] == "E" else "yellow",
        )
        message = message_dict["message"]
        match = style(
            _OUTPUT_WHITESPACE_PATTERN.sub(" ", message_dict["match"]),
            fg="blue",
        )

        echo(
            config.linter_output_format.format(
                filename=filename,
                line=line,
                code=code,
                message=message,
                match=match,
            ),
            err=err,
        )

    return len(errors)


def build_check_output(
    errors: Mapping[str, Sequence[str]], config: Config
) -> int:
    """Build output for reformat check."""
    if not errors:
        return 0

    if not config.quiet and bool(next(iter(errors.values()))):
        colors: dict[str, dict[str, Any]] = {
            "-": {"fg": "yellow"},
            "+": {"fg": "green"},
            "@": {"fg": "blue", "bold": True},
        }
        width, _ = shutil.get_terminal_size()
        echo(
            style(
                f"\n{build_relative_path(next(iter(errors)), config.project_root)}\n",
                fg="green",
                bold=True,
            )
            + style("─" * (width - 1), dim=True)
        )

        for diff in next(iter(errors.values()))[2:]:
            echo(style(diff, **colors.get(diff[:1], {})))

    return count_format_errors(errors)


def count_format_errors(errors: Mapping[str, Sequence[str]]) -> int:
    """Count files with formatting changes."""
    return sum(1 for v in errors.values() if v)


def build_quantity(size: int) -> str:
    """Count files, as in "1 file" or "3 files"."""
    return f"{size} file" + ("" if size == 1 else "s")


def build_quantity_tense(size: int) -> str:
    """Count files with a verb, as in "1 file was" or "3 files were"."""
    return build_quantity(size) + (" was" if size == 1 else " were")


def build_stats_output(
    errors: Collection[Mapping[str, Iterable[LintError]] | None], config: Config
) -> int:
    """Build output for linter statistics."""
    if not errors:
        return 0

    codes = tuple(
        code["code"]
        for error in errors
        if error
        for code in next(iter(error.values()))
    )

    messages = {
        rule["rule"]["name"]: rule["rule"]["message"]
        for rule in config.linter_rules
    }

    err = report_on_stderr(config)
    echo(err=err)
    width, _ = shutil.get_terminal_size()
    echo(
        style("Statistics", fg="green", bold=True)
        + "\n"
        + style("─" * width, dim=True),
        err=err,
    )

    counts = Counter(codes)

    if counts:
        code_width = max(len(code) for code in counts)
        count_width = len(str(max(counts.values())))

        for code, count in sorted(counts.items()):
            echo(
                (
                    style(f"{code:<{code_width}}", fg="yellow")
                    + style(f" {count:<{count_width}}", fg="blue")
                    + f" {messages.get(code, '')}"
                ).rstrip(),
                err=err,
            )

    return len(codes)
