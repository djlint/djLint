#!/usr/bin/python
"""djLint · lint and reformat HTML templates."""

import os
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from pathlib import Path
from typing import Dict, List, Optional

import click
from click import echo
from colorama import Fore, Style, deinit, init
from tqdm import tqdm

from .lint import lint_file
from .output import print_output
from .reformat import reformat_file
from .settings import Config
from .src import get_src


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument(
    "src",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True
    ),
    nargs=-1,
    required=True,
    metavar="SRC ...",
)
@click.version_option(package_name="djlint")
@click.option(
    "-e",
    "--extension",
    type=str,
    default="",
    help="File extension to check [default: html]",
    show_default=False,
)
@click.option(
    "-i",
    "--ignore",
    type=str,
    default="",
    help='Codes to ignore. ex: "H014,H017"',
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
    "--indent",
    type=int,
    help="Indent spacing. [default: 4]",
    show_default=False,
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Do not print diff when reformatting.",
)
@click.option(
    "--profile",
    type=str,
    help="Enable defaults by template language. ops: django, jinja, nunjucks, handlebars, golang",
)
@click.option(
    "--require-pragma",
    is_flag=True,
    help="Only format or lint files that starts with a comment with the text 'djlint:on'",
)
@click.option(
    "--lint",
    is_flag=True,
    help="Lint for common issues. [default option]",
)
@click.option(
    "--use-gitignore",
    is_flag=True,
    help="Use .gitignore file to extend excludes.",
)
def main(
    src: List[str],
    extension: str,
    ignore: str,
    reformat: bool,
    indent: Optional[int],
    check: bool,
    quiet: bool,
    profile: str,
    require_pragma: bool,
    lint: bool,
    use_gitignore: bool,
) -> None:
    """djLint · HTML template linter and formatter."""
    config = Config(
        src[0],
        extension=extension,
        ignore=ignore,
        indent=indent,
        quiet=quiet,
        profile=profile,
        require_pragma=require_pragma,
        lint=lint or not (reformat or check),
        reformat=reformat,
        check=check,
        use_gitignore=use_gitignore,
    )

    temp_file = None

    if "-" in src:
        stdin_stream = click.get_text_stream("stdin")
        stdin_text = stdin_stream.read()

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(str.encode(stdin_text))
        temp_file.seek(0)

        file_list = get_src([Path(temp_file.name)], config)

    else:
        file_list = get_src([Path(x) for x in src], config)

    if len(file_list) == 0:
        return

    message = ""

    if config.check is True:
        message = "Checking"
    elif config.reformat is True:
        message = "Reformatting"

    if config.lint:
        if message != "":
            message += " and "
        message += "Linting"

    # pylint: disable=C0209
    bar_message = (
        "{}{}{} {}{{n_fmt}}/{{total_fmt}}{} {}files{} {{bar}} {}{{elapsed}}{}".format(
            Fore.BLUE + Style.BRIGHT,
            message,
            Style.RESET_ALL,
            Fore.RED + Style.BRIGHT,
            Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT,
            Style.RESET_ALL,
            Fore.GREEN + Style.BRIGHT,
            Style.RESET_ALL + "    ",
        )
    )
    if config.stdin is False or config.lint:
        echo()

    worker_count = os.cpu_count() or 1

    if sys.platform == "win32":
        # Work around https://bugs.python.org/issue26903
        worker_count = min(worker_count, 60)

    with ProcessPoolExecutor(max_workers=worker_count) as exe:
        file_errors = []

        func = partial(process, config)
        futures = {exe.submit(func, this_file): this_file for this_file in file_list}

        if temp_file is None or config.lint:
            elapsed = "00:00"
            with tqdm(
                total=len(file_list),
                bar_format=bar_message,
                colour="BLUE",
                ascii="┈━",
                leave=False,
            ) as pbar:

                for future in as_completed(futures):

                    file_errors.append(future.result())
                    pbar.update()
                    elapsed = pbar.format_interval(pbar.format_dict["elapsed"])

            finshed_bar_message = "{}{}{} {}{{n_fmt}}/{{total_fmt}}{} {}files{} {{bar}} {}{}{}    ".format(
                Fore.BLUE + Style.BRIGHT,
                message,
                Style.RESET_ALL,
                Fore.GREEN + Style.BRIGHT,
                Style.RESET_ALL,
                Fore.BLUE + Style.BRIGHT,
                Style.RESET_ALL,
                Fore.GREEN + Style.BRIGHT,
                elapsed,
                Style.RESET_ALL,
            )

            finished_bar = tqdm(
                total=len(file_list),
                initial=len(file_list),
                bar_format=finshed_bar_message,
                colour="GREEN",
                ascii="┈━",
                leave=True,
            )
            finished_bar.close()

    if temp_file and (config.reformat or config.check):
        # if using stdin, only give back formatted code.
        echo(Path(temp_file.name).read_text(encoding="utf8").rstrip())

    if temp_file:
        temp_file.close()
        os.unlink(temp_file.name)

    if bool(print_output(config, file_errors, len(file_list))):
        sys.exit(1)


def process(config: Config, this_file: Path) -> Dict:
    """Run linter or formatter."""
    output = {}
    if config.reformat or config.check:
        output["format_message"] = reformat_file(config, this_file)

    if config.lint:
        output["lint_message"] = lint_file(config, this_file)

    return output


if __name__ == "__main__":
    init(autoreset=True)
    main()
    deinit()
