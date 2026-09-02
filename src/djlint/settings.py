"""Settings for reformater."""

from __future__ import annotations

import json
import sys
from fnmatch import fnmatch
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

import regex as re
import yaml
from click import BadParameter, UsageError, echo, style
from pathspec import PathSpec

from djlint.const import HTML_TAG_NAMES, HTML_VOID_ELEMENTS
from djlint.helpers import (
    RE_FLAGS_IMSX,
    RE_FLAGS_IMX,
    RE_FLAGS_ISX,
    RE_FLAGS_IX,
    YAML_FRONT_MATTER,
    split_option_list,
)
from djlint.lint import build_flags

try:
    from pathspec.patterns.gitignore import GitIgnorePatternError
except ImportError:
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

_QUOTE_STYLES: Final = frozenset(("double", "single"))


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


def _editorconfig_glob_matches_html(glob: str, extension: str) -> bool:
    """Whether an .editorconfig section applies to template files.

    One level of {a,b} alternation is expanded before matching.
    """
    if glob == "*":
        return True
    globs = [glob]
    if "{" in glob and "}" in glob:
        head, _, rest = glob.partition("{")
        body, _, tail = rest.partition("}")
        globs = [head + alt + tail for alt in body.split(",")]
    names = (f"test.{extension}", "test.html")
    return any(
        fnmatch(name, g.lstrip("*").lstrip("/") if g.startswith("**") else g)
        for g in globs
        for name in names
    )


def load_editorconfig(root: Path, extension: str) -> dict[str, int]:
    """Read indent_size and max_line_length from a root .editorconfig.

    Used as defaults only: the command line and djlint config files take
    precedence. Sections are considered when their glob applies to html
    or the configured extension.
    """
    path = root / ".editorconfig"
    result: dict[str, int] = {}
    if not path.is_file():
        return result

    section_applies = False
    for raw_line in path.read_text(
        encoding="utf-8", errors="ignore"
    ).splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            section_applies = _editorconfig_glob_matches_html(
                line[1:-1], extension
            )
            continue
        key, sep, value = line.partition("=")
        if sep and section_applies:
            key, value = key.strip().lower(), value.strip()
            if key in {"indent_size", "max_line_length"} and value.isdigit():
                result[key] = int(value)
    return result


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


def load_custom_rules(rules_file: Path | None) -> Any:
    """Load custom linter rules from a .djlint_rules.yaml file."""
    if rules_file:
        with rules_file.open("rb") as f:
            return yaml.safe_load(f)

    return ()


def _as_comma_separated(value: Any) -> Any:
    """Allow comma-separated config options to be given as lists."""
    if isinstance(value, (list, tuple)):
        return ",".join(str(x).strip() for x in value)
    return value


def _build_block_alternation(tags: Iterable[str]) -> str:
    return "|".join(
        sorted(
            chain.from_iterable((rf"{tag}\b", rf"end{tag}\b") for tag in tags)
        )
    )


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


def build_exclude(exclude: str) -> str:
    """Build regex string for exclude paths."""
    if "," not in exclude:
        return exclude
    return r" | ".join(split_option_list(exclude))


_CODES_EXCLUDED_BY_PROFILE: Final[dict[str, tuple[str, ...]]] = {
    "html": ("D", "J", "T", "N", "M"),
    "django": ("J", "N", "M"),
    "jinja": ("D", "N", "M"),
    "askama": ("D", "J", "N", "M"),
    "tera": ("D", "J", "N", "M"),
    "liquid": ("D", "J", "N", "M"),
    "nunjucks": ("D", "J", "M"),
    "handlebars": ("D", "J", "N"),
    "golang": ("D", "J", "N", "M"),
    "angular": ("D", "J", "H012", "H026", "H028"),
}

_PROFILES: Final[frozenset[str]] = frozenset(_CODES_EXCLUDED_BY_PROFILE) | {
    "all"
}

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

