"""Settings for reformater."""

from __future__ import annotations

import json
import sys
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

import regex as re
import yaml
from click import echo, style
from pathspec import PathSpec

from djlint.const import HTML_TAG_NAMES, HTML_VOID_ELEMENTS
from djlint.helpers import RE_FLAGS_IMSX, RE_FLAGS_ISX, RE_FLAGS_IX

try:
    from pathspec.patterns.gitignore import GitIgnorePatternError
except ImportError:
    # pathspec < 1.0 exposes the older gitwildmatch implementation.
    from pathspec.patterns.gitwildmatch import (  # type: ignore[attr-defined]
        GitWildMatchPatternError as GitIgnorePatternError,
    )

    _GITIGNORE_PATTERN = "gitwildmatch"
else:
    _GITIGNORE_PATTERN = "gitignore"

if sys.version_info >= (3, 11):
    from typing import final

    try:
        import tomllib
    except ImportError:
        # Help users on older alphas
        if not TYPE_CHECKING:
            import tomli as tomllib
else:
    import tomli as tomllib
    from typing_extensions import final

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Mapping
    from typing import Final

    from pathspec import Pattern
    from typing_extensions import Any, TypeVar

    _TMappingStrAny = TypeVar("_TMappingStrAny", bound=Mapping[str, Any])


