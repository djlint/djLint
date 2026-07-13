"""Build src file list."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

import regex as re
from click import echo, style

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path
    from typing import Final

    from djlint.settings import Config


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


def get_src(src: Iterable[Path], config: Config) -> list[Path]:
    """Get source files."""
    paths = []
    for item in src:
        # normalize path

        normalized_item = item.resolve()

        if normalized_item.is_file():
            if no_pragma(config, normalized_item) and (
                not config.use_gitignore
                or not _gitignore_match(config, normalized_item)
            ):
                paths.append(normalized_item)
            continue

        # remove leading . from extension
        extension = config.extension.removeprefix(".")

        paths.extend(
            x
            for x in normalized_item.glob(f"**/*.{extension}")
            if (
                not _exclude_match(config, x, normalized_item)
                and no_pragma(config, x)
                and (
                    not config.use_gitignore or not _gitignore_match(config, x)
                )
            )
        )

    if not paths:
        print_no_files_to_check()

    return paths


def print_no_files_to_check() -> None:
    echo(style("No files to check! 😢", fg="blue"))


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
