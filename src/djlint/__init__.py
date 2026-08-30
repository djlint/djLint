"""djLint · lint and reformat HTML templates."""
# ruff: noqa: RUF067

from __future__ import annotations

import errno
import io
import os
import sys
from functools import partial, wraps
from pathlib import Path
from typing import TYPE_CHECKING

import click
from click import echo, style

if sys.version_info >= (3, 13):
    from os import process_cpu_count
else:
    from os import cpu_count as process_cpu_count

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import TextIO

    from djlint.settings import Config
    from djlint.types import ProcessResult


def _use_utf8(stream: TextIO) -> None:
    """Retune a std stream to utf-8, whatever codepage the locale hands us.

    Windows consoles and Git Bash arrive on the locale codepage, which cannot
    hold the report's rules or a template's own text. Naming the error handler
    is not decoration: passing an encoding alone silently resets it to strict,
    and a stream carrying diagnostics must never abort the run reporting them.
    """
    try:
        stream.reconfigure(  # type: ignore[attr-defined]
            encoding="utf-8", errors="backslashreplace"
        )
    except Exception:
        pass


def _consumer_hung_up(error: Exception) -> bool:
    """Whether the failure is just the other end of the pipe closing.

    `djlint . | head -1` leaves djLint writing into a pipe nobody is
    reading. POSIX reports that as BrokenPipeError; Windows raises a plain
    OSError with EINVAL out of the flush that follows. EINVAL is broader
    than the case at hand, so the cost of guessing wrong is weighed rather
    than avoided: a mistaken match loses a traceback, never an exit code.
    """
    if isinstance(error, BrokenPipeError):
        return True
    return isinstance(error, OSError) and error.errno in {
        errno.EINVAL,
        errno.EPIPE,
    }


def _fail_with_usage_code(func: Callable[..., None]) -> Callable[..., None]:
    """Keep djLint failing apart from djLint finding things.

    Left to reach the interpreter, an unhandled error exits 1, the same code
    as "found lint errors" or "would reformat", and a pipeline cannot tell a
    crash from a normal failing run: a template djLint cannot read looks
    exactly like a template it disliked. So failures exit 2 instead,
    alongside the usage errors click already exits 2 for. The traceback is
    still printed, so bug reports lose nothing.
    """

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> None:
        try:
            func(*args, **kwargs)
        except (click.ClickException, click.exceptions.Exit, click.Abort):
            # click's own control flow, including --help and usage errors
            raise
        except Exception as error:
            if _consumer_hung_up(error):
                # nothing is left to report to, and the report that was
                # interrupted has nowhere to go, so leave quietly. stdout
                # is swapped out first: the interpreter flushes it once
                # more on the way out, and that flush failing against the
                # same dead pipe would replace the exit code with 120.
                sys.stdout = io.StringIO()
                sys.exit(2)

            import traceback  # noqa: PLC0415

            traceback.print_exc()
            echo(
                style(
                    "djLint failed and did not finish checking. This is not a"
                    " clean run. Please report unexpected failures at"
                    " https://github.com/djlint/djLint/issues",
                    fg="red",
                    bold=True,
                ),
                err=True,
            )
            sys.exit(2)

    return wrapper


