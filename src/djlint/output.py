"""Build djLint console output."""
import shutil
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import regex as re
from click import echo
from colorama import Fore, Style

from .settings import Config

try:
    # this is used for windows + gitbash to set encoding correctly.
    import sys

    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
# pylint:disable=W0703
except BaseException:
    pass


def print_output(
    config: Config, file_errors: List[Dict[Any, Any]], file_count: int
) -> int:
    """Print results to console."""
    file_quantity = build_quantity(file_count)
    # format errors
    reformat_success_message = ""
    lint_success_message = ""
    lint_error_count = 0
    format_error_count = 0
    print_blanks = config.stdin is False and config.quiet is False

    if print_blanks:
        echo()

    for error in sorted(file_errors, key=lambda x: next(iter(list(x.values())[0]))):
        if error.get("format_message") and config.stdin is False:
            # reformat message
            format_error_count += build_check_output(error["format_message"], config)

        if error.get("lint_message"):
            # lint message
            lint_error_count += build_output(error["lint_message"], config)

    if config.statistics and config.lint:
        build_stats_output([x.get("lint_message") for x in file_errors], config)

    tense_message = (
        build_quantity(format_error_count) + " would be"
        if config.check is True
        else build_quantity_tense(format_error_count)
    )
    reformat_success_message = f"{tense_message} updated."

    error_case = "error" if lint_error_count == 1 else "errors"
    lint_success_message += (
        f"Linted {file_quantity}, found {lint_error_count} {error_case}."
    )

    if print_blanks:
        echo()

    if (
        config.quiet is False
        and config.stdin is False
        and (config.reformat or config.check)
    ):
        reformat_success_color = (
            Fore.RED + Style.BRIGHT if (format_error_count) > 0 else Fore.BLUE
        )
        echo(f"{reformat_success_color}{reformat_success_message}{Style.RESET_ALL}")

    if config.lint and config.quiet is False:
        lint_success_color = (
            Fore.RED + Style.BRIGHT if (lint_error_count) > 0 else Fore.BLUE
        )
        echo(f"{lint_success_color}{lint_success_message}{Style.RESET_ALL}")

    if print_blanks:
        echo()

    return lint_error_count + format_error_count


def build_relative_path(url: str, project_root: Path) -> str:
    """Get path relative to project."""
    url_path = Path(url)
    if project_root != url_path and project_root in url_path.parents:
        return str(url_path.relative_to(project_root.resolve()))

    return url


def build_output(error: dict, config: Config) -> int:
    """Build output for file errors."""
    errors = sorted(
        list(error.values())[0], key=lambda x: tuple(map(int, x["line"].split(":")))
    )

    width, _ = shutil.get_terminal_size()

    if len(errors) == 0:
        return 0

    filename = build_relative_path(list(error.keys())[0], config.project_root.resolve())

    if "{filename}" not in config.linter_output_format and not config.stdin:
        echo(
            f"{Fore.GREEN}{Style.BRIGHT}\n{filename}\n{Style.DIM}"
            + "".join(["─" for x in range(1, width)])
            + Style.RESET_ALL
        )

    for message_dict in errors:
        line = Fore.BLUE + message_dict["line"] + Style.RESET_ALL
        code = (
            (Fore.RED if message_dict["code"][:1] == "E" else Fore.YELLOW)
            + message_dict["code"]
            + Style.RESET_ALL
        )
        message = message_dict["message"]
        match = (
            Fore.BLUE
            + re.sub(r"\s{2,}|\n", " ", message_dict["match"])
            + Style.RESET_ALL
        )

        echo(
            config.linter_output_format.format(
                filename=filename, line=line, code=code, message=message, match=match
            ),
            err=False,
        )

    return len(errors)


def build_check_output(errors: dict, config: Config) -> int:
    """Build output for reformat check."""
    if len(errors) == 0:
        return 0

    color = {"-": Fore.YELLOW, "+": Fore.GREEN, "@": Style.BRIGHT + Fore.BLUE}
    width, _ = shutil.get_terminal_size()

    if config.quiet is False and len(list(errors.values())[0]) > 0:
        echo(
            Fore.GREEN
            + Style.BRIGHT
            + "\n"
            + build_relative_path(list(errors.keys())[0], config.project_root.resolve())
            + "\n"
            + Style.DIM
            + "".join(["─" for x in range(1, width)])
            + Style.RESET_ALL
        )

        for diff in list(errors.values())[0][2:]:
            echo(
                f"{ color.get(diff[:1], Style.RESET_ALL)}{diff}{Style.RESET_ALL}",
                err=False,
            )

    return len(list(filter(lambda x: len(x) > 0, errors.values())))


def build_quantity(size: int) -> str:
    """Count files in a list."""
    return str(size) + " file" + ("s" if size > 1 or size == 0 else "")


def build_quantity_tense(size: int) -> str:
    """Count files in a list."""
    return (
        str(size)
        + " file"
        + ("s" if size > 1 or size == 0 else "")
        + " "
        + ("were" if size > 1 or size == 0 else "was")
    )


def build_stats_output(errors: List[Optional[Any]], config: Config) -> int:
    """Build output for linter statistics."""
    if len(errors) == 0:
        return 0

    codes = []
    for error in errors:
        if error:
            for code in list(error.values())[0]:
                codes.append(code["code"])

    messages = {
        rule["rule"]["name"]: rule["rule"]["message"] for rule in config.linter_rules
    }

    echo()
    width, _ = shutil.get_terminal_size()
    echo(
        f"{Fore.GREEN}{Style.BRIGHT}Statistics{Style.RESET_ALL}\n{Style.DIM}{'─' * width}{Style.RESET_ALL}"
    )

    if messages and codes:
        longest_code = len(max(messages.keys(), key=len))
        longest_count = len(
            str(max(Counter(codes).values(), key=lambda x: len(str(x))))
        )

        for code in sorted(Counter(codes).items()):
            code_space = (longest_code - len(str(code[0]))) * " "
            count_space = (longest_count - len(str(code[1]))) * " "

            echo(
                f"{Fore.YELLOW}{code[0]}{Fore.BLUE} {code_space}{code[1]}{Style.RESET_ALL} {count_space}{messages[code[0]]}"
            )

    return sum(Counter(codes).values())
