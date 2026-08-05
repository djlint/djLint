"""Build src file list."""

from __future__ import annotations

import sys
from types import MappingProxyType
from typing import TYPE_CHECKING

import regex as re
from click import echo, style

if sys.version_info >= (3, 13):
    from typing import NamedTuple
else:
    from typing_extensions import NamedTuple

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path
    from typing import Final

    from djlint.settings import Config


class SrcFiles(NamedTuple):
    """Files to process, and why the list may be empty.

    An empty ``paths`` with ``excluded`` set means candidates were found
    and every one of them was deliberately skipped by the configuration -
    a successful no-op. An empty ``paths`` without it means nothing
    matched the requested paths at all, which is a usage error.
    """

    paths: list[Path]
    excluded: bool


def _gitignore_match(config: Config, filepath: Path) -> bool:
    """Check if a file matches gitignore patterns using a relative path.

    pathspec.match_file matches against all path components, so passing
    an absolute path causes false positives when parent directories
    (outside the project) match a gitignore pattern.
    """
    try:
        rel = filepath.relative_to(config.project_root)
    except ValueError:
        return False
    return config.gitignore.match_file(rel)


def _exclude_match(config: Config, filepath: Path, root: Path) -> bool:
    """Check if a file matches exclude patterns using relative paths."""
    relative_roots = (
        (config.project_root,)
        if config.project_root == root
        else (config.project_root, root)
    )
    for relative_root in relative_roots:
        try:
            rel = filepath.relative_to(relative_root)
        except ValueError:
            continue
        rel_path = rel.as_posix()
        if config.exclude_pattern.search(rel_path):
            return True
        if (
            relative_root == config.project_root
            and config.exclude_pattern.search(f"/{rel_path}")
        ):
            return True
    return False


def _included(config: Config, filepath: Path) -> bool:
    """Check a file against the filters that need it to exist on disk."""
    return no_pragma(config, filepath) and (
        not config.use_gitignore or not _gitignore_match(config, filepath)
    )


def get_src(src: Iterable[Path], config: Config) -> SrcFiles:
    """Get source files."""
    paths = []
    excluded = False
    for item in src:
        # normalize path

        normalized_item = item.resolve()

        if normalized_item.is_file():
            if _exclude_match(
                config, normalized_item, config.project_root
            ) or not _included(config, normalized_item):
                excluded = True
            else:
                paths.append(normalized_item)
            continue

        # remove leading . from extension
        extension = config.extension.removeprefix(".")

        for candidate in normalized_item.glob(f"**/*.{extension}"):
            if _exclude_match(config, candidate, normalized_item):
                excluded = True
                continue
            # a directory can match the extension glob too, and it is not a
            # candidate at all - opening one raises rather than excluding it.
            # The exclude pattern above is pure string work, so testing it
            # first spares this syscall for everything the pattern drops.
            if not candidate.is_file():
                continue
            if _included(config, candidate):
                paths.append(candidate)
            else:
                excluded = True

    return SrcFiles(paths, excluded)


def print_no_files_to_check(*, excluded: bool) -> None:
    """Report an empty file list on stderr.

    Never on stdout: that is where formatted code is written, and a
    diagnostic mixed into it would be read back as file contents.
    """
    message = "No files to check! 😢"
    if excluded:
        message += " Everything that matched was skipped by the configuration."
    echo(style(message, fg="blue"), err=True)


_HTML_PRAGMA_PATTERNS: Final = (
    re.compile(r"<!--\s*djlint\:on\s*-->", cache_pattern=False),
)
_TEMPLATE_COMMENT_PRAGMA_PATTERN: Final = re.compile(
    r"\{#\s*djlint\:on\s*#\}", cache_pattern=False
)
_DJANGO_JINJA_PRAGMA_PATTERNS: Final = (
    _TEMPLATE_COMMENT_PRAGMA_PATTERN,
    re.compile(
        r"\{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}",
        cache_pattern=False,
    ),
)
_NUNJUCKS_PRAGMA_PATTERNS: Final = (_TEMPLATE_COMMENT_PRAGMA_PATTERN,)
_HANDLEBARS_PRAGMA_PATTERNS: Final = (
    re.compile(r"\{\{!--\s*djlint\:on\s*--\}\}", cache_pattern=False),
)
_GOLANG_PRAGMA_PATTERNS: Final = (
    re.compile(
        r"\{\{-?\s*/\*\s*djlint\:on\s*\*/\s*-?\}\}", cache_pattern=False
    ),
)
_PRAGMA_PATTERNS: Final = MappingProxyType({
    "html": _HTML_PRAGMA_PATTERNS,
    "django": _DJANGO_JINJA_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "jinja": _DJANGO_JINJA_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "askama": _DJANGO_JINJA_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "tera": _DJANGO_JINJA_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "liquid": _DJANGO_JINJA_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "nunjucks": _NUNJUCKS_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "handlebars": _HANDLEBARS_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "golang": _GOLANG_PRAGMA_PATTERNS + _HTML_PRAGMA_PATTERNS,
    "angular": _HTML_PRAGMA_PATTERNS,
    "all": _DJANGO_JINJA_PRAGMA_PATTERNS
    + _NUNJUCKS_PRAGMA_PATTERNS
    + _HANDLEBARS_PRAGMA_PATTERNS
    + _GOLANG_PRAGMA_PATTERNS
    + _HTML_PRAGMA_PATTERNS,
})


def has_pragma(config: Config, first_line: str) -> bool:
    """Check whether a line enables djLint."""
    for pattern in _PRAGMA_PATTERNS[config.profile]:
        if pattern.match(first_line):
            return True
    return False


def no_pragma(config: Config, this_file: Path) -> bool:
    """Verify there is no pragma present."""
    if not config.require_pragma:
        return True

    with this_file.open(encoding="utf-8") as open_file:
        first_line = open_file.readline()

    return has_pragma(config, first_line)
