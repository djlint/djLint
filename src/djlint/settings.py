"""Settings for reformater."""

from __future__ import annotations

import copy
import json
import tomllib
from functools import cache
from itertools import chain
from pathlib import Path
from string import Formatter
from typing import TYPE_CHECKING, final

import regex as re
import yaml
from click import BadParameter, UsageError, echo, style

from djlint.const import (
    HTML_TAG_NAMES,
    HTML_VOID_ELEMENTS,
    QUOTED_ATTRIBUTE_VALUE,
    SKIP_TEMPLATE_TAG,
    TAG_START,
    TEMPLATE_TAG_NAME,
    TEMPLATE_TAG_WHOLE,
)
from djlint.helpers import (
    RE_FLAGS_IMSX,
    RE_FLAGS_IMX,
    RE_FLAGS_ISX,
    RE_FLAGS_IX,
    YAML_FRONT_MATTER,
    compile_pattern,
    compile_rule_pattern,
    split_option_list,
)
from djlint.lint import build_flags

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator, Mapping, Set as AbstractSet
    from typing import Any, Final

    from pathspec import PathSpec, Pattern
    from typing_extensions import TypeVar

    _TMappingStrAny = TypeVar("_TMappingStrAny", bound=Mapping[str, Any])


_JS_JSON_OBJECT_PATTERN: Final = compile_pattern(r"^\s*\{(?![{%]).*\}\s*$", RE_FLAGS_IX)
_JS_JSON_STRING_PATTERN: Final = compile_pattern(r'["\']([^"\']*)["\']', RE_FLAGS_IX)
_JS_JSON_PROPERTY_PATTERN: Final = compile_pattern(
    r"""
    (?:^|[,{]\s*)
    (?:
        [a-zA-Z_$][a-zA-Z0-9_$]*\s*:
      | (?:get|set)\s+[a-zA-Z_$][a-zA-Z0-9_$]*\s*\(
      | (?:async\s+)?\*?\s*[a-zA-Z_$][a-zA-Z0-9_$]*\s*\(
    )
    """,
    RE_FLAGS_IX,
)

DJLINT_TOML_CONFIG_FILES: Final = ("djlint.toml", ".djlint.toml")

_QUOTE_STYLES: Final = frozenset(("double", "single"))


