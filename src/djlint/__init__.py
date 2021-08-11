#!/usr/bin/python
"""
Check Django template syntax.

usage::

    djlint src

    options:

    -e or --extension | <extension>
    --check | will check html formatting for needed changes
    --reformat | will reformat html

"""

import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from pathlib import Path

import click
from click import echo
from colorama import Fore, Style, deinit, init
from tqdm import tqdm

from .lint import lint_file
from .reformat import reformat_file
from .settings import ignored_paths


def get_src(src: Path, extension=None):
    """Get source files."""
    if Path.is_file(src):
        return [src]

    # remove leading . from extension
    extension = extension[1:] if extension.startswith(".") else extension

    paths = list(
        filter(
            lambda x: not re.search(
                "|".join([re.escape(x) for x in ignored_paths]), str(x)
            ),
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
    width, _ = click.get_terminal_size()

    if len(errors) == 0:
        return 0

    echo(
        "{}\n{}\n{}{}".format(
            Fore.GREEN + Style.BRIGHT,
            list(error.keys())[0],
            Style.DIM,
            "".join(["─" for x in range(1, width)]),
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
    width = click.get_terminal_size().columns

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
            "{}\n{}\n{}{}".format(
                Fore.GREEN + Style.BRIGHT,
                list(errors.keys())[0],
                Style.DIM,
                "".join(["─" for x in range(1, width)]),
            )
            + Style.RESET_ALL
        )

        for diff in list(errors.values())[0][2:]:
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
    "-i",
    "--ignore",
    type=str,
    default="",
    help='Codes to ignore. ex: "W013,W014"',
    show_default=False,
)
@click.option(
    "--reformat",
    is_flag=True,
    help="Reformat the file(s).",
)
@click.option(
    "--check",
    is_flag=True,
    help="Check formatting on the file(s).",
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Do not print diff when reformatting.",
)
def main(
    src: str, extension: str, ignore: str, reformat: bool, check: bool, quiet: bool
):
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

    bar_message = (
        "{}{}{} {}{{n_fmt}}/{{total_fmt}}{} {}files{} {{bar}} {}{{elapsed}}{}".format(
            Fore.BLUE + Style.BRIGHT,
            message + "ing",
            Style.RESET_ALL,
            Fore.RED + Style.BRIGHT,
            Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT,
            Style.RESET_ALL,
            Fore.GREEN + Style.BRIGHT,
            Style.RESET_ALL + "    ",
        )
    )

    echo()

    worker_count = os.cpu_count()

    if sys.platform == "win32":
        # Work around https://bugs.python.org/issue26903
        worker_count = min(worker_count, 60)

    with ProcessPoolExecutor(max_workers=worker_count) as exe:
        file_errors = []
        if reformat is True or check is True:
            func = partial(reformat_file, check)
            futures = {
                exe.submit(func, this_file): this_file for this_file in file_list
            }

        else:
            func = partial(lint_file, ignore)
            futures = {
                exe.submit(func, this_file): this_file for this_file in file_list
            }

        elapsed = "00:00"
        with tqdm(
            total=len(file_list),
            bar_format=bar_message,
            colour="BLUE",
            ascii="┈━",
            leave=False,
        ) as pbar:

            for future in as_completed(futures):

                futures[future]
                file_errors.append(future.result())
                pbar.update()
                elapsed = pbar.format_interval(pbar.format_dict["elapsed"])

        finshed_bar_message = (
            "{}{}{} {}{{n_fmt}}/{{total_fmt}}{} {}files{} {{bar}} {}{}{}    ".format(
                Fore.BLUE + Style.BRIGHT,
                message + "ing",
                Style.RESET_ALL,
                Fore.GREEN + Style.BRIGHT,
                Style.RESET_ALL,
                Fore.BLUE + Style.BRIGHT,
                Style.RESET_ALL,
                Fore.GREEN + Style.BRIGHT,
                elapsed,
                Style.RESET_ALL,
            )
        )

        asdf = tqdm(
            total=len(file_list),
            initial=len(file_list),
            bar_format=finshed_bar_message,
            colour="GREEN",
            ascii="┈━",
            leave=True,
        )
        asdf.close()

    # format errors
    success_message = ""
    error_count = 0
    echo()

    if reformat is True or check is True:
        # reformat message
        for error in file_errors:
            error_count += build_check_output(error, quiet)
            tense_message = (
                build_quantity(error_count) + " would be"
                if check is True
                else build_quantity_tense(error_count)
            )
        success_message = "%s updated." % tense_message

    else:
        # lint message
        for error in file_errors:
            error_count += build_output(error)

        success_message = "%sed %s, found %d errors." % (
            message,
            file_quantity,
            error_count,
        )

    success_color = Fore.RED + Style.BRIGHT if error_count > 0 else Fore.BLUE

    echo(f"\n{success_color}{success_message}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    init(autoreset=True)
    main()
    deinit()
