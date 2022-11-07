"""Settings for reformater."""
# pylint: disable=C0301,C0103
# flake8: noqa


import json
import logging

## get pyproject.toml settings
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from click import echo
from colorama import Fore
from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore

logger = logging.getLogger(__name__)


def find_project_root(src: Path) -> Path:
    """Attempt to get the project root."""
    for directory in [src, *src.resolve().parents]:

        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

        if (directory / ".djlintrc").is_file():
            return directory

    # pylint: disable=W0631
    return directory


def load_gitignore(root: Path) -> PathSpec:
    """Search upstream for a .gitignore file."""

    gitignore = root / ".gitignore"
    git_lines: List[str] = []
    if gitignore.is_file():
        with gitignore.open(encoding="utf-8") as this_file:
            git_lines = this_file.readlines()

    try:
        return PathSpec.from_lines("gitwildmatch", git_lines)

    except GitWildMatchPatternError as e:
        echo(f"Could not parse {gitignore}: {e}", err=True)
        raise


def find_pyproject(root: Path) -> Optional[Path]:
    """Search upstream for a pyproject.toml file."""

    pyproject = root / "pyproject.toml"

    if pyproject.is_file():
        return pyproject

    return None


def find_djlintrc(root: Path) -> Optional[Path]:
    """Search upstream for a pyproject.toml file."""

    djlintrc = root / ".djlintrc"

    if djlintrc.is_file():
        return djlintrc

    return None


def find_djlint_rules(root: Path) -> Optional[Path]:
    """Search upstream for a pyproject.toml file."""

    rules = root / ".djlint_rules.yaml"

    if rules.is_file():
        return rules

    return None


def load_project_settings(src: Path, config: Optional[str]) -> Dict:
    """Load djlint config from pyproject.toml."""

    djlint_content: Dict = {}

    if config:
        try:
            djlint_content = json.loads(
                Path(config).resolve().read_text(encoding="utf8")
            )

        # pylint: disable=broad-except
        except BaseException:
            logger.info(
                "Failed to load config file. Ensure file exists and is in json format."
            )

    pyproject_file = find_pyproject(src)

    if pyproject_file:
        content = tomllib.load(pyproject_file.open("rb"))
        try:
            return {**djlint_content, **content["tool"]["djlint"]}  # type: ignore
        except KeyError:
            logger.info("No pyproject.toml found.")

    djlintrc_file = find_djlintrc(src)

    if djlintrc_file:
        try:
            return {
                **djlint_content,
                **json.loads(djlintrc_file.read_text(encoding="utf8")),
            }
        # pylint: disable=broad-except
        except BaseException:
            logger.info("Failed to load .djlintrc file.")

    return djlint_content


def validate_rules(rules: List) -> List:
    """Validate a list of linter rules. Returns valid rules."""
    clean_rules = []

    for rule in rules:
        # check for name
        warning = 0
        name = rule["rule"].get("name", "undefined")
        if "name" not in rule["rule"]:
            warning += 1
            echo(Fore.RED + "Warning: A rule is missing a name! 😢")
        if "patterns" not in rule["rule"]:
            warning += 1
            echo(Fore.RED + f"Warning: Rule {name} is missing a pattern! 😢")
        if "message" not in rule["rule"]:
            warning += 1
            echo(Fore.RED + f"Warning: Rule {name} is missing a message! 😢")

        if warning == 0:
            clean_rules.append(rule)

    return clean_rules


def load_custom_rules(src: Path) -> List:
    """Load djlint config from pyproject.toml."""

    djlint_content: List = []
    djlint_rules_file = find_djlint_rules(src)

    if djlint_rules_file:
        djlint_content = yaml.load(
            Path(djlint_rules_file).read_text(encoding="utf8"),
            Loader=yaml.SafeLoader,
        )

    return djlint_content


def build_custom_blocks(custom_blocks: Union[str, None]) -> Optional[str]:
    """Build regex string for custom template blocks."""
    if custom_blocks:
        return "|" + "|".join(x.strip() for x in custom_blocks.split(","))
    return None


def build_custom_html(custom_html: Union[str, None]) -> Optional[str]:
    """Build regex string for custom HTML blocks."""
    if custom_html:
        return "|" + "|".join(x.strip() for x in custom_html.split(","))
    return None