def _sets_djlint(pyproject: Path) -> bool:
    """Whether a pyproject.toml has djLint settings.

    Only a missing or empty [tool.djlint] table doesn't count. One that can't
    be read, or that isn't a table, does, so that its error is what the run
    reports, rather than the settings of a folder above it.
    """
    try:
        settings = load_pyproject_config(pyproject)
    except (AttributeError, OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return True
    return not (isinstance(settings, dict) and not settings)


def find_project_root(src: Path) -> Path:
    """Find the folder whose configuration applies to src.

    That's the first folder upward with a djlint.toml, a .djlint.toml, a
    .djlintrc, a .djlint_rules.yaml or a pyproject.toml with djLint settings,
    or the root of a repository, which the search never passes. A pyproject.toml without
    djLint settings, as a package in a monorepo has, is passed by, so the
    configuration of the repository still applies to it; with nothing above,
    its folder is the root.
    """
    settingless: Path | None = None
    for directory in (src, *src.parents):
        if any(
            (directory / name).is_file()
            for name in (*DJLINT_TOML_CONFIG_FILES, ".djlintrc", ".djlint_rules.yaml")
        ):
            return directory

        pyproject = directory / "pyproject.toml"
        if pyproject.is_file():
            if _sets_djlint(pyproject):
                return directory
            settingless = settingless or directory

        if (directory / ".git").exists() or (directory / ".hg").is_dir():
            return directory

    return settingless or (src if src.is_dir() else src.parent)


def load_gitignore(root: Path) -> PathSpec[Pattern]:
    """Search upstream for a .gitignore file.

    pathspec is imported here, as most runs don't read a gitignore and it
    takes as long to import as building a Config.
    """
    from pathspec import PathSpec  # noqa: PLC0415

    try:
        from pathspec.patterns.gitignore import GitIgnorePatternError  # noqa: PLC0415
    except ImportError:
        from pathspec.patterns.gitwildmatch import GitWildMatchPatternError as GitIgnorePatternError  # type: ignore[attr-defined] # noqa: PLC0415

        pattern = "gitwildmatch"
    else:
        pattern = "gitignore"

    gitignore = root / ".gitignore"
    if gitignore.is_file():
        with gitignore.open(encoding="utf-8") as this_file:
            git_lines = this_file.readlines()
    else:
        git_lines = []

    try:
        return PathSpec.from_lines(pattern, git_lines)

    except GitIgnorePatternError as e:
        msg = f"Could not parse {gitignore}: {e}"
        raise UsageError(msg) from None


def find_pyproject(root: Path) -> Path | None:
    """Search upstream for a pyproject.toml file."""
    pyproject = root / "pyproject.toml"

    if pyproject.is_file():
        return pyproject

    return None


def find_djlint_toml(root: Path) -> Path | None:
    """Search upstream for a djlint.toml or .djlint.toml file."""
    for config_file in DJLINT_TOML_CONFIG_FILES:
        djlint_toml = root / config_file

        if djlint_toml.is_file():
            return djlint_toml

    return None


def find_djlintrc(root: Path) -> Path | None:
    """Search upstream for a .djlintrc file."""
    djlintrc = root / ".djlintrc"

    if djlintrc.is_file():
        return djlintrc

    return None


def find_djlint_rules(root: Path) -> Path | None:
    """Search upstream for a .djlint_rules.yaml file."""
    rules = root / ".djlint_rules.yaml"

    if rules.is_file():
        return rules

    return None


_EDITORCONFIG_PROPERTIES: Final = frozenset(("indent_size", "max_line_length"))


def _closing_bracket(glob: str, start: int) -> int:
    """The index of the `]` that closes the `[` at start, or -1 without one."""
    i = start + 1
    while i < len(glob):
        if glob[i] == "\\":
            i += 2
            continue
        if glob[i] == "]" and i > start + 1:
            return i
        i += 1
    return -1


def _brace(glob: str, start: int) -> tuple[int, bool]:
    """The index of the `}` closing the `{` at start, or -1, and if it has alternatives.

    Only a `,` of its own makes them: one unescaped, and outside a nested
    `{...}` or a `[...]`.
    """
    depth = 0
    alternatives = False
    i = start
    while i < len(glob):
        char = glob[i]
        if char == "\\":
            i += 2
            continue
        if char == "[" and (close := _closing_bracket(glob, i)) != -1:
            i = close + 1
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if not depth:
                return i, alternatives
        elif char == "," and depth == 1:
            alternatives = True
        i += 1
    return -1, False


def _character_class(body: str) -> str:
    """The regex of the members of a `[...]` class, `!` or `^` first negating it."""
    negated = body[:1] in {"!", "^"}
    members: list[str] = ["^"] if negated else []
    i = 1 if negated else 0
    while i < len(body):
        if body[i] == "\\" and i + 1 < len(body):
            members.append(re.escape(body[i + 1]))
            i += 2
            continue
        # An unescaped `-` makes a range, as in the glob.
        members.append("-" if body[i] == "-" else re.escape(body[i]))
        i += 1
    return f"[{''.join(members)}]"


@final
class _EditorConfigGlob:
    """An EditorConfig section glob, as the specification reads it.

    `*` and `?` stay within one folder, `**` crosses them, `[...]` and `[!...]`
    are character classes, `{a,b}` alternatives, which can nest, and `{1..9}` a
    number in that range. A glob without a `/` matches a file's name in any
    folder below the .editorconfig; one with a `/` is matched from the folder
    of that file.
    """

    __slots__ = ("pattern", "ranges")

    def __init__(self, glob: str) -> None:
        out: list[str] = []
        # Each {1..9} captures its number, which matches() checks against the
        # range, as the EditorConfig core library does. A number written with
        # a leading zero, such as 060, is never in one.
        ranges: list[tuple[int, int]] = []
        # For each open brace, whether it holds alternatives or is a literal one.
        braces: list[bool] = []
        i = 0
        while i < len(glob):
            char = glob[i]
            if char == "\\" and i + 1 < len(glob):
                out.append(re.escape(glob[i + 1]))
                i += 2
                continue
            if char == "*":
                # A `**/` at the start or after a `/` also stands for no
                # folder, so `pages/**/*.html` takes pages/index.html too.
                if glob.startswith("**/", i) and (i == 0 or glob[i - 1] == "/"):
                    out.append("(?:.*/)?")
                    i += 3
                    continue
                if glob.startswith("**", i):
                    out.append(".*")
                    i += 2
                    continue
                out.append("[^/]*")
            elif char == "?":
                out.append("[^/]")
            elif char == "[" and (close := _closing_bracket(glob, i)) != -1:
                body = glob[i + 1 : close]
                # A class never takes a `/`, so one with a `/` in it is plain
                # text, wildcards and all, as in the core library.
                out.append(
                    re.escape(glob[i : close + 1]) if "/" in body else _character_class(body)
                )
                i = close + 1
                continue
            elif char == "{":
                close, alternatives = _brace(glob, i)
                span = glob[i + 1 : close] if close != -1 else ""
                if numbers := re.fullmatch(r"([+-]?[0-9]+)\.\.([+-]?[0-9]+)", span):
                    low, high = sorted((int(numbers[1]), int(numbers[2])))
                    ranges.append((low, high))
                    out.append("([+-]?(?:0|[1-9][0-9]*))")
                    i = close + 1
                    continue
                braces.append(alternatives)
                out.append("(?:" if braces[-1] else re.escape(char))
            elif char == "}" and braces:
                out.append(")" if braces.pop() else re.escape(char))
            elif char == "," and braces and braces[-1]:
                out.append("|")
            else:
                out.append(re.escape(char))
            i += 1
        pattern = "".join(out)
        pattern = pattern.removeprefix("/") if "/" in glob else f"(?:.*/)?{pattern}"
        try:
            self.pattern = re.compile(pattern)
        except re.error:
            self.pattern = re.compile(r"(?!)")
        self.ranges = tuple(ranges)

    def matches(self, path: str) -> bool:
        """Whether the glob takes a path, relative to its .editorconfig."""
        found = self.pattern.fullmatch(path)
        return found is not None and all(
            number is None or low <= int(number) <= high
            for number, (low, high) in zip(found.groups(), self.ranges, strict=True)
        )


def _read_editorconfig(
    path: Path,
) -> tuple[list[tuple[_EditorConfigGlob, dict[str, int | None]]], bool]:
    """The sections of one .editorconfig with djLint's properties, and its root flag.

    A property set to `unset` is None, which drops what a file further up or a
    section before it gives it.
    """
    sections: list[tuple[_EditorConfigGlob, dict[str, int | None]]] = []
    is_root = False
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            sections.append((_EditorConfigGlob(line[1:-1]), {}))
            continue
        key, sep, value = line.partition("=")
        key, value = key.strip().lower(), value.strip()
        if not sep:
            continue
        if not sections and key == "root":
            is_root = value.lower() == "true"
        elif sections and key in _EDITORCONFIG_PROPERTIES:
            if value.isdecimal():
                sections[-1][1][key] = int(value)
            elif value.lower() == "unset":
                sections[-1][1][key] = None
    return sections, is_root


def editorconfig_files(
    folder: Path, root: Path
) -> tuple[tuple[Path, list[tuple[_EditorConfigGlob, dict[str, int | None]]]], ...]:
    """The .editorconfig files over a folder, nearest first.

    The search ends at one with `root = true`, and goes no higher than the
    project root.
    """
    folders = [folder, *folder.parents]
    found = []
    if root not in folders:
        # A file outside the project of the run, as with `djlint a b`,
        # searches up to its own project's root.
        root = find_project_root(folder)
    for directory in folders[: folders.index(root) + 1]:
        path = directory / ".editorconfig"
        if path.is_file():
            try:
                sections, is_root = _read_editorconfig(path)
            except OSError:
                # One djLint may not read is left out, as editors leave it out.
                continue
            found.append((directory, sections))
            if is_root:
                break
    return tuple(found)


def editorconfig_for(
    file: Path,
    files: tuple[tuple[Path, list[tuple[_EditorConfigGlob, dict[str, int | None]]]], ...],
) -> dict[str, int]:
    """indent_size and max_line_length for a file, as editors read them.

    The nearest .editorconfig wins, the ones above it fill in what it leaves
    out, and within one file a later section wins over an earlier one.
    """
    result: dict[str, int | None] = {}
    for directory, sections in files:
        try:
            relative = file.relative_to(directory).as_posix()
        except ValueError:
            continue
        own: dict[str, int | None] = {}
        for glob, values in sections:
            if glob.matches(relative):
                own.update(values)
        result = {**own, **result}
    return {key: value for key, value in result.items() if value is not None}


def load_pyproject_config(filepath: Path) -> Any:
    """Load djlint config from pyproject.toml."""
    data = tomllib.loads(filepath.read_text(encoding="utf-8"))
    return data.get("tool", {}).get("djlint", {})


def load_djlint_toml_config(filepath: Path) -> dict[str, Any]:
    """Load djlint config from djlint.toml."""
    return tomllib.loads(filepath.read_text(encoding="utf-8"))


def load_djlintrc_config(filepath: Path) -> Any:
    """Load djlint config from .djlintrc."""
    return json.loads(filepath.read_bytes())


def load_config_file(filepath: Path) -> Any:
    """Load djlint config from a config file."""
    if filepath.name == "pyproject.toml":
        return load_pyproject_config(filepath)

    if filepath.suffix == ".toml":
        return load_djlint_toml_config(filepath)

    return load_djlintrc_config(filepath)


def _unreadable_config(path: Path | str, error: Exception) -> UsageError:
    """The error for a configuration file that cannot be read.

    Running on with the defaults instead would check the templates against
    rules nobody chose, and could pass a run that should fail. The reason is
    kept on one line: a YAML error spans several, and an editor that shows
    the last line of a failure would show only the position.
    """
    reason = " ".join(str(error).split())
    return UsageError(f"Could not read {path}: {reason}")


def _settings_table(content: Any, path: Path | str) -> dict[str, Any]:
    """The settings a file holds, which have to map names to values."""
    if not isinstance(content, dict):
        msg = f"Could not read {path}: its djLint settings are not a table of names and values."
        raise UsageError(msg)
    return content


def _named_settings(config: Path | None) -> dict[str, Any]:
    """Settings from the file `--configuration` names."""
    if not config:
        return {}

    try:
        content = load_config_file(config)
    except Exception as error:
        raise _unreadable_config(config, error) from None
    return _settings_table(content, config)


def _project_settings(src: Path, warn: Callable[[str], None]) -> tuple[dict[str, Any], str]:
    """Settings from the project's own file, the first one that holds any.

    The name of that file comes with them, for the messages about a value
    it sets. A djLint file beside the one read is not read, which is worth
    saying: its settings would otherwise do nothing without a word.
    """
    others = [
        path.name
        for path in (*(src / name for name in DJLINT_TOML_CONFIG_FILES), src / ".djlintrc")
        if path.is_file()
    ]
    if pyproject_file := find_pyproject(src):
        try:
            content = load_pyproject_config(pyproject_file)
        except Exception as error:
            raise _unreadable_config(pyproject_file.name, error) from None
        if settings := _settings_table(content, pyproject_file.name):
            for other in others:
                warn(f"{other} is not read, as [tool.djlint] in pyproject.toml comes first.")
            return settings, pyproject_file.name

    if djlint_toml_file := find_djlint_toml(src):
        try:
            content = load_djlint_toml_config(djlint_toml_file)
        except Exception as error:
            raise _unreadable_config(djlint_toml_file.name, error) from None
        for other in others[others.index(djlint_toml_file.name) + 1 :]:
            warn(f"{other} is not read, as {djlint_toml_file.name} comes first.")
        return _settings_table(content, djlint_toml_file.name), djlint_toml_file.name

    if djlintrc_file := find_djlintrc(src):
        try:
            content = load_djlintrc_config(djlintrc_file)
        except Exception as error:
            raise _unreadable_config(djlintrc_file.name, error) from None
        return _settings_table(content, djlintrc_file.name), djlintrc_file.name

    return {}, ""


@cache
def _warn_once(message: str) -> None:
    """Warn about a setting once per run.

    The language server builds a Config for every change to a file, and
    repeating the same warning each time would only fill its log.
    """
    echo(style(f"Warning: {message}", fg="yellow"), err=True)


# The settings a configuration file can hold. tests/test_config/test_warnings.py
# checks that Config reads each of them and nothing else.
_SETTINGS: Final = frozenset((
    "allow_empty_input",
    "blank_line_after_tag",
    "blank_line_before_tag",
    "close_void_tags",
    "css",
    "custom_blocks",
    "custom_html",
    "exclude",
    "extend_exclude",
    "extension",
    "files",
    "format_attribute_js_json",
    "format_attribute_js_json_min_props",
    "format_attribute_js_json_pattern",
    "format_attribute_template_tags",
    "format_css",
    "format_js",
    "ignore",
    "ignore_blocks",
    "ignore_case",
    "include",
    "indent",
    "js",
    "keep_br_inline",
    "line_break_after_multiline_tag",
    "linter_output_format",
    "max_attribute_length",
    "max_blank_lines",
    "max_line_length",
    "name_endblocks",
    "no_entity_formatting",
    "no_function_formatting",
    "no_indent_inner_html",
    "no_line_after_yaml",
    "no_set_formatting",
    "per-file-ignores",
    "preserve_blank_lines",
    "preserve_class_newlines",
    "preserve_leading_space",
    "profile",
    "quiet",
    "quote_style",
    "require_pragma",
    "single_attribute_per_line",
    "sort_attributes",
    "sort_load_tags",
    "use_gitignore",
))

# What linter_output_format can name.
_OUTPUT_FIELDS: Final = frozenset(("code", "end", "filename", "line", "match", "message"))


def _check_settings(
    settings: Mapping[str, Any], sources: Mapping[str, str], warn: Callable[[str], None]
) -> None:
    """Warn about settings in a file that djLint ignores or reads unlike they look.

    A misspelled name would otherwise do nothing without a word.
    """
    for name in settings:
        if name not in _SETTINGS:
            from difflib import get_close_matches  # noqa: PLC0415

            close = get_close_matches(name, _SETTINGS, n=1)
            hint = f" Did you mean {close[0]}?" if close else ""
            warn(f"{sources[name]} sets {name}, which is not a djLint setting.{hint}")


def _format_fields(text: str) -> Iterator[str]:
    """The names a format string looks up, in it and in its format specs.

    A field such as `code[0]` or `message.upper` looks up `code` or `message`.
    """
    for _, field, spec, _ in Formatter().parse(text):
        if field is not None:
            yield re.split(r"[.\[]", field, maxsplit=1)[0]
        if spec:
            yield from _format_fields(spec)


def _check_output_format(output_format: str) -> None:
    """Refuse a linter_output_format naming a field there is none of.

    Otherwise the run would fail at its first finding.
    """
    try:
        fields = set(_format_fields(output_format))
    except ValueError as error:
        msg = f"Invalid linter_output_format {output_format!r}: {error}."
        raise UsageError(msg) from None
    if unknown := sorted(fields - _OUTPUT_FIELDS):
        known = ", ".join(f"{{{field}}}" for field in sorted(_OUTPUT_FIELDS))
        msg = (
            f"Invalid linter_output_format {output_format!r}:"
            f" {', '.join(f'{{{field}}}' for field in unknown)} is not one of {known}."
        )
        raise UsageError(msg)


def _check_codes(
    option: str, codes: Iterable[str], known: AbstractSet[str], warn: Callable[[str], None]
) -> None:
    """Warn about rule codes no rule has, which an option would quietly skip."""
    for code in codes:
        if code not in known:
            hint = f" Did you mean {code.upper()}?" if code.upper() in known else ""
            warn(f"{option} names {code}, which is not a linter rule.{hint}")


def load_project_settings(
    src: Path,
    config: Path | None,
    *,
    prefer_configuration: bool = False,
    warn: Callable[[str], None] = _warn_once,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Load djlint config, and the file each setting was read from.

    `--configuration` names a global file, so the project's own file wins
    where the two set the same thing. `--prefer-configuration` turns that
    around, which is what naming a file on the command line usually means.
    """
    named = _named_settings(config)
    project, project_file = _project_settings(src, warn)
    named_sources = dict.fromkeys(named, str(config))
    project_sources = dict.fromkeys(project, project_file)

    if prefer_configuration:
        return {**project, **named}, {**project_sources, **named_sources}
    return {**named, **project}, {**named_sources, **project_sources}


def validate_rules(
    rules: Iterable[_TMappingStrAny], warn: Callable[[str], None] = _warn_once
) -> Iterator[_TMappingStrAny]:
    """Yield the rules that have what a rule needs, and warn about the rest."""
    for rule in rules:
        name = rule["rule"].get("name", "undefined")
        problems = [
            message
            for missing, message in (
                ("name" not in rule["rule"], "A rule is missing a name! 😢"),
                (
                    "patterns" not in rule["rule"] and "python_module" not in rule["rule"],
                    f"Rule {name} is missing a pattern or a python_module! 😢",
                ),
                ("message" not in rule["rule"], f"Rule {name} is missing a message! 😢"),
            )
            if missing
        ]
        for problem in problems:
            warn(problem)
        if not problems:
            yield rule


# libyaml reads the bundled rules six times as fast, and comes with most
# wheels. A project's rules keep the Python loader: libyaml refuses a tab at
# the start of a block scalar, which a rules file loaded with before.
_YAML_LOADER: Final = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def load_custom_rules(rules_file: Path | None) -> Any:
    """Load custom linter rules from a .djlint_rules.yaml file.

    An empty file holds no rules.
    """
    if not rules_file:
        return ()

    try:
        with rules_file.open("rb") as f:
            rules = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as error:
        raise _unreadable_config(rules_file, error) from None
    if rules is None:
        return ()
    if not isinstance(rules, list):
        msg = f"Could not read {rules_file}: it does not hold a list of rules."
        raise UsageError(msg)
    return rules


def _as_comma_separated(value: Any) -> Any:
    """Allow comma-separated config options to be given as lists."""
    if isinstance(value, (list, tuple)):
        return ",".join(str(x).strip() for x in value)
    return value


def _build_block_alternation(tags: Iterable[str]) -> str:
    return "|".join(sorted(chain.from_iterable((rf"{tag}\b", rf"end{tag}\b") for tag in tags)))


def build_custom_blocks(custom_blocks: str | None) -> str | None:
    """Build regex string for custom template blocks."""
    tags = split_option_list(custom_blocks)
    if not tags:
        return None
    return "|" + _build_block_alternation(tags)


def build_ignore_blocks(ignore_blocks: str | None) -> str | None:
    """Build regex string for template blocks to not format."""
    tags = split_option_list(ignore_blocks)
    if not tags:
        return None
    return _build_block_alternation(tags)


def build_custom_html(custom_html: str | None) -> str | None:
    """Build regex string for custom HTML blocks."""
    tags = split_option_list(custom_html)
    if not tags:
        return None
    return "|" + "|".join(tags)


def _beautifier_config(
    configured: Mapping[str, Any] | None, *, indent_size: int | None
) -> dict[str, Any]:
    """The css or js settings, with an indent given on the command line.

    The option overrides the one key it names, so a `wrap_line_length` or
    any other setting in the config file stays in force beside it.
    """
    settings = dict(configured or {})
    if indent_size:
        settings["indent_size"] = indent_size
    return settings


def _split_patterns(value: str, *, split: bool = True) -> list[str]:
    r"""Split comma-separated verbose regexes, dropping entries with no pattern.

    A comma inside `{1,2}` or `[,;]`, or escaped as `\,`, belongs to its
    regex, so `report[0-9]{1,2}\.html` stays one pattern. A `#` comment ends
    at the next comma, whatever brackets or backslashes it holds. An entry of
    only whitespace and comments would match every path, so it is dropped.
    With `split` off, the value is one regex, commas and all.
    """
    parts: list[str] = []
    current: list[str] = []
    braces = 0
    in_class = in_comment = has_pattern = False
    i = 0
    while i < len(value):
        char = value[i]
        if split and char == "," and (in_comment or not (braces or in_class)):
            if has_pattern:
                parts.append(_strip_pattern("".join(current)))
            current = []
            braces = 0
            in_comment = has_pattern = False
            i += 1
            continue
        if in_comment:
            in_comment = char != "\n"
        elif char == "\\" and i + 1 < len(value):
            current.append(value[i : i + 2])
            has_pattern = True
            i += 2
            continue
        elif in_class:
            in_class = char != "]"
        elif char == "#":
            in_comment = True
        elif not char.isspace():
            has_pattern = True
            if char == "[":
                in_class = True
            elif char == "{":
                braces += 1
            elif char == "}" and braces:
                braces -= 1
        current.append(char)
        i += 1
    if has_pattern:
        parts.append(_strip_pattern("".join(current)))
    return parts


def _strip_pattern(pattern: str) -> str:
    r"""Strip the whitespace around a verbose regex, but keep a space escaped as `\ `."""
    stripped = pattern.rstrip()
    if len(stripped) < len(pattern) and (len(stripped) - len(stripped.rstrip("\\"))) % 2:
        stripped += pattern[len(stripped)]
    return stripped.lstrip()


def build_exclude(exclude: str | list[Any]) -> list[str]:
    """Split an exclude setting into its regexes.

    A list from a config file holds one regex per item, commas and all.
    """
    if isinstance(exclude, str):
        return _split_patterns(exclude)
    return [entry for x in exclude for entry in _split_patterns(str(x), split=False)]


def _check_regex(setting: str, pattern: str) -> None:
    """Refuse a setting whose value is no regular expression.

    exclude, extend_exclude and per-file-ignores take regexes, and a shell glob
    such as *.min.html isn't one; it would otherwise stop the run with a
    traceback.
    """
    try:
        compile_pattern(pattern, re.X)
    except re.error as error:
        msg = (
            f"Invalid {setting} {pattern!r}: {error}. It takes regular expressions,"
            r" so *.min.html is written .*\.min\.html."
        )
        raise UsageError(msg) from None


_CODES_EXCLUDED_BY_PROFILE: Final[dict[str, tuple[str, ...]]] = {
    "html": ("D", "J", "T", "N", "M"),
    "django": ("J", "N", "M"),
    "jinja": ("D", "N", "M"),
    "askama": ("D", "J", "N", "M"),
    "tera": ("D", "J", "N", "M"),
    "liquid": ("D", "J", "N", "M"),
    "mako": ("D", "J", "T", "N", "M"),
    "nunjucks": ("D", "J", "M"),
    "handlebars": ("D", "J", "N"),
    "golang": ("D", "J", "N", "M"),
    "angular": ("D", "J", "H012", "H026"),
}

_PROFILES: Final[frozenset[str]] = frozenset(_CODES_EXCLUDED_BY_PROFILE) | {"all"}

_DEFAULT_EXCLUDE: Final = r"""
    __pypackages__
    | _build
    | _site
    | \.bzr
    | \.direnv
    | \.eggs
    | \.git
    | \.git-rewrite
    | \.hg
    | \.nox
    | \.svn
    | \.tox
    | \.venv
    | build
    | dist
    | htmlcov
    | node_modules
    | site-packages
    | venv
"""

_DEFAULT_JS_JSON_PATTERN: Final = (
    r"^(?:"
    r"on[a-z]+|"
    r"x-[a-z\-]+|"
    r"@[a-z\-]+|"
    r":[a-z\-]+|"
    r"v-[a-z\-]+|"
    r"\([a-z\-]+\)|"
    r"\[[a-z\-]+\]|"
    r"\*ng[A-Z][a-zA-Z]*|"
    r"[a-z\-]+\.(bind|delegate|call|trigger)"
    r")$"
)

_TEMPLATE_IF_FOR_BLOCK_WITH_END_TAG: Final = r"""
    (?:
        {%[-+]?\s?(?:if|for|asyncAll|asyncEach)[^}]*?%}
        (?:.*?{%[-+]?\s?end(?:if|for|each|all)[^}]*?[-+]?%})+?
    )
