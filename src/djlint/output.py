"""Build djLint console output."""
import shutil
from typing import Any, Dict, List

import regex as re
from click import echo
from colorama import Fore, Style

from .settings import Config


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

    if config.stdin is False or config.lint:
        echo()

    for error in file_errors:
        if error.get("format_message") and config.stdin is False:
            # reformat message
            format_error_count += build_check_output(
                error["format_message"], config.quiet
            )

        if error.get("lint_message"):
            # lint message
            lint_error_count += build_output(error["lint_message"])

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

    if config.stdin is False or config.lint:
        echo()

    if config.stdin is False and (config.reformat or config.check):
        reformat_success_color = (
            Fore.RED + Style.BRIGHT if (format_error_count) > 0 else Fore.BLUE
        )
        echo(f"{reformat_success_color}{reformat_success_message}{Style.RESET_ALL}")

    if config.lint:
        lint_success_color = (
            Fore.RED + Style.BRIGHT if (lint_error_count) > 0 else Fore.BLUE
        )
        echo(f"{lint_success_color}{lint_success_message}{Style.RESET_ALL}")

    if config.stdin is False or config.lint:
        echo()

    return lint_error_count + format_error_count


def build_output(error: dict) -> int:
    """Build output for file errors."""
    errors = sorted(list(error.values())[0], key=lambda x: int(x["line"].split(":")[0]))
    width, _ = shutil.get_terminal_size()

    if len(errors) == 0:
        return 0

    echo(
        f"{Fore.GREEN}{Style.BRIGHT}\n{list(error.keys())[0]}\n{Style.DIM}"
        + "".join(["─" for x in range(1, width)])
        + Style.RESET_ALL
    )

    for message in errors:
        echo(
            (Fore.RED if bool(message["code"][:1] == "E") else Fore.YELLOW)
            + message["code"]
            + Style.RESET_ALL
            + Fore.BLUE
            + " "
            + message["line"]
            + Style.RESET_ALL
            + " "
            + re.sub(r"\s{2,}", " ", message["message"])
            + Fore.BLUE
            + " "
            + message["match"],
            err=False,
        )
    return len(errors)


def build_check_output(errors: dict, quiet: bool) -> int:
    """Build output for reformat check."""
    if len(errors) == 0:
        return 0

    color = {"-": Fore.YELLOW, "+": Fore.GREEN, "@": Style.BRIGHT + Fore.BLUE}
    width, _ = shutil.get_terminal_size()

    if quiet is True and len(list(errors.values())[0]) > 0:
        echo(
            Fore.GREEN
            + Style.BRIGHT
            + str(list(errors.keys())[0])
            + Style.DIM
            + Style.RESET_ALL
        )

    elif quiet is False and len(list(errors.values())[0]) > 0:
        echo(
            Fore.GREEN
            + Style.BRIGHT
            + "\n"
            + str(list(errors.keys())[0])
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