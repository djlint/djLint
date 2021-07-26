#!/usr/bin/python
"""
Check Django template syntax.

usage::

    djlint INPUT -e <extension>

    options:

    --check | will check html formatting for needed changes
    --reformat | will reformat html

"""

import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

import click
from click import echo
from colorama import Fore, Style, deinit, init

from djlint.lint import lint_file
from djlint.reformat import reformat_file
from djlint.settings import ignored_paths


def get_src(src: Path, extension=None):
    """Get source files."""
    if Path.is_file(src):
        return [src]

    # remove leading . from extension
    extension = extension[1:] if extension.startswith(".") else extension

    paths = list(
        filter(
            lambda x: not re.search(ignored_paths, str(x)),
            list(src.glob(r"**/*.%s" % extension)),
        )
    )

    if len(paths) == 0:
        echo(Fore.BLUE + "No files to check! 😢")
        return []

    return paths


def build_output(error):
    """Build output for file errors."""
    errors = sorted(list(error.values())[0], key=lambda x: int(x["line"].split(":")[0]))

    if len(errors) == 0:
        return 0

    echo(
        "{}\n{}\n{}===============================".format(
            Fore.GREEN + Style.BRIGHT, list(error.keys())[0], Style.DIM
        )
        + Style.RESET_ALL
    )

    for message in errors:
        error = bool(message["code"][:1] == "E")
        echo(
            "{} {} {} {} {}".format(
                (Fore.RED if error else Fore.YELLOW),
                message["code"] + Style.RESET_ALL,
                Fore.BLUE + message["line"] + Style.RESET_ALL,
                message["message"],
                Fore.BLUE + message["match"],
            ),
            err=False,
        )
    return len(errors)


def build_check_output(errors, quiet):
    """Build output for reformat check."""
    if len(errors) == 0:
        return 0

    color = {"-": Fore.YELLOW, "+": Fore.GREEN, "@": Style.BRIGHT + Fore.BLUE}

    if quiet is True or len(list(errors.values())[0]) == 0:
        echo(
            Fore.GREEN
            + Style.BRIGHT
            + str(list(errors.keys())[0])
            + Style.DIM
            + Style.RESET_ALL
        )

    else:
        echo(
            "{}\n{}\n{}===============================".format(
                Fore.GREEN + Style.BRIGHT, list(errors.keys())[0], Style.DIM
            )
            + Style.RESET_ALL
        )

        for diff in list(errors.values())[0]:
            echo(
                "{}{}{}".format(
                    color.get(diff[:1], Style.RESET_ALL), diff, Style.RESET_ALL
                ),
                err=False,
            )

    return len(list(filter(lambda x: len(x) > 0, errors.values())))


def build_quantity(size: int):
    """Count files in a list."""
    return "%d file%s" % (size, ("s" if size > 1 else ""))


def build_quantity_tense(size: int):
    """Count files in a list."""
    return "%d file%s %s" % (
        size,
        ("s" if size > 1 or size == 0 else ""),
        ("were" if size > 1 or size == 0 else "was"),
    )


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument(
    "src",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True
    ),
    nargs=1,
    metavar="SRC ...",
)
@click.option(
    "-e",
    "--extension",
    type=str,
    default="html",
    help="File extension to lint",
    show_default=True,
)
@click.option(
    "--reformat",
    is_flag=True,
    help="Reformat the file.",
)
@click.option(
    "--check",
    is_flag=True,
    help="Reformat the file.",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Reformat the file.",
)
def main(src: str, extension: str, reformat: bool, check: bool, quiet: bool):
    """Djlint django template files."""
    file_list = get_src(Path(src), extension)

    if len(file_list) == 0:
        return

    file_quantity = build_quantity(len(file_list))

    message = "Lint"

    if check is True:
        message = "Check"
    elif reformat is True:
        message = "Reformatt"

    echo(
        "%sing %s!\n"
        % (
            message,
            file_quantity,
        )
    )

    worker_count = os.cpu_count()

    if sys.platform == "win32":
        # Work around https://bugs.python.org/issue26903
        worker_count = min(worker_count, 60)

    with ProcessPoolExecutor(max_workers=worker_count) as exe:
        if reformat is True:
            func = partial(reformat_file, check)
            file_errors = exe.map(func, file_list)
        else:
            file_errors = exe.map(lint_file, file_list)

    # format errors
    success_message = ""
    error_count = 0

    if reformat is not True:
        for error in file_errors:
            error_count += build_output(error)

        success_message = "%sed %s, found %d errors." % (
            message,
            file_quantity,
            error_count,
        )
    else:
        for error in file_errors:
            error_count += build_check_output(error, quiet)
            tense_message = (
                build_quantity(error_count) + " would be"
                if check is True
                else build_quantity_tense(error_count)
            )
        success_message = "%s updated." % tense_message

    echo("\n%s\n" % (success_message))


if __name__ == "__main__":
    init(autoreset=True)
    main()
    deinit()