"""

_ATTRIBUTE_NAME_CHAR: Final = r"""(?:[^\s"'=<>/{}\x00]|/(?!>))"""

_ATTRIBUTE_PATTERN: Final = (
    rf"""
    (?:
        (
            (?:
                {_ATTRIBUTE_NAME_CHAR} # a name character
               | (?>{{{{[\s\S]*?}}}})
                 (?={_ATTRIBUTE_NAME_CHAR}|[ ]*=) # a leading template variable
               | (?!{{%[-+]?\s*(?:for|asyncAll|asyncEach)\b)
                 (?!{{%[-+]?\s*if\b[^}}]*?%}}(?:required|checked){{%[-+]?\s*endif\b[^}}]*?%}})
                 (?>{_TEMPLATE_IF_FOR_BLOCK_WITH_END_TAG})
                 (?={_ATTRIBUTE_NAME_CHAR}|[ ]*=) # a leading template block
            )
            (?:
                {_ATTRIBUTE_NAME_CHAR} # more name characters
               | (?>{{{{[\s\S]*?}}}}|{{%[\s\S]*?%}}) # or an embedded template tag
            )*
            | required | checked
        )? # attribute name
        (?:  [ ]*=[ ]* # followed by "="
            (
                \"[^\"]*? # double quoted attribute
                (?:
                    {_TEMPLATE_IF_FOR_BLOCK_WITH_END_TAG} # if or for loop
                   | {{{{[\s\S]*?}}}} # template stuff
                   | {{%[\s\S]*?%}}
                   | [^\"] # anything else
                )*?
                \" # closing quote
              | '[^']*? # single quoted attribute
                (?:
                    {_TEMPLATE_IF_FOR_BLOCK_WITH_END_TAG} # if or for loop
                   | {{{{[\s\S]*?}}}} # template stuff
                   | {{%[\s\S]*?%}}
                   | [^'] # anything else
                )*?
                \' # closing quote
              | (?: # or a non-quoted string value. A template tag glued to
                    # the rest of the value is part of that one value, not
                    # the start of a second attribute.
                    {_ATTRIBUTE_NAME_CHAR}
                   | (?>{{{{[\s\S]*?}}}}|{{%[\s\S]*?%}}) # embedded template tag
                )+
              | {_TEMPLATE_IF_FOR_BLOCK_WITH_END_TAG} # a non-quoted if statement

            )
        )? # attribute value
    )
    | ({_TEMPLATE_IF_FOR_BLOCK_WITH_END_TAG}
    """
    r"""
    | (?:\'|\") # allow random trailing quotes
    | {{[\s\S]*?}}
    | {\#[\s\S]*?\#}
    | {%[\s\S]*?%})
    """
)

_ATTRIBUTE_X_PATTERN: Final = compile_pattern(_ATTRIBUTE_PATTERN, re.X)

# A second opener means the first never closed, as the tokenizer reads it,
# so a run of unclosed tags is read once.
_TEMPLATE_TAGS: Final = r"""
    {{(?:(?!}}|{{).)*}}|{%(?:(?!%}|{%).)*%}
"""
_TEMPLATE_TAGS_IMX_PATTERN: Final = compile_pattern(_TEMPLATE_TAGS, RE_FLAGS_IMX)

_TAG_UNINDENT_LINE_TEMPLATE: Final = r"""
      (?:\{%[-+]?[ ]*(?:BRANCHES))
    | (?:
        \{\{[ ]*
        (
            (?:else|\^)
            [ ]*\}\}
        )
      )
"""
_TAG_UNINDENT_LINE: Final = _TAG_UNINDENT_LINE_TEMPLATE.replace(
    "BRANCHES", "elif|else|empty|plural"
)
_LIQUID_TAG_UNINDENT_LINE: Final = _TAG_UNINDENT_LINE_TEMPLATE.replace(
    "BRANCHES", "elif|elsif|else|empty|plural|when"
)

_BREAK_BEFORE: Final = r"(?<!\n[ \t]*?)"

_PROFILE_ONLY_BLOCKS: Final[dict[str, str]] = {
    "tera": "component",
    "liquid": "case,capture,tablerow,form,paginate,highlight",
}

_GOLANG_BLOCK_OPEN: Final = r"|\{\{-?[ ]*(?:if|range|with|block|define)\b"
_GOLANG_BLOCK_CLOSE: Final = r"|(?:\{\{-?[ ]*end(?![\w]))"
_GOLANG_BRANCH: Final = r"|(?:\{\{-?[ ]*else(?![\w]))"

_IGNORED_ATTRIBUTES: Final = frozenset({
    "href",
    "action",
    "data-url",
    "src",
    "url",
    "srcset",
    "data-src",
})

_INDENT_TEMPLATE_TAGS: Final = r""" (?:if
    | unless
    | ifchanged
    | for
    | asyncEach
    | asyncAll
    | embed
    | apply
    | sandbox
    | guard
    | ifequal
    | ifnotequal
    | block(?!trans|translate)
    | spaceless
    | compress
    | cache
    | localize
    | localtime
    | timezone
    | addto
    | language
    | with
    | assets
    | verbatim
    | autoescape
    | filter
    | each
    | macro
    | call
    | raw
    | blocktrans(?!late)
    | blocktranslate
    | partialdef
    | thumbnail
    | set(?!(?:(?!%}).)*=)
"""

_START_TEMPLATE_TAGS: Final = r"""
      (?:if
    | ifchanged
    | unless
    | embed
    | apply
    | sandbox
    | guard
    | ifequal
    | ifnotequal
    | for
    | asyncEach
    | asyncAll
    | block(?!trans)
    | spaceless
    | compress
    | cache
    | localize
    | localtime
    | timezone
    | load
    | assets
    | addto
    | language
    | with
    | assets
    | autoescape
    | filter
    | verbatim
    | each
    | macro
    | call
    | raw
    | blocktrans(?!late)
    | blocktranslate
    | partialdef
    | thumbnail
    | set(?!(?:(?!%}).)*=)

"""

_BREAK_TEMPLATE_TAGS: Final = r"""
      (?:if
    | unless
    | endif
    | for
    | endfor
    | asyncEach
    | endeach
    | asyncAll
    | endall
    | block(?!trans)
    | endblock(?!trans)
    | else
    | plural
    | spaceless
    | endspaceless
    | compress
    | endcompress
    | cache
    | endcache
    | localize
    | endlocalize
    | localtime
    | endlocaltime
    | timezone
    | endtimezone
    | load
    | include
    | assets
    | endassets
    | addto
    | language
    | with
    | endwith
    | autoescape
    | endautoescape
    | apply
    | endapply
    | sandbox
    | endsandbox
    | guard
    | endguard
    | ifequal
    | endifequal
    | ifnotequal
    | endifnotequal
    | filter
    | endfilter
    | elif
    | resetcycle
    | verbatim
    | endverbatim
    | each
    | macro
    | endmacro
    | raw
    | endraw
    | call
    | endcall
    | image
    | blocktrans(?!late)
    | endblocktrans(?!late)
    | blocktranslate
    | endblocktranslate
    | partialdef
    | endpartialdef
    | partial
    | set(?!(?:(?!%}).)*=)
    | endset
    | thumbnail
    | endthumbnail
"""

_BREAK_HTML_TAGS: Final = r"""
      html
    | head
    | body
    | div
    #   | a # a gets no breaks #177
    | nav
    | ul
    | ol
    | dl
    | dd
    | dt
    | li
    | table
    | thead
    | tbody
    | tr
    | th
    | td
    | blockquote
    | select
    | form
    | option
    | optgroup
    | fieldset
    | legend
    | label
    | header
    | cache
    | main
    | section
    | aside
    | footer
    | figure
    | figcaption
    | video
    #   | span # span gets no breaks #171
    | p
    | g
    | svg
    | h\d
    | button
    | path
    | picture
    | script
    | style
    | details
    | summary
    | """

_ALWAYS_SELF_CLOSING_HTML_TAGS: Final = "|".join(HTML_VOID_ELEMENTS)

_OPTIONAL_SINGLE_LINE_HTML_TAGS: Final = r"""
      button
    | a
    | h1
    | h2
    | h3
    | h4
    | h5
    | h6
    | td
    | th
    | strong
    | small
    | em
    | icon
    | span
    | title
    | link
    | path
    | label
    | div
    | li
    | script
    | style
    | head
    | body
    | p
    | select
    | article
    | option
    | legend
    | summary
    | dt
    | figcaption
    | tr
    | li
"""

_OPTIONAL_SINGLE_LINE_TEMPLATE_TAGS: Final = r"""
      if
    | for
    | unless
    | block
    | with
    | asyncEach
    | asyncAll
"""

_IGNORED_INLINE_BLOCKS_TAIL: Final = r"""
      <!--.*?-->
    | {\*.*?\*}
    | (?<!\{){\#(?!.*djlint:[ ]*(?:off|on)\b).*?\#}
    | <\?php.*?\?>
    | <%(?!\w).*?%>
    | {%[ ]*comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?{%[ ]*endcomment[ ]*%}
    | {%[ ]*filter\b(?:(?!%}).)*?%}.*?{%[ ]*endfilter[ ]*%}
    # liquid/shopify blocks whose bodies are json, css or js
    | {%[-+]?[ ]*(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
      .*?
      {%[-+]?[ ]*end(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
    | {%[ ]*blocktrans(?:late)?\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktrans(?:late)?[ ]*%}
"""


def _build_ignored_inline_blocks(*, for_linting: bool) -> str:
    """Build the alternation of one-line blocks djLint leaves alone.

    A block closed on the line that opens it leaves nothing open, so each
    span runs through the closing tag. Linting leaves the raw text
    elements out, so a rule can still see the attributes on the opening
    tag; their bodies are skipped by the multi-line spans either way.
    """
    if for_linting:
        return _IGNORED_INLINE_BLOCKS_TAIL

    return (
        r"""
      <script.*?\</script>
    | <style.*?\</style>
    | <pre.*?\</pre>
    | <textarea.*?\</textarea>
    |"""
        + _IGNORED_INLINE_BLOCKS_TAIL
    )


_IGNORED_INLINE_BLOCKS: Final = _build_ignored_inline_blocks(for_linting=False)
_LINT_IGNORED_INLINE_BLOCKS: Final = _build_ignored_inline_blocks(for_linting=True)

_IGNORED_BLOCKS_TAIL: Final = (
    r"""
    # html comment
    | <!--\s*djlint\:off\s*-->(?:(?!<!--\s*djlint\:on\s*-->).)*
    # django/jinja/nunjucks
    | {\#\s*djlint\:\s*off\s*\#}(?:(?!{\#\s*djlint\:\s*on\s*\#}).)*
    | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}(?:(?!{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}).)*
    # inline jinja comments; "{{#" opens a handlebars section, not a comment
    | (?<!\{){\#(?!\s*djlint\:\s*(?:off|on)).*?\#}
    # handlebars
    | {{!--\s*djlint\:off\s*--}}(?:(?!{{!--\s*djlint\:on\s*--}}).)*
    # golang
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}(?:(?!{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}).)*
    # inline golang comments
    | {{-?\s*/\*(?!\s*djlint\:\s*(?:off|on)).*?\*/\s*-?}}
    | <!--.*?-->
    | <\?php.*?\?>
    | <%(?!\w).*?%>
    | {%[ ]*filter\b(?:(?!%}).)*?%}.*?{%[ ]*endfilter[ ]*%}
    # liquid/shopify blocks whose bodies are json, css or js
    | {%[-+]?[ ]*(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
      .*?
      {%[-+]?[ ]*end(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
    | {%[ ]*blocktranslate\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktranslate[ ]*%}
    | {%[ ]*blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktrans[ ]*%}
    | {%[ ]*comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*endcomment[ ]*%})
    |"""
    + YAML_FRONT_MATTER
)


# A self closed tag opens nothing, and the quoted values are stepped over
# so that a "/" written inside one is not read as the close.
_TEMPLATE_NAMED_OPENING_TAG: Final = (
    rf"<(?:{TEMPLATE_TAG_NAME})(?!(?:[^>\"']|\"[^\"]*\"|'[^']*')*?/>)"
)

# A template tag is read whole, so a ">" in one is not the tag's end, and
# another tag's start ends one that was never closed.
_RAW_TEXT_OPENING_TAG: Final = (
    rf"""(?:{QUOTED_ATTRIBUTE_VALUE}|{TEMPLATE_TAG_WHOLE}|(?!{TAG_START})[^>\"'{{]|\{{)*+>"""
)


def _build_ignored_blocks(*, for_linting: bool) -> str:
    """Build the alternation of blocks djLint leaves alone.

    The formatter's span runs from the opening tag to the "<" of the
    closing one, so that it can still indent the closing tag while leaving
    the contents alone.

    Linting skips the contents only. A span covering the opening tag would
    hide it from every rule, which left `H024` unable to report the
    `type="text/javascript"` it exists for, and `D004` blind to the
    `<script src>` its own pattern names. A span covering the whole
    element instead leaves a rule that pairs tags (`H025`) with a closing
    tag whose opening tag it never saw.
    """
    if for_linting:
        return (
            rf"""
      <(pre|textarea){_RAW_TEXT_OPENING_TAG}\K(?:(?!</(?:\1)\b)[\s\S])*
    | <(script|style){_RAW_TEXT_OPENING_TAG}\K(?:(?!</(?:\2)\b)[\s\S])*
"""
            + _IGNORED_BLOCKS_TAIL
        )

    return (
        r"""
      <(pre|textarea).*?</(\1)>
    | <(script|style).*?(?=(\</(?:\3)>))
"""
        + _IGNORED_BLOCKS_TAIL
    )


_IGNORED_BLOCKS: Final = _build_ignored_blocks(for_linting=False)
_LINT_IGNORED_BLOCKS: Final = _build_ignored_blocks(for_linting=True)

_RAW_TEXT_INLINE: Final = r"""
    <(script|style|pre|textarea).*?</(?:\1)>
"""
_RAW_TEXT_OPENING_PATTERN: Final = compile_pattern(
    r"""
      <style
    | <script
    | <pre
    | <textarea
    """,
    RE_FLAGS_IX,
)
_RAW_TEXT_CLOSING_PATTERN: Final = compile_pattern(
    r"""
      </style
    | </script
    | </pre
    | </textarea
    """,
    RE_FLAGS_IX,
)
_RAW_TEXT_INLINE_IMSX_PATTERN: Final = compile_pattern(_RAW_TEXT_INLINE, RE_FLAGS_IMSX)
_RAW_TEXT_INLINE_IX_PATTERN: Final = compile_pattern(_RAW_TEXT_INLINE, RE_FLAGS_IX)
_IGNORED_BLOCK_OPENING_PATTERN: Final = compile_pattern(
    r"""
      <style
    | {\*
    | <\?php
    | <%(?!\w)
    | <script
    | <!--
    | [^\{]{\#(?!\s*djlint\:\s*(?:on|off))
    | ^{\#(?!\s*djlint\:\s*(?:on|off))
    | <pre
    | <textarea
    | {%[ ]*blocktrans(?:late)?(?:(?!%}|\btrimmed\b).)*?%}
    | {%[-+]?[ ]*(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
    | {%[ ]*filter\b(?:(?!%}).)*?%}
    | {\#\s*djlint\:\s*off\s*\#}
    | {%[ ]+?comment[ ]+?(?:(?!%}).)*?%}
    | {{!--\s*djlint\:off\s*--}}
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}
    |"""
    + SKIP_TEMPLATE_TAG,
    RE_FLAGS_IX,
)
_IGNORED_BLOCK_CLOSING_BEFORE: Final = r"""
      </style
    | \*}
    | \?>
    | %>
    | </script
"""
# a "-->" reachable without crossing the start of a raw text element.
# Past one, markup is text: "<pre>&lt;!-- x -->" closes no comment.
_IGNORED_BLOCK_CLOSING_AT_START: Final = r"""
      (?:(?!<pre\b|<textarea\b).)*?-->
    | (?:(?!{\#).)*\#} # lines that have a #}, but not a {#
"""
# An endcomment written right after "djlint:off" closes nothing. That is
# looked for behind the tag once it is found: looked for first, a lookbehind
# of no fixed length was tried from every position of the line, each time
# back to its start, which took quadratic time on a long one.
_IGNORED_BLOCK_CLOSING_AFTER: Final = r"""
      </pre
    | </textarea
    | {%[ ]*endfilter(?:(?!%}).)*?%}
    | {\#\s*djlint\:\s*on\s*\#}
    | {%[ ]+?endcomment[ ]+?%}(?<!djlint:off\s*?{%[ ]+endcomment[ ]+%})
    | {{!--\s*djlint\:on\s*--}}
    | {{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}
    | {%[ ]*endblocktrans(?:late)?(?:(?!%}).)*?%}
    | {%[-+]?[ ]*end(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
"""
_IGNORED_BLOCK_CLOSING_PATTERN: Final = compile_pattern(
    _IGNORED_BLOCK_CLOSING_BEFORE
    + rf"| ^(?:{_IGNORED_BLOCK_CLOSING_AT_START})|"
    + _IGNORED_BLOCK_CLOSING_AFTER,
    RE_FLAGS_IX,
)
_IGNORED_BLOCK_CLOSING_AT_START_PATTERN: Final = compile_pattern(
    _IGNORED_BLOCK_CLOSING_AT_START, RE_FLAGS_IX
)
_IGNORED_BLOCK_CLOSING_ANYWHERE_PATTERN: Final = compile_pattern(
    _IGNORED_BLOCK_CLOSING_BEFORE + "|" + _IGNORED_BLOCK_CLOSING_AFTER, RE_FLAGS_IX
)
_IGNORED_BLOCKS_PATTERN: Final = compile_pattern(
    _IGNORED_BLOCKS + "|" + SKIP_TEMPLATE_TAG, RE_FLAGS_IMSX
)
_LINT_IGNORED_BLOCKS_PATTERN: Final = compile_pattern(
    _LINT_IGNORED_BLOCKS + "|" + SKIP_TEMPLATE_TAG, RE_FLAGS_IMSX
)
_IGNORED_BLOCKS_INLINE_PATTERN: Final = compile_pattern(
    r"""
      <(pre|textarea).*?</(\1)>
    | <(script|style).*?(?=(\</(?:\3)>))
    # html comment
    | <!--\s*djlint\:off\s*-->.*?(?=<!--\s*djlint\:on\s*-->)
    # django/jinja/nunjucks
    | {\#\s*djlint\:\s*off\s*\#}.*?(?={\#\s*djlint\:\s*on\s*\#})
    | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}.*?(?={%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\})
    # inline jinja comments; "{{#" opens a handlebars section, not a comment
    | (?<!\{){\#(?!\s*djlint\:\s*(?:off|on)).*?\#}
    # handlebars
    | {{!--\s*djlint\:off\s*--}}.*?(?={{!--\s*djlint\:on\s*--}})
    # golang
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}.*?(?={{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}})
    # inline golang comments
    | {{-?\s*/\*(?!\s*djlint\:\s*(?:off|on)).*?\*/\s*-?}}
    | <!--.*?-->
    | <\?php.*?\?>
    | <%(?!\w).*?%>
    | {%[ ]*filter\b(?:(?!%}).)*?%}.*?{%[ ]*endfilter[ ]*%}
    | {%[ ]*blocktranslate\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktranslate[ ]*%}
    | {%[ ]*blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktrans[ ]*%}
    | {%[ ]*comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*endcomment[ ]*%})
    |"""
    + YAML_FRONT_MATTER
    + "|"
    + SKIP_TEMPLATE_TAG,
    RE_FLAGS_IMSX,
)
_IGNORED_INLINE_BLOCKS_IX_PATTERN: Final = compile_pattern(
    _IGNORED_INLINE_BLOCKS + "|" + SKIP_TEMPLATE_TAG, RE_FLAGS_IX
)
_LINT_IGNORED_INLINE_BLOCKS_IX_PATTERN: Final = compile_pattern(
    _LINT_IGNORED_INLINE_BLOCKS + "|" + SKIP_TEMPLATE_TAG, RE_FLAGS_IX
)
_IGNORED_LINTER_BLOCKS_PATTERN: Final = compile_pattern(
    r"""
    {%[-+]?[ ]*(raw|verbatim)\b(?:(?!%}).)*?[-+]?%}.*?{%[-+]?[ ]*end\1[ ]*[-+]?%}
    """,
    RE_FLAGS_IMSX,
)
_UNFORMATTED_BLOCKS_COARSE_PATTERN: Final = compile_pattern(r"djlint\:\s*off", RE_FLAGS_IMSX)
_UNFORMATTED_BLOCKS_PATTERN: Final = compile_pattern(
    r"""
    # html comment
      <!--\s*djlint\:off\s*-->(?:(?!<!--\s*djlint\:on\s*-->).)*
    # django/jinja/nunjucks
    | (?<!{){\#\s*djlint\:\s*off\s*\#}(?:(?!{\#\s*djlint\:\s*on\s*\#}).)*
    | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}(?:(?!{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}).)*
    # inline jinja comments
    | (?<!{){\#(?!\s*djlint\:\s*(?:off|on)).*?\#}
    # handlebars
    | {{!--\s*djlint\:off\s*--}}(?:(?!{{!--\s*djlint\:on\s*--}}).)*
    # golang
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}(?:(?!{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}).)*
    |"""
    + YAML_FRONT_MATTER
    + "|"
    + SKIP_TEMPLATE_TAG,
    RE_FLAGS_IMSX,
)
_IGNORED_RULE_PATTERNS: Final = tuple(
    compile_pattern(pattern, RE_FLAGS_ISX)
    for pattern in (
        r"""
        # html comment
        <!--\s*djlint\:off(.+?)-->(?:(?!<!--\s*djlint\:on\s*-->).)*
        """,
        r"""
        # django/jinja/nunjucks
        {\#\s*djlint\:\s*off(.+?)\#}(?:(?!{\#\s*djlint\:\s*on\s*\#}).)*
        """,
        r"""
        # django/jinja/nunjucks comment block
        {%\s*comment\s*%\}\s*djlint\:off(.*?)\{%\s*endcomment\s*%\}
        (?:(?!{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}).)*
        """,
        r"""
        # handlebars
        {{!--\s*djlint\:off(.*?)--}}(?:(?!{{!--\s*djlint\:on\s*--}}).)*
        """,
        r"""
        # golang
        {{-?\s*/\*\s*djlint\:off(.*?)\*/\s*-?}}(?:(?!{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}).)*
        """,
    )
)
_IGNORED_TRANS_BLOCKS_PATTERN: Final = compile_pattern(
    r"""
      {%[ ]*blocktranslate?\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktranslate?[ ]*%}
    | {%[ ]*blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktrans[ ]*%}
    """,
    RE_FLAGS_ISX,
)
_TRANS_TRIMMED_BLOCKS_PATTERN: Final = compile_pattern(
    r"""
      {%[ ]*blocktranslate\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%}.*?{%[ ]*endblocktranslate[ ]*%}
    | {%[ ]*blocktrans\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%}.*?{%[ ]*endblocktrans[ ]*%}
    """,
    RE_FLAGS_ISX,
)
_IGNORED_TRANS_BLOCKS_CLOSING_PATTERN: Final = compile_pattern(
    r"""
    {%[ ]*endblocktrans(?:late)?(?:(?!%}).)*?%}
    """,
    RE_FLAGS_IX,
)
_SAFE_CLOSING_TAG_PATTERN: Final = compile_pattern(
    r"""
      </script
    | </style
    | {\#\s*djlint\:\s*on\s*\#}
    | {%[ ]+?endcomment[ ]+?%}
    | {{!--\s*djlint\:on\s*--}}
    | {{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}
    """,
    RE_FLAGS_IX,
)
_SAFE_CLOSING_BLOCK_PATTERN: Final = compile_pattern(
    _IGNORED_INLINE_BLOCKS + r" | " + _IGNORED_BLOCKS, RE_FLAGS_IMSX
)
_TEMPLATE_BLOCKS_PATTERN: Final = compile_pattern(
    r"""
    {%((?!%}|{%).)+%}|{{((?!}}|{{).)+}}
    """,
    RE_FLAGS_IMSX,
)
_OPTIONAL_SINGLE_LINE_HTML_PATTERN: Final = compile_pattern(
    rf"^(?:{_OPTIONAL_SINGLE_LINE_HTML_TAGS})$", RE_FLAGS_IX
)
_OPTIONAL_SINGLE_LINE_TEMPLATE_PATTERN: Final = compile_pattern(
    rf"^(?:{_OPTIONAL_SINGLE_LINE_TEMPLATE_TAGS})$", RE_FLAGS_IX
)


@final
class Config:
    """Djlint Config."""

    __slots__ = (
        "_editorconfig_files",
        "allow_empty_input",
        "always_self_closing_html_tags",
        "attribute_pattern",
        "blank_line_after_tag",
        "blank_line_before_tag",
        "break_before",
        "break_html_tags",
        "break_template_tags",
        "check",
        "close_void_tags",
        "css_config",
        "custom_blocks",
        "custom_html",
        "editorconfig_defaults",
        "entity_pattern",
        "exclude",
        "exclude_pattern",
        "extension",
        "files",
        "format_attribute_js_json",
        "format_attribute_js_json_min_props",
        "format_attribute_js_json_object_pattern",
        "format_attribute_js_json_pattern",
        "format_attribute_js_json_property_pattern",
        "format_attribute_js_json_string_pattern",
        "format_attribute_template_tags",
        "format_css",
        "format_js",
        "github_output",
        "gitignore",
        "has_profile",
        "ignore",
        "ignore_blocks",
        "ignore_case",
        "ignored_attributes",
        "ignored_block_closing_anywhere_pattern",
        "ignored_block_closing_at_start_pattern",
        "ignored_block_closing_pattern",
        "ignored_block_opening_pattern",
        "ignored_blocks_inline_pattern",
        "ignored_blocks_pattern",
        "ignored_inline_blocks",
        "ignored_inline_blocks_ix_pattern",
        "ignored_linter_blocks_pattern",
        "ignored_rule_patterns",
        "ignored_trans_blocks_closing_pattern",
        "ignored_trans_blocks_pattern",
        "include",
        "indent",
        "indent_html_tags",
        "indent_size",
        "js_config",
        "keep_br_inline",
        "line_break_after_multiline_tag",
        "lint",
        "lint_ignored_blocks_pattern",
        "lint_ignored_inline_blocks_ix_pattern",
        "linter_output_format",
        "linter_rules",
        "max_attribute_length",
        "max_blank_lines",
        "max_line_length",
        "name_endblocks",
        "no_entity_formatting",
        "no_function_formatting",
        "no_indent_inner_html",
        "no_line_after_yaml",
        "no_set_formatting",
        "optional_single_line_html_pattern",
        "optional_single_line_html_tags",
        "optional_single_line_template_pattern",
        "optional_single_line_template_tags",
        "per_file_ignores",
        "preserve_blank_lines",
        "preserve_class_newlines",
        "preserve_leading_space",
        "profile",
        "project_root",
        "quiet",
        "quote_style",
        "raw_text_closing_pattern",
        "raw_text_inline_imsx_pattern",
        "raw_text_inline_ix_pattern",
        "raw_text_opening_pattern",
        "reformat",
        "require_pragma",
        "safe_closing_block_pattern",
        "safe_closing_tag_pattern",
        "sarif",
        "single_attribute_per_line",
        "single_line_template_tags",
        "skipped_rules",
        "sort_attributes",
        "sort_load_tags",
        "start_template_tags",
        "statistics",
        "stdin",
        "stdin_filename",
        "tag_indent",
        "tag_unindent",
        "tag_unindent_line",
        "tag_unindent_line_ix_pattern",
        "template_blocks_pattern",
        "template_indent",
        "template_indent_imx_pattern",
        "template_indent_ix_pattern",
        "template_tags",
        "template_tags_imx_pattern",
        "template_unindent",
        "template_unindent_imx_pattern",
        "template_unindent_ix_pattern",
        "trans_trimmed_blocks_pattern",
        "unformatted_blocks_coarse_pattern",
        "unformatted_blocks_pattern",
        "use_gitignore",
        "warn",
    )

    def __new__(cls, *_args: object, **_kwargs: object) -> Config:
        # for_file copies a Config. Under mypyc, a class without its own
        # __new__ runs __init__ again for a copy, which would read the
        # configuration of the current folder.
        return super().__new__(cls)

    def __init__(
        self,
        src: str = ".",
        *,
        ignore: str = "",
        extension: str = "",
        indent: int | None = None,
        quiet: bool = False,
        profile: str | None = None,
        require_pragma: bool = False,
        reformat: bool = False,
        check: bool = False,
        lint: bool = False,
        use_gitignore: bool = False,
        allow_empty_input: bool = False,
        warn: bool = False,
        preserve_leading_space: bool = False,
        preserve_blank_lines: bool = False,
        preserve_class_newlines: bool = False,
        format_css: bool = False,
        format_js: bool = False,
        configuration: Path | None = None,
        prefer_configuration: bool = False,
        rules: Path | None = None,
        statistics: bool = False,
        include: str = "",
        ignore_case: bool = False,
        ignore_blocks: str = "",
        custom_blocks: str = "",
        blank_line_after_tag: str = "",
        blank_line_before_tag: str = "",
        line_break_after_multiline_tag: bool = False,
        custom_html: str = "",
        exclude: str = "",
        extend_exclude: str = "",
        linter_output_format: str = "",
        max_line_length: int | None = None,
        max_attribute_length: int | None = None,
        format_attribute_template_tags: bool = False,
        single_attribute_per_line: bool = False,
        format_attribute_js_json: bool = False,
        format_attribute_js_json_pattern: str = "",
        format_attribute_js_json_min_props: int | None = None,
        per_file_ignores: tuple[tuple[str, str], ...] = (),
        indent_css: int | None = None,
        indent_js: int | None = None,
        close_void_tags: bool = False,
        no_line_after_yaml: bool = False,
        no_indent_inner_html: bool = False,
        sort_attributes: bool = False,
        sort_load_tags: bool = False,
        name_endblocks: bool = False,
        keep_br_inline: bool = False,
        no_entity_formatting: bool = False,
        no_function_formatting: bool = False,
        no_set_formatting: bool = False,
        quote_style: str | None = None,
        max_blank_lines: int | None = None,
        github_output: bool = False,
        sarif: bool = False,
        stdin: bool | None = None,
        stdin_filename: str | None = None,
        python_rules: bool = True,
        on_warning: Callable[[str], None] | None = None,
    ) -> None:
        # A program that shows the warnings itself gets each of them, every
        # time; the command line prints each one once per run.
        report = on_warning or _warn_once
        if src != "-":
            start = Path(src).resolve()
        elif stdin_filename is None:
            start = Path.cwd()
        else:
            start = Path(stdin_filename).resolve().parent
        self.project_root = find_project_root(start)
        djlint_settings, setting_sources = load_project_settings(
            self.project_root, configuration, prefer_configuration=prefer_configuration, warn=report
        )
        if prefer_configuration and configuration is None:
            report("--prefer-configuration has no effect without --configuration.")
        _check_settings(djlint_settings, setting_sources, report)

        def setting_int(key: str, default: int) -> int:
            """Read a whole number from the config file.

            The text of one works too, with a warning, as djLint always took
            it. true and false are numbers to Python, and 2.5 would quietly
            become 2, so both are refused.
            """
            value = djlint_settings.get(key, default)
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            if isinstance(value, int) and not isinstance(value, bool):
                return value
            if isinstance(value, str):
                try:
                    number = int(value)
                except ValueError:
                    pass
                else:
                    if key in djlint_settings:
                        report(
                            f"{key} in {setting_sources[key]} should be the number {number},"
                            f" not the text {json.dumps(value)}."
                        )
                    return number
            msg = (
                f"Invalid {setting_sources[key]} {key} value {djlint_settings[key]}."
                " It must be a whole number."
            )
            raise UsageError(msg)

        def setting_bool(key: str) -> bool:
            """Read a switch from the config file: true or false.

            The text "true" or "false" works too, with a warning, since older
            configurations quote it. Anything else is refused rather than read
            as true, so no text can turn a switch on by being there.
            """
            value = djlint_settings.get(key, False)
            if isinstance(value, bool):
                return value
            if isinstance(value, str) and (text := value.strip().lower()) in {"true", "false"}:
                report(
                    f"{key} in {setting_sources[key]} should be {text},"
                    f" not the text {json.dumps(value)}."
                )
                return text == "true"
            msg = (
                f"Invalid {setting_sources[key]} {key} value {djlint_settings[key]}."
                " It must be true or false."
            )
            raise UsageError(msg)

        self.reformat = reformat
        self.check = check
        self.lint = lint
        self.warn = warn
        self.github_output = github_output
        self.sarif = sarif
        self.statistics = statistics
        self.stdin_filename = stdin_filename

        self.extension = str(extension or djlint_settings.get("extension", "html"))
        self.quiet = quiet or setting_bool("quiet")
        self.require_pragma = require_pragma or setting_bool("require_pragma")
        self.preserve_leading_space = preserve_leading_space or setting_bool(
            "preserve_leading_space"
        )
        self.preserve_blank_lines = preserve_blank_lines or setting_bool("preserve_blank_lines")
        self.preserve_class_newlines = preserve_class_newlines or setting_bool(
            "preserve_class_newlines"
        )
        self.format_js = format_js or setting_bool("format_js")
        self.format_css = format_css or setting_bool("format_css")
        self.ignore_case = ignore_case or setting_bool("ignore_case")
        self.close_void_tags = close_void_tags or setting_bool("close_void_tags")
        self.no_line_after_yaml = no_line_after_yaml or setting_bool("no_line_after_yaml")
        self.no_indent_inner_html = no_indent_inner_html or setting_bool("no_indent_inner_html")
        self.sort_attributes = sort_attributes or setting_bool("sort_attributes")
        self.sort_load_tags = sort_load_tags or setting_bool("sort_load_tags")
        self.name_endblocks = name_endblocks or setting_bool("name_endblocks")
        selected_profile = str(profile or djlint_settings.get("profile", "")).lower()
        expressions_are_rust = selected_profile == "askama"
        self.no_set_formatting = (
            no_set_formatting or setting_bool("no_set_formatting") or expressions_are_rust
        )
        self.no_function_formatting = (
            no_function_formatting or setting_bool("no_function_formatting") or expressions_are_rust
        )
        self.no_entity_formatting = no_entity_formatting or setting_bool("no_entity_formatting")
        self.keep_br_inline = keep_br_inline or setting_bool("keep_br_inline")
        self.quote_style = str(quote_style or djlint_settings.get("quote_style", "double")).lower()
        if self.quote_style not in _QUOTE_STYLES:
            msg = (
                f"Invalid quote style {self.quote_style!r}."
                f" Choose from {', '.join(sorted(_QUOTE_STYLES))}."
            )
            raise BadParameter(msg, param_hint="'--quote-style'")
        self.format_attribute_template_tags = format_attribute_template_tags or setting_bool(
            "format_attribute_template_tags"
        )
        self.single_attribute_per_line = single_attribute_per_line or setting_bool(
            "single_attribute_per_line"
        )
        self.format_attribute_js_json = format_attribute_js_json or setting_bool(
            "format_attribute_js_json"
        )
        self.format_attribute_js_json_min_props = (
            format_attribute_js_json_min_props
            if format_attribute_js_json_min_props is not None
            else setting_int("format_attribute_js_json_min_props", 2)
        )
        self.linter_output_format = linter_output_format or djlint_settings.get(
            "linter_output_format", "{code} {line} {message} {match}"
        )
        _check_output_format(self.linter_output_format)
        # The codes can be a list, as in the other options that take several.
        self.per_file_ignores = {
            pattern: str(_as_comma_separated(codes))
            for pattern, codes in (
                dict(per_file_ignores)
                if per_file_ignores
                else djlint_settings.get("per-file-ignores", {})
            ).items()
        }
        for pattern in self.per_file_ignores:
            _check_regex("per-file-ignores", pattern)
        self.blank_line_after_tag = blank_line_after_tag or _as_comma_separated(
            djlint_settings.get("blank_line_after_tag", None)
        )
        self.blank_line_before_tag = blank_line_before_tag or _as_comma_separated(
            djlint_settings.get("blank_line_before_tag", None)
        )
        self.line_break_after_multiline_tag = line_break_after_multiline_tag or setting_bool(
            "line_break_after_multiline_tag"
        )
        self.js_config = _beautifier_config(djlint_settings.get("js"), indent_size=indent_js)
        self.css_config = _beautifier_config(djlint_settings.get("css"), indent_size=indent_css)
        if not self.format_js and (indent_js is not None or djlint_settings.get("js")):
            report("--indent-js and the js settings have no effect without format_js.")
        if not self.format_css and (indent_css is not None or djlint_settings.get("css")):
            report("--indent-css and the css settings have no effect without format_css.")
        if not self.format_attribute_js_json and (
            unused := [
                name
                for name, given in (
                    ("format_attribute_js_json_pattern", bool(format_attribute_js_json_pattern)),
                    (
                        "format_attribute_js_json_min_props",
                        format_attribute_js_json_min_props is not None,
                    ),
                )
                if given or name in djlint_settings
            ]
        ):
            report(
                f"{' and '.join(unused)} {'has' if len(unused) == 1 else 'have'}"
                " no effect without format_attribute_js_json."
            )

        # .editorconfig only fills in what neither the command line nor the
        # configuration sets. Each file gets its own (see for_file); this is
        # for a file of the configured extension in the folder checked.
        self.editorconfig_defaults = frozenset(
            name
            for name, given in (
                ("indent_size", indent or "indent" in djlint_settings),
                ("max_line_length", max_line_length or "max_line_length" in djlint_settings),
            )
            if not given
        )
        self._editorconfig_files: dict[Path, tuple[Any, ...]] = {}
        folder = start if start.is_dir() else start.parent
        editorconfig = self._editorconfig_for(folder / f"_.{self.extension}")
        indent = indent or setting_int("indent", editorconfig.get("indent_size", 4))
        self.indent_size = indent
        self.indent = indent * " "
        self.max_line_length = max_line_length or setting_int(
            "max_line_length", editorconfig.get("max_line_length", 120)
        )
        self.max_attribute_length = (
            max_attribute_length
            if max_attribute_length is not None
            else setting_int("max_attribute_length", 70)
        )
        self.max_blank_lines = (
            max_blank_lines if max_blank_lines is not None else setting_int("max_blank_lines", 0)
        )
        if self.preserve_blank_lines and self.max_blank_lines > 0:
            report("max_blank_lines has no effect with preserve_blank_lines.")

        excludes = build_exclude(exclude or djlint_settings.get("exclude", _DEFAULT_EXCLUDE))
        extensions = build_exclude(extend_exclude or djlint_settings.get("extend_exclude", ""))
        for setting, patterns in (("exclude", excludes), ("extend_exclude", extensions)):
            for pattern in patterns:
                _check_regex(setting, pattern)
        self.exclude = "\n| ".join(excludes + extensions)
        # The patterns are verbose, so each gets a group and a line of its own: a
        # `#` comment in one ends with it, and nothing in one runs into the next.
        # Nothing to exclude matches no path.
        alternatives = "|".join(f"(?:{pattern}\n)" for pattern in excludes + extensions) or "(?!)"
        self.exclude_pattern = compile_pattern(rf"(?:^|/)(?:{alternatives})(?=$|/|(?<=/))", re.X)

        self.files = djlint_settings.get("files", None)
        self.stdin = (src == "-" if stdin is None else stdin) and (
            not self.files or stdin_filename is not None
        )
        self.use_gitignore = (use_gitignore or setting_bool("use_gitignore")) and (
            not self.stdin or stdin_filename is not None
        )
        self.gitignore: PathSpec[Pattern] | None = (
            load_gitignore(self.project_root) if self.use_gitignore else None
        )
        self.allow_empty_input = allow_empty_input or setting_bool("allow_empty_input")

        self.has_profile = bool(selected_profile)
        self.profile = selected_profile or "all"
        if self.profile not in _PROFILES:
            msg = f"Invalid profile {self.profile!r}. Choose from {', '.join(sorted(_PROFILES))}."
            raise BadParameter(msg, param_hint="'--profile'")
        # with no profile the formatter reads every template language, as
        # under "all", and the linter picks the rules html does
        lint_profile = selected_profile or "html"
        profile_codes = _CODES_EXCLUDED_BY_PROFILE.get(lint_profile, ())
        self.ignore = str(ignore or _as_comma_separated(djlint_settings.get("ignore", "")))
        self.include = str(include or _as_comma_separated(djlint_settings.get("include", "")))
        with (Path(__file__).parent / "rules.yaml").open("rb") as f:
            default_rules = yaml.load(f, Loader=_YAML_LOADER)  # noqa: S506
        custom_rules = load_custom_rules(rules or find_djlint_rules(self.project_root))
        self.skipped_rules: tuple[str, ...] = ()
        if not python_rules:
            self.skipped_rules = tuple(
                str(x["rule"].get("name", "undefined"))
                for x in custom_rules
                if "python_module" in x["rule"]
            )
            custom_rules = tuple(x for x in custom_rules if "python_module" not in x["rule"])
        rule_set = tuple(validate_rules(chain(default_rules, custom_rules), report))
        ignored_codes = set(split_option_list(self.ignore))
        included_codes = set(split_option_list(self.include))
        rules_by_code = {x["rule"]["name"]: x["rule"] for x in rule_set}
        known_codes = {*rules_by_code, *self.skipped_rules}
        _check_codes("ignore", sorted(ignored_codes), known_codes, report)
        _check_codes("include", sorted(included_codes), known_codes, report)
        for codes in self.per_file_ignores.values():
            _check_codes("per-file-ignores", split_option_list(codes), known_codes, report)
        for code in sorted(ignored_codes & included_codes):
            report(f"{code} is in both ignore and include, so it stays off.")
        if self.ignore_case:
            ignored_codes.update(("H009", "H010"))
        # the formatter writes `<img />` under it, which H018 rejects
        if self.close_void_tags:
            ignored_codes.add("H018")

        def rule_applies(rule: Mapping[str, Any]) -> bool:
            """Whether the rule runs under the profile in force.

            A profile that names the rule, in the rule's own exclude or by
            its full code, always drops it, as the rule is wrong for that
            template language. A rule named in include runs under any other
            profile, even one that leaves out its family of codes. Otherwise
            "all", being every template language at once, drops a rule
            excluded for any one of them.
            """
            name = rule["name"]
            excluded_profiles = rule.get("exclude", ())
            if lint_profile in excluded_profiles or name in profile_codes:
                return False
            if name in included_codes:
                return True
            if excluded_profiles and lint_profile == "all":
                return False
            return not any(name.startswith(code) for code in profile_codes)

        # With no profile set, naming html would read as if one were.
        profile_name = (
            f"the {lint_profile} profile"
            if selected_profile
            else "no profile, where the linter follows html"
        )
        for code in sorted(included_codes.intersection(rules_by_code)):
            if lint_profile in rules_by_code[code].get("exclude", ()) or code in profile_codes:
                report(f"include names {code}, which never runs under {profile_name}.")

        self.entity_pattern = next(
            (
                re.compile(x["rule"]["patterns"][0], build_flags(x["rule"].get("flags", "re.S")))
                for x in rule_set
                if x["rule"]["name"] == "H023" and "patterns" in x["rule"]
            ),
            None,
        )
        self.linter_rules = tuple(
            x
            for x in rule_set
            if x["rule"]["name"] not in ignored_codes
            and rule_applies(x["rule"])
            and (x["rule"].get("default", True) or x["rule"]["name"] in included_codes)
        )
        for entry in self.linter_rules:
            linter_rule = entry["rule"]
            if "patterns" in linter_rule:
                rule_flags = build_flags(linter_rule.get("flags", "re.S"))
                linter_rule["compiled_patterns"] = tuple(
                    compile_rule_pattern(pattern, rule_flags) for pattern in linter_rule["patterns"]
                )

        if self.lint:
            enabled_rules = {x["rule"]["name"] for x in self.linter_rules}
            if {"H017", "H018"} <= enabled_rules:
                report(
                    "H017 and H018 enforce opposite void tag styles. Enable only one convention. 😢"
                )

        self.custom_blocks = str(
            build_custom_blocks(
                ",".join(
                    x
                    for x in (
                        str(
                            custom_blocks
                            or _as_comma_separated(djlint_settings.get("custom_blocks"))
                            or ""
                        ),
                        _PROFILE_ONLY_BLOCKS.get(self.profile, ""),
                    )
                    if x
                )
            )
            or ""
        )
        django_cotton_components = r"|c-[\w.-]+"
        self.custom_html = (
            str(
                build_custom_html(
                    custom_html or _as_comma_separated(djlint_settings.get("custom_html"))
                )
                or ""
            )
            + django_cotton_components
        )
        self.ignore_blocks = build_ignore_blocks(
            ignore_blocks or _as_comma_separated(djlint_settings.get("ignore_blocks", ""))
        )
        ignore_blocks_guard = rf"(?!{self.ignore_blocks})" if self.ignore_blocks else ""
        self.format_attribute_js_json_pattern = compile_pattern(
            format_attribute_js_json_pattern
            or djlint_settings.get("format_attribute_js_json_pattern", _DEFAULT_JS_JSON_PATTERN),
            RE_FLAGS_IX,
        )

        indenting_html_tags = (
            HTML_TAG_NAMES - {"html"} if self.no_indent_inner_html else HTML_TAG_NAMES
        )
        self.indent_html_tags = "|".join(indenting_html_tags) + self.custom_html
        self.always_self_closing_html_tags = _ALWAYS_SELF_CLOSING_HTML_TAGS

        not_self_closed = r"\b(?!(?:(?!%\}).)*/\s*-?%\})"
        custom_block_openers = self.custom_blocks.replace(r"\b", not_self_closed)
        is_golang = self.profile == "golang"
        self.template_indent = (
            r"""
            (?:\{\{\#|\{%[-+]?)[ ]*
                ("""
            + ignore_blocks_guard
            + _INDENT_TEMPLATE_TAGS
            + custom_block_openers
            + r")\b"
            + r"""
            ) | \{{-?[ ]*form_start
            """
            + (_GOLANG_BLOCK_OPEN if is_golang else "")
        )
        trans_is_a_custom_block = (
            r"|trans\b" in self.custom_blocks or r"|translate\b" in self.custom_blocks
        )
        end_tag_guard = (
            r"(?!comment)" if trans_is_a_custom_block else r"(?!comment|trans(?:late)?\b)"
        )
        self.template_unindent = (
            r"""
                (?:
                  # handlebars block close {{/name}}, but not a golang
                  # comment {{/* ... */}}, which closes nothing
                  (?:\{\{\/(?!\*))
                | (?:\{%[-+]?[ ]*end"""
            + end_tag_guard
            + ignore_blocks_guard
            + r""")
                | (?:\{{-?[ ]*form_end)
            """
            + (_GOLANG_BLOCK_CLOSE if is_golang else "")
            + r"""
              )
            """
        )
        self.start_template_tags = (
            ignore_blocks_guard
            + _START_TEMPLATE_TAGS
            + custom_block_openers
            + r""")
        """
            + (_GOLANG_BLOCK_OPEN if is_golang else "")
        )
        self.single_line_template_tags = (
            ignore_blocks_guard + _INDENT_TEMPLATE_TAGS + custom_block_openers + r")"
        )
        self.break_template_tags = (
            ignore_blocks_guard
            + _BREAK_TEMPLATE_TAGS
            + self.custom_blocks
            + (r"|when\b|elsif\b" if self.profile == "liquid" else "")
            + r""")
        """
        )
        self.break_html_tags = (
            _BREAK_HTML_TAGS
            + self.always_self_closing_html_tags
            + self.custom_html
            + """
        """
        )
        self.tag_indent = (
            self.template_indent
            + """
            | (?:<
                (?:
                    """
            + self.indent_html_tags
            + """
                )\\b
              )
            | (?:"""
            + _TEMPLATE_NAMED_OPENING_TAG
            + """)
        """
        )
        self.tag_unindent = (
            r"""
                ^
                """
            + self.template_unindent
            + """
            | (?:^</
                (?:
                    """
            + self.indent_html_tags
            + """
                )\\b
              )
            | (?:^</(?:"""
            + TEMPLATE_TAG_NAME
            + """))
            | (?:</
                (?:
                    """
            + self.indent_html_tags
            + """
                )>$
              )
            | (?:</(?:"""
            + TEMPLATE_TAG_NAME
            + """)>$)
        """
        )

        self.template_indent_ix_pattern = compile_pattern(self.template_indent, RE_FLAGS_IX)
        self.template_indent_imx_pattern = compile_pattern(self.template_indent, RE_FLAGS_IMX)
        self.template_unindent_ix_pattern = compile_pattern(self.template_unindent, RE_FLAGS_IX)
        self.template_unindent_imx_pattern = compile_pattern(self.template_unindent, RE_FLAGS_IMX)

        self.attribute_pattern = _ATTRIBUTE_X_PATTERN
        self.template_tags = _TEMPLATE_TAGS
        self.template_tags_imx_pattern = _TEMPLATE_TAGS_IMX_PATTERN
        self.tag_unindent_line = (
            _LIQUID_TAG_UNINDENT_LINE if self.profile == "liquid" else _TAG_UNINDENT_LINE
        )
        if is_golang:
            self.tag_unindent_line += _GOLANG_BRANCH
        self.tag_unindent_line_ix_pattern = compile_pattern(self.tag_unindent_line, RE_FLAGS_IX)
        self.break_before = _BREAK_BEFORE
        self.ignored_attributes = _IGNORED_ATTRIBUTES
        self.ignored_inline_blocks = _IGNORED_INLINE_BLOCKS
        self.optional_single_line_html_tags = _OPTIONAL_SINGLE_LINE_HTML_TAGS
        self.optional_single_line_template_tags = _OPTIONAL_SINGLE_LINE_TEMPLATE_TAGS
        self.format_attribute_js_json_object_pattern = _JS_JSON_OBJECT_PATTERN
        self.format_attribute_js_json_string_pattern = _JS_JSON_STRING_PATTERN
        self.format_attribute_js_json_property_pattern = _JS_JSON_PROPERTY_PATTERN
        self.raw_text_opening_pattern = _RAW_TEXT_OPENING_PATTERN
        self.raw_text_closing_pattern = _RAW_TEXT_CLOSING_PATTERN
        self.raw_text_inline_imsx_pattern = _RAW_TEXT_INLINE_IMSX_PATTERN
        self.raw_text_inline_ix_pattern = _RAW_TEXT_INLINE_IX_PATTERN
        self.ignored_block_opening_pattern = _IGNORED_BLOCK_OPENING_PATTERN
        self.ignored_block_closing_pattern = _IGNORED_BLOCK_CLOSING_PATTERN
        self.ignored_block_closing_at_start_pattern = _IGNORED_BLOCK_CLOSING_AT_START_PATTERN
        self.ignored_block_closing_anywhere_pattern = _IGNORED_BLOCK_CLOSING_ANYWHERE_PATTERN
        self.ignored_blocks_pattern = _IGNORED_BLOCKS_PATTERN
        self.lint_ignored_blocks_pattern = _LINT_IGNORED_BLOCKS_PATTERN
        self.ignored_blocks_inline_pattern = _IGNORED_BLOCKS_INLINE_PATTERN
        self.ignored_inline_blocks_ix_pattern = _IGNORED_INLINE_BLOCKS_IX_PATTERN
        self.lint_ignored_inline_blocks_ix_pattern = _LINT_IGNORED_INLINE_BLOCKS_IX_PATTERN
        self.ignored_linter_blocks_pattern = _IGNORED_LINTER_BLOCKS_PATTERN
        self.ignored_trans_blocks_pattern = _IGNORED_TRANS_BLOCKS_PATTERN
        self.ignored_trans_blocks_closing_pattern = _IGNORED_TRANS_BLOCKS_CLOSING_PATTERN
        self.trans_trimmed_blocks_pattern = _TRANS_TRIMMED_BLOCKS_PATTERN
        self.safe_closing_block_pattern = _SAFE_CLOSING_BLOCK_PATTERN
        self.safe_closing_tag_pattern = _SAFE_CLOSING_TAG_PATTERN
        self.template_blocks_pattern = _TEMPLATE_BLOCKS_PATTERN
        self.unformatted_blocks_coarse_pattern = _UNFORMATTED_BLOCKS_COARSE_PATTERN
        self.unformatted_blocks_pattern = _UNFORMATTED_BLOCKS_PATTERN
        self.ignored_rule_patterns = _IGNORED_RULE_PATTERNS
        self.optional_single_line_html_pattern = _OPTIONAL_SINGLE_LINE_HTML_PATTERN
        self.optional_single_line_template_pattern = _OPTIONAL_SINGLE_LINE_TEMPLATE_PATTERN
        if self.profile == "mako":
            # The block tags under this profile stand for Mako's control lines,
            # which a block put on one line would join.
            self.optional_single_line_template_tags = "(?!)"
            self.optional_single_line_template_pattern = compile_pattern("(?!)")
        if profile_blocks := _PROFILE_ONLY_BLOCKS.get(self.profile):
            self.optional_single_line_template_tags += "|" + "|".join(
                split_option_list(profile_blocks)
            )
            self.optional_single_line_template_pattern = compile_pattern(
                rf"^(?:{self.optional_single_line_template_tags})$", RE_FLAGS_IX
            )

    def _editorconfig_for(self, file: Path) -> dict[str, int]:
        folder = file.parent
        if folder not in self._editorconfig_files:
            self._editorconfig_files[folder] = editorconfig_files(folder, self.project_root)
        return editorconfig_for(file, self._editorconfig_files[folder])

    def for_file(self, file: Path) -> Config:
        """This configuration with the .editorconfig of a file, where it applies.

        The configuration is built for the folder a run starts from, but
        editors read .editorconfig for each file, by its path. Only what the
        command line and the configuration leave to .editorconfig changes.
        """
        if not self.editorconfig_defaults:
            return self
        found = self._editorconfig_for(file.resolve())
        indent_size = (
            found.get("indent_size", 4)
            if "indent_size" in self.editorconfig_defaults
            else self.indent_size
        )
        max_line_length = (
            found.get("max_line_length", 120)
            if "max_line_length" in self.editorconfig_defaults
            else self.max_line_length
        )
        if (indent_size, max_line_length) == (self.indent_size, self.max_line_length):
            return self
        config = copy.copy(self)
        config.indent_size = indent_size
        config.indent = indent_size * " "
        config.max_line_length = max_line_length
        return config