class Config:
    """Djlint Config."""

    def __init__(
        self,
        src: str,
        ignore: Optional[str] = None,
        extension: Optional[str] = None,
        indent: Optional[int] = None,
        quiet: bool = False,
        profile: Optional[str] = None,
        require_pragma: bool = False,
        reformat: bool = False,
        check: bool = False,
        lint: bool = False,
        use_gitignore: bool = False,
        warn: bool = False,
        preserve_leading_space: bool = False,
        preserve_blank_lines: bool = False,
        format_css: bool = False,
        format_js: bool = False,
        configuration: Optional[str] = None,
        statistics: bool = False,
    ):

        self.reformat = reformat
        self.check = check
        self.lint = lint
        self.warn = warn

        if src == "-":
            self.project_root = find_project_root(Path.cwd())
        else:
            self.project_root = find_project_root(Path(src))

        djlint_settings = load_project_settings(self.project_root, configuration)

        self.gitignore = load_gitignore(self.project_root)
        # custom configuration options

        self.use_gitignore: bool = use_gitignore or djlint_settings.get(
            "use_gitignore", False
        )
        self.extension: str = str(extension or djlint_settings.get("extension", "html"))
        self.quiet: bool = quiet or djlint_settings.get("quiet", False)
        self.require_pragma: bool = (
            require_pragma
            or str(djlint_settings.get("require_pragma", "false")).lower() == "true"
        )

        self.custom_blocks: str = str(
            build_custom_blocks(djlint_settings.get("custom_blocks")) or ""
        )

        self.custom_html: str = str(
            build_custom_html(djlint_settings.get("custom_html")) or ""
        )

        self.format_attribute_template_tags: bool = djlint_settings.get(
            "format_attribute_template_tags", False
        )

        self.preserve_leading_space: bool = (
            preserve_leading_space
            or djlint_settings.get("preserve_leading_space", False)
        )

        self.preserve_blank_lines: bool = preserve_blank_lines or djlint_settings.get(
            "preserve_blank_lines", False
        )

        self.format_js: bool = format_js or djlint_settings.get("format_js", False)

        self.js_config = djlint_settings.get("js")
        self.css_config = djlint_settings.get("css")

        self.format_css: bool = format_css or djlint_settings.get("format_css", False)

        # ignore is based on input and also profile
        self.ignore: str = str(ignore or djlint_settings.get("ignore", ""))

        self.files: Optional[List[str]] = djlint_settings.get("files", None)
        self.stdin = "-" in src and self.files is None

        # codes to exclude
        profile_dict: Dict[str, List[str]] = {
            "html": ["D", "J", "T", "N", "M"],
            "django": ["J", "N", "M"],
            "jinja": ["D", "N", "M"],
            "nunjucks": ["D", "J", "M"],
            "handlebars": ["D", "J", "N"],
            "golang": ["D", "J", "N", "M"],
            "angular": ["D", "J", "H012", "H026", "H028"],
        }

        self.profile_code: List[str] = profile_dict.get(
            str(profile or djlint_settings.get("profile", "html")).lower(), []
        )
        self.profile: str = str(
            profile or djlint_settings.get("profile", "all")
        ).lower()

        self.linter_output_format: str = djlint_settings.get(
            "linter_output_format", "{code} {line} {message} {match}"
        )

        # load linter rules
        rule_set = validate_rules(
            yaml.load(
                (Path(__file__).parent / "rules.yaml").read_text(encoding="utf8"),
                Loader=yaml.SafeLoader,
            )
            + load_custom_rules(self.project_root)
        )

        self.linter_rules = list(
            filter(
                lambda x: x["rule"]["name"] not in self.ignore.split(",")
                and not any(
                    x["rule"]["name"].startswith(code) for code in self.profile_code
                )
                and self.profile not in x["rule"].get("exclude", []),
                rule_set,
            )
        )

        self.statistics = statistics

        # base options
        default_indent = 4
        if not indent:
            try:
                indent = int(djlint_settings.get("indent", default_indent))
            except ValueError:
                echo(
                    Fore.RED
                    + f"Error: Invalid pyproject.toml indent value {djlint_settings['indent']}"
                )
                indent = default_indent
        self.indent: str = indent * " "

        default_exclude: str = r"""
            \.venv
            | venv/
            | \.tox
            | \.eggs
            | \.git
            | \.hg
            | \.mypy_cache
            | \.nox
            | \.svn
            | \.bzr
            | _build/
            | buck-out/
            | build/
            | dist/
            | \.pants\.d
            | \.direnv
            | node_modules/
            | __pypackages__
        """

        self.exclude: str = djlint_settings.get("exclude", default_exclude)

        extend_exclude: str = djlint_settings.get("extend_exclude", "")

        if extend_exclude:
            self.exclude += r" | " + r" | ".join(
                x.strip() for x in extend_exclude.split(",")
            )

        self.per_file_ignores = djlint_settings.get("per-file-ignores", {})

        # add blank line after load tags
        self.blank_line_after_tag: Optional[str] = djlint_settings.get(
            "blank_line_after_tag", None
        )

        # add blank line before load tags
        self.blank_line_before_tag: Optional[str] = djlint_settings.get(
            "blank_line_before_tag", None
        )

        # contents of tags will not be formatted
        self.ignored_block_opening: str = r"""
              <style
            | {\*
            | <\?php
            | <script
            | <!--
            | [^\{]{\#(?!\s*djlint\:\s*(?:on|off))
            | ^{\#(?!\s*djlint\:\s*(?:on|off))
            | <pre
            | <textarea
            | {%[ ]*?blocktrans(?:late)?[^(?:%})]*?%}
            | {\#\s*djlint\:\s*off\s*\#}
            | {%[ ]+?comment[ ]+?[^(?:%})]*?%}
            | {{!--\s*djlint\:off\s*--}}
            | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}
        """

        self.ignored_block_closing: str = r"""
              </style
            | \*}
            | \?>
            | </script
            |  -->
            | ^(?:(?!{\#).)*\#} # lines that have a #}, but not a {#
            | </pre
            | </textarea
            | {\#\s*djlint\:\s*on\s*\#}
            | {%[ ]+?endcomment[ ]+?%}
            | {{!--\s*djlint\:on\s*--}}
            | {{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}
            | {%[ ]*?endblocktrans(?:late)?[^(?:%})]*?%}
        """

        # ignored block closing tags that
        # we can safely indent.
        self.safe_closing_tag: str = r"""
              </script
            | </style
            | {\#\s*djlint\:\s*on\s*\#}
            | {%[ ]+?endcomment[ ]+?%}
            | {{!--\s*djlint\:on\s*--}}
            | {{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}
        """

        # all html tags possible
        self.indent_html_tags: str = "|".join(html_tag_names) + self.custom_html

        self.indent_template_tags: str = (
            r"""  if
                | for
                | block(?!trans|translate)
            #    | blocktrans(?:late)?[ ]+?trimmed
                | spaceless
                | compress
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
            """
            + self.custom_blocks
        )

        self.template_indent: str = (
            r"""
            (?:\{\{\#|\{%-?)[ ]*?
                ("""
            + self.indent_template_tags
            + r"""
            )"""
        )

        self.template_unindent: str = r"""
                (?:
                  (?:\{\{\/)
                | (?:\{%-?[ ]*?end(?!comment))
              )
            """

        # these tags should be unindented and next line will be indented
        self.tag_unindent_line: str = r"""
              (?:\{%-?[ ]*?(?:elif|else|empty))
            | (?:
                \{\{[ ]*?
                (
                    (?:else|\^)
                    [ ]*?\}\}
                )
              )
        """

        self.break_before = r"(?<!\n[ ]*?)"

        # if lines are longer than x
        self.max_line_length = 120

        try:
            self.max_line_length = int(
                djlint_settings.get("max_line_length", self.max_line_length)
            )
        except ValueError:
            echo(
                Fore.RED
                + f"Error: Invalid pyproject.toml max_line_length value {djlint_settings['max_line_length']}"
            )

        self.max_attribute_length = 70

        try:
            self.max_attribute_length = int(
                djlint_settings.get("max_attribute_length", self.max_attribute_length)
            )
        except ValueError:
            echo(
                Fore.RED
                + f"Error: Invalid pyproject.toml max_attribute_length value {djlint_settings['max_attribute_length']}"
            )

        self.template_if_for_pattern = (
            r"(?:{%-?\s?(?:if|for)[^}]*?%}(?:.*?{%\s?end(?:if|for)[^}]*?-?%})+?)"
        )

        self.attribute_pattern: str = (
            rf"""
            (?:
                (
                    (?:\w|-|\.)+ | required | checked
                )? # attribute name
                (?:  [ ]*?=[ ]*? # followed by "="
                    (
                        \"[^\"]*? # double quoted attribute
                        (?:
                            {self.template_if_for_pattern} # if or for loop
                           | {{{{.*?}}}} # template stuff
                           | {{%[^}}]*?%}}
                           | [^\"] # anything else
                        )*?
                        \" # closing quote
                      | '[^']*? # single quoted attribute
                        (?:
                            {self.template_if_for_pattern} # if or for loop
                           | {{{{.*?}}}} # template stuff
                           | {{%[^}}]*?%}}
                           | [^'] # anything else
                        )*?
                        \' # closing quote
                      | (?:\w|-)+ # or a non-quoted string value
                      | {{{{.*?}}}} # a non-quoted template var
                      | {{%[^}}]*?%}} # a non-quoted template tag
                      | {self.template_if_for_pattern} # a non-quoted if statement

                    )
                )? # attribute value
            )
            | ({self.template_if_for_pattern}
            """
            + r"""
            | {{.*?}}
            | {\#.*?\#}
            | {%.*?%})
        """
        )

        self.attribute_style_pattern: str = r"^(.*?)(style=)([\"|'])(([^\"']+?;)+?)\3"
        self.ignored_attributes = [
            "href",
            "action",
            "data-url",
            "src",
            "url",
            "srcset",
            "data-src",
        ]
        self.start_template_tags: str = (
            r"""
              if
            | for
            | block(?!trans)
            | spaceless
            | compress
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
            """
            + self.custom_blocks
            + r"""
        """
        )

        self.break_template_tags: str = (
            r"""
              if
            | endif
            | for
            | endfor
            | block(?!trans)
            | endblock(?!trans)
            | else
            | spaceless
            | endspaceless
            | compress
            | endcompress
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
            """
            + self.custom_blocks
            + r"""
        """
        )
        self.template_blocks: str = r"""
        {%((?!%}).)+%}
        """
        self.ignored_blocks: str = r"""
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
            | <!--.*?-->
            | <\?php.*?\?>
            | {%[ ]*?blocktranslate\b[^(?:%})]*?%}.*?{%[ ]*?endblocktranslate[ ]*?%}
            | {%[ ]*?blocktrans\b[^(?:%})]*?%}.*?{%[ ]*?endblocktrans[ ]*?%}
            | {%[ ]*?comment\b[^(?:%})]*?%}.*?(?={%[ ]*?endcomment[ ]*?%})
            | ^---[\s\S]+?---
        """

        self.ignored_rules: List[str] = [
            # html comment
            r"<!--\s*djlint\:off(.+?)-->.*?(?=<!--\s*djlint\:on\s*-->)",
            # django/jinja/nunjucks
            r"{\#\s*djlint\:\s*off(.+?)\#}.*?(?={\#\s*djlint\:\s*on\s*\#})",
            r"{%\s*comment\s*%\}\s*djlint\:off(.*?)\{%\s*endcomment\s*%\}.*?(?={%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\})",
            # handlebars
            r"{{!--\s*djlint\:off(.*?)--}}.*?(?={{!--\s*djlint\:on\s*--}})",
            # golang
            r"{{-?\s*/\*\s*djlint\:off(.*?)\*/\s*-?}}.*?(?={{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}})",
        ]

        self.ignored_inline_blocks: str = r"""
              <!--.*?-->
            | <script.*?\</script>
            | <style.*?\</style>
            | {\*.*?\*}
            | {\#(?!.*djlint:[ ]*?(?:off|on)\b).*\#}
            | <\?php.*?\?>
            | {%[ ]*?comment\b[^(?:%})]*?%}.*?{%[ ]*?endcomment[ ]*?%}
            | {%[ ]*?blocktranslate\b[^(?:%})]*?%}.*?{%[ ]*?endblocktranslate[ ]*?%}
            | {%[ ]*?blocktrans\b[^(?:%})]*?%}.*?{%[ ]*?endblocktrans[ ]*?%}
        """

        self.optional_single_line_html_tags: str = r"""
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
        """

        self.always_self_closing_html_tags: str = "|".join(html_void_elements)

        self.optional_single_line_template_tags: str = r"""
              if
            | for
            | block
            | with
        """

        self.break_html_tags: str = (
            r"""
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
            + self.always_self_closing_html_tags
            + self.custom_html
            + """
        """
        )

        # the contents of these tag blocks will be indented, then unindented
        self.tag_indent: str = (
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
        self.tag_unindent: str = (
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