_JS_JSON_OBJECT_PATTERN: Final = re.compile(
    r"^\s*\{(?![{%]).*\}\s*$", RE_FLAGS_IX, cache_pattern=False
)
_JS_JSON_STRING_PATTERN: Final = re.compile(
    r'["\']([^"\']*)["\']', RE_FLAGS_IX, cache_pattern=False
)
_JS_JSON_PROPERTY_PATTERN: Final = re.compile(
    r"""
    (?:^|[,{]\s*)
    (?:
        [a-zA-Z_$][a-zA-Z0-9_$]*\s*:
      | (?:get|set)\s+[a-zA-Z_$][a-zA-Z0-9_$]*\s*\(
      | (?:async\s+)?\*?\s*[a-zA-Z_$][a-zA-Z0-9_$]*\s*\(
    )
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)

DJLINT_TOML_CONFIG_FILES: Final = ("djlint.toml", ".djlint.toml")


def find_project_root(src: Path) -> Path:
    """Attempt to get the project root."""
    for directory in (src, *src.parents):
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

        for config_file in DJLINT_TOML_CONFIG_FILES:
            if (directory / config_file).is_file():
                return directory

        if (directory / ".djlintrc").is_file():
            return directory

    return src if src.is_dir() else src.parent


def load_gitignore(root: Path) -> PathSpec[Pattern]:
    """Search upstream for a .gitignore file."""
    gitignore = root / ".gitignore"
    if gitignore.is_file():
        with gitignore.open(encoding="utf-8") as this_file:
            git_lines = this_file.readlines()
    else:
        git_lines = []

    try:
        return PathSpec.from_lines(_GITIGNORE_PATTERN, git_lines)

    except GitIgnorePatternError as e:
        echo(f"Could not parse {gitignore}: {e}", err=True)
        raise


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


def load_project_settings(src: Path, config: Path | None) -> dict[str, Any]:
    """Load djlint config."""
    djlint_content: dict[str, Any] = {}

    if config:
        try:
            djlint_content.update(load_config_file(config))
        except Exception as error:
            echo(
                style(
                    f"Failed to load config file {config}. {error}", fg="red"
                ),
                err=True,
            )

    if pyproject_file := find_pyproject(src):
        try:
            content = load_pyproject_config(pyproject_file)
        except Exception as error:
            echo(
                style(f"Failed to load pyproject.toml file. {error}", fg="red"),
                err=True,
            )
        else:
            if content:
                djlint_content.update(content)
                return djlint_content

    if djlint_toml_file := find_djlint_toml(src):
        try:
            djlint_content.update(load_djlint_toml_config(djlint_toml_file))
        except Exception as error:
            echo(
                style(
                    f"Failed to load {djlint_toml_file.name} file. {error}",
                    fg="red",
                ),
                err=True,
            )

    elif djlintrc_file := find_djlintrc(src):
        try:
            djlint_content.update(load_djlintrc_config(djlintrc_file))
        except Exception as error:
            echo(
                style(f"Failed to load .djlintrc file. {error}", fg="red"),
                err=True,
            )

    return djlint_content


def validate_rules(
    rules: Iterable[_TMappingStrAny],
) -> Iterator[_TMappingStrAny]:
    """Validate a list of linter rules. Returns valid rules."""
    for rule in rules:
        warning = False
        name = rule["rule"].get("name", "undefined")
        if "name" not in rule["rule"]:
            warning = True
            echo(
                style("Warning: A rule is missing a name! 😢", fg="red"),
                err=True,
            )
        if (
            "patterns" not in rule["rule"]
            and "python_module" not in rule["rule"]
        ):
            warning = True
            echo(
                style(
                    f"Warning: Rule {name} is missing a pattern or a python_module! 😢",
                    fg="red",
                ),
                err=True,
            )
        if "message" not in rule["rule"]:
            warning = True
            echo(
                style(
                    f"Warning: Rule {name} is missing a message! 😢", fg="red"
                ),
                err=True,
            )

        if not warning:
            yield rule


def load_custom_rules(src: Path) -> Any:
    """Load djlint config from pyproject.toml."""
    djlint_rules_file = find_djlint_rules(src)

    if djlint_rules_file:
        return yaml.load(
            djlint_rules_file.read_text(encoding="utf-8"),
            Loader=yaml.SafeLoader,
        )

    return ()


def build_custom_blocks(custom_blocks: str | None) -> str | None:
    """Build regex string for custom template blocks."""
    if custom_blocks:
        open_tags = {x.strip() + r"\b" for x in custom_blocks.split(",")}
        close_tags = {f"end{x}" for x in open_tags}
        return "|" + "|".join(sorted(open_tags | close_tags))
    return None


def build_ignore_blocks(ignore_blocks: str | None) -> str | None:
    """Build regex string for template blocks to not format."""
    if ignore_blocks:
        open_tags = {x.strip() + r"\b" for x in ignore_blocks.split(",")}
        close_tags = {f"end{x}" for x in open_tags}
        return "|".join(sorted(open_tags | close_tags))
    return None


def build_custom_html(custom_html: str | None) -> str | None:
    """Build regex string for custom HTML blocks."""
    if custom_html:
        return "|" + "|".join(x.strip() for x in custom_html.split(","))
    return None


def build_exclude(exclude: str) -> str:
    """Build regex string for exclude paths."""
    if "," not in exclude:
        return exclude
    return r" | ".join(x.strip() for x in exclude.split(",") if x.strip())


# The patterns below do not depend on configuration and are built once at
# import time, like the _JS_JSON_* patterns above.

# codes to exclude per profile
_PROFILE_CODES: Final[dict[str, tuple[str, ...]]] = {
    "html": ("D", "J", "T", "N", "M"),
    "django": ("J", "N", "M"),
    "jinja": ("D", "N", "M"),
    "nunjucks": ("D", "J", "M"),
    "handlebars": ("D", "J", "N"),
    "golang": ("D", "J", "N", "M"),
    "angular": ("D", "J", "H012", "H026", "H028"),
}

# From ruff and black
_DEFAULT_EXCLUDE: Final = r"""
    __pypackages__
    | _build
    | \.bzr
    | \.direnv
    | \.eggs
    | \.git
    | \.git-rewrite
    | \.hg
    | \.ipynb_checkpoints
    | \.mypy_cache
    | \.nox
    | \.pants\.d
    | \.pytest_cache
    | \.pytype
    | \.ruff_cache
    | \.svn
    | \.tox
    | \.venv
    | \.vscode
    | buck-out
    | build
    | dist
    | node_modules
    | venv
"""

# Default pattern for common JS-bearing attributes. data-* attributes
# are intentionally opt-in via format_attribute_js_json_pattern.
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

_TEMPLATE_IF_FOR_PATTERN: Final = r"(?:{%-?\s?(?:if|for|asyncAll|asyncEach)[^}]*?%}(?:.*?{%\s?end(?:if|for|each|all)[^}]*?-?%})+?)"

_ATTRIBUTE_PATTERN: Final = (
    rf"""
    (?:
        (
            (?:
                (?:\w|-|\.|\:|@|\*|/(?!>)) # a name character
               | (?>{{{{[\s\S]*?}}}})
                 (?=(?:\w|-|\.|\:|@|\*|/(?!>))|[ ]*=) # a leading template variable
               | (?!{{%-?\s*(?:for|asyncAll|asyncEach)\b)
                 (?!{{%-?\s*if\b[^}}]*?%}}(?:required|checked){{%-?\s*endif\b[^}}]*?%}})
                 (?>{_TEMPLATE_IF_FOR_PATTERN})
                 (?=(?:\w|-|\.|\:|@|\*|/(?!>))|[ ]*=) # a leading template block
            )
            (?:
                (?:\w|-|\.|\:|@|\*|/(?!>)) # more name characters
               | (?>{{{{[\s\S]*?}}}}|{{%[\s\S]*?%}}) # or an embedded template tag
            )*
            | required | checked
        )? # attribute name
        (?:  [ ]*?=[ ]*? # followed by "="
            (
                \"[^\"]*? # double quoted attribute
                (?:
                    {_TEMPLATE_IF_FOR_PATTERN} # if or for loop
                   | {{{{[\s\S]*?}}}} # template stuff
                   | {{%[\s\S]*?%}}
                   | [^\"] # anything else
                )*?
                \" # closing quote
              | '[^']*? # single quoted attribute
                (?:
                    {_TEMPLATE_IF_FOR_PATTERN} # if or for loop
                   | {{{{[\s\S]*?}}}} # template stuff
                   | {{%[\s\S]*?%}}
                   | [^'] # anything else
                )*?
                \' # closing quote
              | (?:\w|-)+ # or a non-quoted string value
              | {{{{[\s\S]*?}}}} # a non-quoted template var
              | {{%[\s\S]*?%}} # a non-quoted template tag
              | {_TEMPLATE_IF_FOR_PATTERN} # a non-quoted if statement

            )
        )? # attribute value
    )
    | ({_TEMPLATE_IF_FOR_PATTERN}
    """
    r"""
    | (?:\'|\") # allow random trailing quotes
    | {{[\s\S]*?}}
    | {\#[\s\S]*?\#}
    | {%[\s\S]*?%})
    """
)

_TEMPLATE_TAGS: Final = r"""
    {{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}
"""

# these tags should be unindented and next line will be indented
_TAG_UNINDENT_LINE: Final = r"""
      (?:\{%-?[ ]*?(?:elif|else|empty|plural))
    | (?:
        \{\{[ ]*?
        (
            (?:else|\^)
            [ ]*?\}\}
        )
      )
"""

_BREAK_BEFORE: Final = r"(?<!\n[ \t]*?)"

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
    | unless
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

_IGNORED_INLINE_BLOCKS: Final = r"""
      <!--.*?-->
    | <script.*?\</script>
    | <style.*?\</style>
    | {\*.*?\*}
    | {\#(?!.*djlint:[ ]*?(?:off|on)\b).*\#}
    | <\?php.*?\?>
    | {%[ ]*?comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?{%[ ]*?endcomment[ ]*?%}
    | {%[ ]*?filter\b(?:(?!%}).)*?%}.*?{%[ ]*?endfilter[ ]*?%}
    | {%[ ]*?blocktrans(?:late)?\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*?endblocktrans(?:late)?[ ]*?%}
"""

_IGNORED_BLOCKS: Final = r"""
      <(pre|textarea).*?</(\1)>
    | <(script|style).*?(?=(\</(?:\3)>))
    # html comment
    | <!--\s*djlint\:off\s*-->.(?:(?!<!--\s*djlint\:on\s*-->).)*
    # django/jinja/nunjucks
    | {\#\s*djlint\:\s*off\s*\#}(?:(?!{\#\s*djlint\:\s*on\s*\#}).)*
    | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}(?:(?!{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}).)*
    # inline jinja comments
    | {\#(?!\s*djlint\:\s*(?:off|on)).*?\#}
    # handlebars
    | {{!--\s*djlint\:off\s*--}}(?:(?!{{!--\s*djlint\:on\s*--}}).)*
    # golang
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}(?:(?!{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}).)*
    # inline golang comments
    | {{-?\s*/\*(?!\s*djlint\:\s*(?:off|on)).*?\*/\s*-?}}
    | <!--.*?-->
    | <\?php.*?\?>
    | {%[ ]*?filter\b(?:(?!%}).)*?%}.*?{%[ ]*?endfilter[ ]*?%}
    | {%[ ]*?blocktranslate\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*?endblocktranslate[ ]*?%}
    | {%[ ]*?blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*?endblocktrans[ ]*?%}
    | {%[ ]*?comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*?endcomment[ ]*?%})
    | ^---[\s\S]+?---
"""

_SCRIPT_STYLE_INLINE: Final = r"""
    <(script|style).*?(?=(\</(?:\1)>))
"""

# contents of tags will not be formatted
_SCRIPT_STYLE_OPENING_PATTERN: Final = re.compile(
    r"""
      <style
    | <script
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_SCRIPT_STYLE_CLOSING_PATTERN: Final = re.compile(
    r"""
      </style
    | </script
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_SCRIPT_STYLE_INLINE_IMSX_PATTERN: Final = re.compile(
    _SCRIPT_STYLE_INLINE, RE_FLAGS_IMSX, cache_pattern=False
)
_SCRIPT_STYLE_INLINE_IX_PATTERN: Final = re.compile(
    _SCRIPT_STYLE_INLINE, RE_FLAGS_IX, cache_pattern=False
)
_IGNORED_BLOCK_OPENING_PATTERN: Final = re.compile(
    r"""
      <style
    | {\*
    | <\?php
    | <script
    | <!--
    | [^\{]{\#(?!\s*djlint\:\s*(?:on|off))
    | ^{\#(?!\s*djlint\:\s*(?:on|off))
    | <pre
    | <textarea
    | {%[ ]*?blocktrans(?:late)?(?:(?!%}|\btrimmed\b).)*?%}
    | {%[ ]*?filter\b(?:(?!%}).)*?%}
    | {\#\s*djlint\:\s*off\s*\#}
    | {%[ ]+?comment[ ]+?(?:(?!%}).)*?%}
    | {{!--\s*djlint\:off\s*--}}
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_IGNORED_BLOCK_CLOSING_PATTERN: Final = re.compile(
    r"""
      </style
    | \*}
    | \?>
    | </script
    |  -->
    | ^(?:(?!{\#).)*\#} # lines that have a #}, but not a {#
    | </pre
    | </textarea
    | {%[ ]*?endfilter(?:(?!%}).)*?%}
    | {\#\s*djlint\:\s*on\s*\#}
    | (?<!djlint:off\s*?){%[ ]+?endcomment[ ]+?%}
    | {{!--\s*djlint\:on\s*--}}
    | {{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}
    | {%[ ]*?endblocktrans(?:late)?(?:(?!%}).)*?%}
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_IGNORED_BLOCKS_PATTERN: Final = re.compile(
    _IGNORED_BLOCKS, RE_FLAGS_IMSX, cache_pattern=False
)
_IGNORED_BLOCKS_INLINE_PATTERN: Final = re.compile(
    r"""
      <(pre|textarea).*?</(\1)>
    | <(script|style).*?(?=(\</(?:\3)>))
    # html comment
    | <!--\s*djlint\:off\s*-->.*?(?=<!--\s*djlint\:on\s*-->)
    # django/jinja/nunjucks
    | {\#\s*djlint\:\s*off\s*\#}.*?(?={\#\s*djlint\:\s*on\s*\#})
    | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}.*?(?={%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\})
    # inline jinja comments
    | {\#(?!\s*djlint\:\s*(?:off|on)).*?\#}
    # handlebars
    | {{!--\s*djlint\:off\s*--}}.*?(?={{!--\s*djlint\:on\s*--}})
    # golang
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}.*?(?={{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}})
    # inline golang comments
    | {{-?\s*/\*(?!\s*djlint\:\s*(?:off|on)).*?\*/\s*-?}}
    | <!--.*?-->
    | <\?php.*?\?>
    | {%[ ]*?filter\b(?:(?!%}).)*?%}.*?{%[ ]*?endfilter[ ]*?%}
    | {%[ ]*?blocktranslate\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*?endblocktranslate[ ]*?%}
    | {%[ ]*?blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*?endblocktrans[ ]*?%}
    | {%[ ]*?comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*?endcomment[ ]*?%})
    | ^---[\s\S]+?---
    """,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_IGNORED_INLINE_BLOCKS_IX_PATTERN: Final = re.compile(
    _IGNORED_INLINE_BLOCKS, RE_FLAGS_IX, cache_pattern=False
)
_IGNORED_LINTER_BLOCKS_PATTERN: Final = re.compile(
    r"""
    {%-?[ ]*?raw\b(?:(?!%}).)*?-?%}.*?(?={%-?[ ]*?endraw[ ]*?-?%})
    """,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_UNFORMATTED_BLOCKS_COARSE_PATTERN: Final = re.compile(
    r"djlint\:\s*off", RE_FLAGS_IMSX, cache_pattern=False
)
_UNFORMATTED_BLOCKS_PATTERN: Final = re.compile(
    r"""
    # html comment
    | <!--\s*djlint\:off\s*-->.(?:(?!<!--\s*djlint\:on\s*-->).)*
    # django/jinja/nunjucks
    | (?<!{){\#\s*djlint\:\s*off\s*\#}(?:(?!{\#\s*djlint\:\s*on\s*\#}).)*
    | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}(?:(?!{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}).)*
    # inline jinja comments
    | (?<!{){\#(?!\s*djlint\:\s*(?:off|on)).*?\#}
    # handlebars
    | {{!--\s*djlint\:off\s*--}}(?:(?!{{!--\s*djlint\:on\s*--}}).)*
    # golang
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}(?:(?!{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}).)*
    | ^---[\s\S]+?---
    """,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_IGNORED_RULE_PATTERNS: Final = tuple(
    re.compile(pattern, RE_FLAGS_ISX, cache_pattern=False)
    for pattern in (
        # html comment
        r"<!--\s*djlint\:off(.+?)-->(?:(?!<!--\s*djlint\:on\s*-->).)*",
        # django/jinja/nunjucks
        r"{\#\s*djlint\:\s*off(.+?)\#}(?:(?!{\#\s*djlint\:\s*on\s*\#}).)*",
        r"{%\s*comment\s*%\}\s*djlint\:off(.*?)\{%\s*endcomment\s*%\}(?:(?!{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}).)*",
        # handlebars
        r"{{!--\s*djlint\:off(.*?)--}}(?:(?!{{!--\s*djlint\:on\s*--}}).)*",
        # golang
        r"{{-?\s*/\*\s*djlint\:off(.*?)\*/\s*-?}}(?:(?!{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}).)*",
    )
)
_IGNORED_TRANS_BLOCKS_PATTERN: Final = re.compile(
    r"""
      {%[ ]*?blocktranslate?\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*?endblocktranslate?[ ]*?%}
    | {%[ ]*?blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*?endblocktrans[ ]*?%}
    """,
    RE_FLAGS_ISX,
    cache_pattern=False,
)
_TRANS_TRIMMED_BLOCKS_PATTERN: Final = re.compile(
    r"""
      {%[ ]*?blocktranslate\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%}.*?{%[ ]*?endblocktranslate[ ]*?%}
    | {%[ ]*?blocktrans\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%}.*?{%[ ]*?endblocktrans[ ]*?%}
    """,
    RE_FLAGS_ISX,
    cache_pattern=False,
)
_IGNORED_TRANS_BLOCKS_CLOSING_PATTERN: Final = re.compile(
    r"""
    {%[ ]*?endblocktrans(?:late)?(?:(?!%}).)*?%}
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
# ignored block closing tags that
# we can safely indent.
_SAFE_CLOSING_TAG_PATTERN: Final = re.compile(
    r"""
      </script
    | </style
    | {\#\s*djlint\:\s*on\s*\#}
    | {%[ ]+?endcomment[ ]+?%}
    | {{!--\s*djlint\:on\s*--}}
    | {{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_SAFE_CLOSING_BLOCK_PATTERN: Final = re.compile(
    _IGNORED_INLINE_BLOCKS + r" | " + _IGNORED_BLOCKS,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_TEMPLATE_BLOCKS_PATTERN: Final = re.compile(
    r"""
    {%((?!%}).)+%}|{{((?!}}).)+}}
    """,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_OPTIONAL_SINGLE_LINE_HTML_PATTERN: Final = re.compile(
    rf"^(?:{_OPTIONAL_SINGLE_LINE_HTML_TAGS})$",
    RE_FLAGS_IX,
    cache_pattern=False,
)
_OPTIONAL_SINGLE_LINE_TEMPLATE_PATTERN: Final = re.compile(
    rf"^(?:{_OPTIONAL_SINGLE_LINE_TEMPLATE_TAGS})$",
    RE_FLAGS_IX,
    cache_pattern=False,
)


@final
class Config:
    """Djlint Config."""

    __slots__ = (
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
        "ignore",
        "ignore_blocks",
        "ignore_case",
        "ignored_attributes",
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
        "line_break_after_multiline_tag",
        "lint",
        "linter_output_format",
        "linter_rules",
        "max_attribute_length",
        "max_blank_lines",
        "max_line_length",
        "no_function_formatting",
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
        "reformat",
        "require_pragma",
        "safe_closing_block_pattern",
        "safe_closing_tag_pattern",
        "script_style_closing_pattern",
        "script_style_inline_imsx_pattern",
        "script_style_inline_ix_pattern",
        "script_style_opening_pattern",
        "single_attribute_per_line",
        "start_template_tags",
        "statistics",
        "stdin",
        "tag_indent",
        "tag_unindent",
        "tag_unindent_line",
        "template_blocks_pattern",
        "template_indent",
        "template_tags",
        "template_unindent",
        "trans_trimmed_blocks_pattern",
        "unformatted_blocks_coarse_pattern",
        "unformatted_blocks_pattern",
        "use_gitignore",
        "warn",
    )

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
        warn: bool = False,
        preserve_leading_space: bool = False,
        preserve_blank_lines: bool = False,
        preserve_class_newlines: bool = False,
        format_css: bool = False,
        format_js: bool = False,
        configuration: Path | None = None,
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
        no_function_formatting: bool = False,
        no_set_formatting: bool = False,
        max_blank_lines: int | None = None,
        github_output: bool = False,
        stdin: bool | None = None,
    ) -> None:
        self.project_root = find_project_root(
            Path.cwd() if src == "-" else Path(src).resolve()
        )
        djlint_settings = load_project_settings(
            self.project_root, configuration
        )
        self.gitignore = load_gitignore(self.project_root)

        def setting_int(key: str, default: int) -> int:
            """Read an integer option from the config file."""
            try:
                return int(djlint_settings.get(key, default))
            except ValueError:
                echo(
                    style(
                        f"Error: Invalid pyproject.toml {key} value"
                        f" {djlint_settings[key]}",
                        fg="red",
                    ),
                    err=True,
                )
                return default

        # command line only options
        self.reformat = reformat
        self.check = check
        self.lint = lint
        self.warn = warn
        self.github_output = github_output
        self.statistics = statistics

        # simple options; the command line takes precedence over the config
        self.extension = str(
            extension or djlint_settings.get("extension", "html")
        )
        self.quiet = quiet or djlint_settings.get("quiet", False)
        self.require_pragma = (
            require_pragma
            or str(djlint_settings.get("require_pragma", "false")).lower()
            == "true"
        )
        self.preserve_leading_space = (
            preserve_leading_space
            or djlint_settings.get("preserve_leading_space", False)
        )
        self.preserve_blank_lines = preserve_blank_lines or djlint_settings.get(
            "preserve_blank_lines", False
        )
        self.preserve_class_newlines = (
            preserve_class_newlines
            or djlint_settings.get("preserve_class_newlines", False)
        )
        self.format_js = format_js or djlint_settings.get("format_js", False)
        self.format_css = format_css or djlint_settings.get("format_css", False)
        self.ignore_case = ignore_case or djlint_settings.get(
            "ignore_case", False
        )
        self.close_void_tags = close_void_tags or djlint_settings.get(
            "close_void_tags", False
        )
        self.no_line_after_yaml = no_line_after_yaml or djlint_settings.get(
            "no_line_after_yaml", False
        )
        self.no_set_formatting = no_set_formatting or djlint_settings.get(
            "no_set_formatting", False
        )
        self.no_function_formatting = (
            no_function_formatting
            or djlint_settings.get("no_function_formatting", False)
        )
        self.format_attribute_template_tags = (
            format_attribute_template_tags
            or djlint_settings.get("format_attribute_template_tags", False)
        )
        self.single_attribute_per_line = (
            single_attribute_per_line
            or djlint_settings.get("single_attribute_per_line", False)
        )
        self.format_attribute_js_json = (
            format_attribute_js_json
            or djlint_settings.get("format_attribute_js_json", False)
        )
        self.format_attribute_js_json_min_props = (
            format_attribute_js_json_min_props
            if format_attribute_js_json_min_props is not None
            else setting_int("format_attribute_js_json_min_props", 2)
        )
        self.linter_output_format = linter_output_format or djlint_settings.get(
            "linter_output_format", "{code} {line} {message} {match}"
        )
        self.per_file_ignores = (
            dict(per_file_ignores)
            if per_file_ignores
            else djlint_settings.get("per-file-ignores", {})
        )
        # add blank line after load tags
        self.blank_line_after_tag = blank_line_after_tag or djlint_settings.get(
            "blank_line_after_tag", None
        )
        # add blank line before load tags
        self.blank_line_before_tag = (
            blank_line_before_tag
            or djlint_settings.get("blank_line_before_tag", None)
        )
        # add line break after multi-line tags
        self.line_break_after_multiline_tag = (
            line_break_after_multiline_tag
            or djlint_settings.get("line_break_after_multiline_tag", False)
        )
        self.js_config = (
            {"indent_size": indent_js}
            if indent_js
            else djlint_settings.get("js")
        ) or {}
        self.css_config = (
            {"indent_size": indent_css}
            if indent_css
            else djlint_settings.get("css")
        ) or {}

        indent = indent or setting_int("indent", 4)
        self.indent_size = indent
        self.indent = indent * " "
        self.max_line_length = max_line_length or setting_int(
            "max_line_length", 120
        )
        self.max_attribute_length = (
            max_attribute_length
            if max_attribute_length is not None
            else setting_int("max_attribute_length", 70)
        )
        self.max_blank_lines = (
            max_blank_lines
            if max_blank_lines is not None
            else setting_int("max_blank_lines", 0)
        )

        # regex for excluded paths
        exclude = build_exclude(
            exclude or djlint_settings.get("exclude", _DEFAULT_EXCLUDE)
        )
        extend_exclude = extend_exclude or djlint_settings.get(
            "extend_exclude", ""
        )
        if extend_exclude:
            exclude += r" | " + build_exclude(extend_exclude)
        self.exclude = exclude
        self.exclude_pattern = re.compile(
            rf"(?:^|/)(?:{exclude})(?=$|/|(?<=/))", re.X, cache_pattern=False
        )

        self.files = djlint_settings.get("files", None)
        self.stdin = (src == "-" if stdin is None else stdin) and not self.files
        self.use_gitignore = (
            use_gitignore or bool(djlint_settings.get("use_gitignore", False))
        ) and not self.stdin

        # linter rules, minus the ignored codes and the profile's excludes
        self.profile = str(
            profile or djlint_settings.get("profile", "all")
        ).lower()
        profile_codes = _PROFILE_CODES.get(
            str(profile or djlint_settings.get("profile", "html")).lower(), ()
        )
        self.ignore = str(ignore or djlint_settings.get("ignore", ""))
        self.include = str(include or djlint_settings.get("include", ""))
        rule_set = validate_rules(
            chain(
                yaml.safe_load(
                    (Path(__file__).parent / "rules.yaml").read_text(
                        encoding="utf-8"
                    )
                ),
                load_custom_rules(self.project_root),
            )
        )
        self.linter_rules = tuple(
            x
            for x in rule_set
            if x["rule"]["name"] not in self.ignore.split(",")
            and not any(
                x["rule"]["name"].startswith(code) for code in profile_codes
            )
            and self.profile not in x["rule"].get("exclude", set())
            and (
                x["rule"].get("default", True)
                or x["rule"]["name"] in self.include.split(",")
            )
        )

        # patterns built from configuration options
        self.custom_blocks = str(
            build_custom_blocks(
                custom_blocks or djlint_settings.get("custom_blocks")
            )
            or ""
        )
        # django-cotton component tags (<c-name>, <c-folder.name>) are
        # treated as block html tags out of the box.
        self.custom_html = (
            str(
                build_custom_html(
                    custom_html or djlint_settings.get("custom_html")
                )
                or ""
            )
            + r"|c-[\w.-]+"
        )
        self.ignore_blocks = build_ignore_blocks(
            ignore_blocks or djlint_settings.get("ignore_blocks", "")
        )
        ignore_blocks_guard = (
            rf"(?!{self.ignore_blocks})" if self.ignore_blocks else ""
        )
        self.format_attribute_js_json_pattern = re.compile(
            format_attribute_js_json_pattern
            or djlint_settings.get(
                "format_attribute_js_json_pattern", _DEFAULT_JS_JSON_PATTERN
            ),
            RE_FLAGS_IX,
            cache_pattern=False,
        )

        # all html tags possible
        self.indent_html_tags = "|".join(HTML_TAG_NAMES) + self.custom_html
        self.always_self_closing_html_tags = _ALWAYS_SELF_CLOSING_HTML_TAGS

        self.template_indent = (
            r"""
            (?:\{\{\#|\{%-?)[ ]*?
                ("""
            + ignore_blocks_guard
            + _INDENT_TEMPLATE_TAGS
            + self.custom_blocks
            + r")\b"
            + r"""
            ) | \{{-?[ ]*?form_start
            """
        )
        # jinja/twig block {% trans %} has no matching indent tag, so its
        # end tag must not unindent — unless the user made trans a custom
        # block, in which case the open tag does indent.
        end_tag_guard = r"(?!comment)"
        if (
            r"|trans\b" not in self.custom_blocks
            and r"|translate\b" not in self.custom_blocks
        ):
            end_tag_guard = r"(?!comment|trans(?:late)?\b)"
        self.template_unindent = (
            r"""
                (?:
                  (?:\{\{\/)
                | (?:\{%-?[ ]*?end"""
            + end_tag_guard
            + ignore_blocks_guard
            + r""")
                | (?:\{{-?[ ]*?form_end)
              )
            """
        )
        self.start_template_tags = (
            ignore_blocks_guard
            + _START_TEMPLATE_TAGS
            + self.custom_blocks
            + r""")
        """
        )
        self.break_template_tags = (
            ignore_blocks_guard
            + _BREAK_TEMPLATE_TAGS
            + self.custom_blocks
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
        # the contents of these tag blocks will be indented, then unindented
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
        """
        )
        # either a template tag at the start of a line,
        # a html tag at the start of a line,
        # or an html tag as the end of a line.
        # Nothing in between!
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
            | (?:</
                (?:
                    """
            + self.indent_html_tags
            + """
                )>$
              )
        """
        )

        # static patterns, built once at module import
        self.attribute_pattern = _ATTRIBUTE_PATTERN
        self.template_tags = _TEMPLATE_TAGS
        self.tag_unindent_line = _TAG_UNINDENT_LINE
        self.break_before = _BREAK_BEFORE
        self.ignored_attributes = _IGNORED_ATTRIBUTES
        self.ignored_inline_blocks = _IGNORED_INLINE_BLOCKS
        self.optional_single_line_html_tags = _OPTIONAL_SINGLE_LINE_HTML_TAGS
        self.optional_single_line_template_tags = (
            _OPTIONAL_SINGLE_LINE_TEMPLATE_TAGS
        )
        self.format_attribute_js_json_object_pattern = _JS_JSON_OBJECT_PATTERN
        self.format_attribute_js_json_string_pattern = _JS_JSON_STRING_PATTERN
        self.format_attribute_js_json_property_pattern = (
            _JS_JSON_PROPERTY_PATTERN
        )
        self.script_style_opening_pattern = _SCRIPT_STYLE_OPENING_PATTERN
        self.script_style_closing_pattern = _SCRIPT_STYLE_CLOSING_PATTERN
        self.script_style_inline_imsx_pattern = (
            _SCRIPT_STYLE_INLINE_IMSX_PATTERN
        )
        self.script_style_inline_ix_pattern = _SCRIPT_STYLE_INLINE_IX_PATTERN
        self.ignored_block_opening_pattern = _IGNORED_BLOCK_OPENING_PATTERN
        self.ignored_block_closing_pattern = _IGNORED_BLOCK_CLOSING_PATTERN
        self.ignored_blocks_pattern = _IGNORED_BLOCKS_PATTERN
        self.ignored_blocks_inline_pattern = _IGNORED_BLOCKS_INLINE_PATTERN
        self.ignored_inline_blocks_ix_pattern = (
            _IGNORED_INLINE_BLOCKS_IX_PATTERN
        )
        self.ignored_linter_blocks_pattern = _IGNORED_LINTER_BLOCKS_PATTERN
        self.ignored_trans_blocks_pattern = _IGNORED_TRANS_BLOCKS_PATTERN
        self.ignored_trans_blocks_closing_pattern = (
            _IGNORED_TRANS_BLOCKS_CLOSING_PATTERN
        )
        self.trans_trimmed_blocks_pattern = _TRANS_TRIMMED_BLOCKS_PATTERN
        self.safe_closing_block_pattern = _SAFE_CLOSING_BLOCK_PATTERN
        self.safe_closing_tag_pattern = _SAFE_CLOSING_TAG_PATTERN
        self.template_blocks_pattern = _TEMPLATE_BLOCKS_PATTERN
        self.unformatted_blocks_coarse_pattern = (
            _UNFORMATTED_BLOCKS_COARSE_PATTERN
        )
        self.unformatted_blocks_pattern = _UNFORMATTED_BLOCKS_PATTERN
        self.ignored_rule_patterns = _IGNORED_RULE_PATTERNS
        self.optional_single_line_html_pattern = (
            _OPTIONAL_SINGLE_LINE_HTML_PATTERN
        )
        self.optional_single_line_template_pattern = (
            _OPTIONAL_SINGLE_LINE_TEMPLATE_PATTERN
        )
