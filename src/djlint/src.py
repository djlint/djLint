"""Build src file list."""
import re
from pathlib import Path
from typing import List

from click import echo
from colorama import Fore

from .settings import Config


def get_src(src: List[Path], config: Config) -> List[Path]:
    """Get source files."""
    paths = []
    for item in src:
        # normalize path

        normalized_item = item.resolve()

        if (
            Path.is_file(normalized_item)
            and no_pragma(config, normalized_item)
            and (
                (
                    config.use_gitignore
                    and not config.gitignore.match_file(normalized_item)
                )
                or not config.use_gitignore
            )
        ):
            paths.append(normalized_item)
            continue

        # remove leading . from extension
        extension = str(config.extension)
        extension = extension[1:] if extension.startswith(".") else extension

        paths.extend(
            filter(
                lambda x: not re.search(config.exclude, x.as_posix(), re.VERBOSE)
                and no_pragma(config, x)
                and (
                    (config.use_gitignore and not config.gitignore.match_file(x))
                    or not config.use_gitignore
                ),
                list(normalized_item.glob(f"**/*.{extension}")),
            )
        )

    if len(paths) == 0:
        echo(Fore.BLUE + "No files to check! 😢")

    return paths


html_patterns = [re.compile(r"<!--\s*djlint\:on\s*-->")]
django_jinja_patterns = [
    re.compile(r"\{#\s*djlint\:on\s*#\}"),
    re.compile(r"\{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}"),
]
nunjucks_patterns = [re.compile(r"\{#\s*djlint\:on\s*#\}")]
handlebars_patterns = [re.compile(r"\{\{!--\s*djlint\:on\s*--\}\}")]
golang_patterns = [re.compile(r"\{\{-?\s*/\*\s*djlint\:on\s*\*/\s*-?\}\}")]


def no_pragma(config: Config, this_file: Path) -> bool:
    """Verify there is no pragma present."""
    if config.require_pragma is False:
        return True

    with this_file.open(encoding="utf8") as open_file:
        first_line = open_file.readline()

        pragma_patterns = {
            "html": html_patterns,
            "django": django_jinja_patterns + html_patterns,
            "jinja": django_jinja_patterns + html_patterns,
            "nunjucks": nunjucks_patterns + html_patterns,
            "handlebars": handlebars_patterns + html_patterns,
            "golang": golang_patterns + html_patterns,
            "angular": html_patterns,
            "all": django_jinja_patterns
            + nunjucks_patterns
            + handlebars_patterns
            + golang_patterns
            + html_patterns,
        }

        return any(
            re.match(pattern, first_line) for pattern in pragma_patterns[config.profile]
        )