_ATTRIBUTE_X_PATTERN: Final = re.compile(
    _ATTRIBUTE_PATTERN, re.X, cache_pattern=False
)

_TEMPLATE_TAGS: Final = r"""
    {{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}
"""
_TEMPLATE_TAGS_IMX_PATTERN: Final = re.compile(
    _TEMPLATE_TAGS, RE_FLAGS_IMX, cache_pattern=False
)

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

_IGNORED_INLINE_BLOCKS_TAIL: Final = r"""
      <!--.*?-->
    | {\*.*?\*}
    | (?<!\{){\#(?!.*djlint:[ ]*(?:off|on)\b).*\#}
    | <\?php.*?\?>
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
_LINT_IGNORED_INLINE_BLOCKS: Final = _build_ignored_inline_blocks(
    for_linting=True
)

_IGNORED_BLOCKS_TAIL: Final = (
    r"""
    # html comment
    | <!--\s*djlint\:off\s*-->.(?:(?!<!--\s*djlint\:on\s*-->).)*
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


_RAW_TEXT_OPENING_TAG: Final = r"""(?:\"[^\"]*\"|'[^']*'|[^>\"'])*>"""


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
_RAW_TEXT_OPENING_PATTERN: Final = re.compile(
    r"""
      <style
    | <script
    | <pre
    | <textarea
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_RAW_TEXT_CLOSING_PATTERN: Final = re.compile(
    r"""
      </style
    | </script
    | </pre
    | </textarea
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_RAW_TEXT_INLINE_IMSX_PATTERN: Final = re.compile(
    _RAW_TEXT_INLINE, RE_FLAGS_IMSX, cache_pattern=False
)
_RAW_TEXT_INLINE_IX_PATTERN: Final = re.compile(
    _RAW_TEXT_INLINE, RE_FLAGS_IX, cache_pattern=False
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
    | {%[ ]*blocktrans(?:late)?(?:(?!%}|\btrimmed\b).)*?%}
    | {%[-+]?[ ]*(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
    | {%[ ]*filter\b(?:(?!%}).)*?%}
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
    # a "-->" reachable without crossing the start of a raw text element.
    # Past one, markup is text: "<pre>&lt;!-- x -->" closes no comment.
    | ^(?:(?!<pre\b|<textarea\b).)*?-->
    | ^(?:(?!{\#).)*\#} # lines that have a #}, but not a {#
    | </pre
    | </textarea
    | {%[ ]*endfilter(?:(?!%}).)*?%}
    | {\#\s*djlint\:\s*on\s*\#}
    | (?<!djlint:off\s*?){%[ ]+?endcomment[ ]+?%}
    | {{!--\s*djlint\:on\s*--}}
    | {{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}
    | {%[ ]*endblocktrans(?:late)?(?:(?!%}).)*?%}
    | {%[-+]?[ ]*end(?:schema|javascript|stylesheet|style)[ ]*[-+]?%}
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
_IGNORED_BLOCKS_PATTERN: Final = re.compile(
    _IGNORED_BLOCKS, RE_FLAGS_IMSX, cache_pattern=False
)
_LINT_IGNORED_BLOCKS_PATTERN: Final = re.compile(
    _LINT_IGNORED_BLOCKS, RE_FLAGS_IMSX, cache_pattern=False
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
    | {%[ ]*filter\b(?:(?!%}).)*?%}.*?{%[ ]*endfilter[ ]*%}
    | {%[ ]*blocktranslate\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktranslate[ ]*%}
    | {%[ ]*blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktrans[ ]*%}
    | {%[ ]*comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*endcomment[ ]*%})
    |"""
    + YAML_FRONT_MATTER,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_IGNORED_INLINE_BLOCKS_IX_PATTERN: Final = re.compile(
    _IGNORED_INLINE_BLOCKS, RE_FLAGS_IX, cache_pattern=False
)
_LINT_IGNORED_INLINE_BLOCKS_IX_PATTERN: Final = re.compile(
    _LINT_IGNORED_INLINE_BLOCKS, RE_FLAGS_IX, cache_pattern=False
)
_IGNORED_LINTER_BLOCKS_PATTERN: Final = re.compile(
    r"""
    {%[-+]?[ ]*(raw|verbatim)\b(?:(?!%}).)*?[-+]?%}.*?{%[-+]?[ ]*end\1[ ]*[-+]?%}
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
      <!--\s*djlint\:off\s*-->.(?:(?!<!--\s*djlint\:on\s*-->).)*
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
    + YAML_FRONT_MATTER,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_IGNORED_RULE_PATTERNS: Final = tuple(
    re.compile(pattern, RE_FLAGS_ISX, cache_pattern=False)
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
_IGNORED_TRANS_BLOCKS_PATTERN: Final = re.compile(
    r"""
      {%[ ]*blocktranslate?\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktranslate?[ ]*%}
    | {%[ ]*blocktrans\b(?:(?!%}|\btrimmed\b).)*?%}.*?{%[ ]*endblocktrans[ ]*%}
    """,
    RE_FLAGS_ISX,
    cache_pattern=False,
)
_TRANS_TRIMMED_BLOCKS_PATTERN: Final = re.compile(
    r"""
      {%[ ]*blocktranslate\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%}.*?{%[ ]*endblocktranslate[ ]*%}
    | {%[ ]*blocktrans\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%}.*?{%[ ]*endblocktrans[ ]*%}
    """,
    RE_FLAGS_ISX,
    cache_pattern=False,
)
_IGNORED_TRANS_BLOCKS_CLOSING_PATTERN: Final = re.compile(
    r"""
    {%[ ]*endblocktrans(?:late)?(?:(?!%}).)*?%}
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)
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
        "no_entity_formatting",
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
        "quote_style",
        "raw_text_closing_pattern",
        "raw_text_inline_imsx_pattern",
        "raw_text_inline_ix_pattern",
        "raw_text_opening_pattern",
        "reformat",
        "require_pragma",
        "safe_closing_block_pattern",
        "safe_closing_tag_pattern",
        "single_attribute_per_line",
        "single_line_template_tags",
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
        keep_br_inline: bool = False,
        no_entity_formatting: bool = False,
        no_function_formatting: bool = False,
        no_set_formatting: bool = False,
        quote_style: str | None = None,
        max_blank_lines: int | None = None,
        github_output: bool = False,
        stdin: bool | None = None,
        stdin_filename: str | None = None,
    ) -> None:
        self.project_root = find_project_root(
            Path.cwd() if src == "-" else Path(src).resolve()
        )
        djlint_settings = load_project_settings(
            self.project_root, configuration
        )

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

        self.reformat = reformat
        self.check = check
        self.lint = lint
        self.warn = warn
        self.github_output = github_output
        self.statistics = statistics
        self.stdin_filename = stdin_filename

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
        selected_profile = str(
            profile or djlint_settings.get("profile", "")
        ).lower()
        expressions_are_rust = selected_profile == "askama"
        self.no_set_formatting = (
            no_set_formatting
            or djlint_settings.get("no_set_formatting", False)
            or expressions_are_rust
        )
        self.no_function_formatting = (
            no_function_formatting
            or djlint_settings.get("no_function_formatting", False)
            or expressions_are_rust
        )
        self.no_entity_formatting = no_entity_formatting or djlint_settings.get(
            "no_entity_formatting", False
        )
        self.keep_br_inline = keep_br_inline or djlint_settings.get(
            "keep_br_inline", False
        )
        self.quote_style = str(
            quote_style or djlint_settings.get("quote_style", "double")
        ).lower()
        if self.quote_style not in _QUOTE_STYLES:
            msg = (
                f"Invalid quote style {self.quote_style!r}."
                f" Choose from {', '.join(sorted(_QUOTE_STYLES))}."
            )
            raise BadParameter(msg, param_hint="'--quote-style'")
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
        self.blank_line_after_tag = blank_line_after_tag or _as_comma_separated(
            djlint_settings.get("blank_line_after_tag", None)
        )
        self.blank_line_before_tag = (
            blank_line_before_tag
            or _as_comma_separated(
                djlint_settings.get("blank_line_before_tag", None)
            )
        )
        self.line_break_after_multiline_tag = (
            line_break_after_multiline_tag
            or djlint_settings.get("line_break_after_multiline_tag", False)
        )
        self.js_config = _beautifier_config(
            djlint_settings.get("js"), indent_size=indent_js
        )
        self.css_config = _beautifier_config(
            djlint_settings.get("css"), indent_size=indent_css
        )

        editorconfig = load_editorconfig(self.project_root, self.extension)
        indent = indent or setting_int(
            "indent", editorconfig.get("indent_size", 4)
        )
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
            max_blank_lines
            if max_blank_lines is not None
            else setting_int("max_blank_lines", 0)
        )

        exclude = build_exclude(
            exclude
            or _as_comma_separated(
                djlint_settings.get("exclude", _DEFAULT_EXCLUDE)
            )
        )
        extend_exclude = extend_exclude or _as_comma_separated(
            djlint_settings.get("extend_exclude", "")
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
        self.gitignore = (
            load_gitignore(self.project_root)
            if self.use_gitignore
            else PathSpec([])
        )
        self.allow_empty_input = allow_empty_input or bool(
            djlint_settings.get("allow_empty_input", False)
        )

        self.profile = selected_profile or "all"
        if self.profile not in _PROFILES:
            msg = (
                f"Invalid profile {self.profile!r}."
                f" Choose from {', '.join(sorted(_PROFILES))}."
            )
            raise BadParameter(msg, param_hint="'--profile'")
        profile_codes = _CODES_EXCLUDED_BY_PROFILE.get(
            selected_profile or "html", ()
        )
        self.ignore = str(
            ignore or _as_comma_separated(djlint_settings.get("ignore", ""))
        )
        self.include = str(
            include or _as_comma_separated(djlint_settings.get("include", ""))
        )
        with (Path(__file__).parent / "rules.yaml").open("rb") as f:
            default_rules = yaml.safe_load(f)
        rule_set = tuple(
            validate_rules(
                chain(
                    default_rules,
                    load_custom_rules(
                        rules or find_djlint_rules(self.project_root)
                    ),
                )
            )
        )
        ignored_codes = set(split_option_list(self.ignore))
        included_codes = set(split_option_list(self.include))
        if self.ignore_case:
            ignored_codes.update(("H009", "H010"))

        def rule_applies(rule: Mapping[str, Any]) -> bool:
            """Whether the rule runs under the profile in force.

            "all" is every template language at once, so a rule excluded
            for any one of them cannot be trusted under it either.
            """
            excluded_profiles = rule.get("exclude", ())
            if excluded_profiles and (
                self.profile == "all" or self.profile in excluded_profiles
            ):
                return False
            return not any(
                rule["name"].startswith(code) for code in profile_codes
            )

        self.entity_pattern = next(
            (
                re.compile(
                    x["rule"]["patterns"][0],
                    build_flags(x["rule"].get("flags", "re.S")),
                )
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
            and (
                x["rule"].get("default", True)
                or x["rule"]["name"] in included_codes
            )
        )
        if self.lint:
            enabled_rules = {x["rule"]["name"] for x in self.linter_rules}
            if {"H017", "H018"} <= enabled_rules:
                echo(
                    style(
                        "Warning: H017 and H018 enforce opposite void tag"
                        " styles. Enable only one convention. 😢",
                        fg="yellow",
                    ),
                    err=True,
                )

        self.custom_blocks = str(
            build_custom_blocks(
                ",".join(
                    x
                    for x in (
                        str(
                            custom_blocks
                            or _as_comma_separated(
                                djlint_settings.get("custom_blocks")
                            )
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
                    custom_html
                    or _as_comma_separated(djlint_settings.get("custom_html"))
                )
                or ""
            )
            + django_cotton_components
        )
        self.ignore_blocks = build_ignore_blocks(
            ignore_blocks
            or _as_comma_separated(djlint_settings.get("ignore_blocks", ""))
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

        self.indent_html_tags = "|".join(HTML_TAG_NAMES) + self.custom_html
        self.always_self_closing_html_tags = _ALWAYS_SELF_CLOSING_HTML_TAGS

        not_self_closed = r"\b(?!(?:(?!%\}).)*/\s*-?%\})"
        custom_block_openers = self.custom_blocks.replace(
            r"\b", not_self_closed
        )
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
            r"|trans\b" in self.custom_blocks
            or r"|translate\b" in self.custom_blocks
        )
        end_tag_guard = (
            r"(?!comment)"
            if trans_is_a_custom_block
            else r"(?!comment|trans(?:late)?\b)"
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
            ignore_blocks_guard
            + _INDENT_TEMPLATE_TAGS
            + custom_block_openers
            + r")"
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
            | (?:</
                (?:
                    """
            + self.indent_html_tags
            + """
                )>$
              )
        """
        )

        self.template_indent_ix_pattern = re.compile(
            self.template_indent, RE_FLAGS_IX, cache_pattern=False
        )
        self.template_indent_imx_pattern = re.compile(
            self.template_indent, RE_FLAGS_IMX, cache_pattern=False
        )
        self.template_unindent_ix_pattern = re.compile(
            self.template_unindent, RE_FLAGS_IX, cache_pattern=False
        )
        self.template_unindent_imx_pattern = re.compile(
            self.template_unindent, RE_FLAGS_IMX, cache_pattern=False
        )

        self.attribute_pattern = _ATTRIBUTE_X_PATTERN
        self.template_tags = _TEMPLATE_TAGS
        self.template_tags_imx_pattern = _TEMPLATE_TAGS_IMX_PATTERN
        self.tag_unindent_line = (
            _LIQUID_TAG_UNINDENT_LINE
            if self.profile == "liquid"
            else _TAG_UNINDENT_LINE
        )
        if is_golang:
            self.tag_unindent_line += _GOLANG_BRANCH
        self.tag_unindent_line_ix_pattern = re.compile(
            self.tag_unindent_line, RE_FLAGS_IX, cache_pattern=False
        )
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
        self.raw_text_opening_pattern = _RAW_TEXT_OPENING_PATTERN
        self.raw_text_closing_pattern = _RAW_TEXT_CLOSING_PATTERN
        self.raw_text_inline_imsx_pattern = _RAW_TEXT_INLINE_IMSX_PATTERN
        self.raw_text_inline_ix_pattern = _RAW_TEXT_INLINE_IX_PATTERN
        self.ignored_block_opening_pattern = _IGNORED_BLOCK_OPENING_PATTERN
        self.ignored_block_closing_pattern = _IGNORED_BLOCK_CLOSING_PATTERN
        self.ignored_blocks_pattern = _IGNORED_BLOCKS_PATTERN
        self.lint_ignored_blocks_pattern = _LINT_IGNORED_BLOCKS_PATTERN
        self.ignored_blocks_inline_pattern = _IGNORED_BLOCKS_INLINE_PATTERN
        self.ignored_inline_blocks_ix_pattern = (
            _IGNORED_INLINE_BLOCKS_IX_PATTERN
        )
        self.lint_ignored_inline_blocks_ix_pattern = (
            _LINT_IGNORED_INLINE_BLOCKS_IX_PATTERN
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
        if profile_blocks := _PROFILE_ONLY_BLOCKS.get(self.profile):
            self.optional_single_line_template_tags += "|" + "|".join(
                split_option_list(profile_blocks)
            )
            self.optional_single_line_template_pattern = re.compile(
                rf"^(?:{self.optional_single_line_template_tags})$",
                RE_FLAGS_IX,
                cache_pattern=False,
            )