@click.command(
    "main",
    context_settings={"help_option_names": ["-h", "--help"]},
    help="djLint · HTML template linter and formatter.",
)
@click.argument(
    "src",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        allow_dash=True,
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
@click.option("--reformat", is_flag=True, help="Reformat the file(s).")
@click.option("--check", is_flag=True, help="Check formatting on the file(s).")
@click.option(
    "--stdin-filename",
    type=str,
    default=None,
    help=(
        "Filename to use for per-file-ignores and messages when reading"
        " from stdin. [default: -]"
    ),
    show_default=False,
)
@click.option(
    "--indent",
    type=int,
    help="Indent spacing. [default: 4]",
    show_default=False,
)
@click.option(
    "--quiet", is_flag=True, help="Do not print diff when reformatting."
)
@click.option(
    "--profile",
    type=str,
    help="Enable defaults by template language. ops: django, jinja, nunjucks, handlebars, liquid, golang, angular, tera, askama, html [default: html]",
)
@click.option(
    "--require-pragma",
    is_flag=True,
    help="Only format or lint files that starts with a comment with the text 'djlint:on'",
)
@click.option(
    "--lint", is_flag=True, help="Lint for common issues. [default option]"
)
@click.option(
    "--use-gitignore",
    is_flag=True,
    help="Use .gitignore file to extend excludes.",
)
@click.option(
    "--allow-empty-input",
    is_flag=True,
    help="Exit with 0 instead of 2 when the given paths match no files.",
)
@click.option("--warn", is_flag=True, help="Return errors as warnings.")
@click.option(
    "--preserve-leading-space",
    is_flag=True,
    help="Attempt to preserve leading space on text.",
)
@click.option(
    "--preserve-blank-lines",
    is_flag=True,
    help="Attempt to preserve blank lines.",
)
@click.option(
    "--preserve-class-newlines",
    is_flag=True,
    help="Preserve line breaks inside multiline class attributes.",
)
@click.option(
    "--format-css", is_flag=True, help="Also format contents of <style> tags."
)
@click.option(
    "--format-js", is_flag=True, help="Also format contents of <script> tags."
)
@click.option(
    "--format-attribute-js-json",
    is_flag=True,
    help="Also format JavaScript/JSON inside HTML attributes.",
)
@click.option(
    "--format-attribute-js-json-pattern",
    type=str,
    default="",
    help="Regex pattern to match JavaScript attributes.",
    show_default=False,
)
@click.option(
    "--format-attribute-js-json-min-props",
    type=int,
    help="Minimum number of properties to treat attribute content as JS/JSON.",
    show_default=False,
)
@click.option(
    "--configuration",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
        path_type=Path,
    ),
    help="Path to global configuration file in djlint.toml, .djlint.toml, or .djlintrc format",
)
@click.option(
    "--rules",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to custom rules file in .djlint_rules.yaml format",
)
@click.option(
    "--statistics",
    is_flag=True,
    help="Count the number of occurrences of each error/warning code.",
)
@click.option(
    "--include",
    type=str,
    default="",
    help='Codes to include. ex: "H014,H017"',
    show_default=False,
)
@click.option(
    "--ignore-case", is_flag=True, help="Do not fix case on known html tags."
)
@click.option(
    "--ignore-blocks",
    type=str,
    default="",
    help="Comma list of template blocks to not indent.",
)
@click.option(
    "--blank-line-after-tag",
    type=str,
    default="",
    help="Add an additional blank line after {% <tag> ... %} tag groups.",
)
@click.option(
    "--blank-line-before-tag",
    type=str,
    default="",
    help="Add an additional blank line before {% <tag> ... %} tag groups.",
)
@click.option(
    "--line-break-after-multiline-tag",
    is_flag=True,
    help="Do not condense the content of multi-line tags into the line of the last attribute.",
)
@click.option(
    "--custom-blocks",
    type=str,
    default="",
    help="Indent custom template blocks. For example {% toc %}...{% endtoc %}",
)
@click.option(
    "--custom-html",
    type=str,
    default="",
    help="Indent custom HTML tags. For example <mjml>",
)
@click.option(
    "--exclude",
    type=str,
    default="",
    help="Override the default exclude paths.",
)
@click.option(
    "--extend-exclude",
    type=str,
    default="",
    help="Add additional paths to the default exclude.",
)
@click.option(
    "--linter-output-format",
    type=str,
    default="",
    help="Customize order of linter output message.",
)
@click.option(
    "--max-line-length",
    type=int,
    help="Max line length. [default: 120]",
    show_default=False,
)
@click.option(
    "--max-attribute-length",
    type=int,
    help="Max attribute length. [default: 70]",
    show_default=False,
)
@click.option(
    "--format-attribute-template-tags",
    is_flag=True,
    help="Attempt to format template syntax inside of tag attributes.",
)
@click.option(
    "--single-attribute-per-line",
    is_flag=True,
    help="When an opening tag wraps, put each attribute on its own line.",
)
@click.option(
    "--per-file-ignores",
    type=(str, str),
    multiple=True,
    help="Ignore linter rules on a per-file basis.",
)
@click.option(
    "--indent-css", type=int, help="Set CSS indent level.", show_default=False
)
@click.option(
    "--indent-js", type=int, help="Set JS indent level.", show_default=False
)
@click.option(
    "--close-void-tags",
    is_flag=True,
    help="Add closing mark on known void tags. Ex: <img> becomes <img />",
)
@click.option(
    "--no-line-after-yaml",
    is_flag=True,
    help="Do not add a blank line after yaml front matter.",
)
@click.option(
    "--no-function-formatting",
    is_flag=True,
    help="Do not attempt to format function contents.",
)
@click.option(
    "--no-set-formatting",
    is_flag=True,
    help="Do not attempt to format set contents.",
)
@click.option(
    "--max-blank-lines",
    type=int,
    help="Consolidate blank lines down to x lines. [default: 0]",
    show_default=False,
)
@click.option(
    "--github-output/--no-github-output",
    is_flag=True,
    default=None,
    help="Output GitHub-compatible formatting.",
)
@partial  # mypyc-compiled wheels crash without this hack
@_fail_with_usage_code
def main(
    *,
    src: tuple[str, ...],
    extension: str,
    ignore: str,
    reformat: bool,
    indent: int | None,
    check: bool,
    stdin_filename: str | None,
    quiet: bool,
    profile: str | None,
    require_pragma: bool,
    lint: bool,
    use_gitignore: bool,
    allow_empty_input: bool,
    warn: bool,
    preserve_leading_space: bool,
    preserve_blank_lines: bool,
    preserve_class_newlines: bool,
    format_css: bool,
    format_js: bool,
    configuration: Path | None,
    rules: Path | None,
    statistics: bool,
    include: str,
    ignore_case: bool,
    ignore_blocks: str,
    blank_line_after_tag: str,
    blank_line_before_tag: str,
    line_break_after_multiline_tag: bool,
    custom_blocks: str,
    custom_html: str,
    exclude: str,
    extend_exclude: str,
    linter_output_format: str,
    max_line_length: int | None,
    max_attribute_length: int | None,
    format_attribute_template_tags: bool,
    single_attribute_per_line: bool,
    format_attribute_js_json: bool,
    format_attribute_js_json_pattern: str,
    format_attribute_js_json_min_props: int | None,
    per_file_ignores: tuple[tuple[str, str], ...],
    indent_css: int | None,
    indent_js: int | None,
    close_void_tags: bool,
    no_line_after_yaml: bool,
    no_function_formatting: bool,
    no_set_formatting: bool,
    max_blank_lines: int | None,
    github_output: bool | None = None,
) -> None:
    """djLint · HTML template linter and formatter."""
    # Both streams, before anything can write to either: djlint.output is
    # imported too late for the config warnings and is skipped altogether on
    # the --require-pragma path, and a library import has no business
    # retuning the process's streams.
    _use_utf8(sys.stdout)
    _use_utf8(sys.stderr)

    from djlint.settings import Config  # noqa: PLC0415
    from djlint.src import (  # noqa: PLC0415
        get_src,
        has_pragma,
        print_no_files_to_check,
    )

    if os.getenv("NO_COLOR") is not None:
        click.get_current_context().color = False

    if github_output is None:
        github_output = bool(os.getenv("GITHUB_ACTIONS"))

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
        stdin_filename=stdin_filename,
        use_gitignore=use_gitignore,
        allow_empty_input=allow_empty_input,
        warn=warn,
        preserve_leading_space=preserve_leading_space,
        preserve_blank_lines=preserve_blank_lines,
        preserve_class_newlines=preserve_class_newlines,
        format_css=format_css,
        format_js=format_js,
        configuration=configuration,
        rules=rules,
        statistics=statistics,
        include=include,
        ignore_case=ignore_case,
        ignore_blocks=ignore_blocks,
        blank_line_after_tag=blank_line_after_tag,
        blank_line_before_tag=blank_line_before_tag,
        line_break_after_multiline_tag=line_break_after_multiline_tag,
        custom_blocks=custom_blocks,
        custom_html=custom_html,
        exclude=exclude,
        extend_exclude=extend_exclude,
        linter_output_format=linter_output_format,
        max_line_length=max_line_length,
        max_attribute_length=max_attribute_length,
        format_attribute_template_tags=format_attribute_template_tags,
        single_attribute_per_line=single_attribute_per_line,
        format_attribute_js_json=format_attribute_js_json,
        format_attribute_js_json_pattern=format_attribute_js_json_pattern,
        format_attribute_js_json_min_props=format_attribute_js_json_min_props,
        per_file_ignores=per_file_ignores,
        indent_css=indent_css,
        indent_js=indent_js,
        close_void_tags=close_void_tags,
        no_line_after_yaml=no_line_after_yaml,
        no_function_formatting=no_function_formatting,
        no_set_formatting=no_set_formatting,
        max_blank_lines=max_blank_lines,
        github_output=github_output,
        stdin="-" in src,
    )

    if "-" in src and not config.files:
        # click's get_text_stream helper is deprecated, so decode stdin here:
        # the bytes on the pipe are utf-8 whatever the locale's default is.
        # Strict is deliberate: --reformat hands this text straight back to
        # the editor that piped it in, so papering over a bad byte would
        # silently corrupt the buffer it gets written to. newline="" is the
        # same bargain for line endings - universal newlines would hand the
        # formatter LF for a CRLF buffer and quietly rewrite every line of
        # it, where reformat_file opens with newline="" and keeps them.
        try:
            sys.stdin.reconfigure(  # type: ignore[union-attr]
                encoding="utf-8", errors="strict", newline=""
            )
        except Exception:
            pass
        try:
            stdin_text = sys.stdin.read()
        except UnicodeDecodeError as e:
            # the pipe held something that is not utf-8. That is bad input,
            # not a djLint bug, so it must not surface as a crash report.
            msg = f"Input on stdin is not valid UTF-8: {e}"
            raise click.UsageError(msg) from None

        if config.require_pragma and not has_pragma(
            config, stdin_text.split("\n", 1)[0]
        ):
            # the pragma is an opt-in, so input without one was skipped on
            # purpose. Hand it back byte for byte: an editor piping a buffer
            # through djLint writes whatever lands on stdout back to the file.
            print_no_files_to_check(excluded=True)
            if config.reformat or config.check:
                echo(stdin_text.encode("utf-8"), nl=False)
            return

        file_error, formatted_code = process_stdin(config, stdin_text)
        file_errors = [file_error]
        files_count = 1

        if config.reformat or config.check:
            # formatter() already ends its output with the line ending the
            # input used, so stripping and re-adding one here would flatten
            # a CRLF buffer's last line on its way back to the editor.
            echo((formatted_code or "").encode("utf-8"), nl=False)

    else:
        file_src = config.files if "-" in src and config.files else src
        file_list, excluded = get_src((Path(x) for x in file_src), config)
        if not file_list:
            print_no_files_to_check(excluded=excluded)
            # excluding every candidate is the configuration doing its job,
            # so it is a success. Matching nothing at all means the run
            # checked nothing it was asked to check, which is a usage error
            # and stays loud unless it was opted into.
            if excluded or config.allow_empty_input:
                return
            sys.exit(2)

        if config.check:
            message = "Checking"
        elif config.reformat:
            message = "Reformatting"
        else:
            message = ""

        if config.lint:
            if message:
                message += " and "
            message += "Linting"

        if not config.quiet and not config.github_output:
            echo()

        files_count = len(file_list)
        max_workers = min(process_cpu_count() or 1, files_count)

        file_errors = []
        progress_label = click.style(
            f"{message} {files_count}/{files_count} files", fg="blue", bold=True
        )
        progress_template = (
            click.style(f"{message} %(info)s files", fg="blue", bold=True)
            + " "
            + click.style("[%(bar)s]", fg="blue")
        )
        with click.progressbar(
            length=files_count,
            label=progress_label,
            show_eta=False,
            show_percent=False,
            show_pos=True,
            bar_template=progress_template,
            file=sys.stderr,
            hidden=config.github_output or config.quiet,
        ) as bar:
            if max_workers == 1:
                for this_file in file_list:
                    file_errors.append(process(config, this_file))
                    bar.update(1)
            else:
                import concurrent.futures  # noqa: PLC0415

                if _is_free_threaded_python():
                    executor_cls = concurrent.futures.ThreadPoolExecutor
                else:
                    executor_cls = concurrent.futures.ProcessPoolExecutor
                    if sys.platform == "win32":
                        # Windows has a hard limit of 61 processes
                        max_workers = min(max_workers, 61)

                with executor_cls(max_workers=max_workers) as exe:
                    futures = {
                        exe.submit(process, config, this_file): this_file
                        for this_file in file_list
                    }
                    for future in concurrent.futures.as_completed(futures):
                        file_errors.append(future.result())
                        bar.update(1)

    if config.github_output:
        from djlint.github_output import print_github_output  # noqa: PLC0415

        if (
            print_github_output(config, file_errors, files_count)
            and not config.warn
        ):
            sys.exit(1)

    else:
        from djlint.output import print_output  # noqa: PLC0415

        if print_output(config, file_errors, files_count) and not config.warn:
            sys.exit(1)


