#!/usr/bin/python
"""
Check Django template syntax.

usage::

    djlint INPUT -e <extension>

"""

import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import click
import yaml
from click import echo
from colorama import Fore, Style, deinit, init

rules = yaml.load(
    (Path(__file__).parent / "rules.yaml").read_text(encoding="utf8"),
    Loader=yaml.SafeLoader,
)


def get_line(start, line_ends):
    """Get the line number and index of match."""
    #    print(start, line_ends)
    line = list(filter(lambda pair: pair["end"] > start, line_ends))[0]

    return "%d:%d" % (line_ends.index(line) + 1, start - line["start"])


def lint_file(this_file: Path):
    """Check file for formatting errors."""
    file_name = str(this_file)
    errors: dict = {file_name: []}
    html = this_file.read_text(encoding="utf8")

    # build list of line ends for file
    line_ends = [
        {"start": m.start(), "end": m.end()}
        for m in re.finditer(r"(?:.*\n)|(?:[^\n]+$)", html)
    ]

    for rule in rules:
        rule = rule["rule"]

        for pattern in rule["patterns"]:
            for match in re.finditer(pattern, html, re.DOTALL):
                errors[file_name].append(
                    {
                        "code": rule["name"],
                        "line": get_line(match.start(), line_ends),
                        "match": match.group()[:20].strip(),
                        "message": rule["message"],
                    }
                )

    return errors


def get_src(src: Path, extension=None):
    """Get source files."""
    if Path.is_file(src):
        return [src]

    # remove leading . from extension
    extension = extension[1:] if extension.startswith(".") else extension

    paths = list(src.glob(r"**/*.%s" % extension))

    if len(paths) == 0:
        echo(Fore.BLUE + "No files to lint! 😢")
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
def main(src: str, extension: str):
    """Djlint django template files."""
    file_list = get_src(Path(src), extension)

    if len(file_list) == 0:
        return

    file_quantity = "%d file%s" % (len(file_list), ("s" if len(file_list) > 1 else ""))

    echo("\nChecking %s!" % file_quantity)

    worker_count = os.cpu_count()

    if sys.platform == "win32":
        # Work around https://bugs.python.org/issue26903
        worker_count = min(worker_count, 60)

    with ProcessPoolExecutor(max_workers=worker_count) as exe:
        file_errors = exe.map(lint_file, file_list)

    # format errors
    error_count = 0
    for error in file_errors:
        error_count += build_output(error)

    success_message = "Checked %s, found %d errors." % (
        file_quantity,
        error_count,
    )

    echo("\n%s\n" % (success_message))


if __name__ == "__main__":
    init(autoreset=True)
    main()
    deinit()