def _is_free_threaded_python() -> bool:
    is_gil_enabled = getattr(sys, "_is_gil_enabled", None)
    if not callable(is_gil_enabled):
        return False
    return not bool(is_gil_enabled())


def process(config: Config, this_file: Path) -> ProcessResult:
    """Run linter or formatter."""
    output: ProcessResult = {}
    if config.reformat or config.check:
        from djlint.reformat import reformat_file  # noqa: PLC0415

        output["format_message"] = reformat_file(config, this_file)

    if config.lint:
        from djlint.lint import lint_file  # noqa: PLC0415

        output["lint_message"] = lint_file(config, this_file)

    return output


def process_stdin(
    config: Config, stdin_text: str
) -> tuple[ProcessResult, str | None]:
    """Run linter or formatter on stdin."""
    output: ProcessResult = {}
    html = stdin_text
    formatted_code = None
    stdin_filename = config.stdin_filename or "-"

    if config.reformat or config.check:
        from djlint.reformat import reformat_string  # noqa: PLC0415

        output["format_message"], formatted_code = reformat_string(
            config, stdin_text, stdin_filename
        )
        html = formatted_code

    if config.lint:
        from djlint.lint import linter  # noqa: PLC0415

        # as lint_file() does, match per_file_ignores against a posix path
        output["lint_message"] = linter(
            config, html, stdin_filename, Path(stdin_filename).as_posix()
        )

    return output, formatted_code
