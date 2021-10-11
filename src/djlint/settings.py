"""Settings for reformater."""
# pylint: disable=C0301,C0103
# flake8: noqa


import logging
import re

## get pyproject.toml settings
from pathlib import Path
from typing import Dict, List, Optional, Union

import tomlkit
import yaml
from click import echo
from colorama import Fore

logger = logging.getLogger(__name__)


def find_pyproject(src: Path) -> Optional[Path]:
    """Search upstream for a pyprojec.toml file."""

    for directory in [src, *src.resolve().parents]:

        candidate = directory / "pyproject.toml"

        if candidate.is_file():
            return candidate

    return None


def find_djlint_rules(src: Path) -> Optional[Path]:
    """Search upstream for a pyprojec.toml file."""

    for directory in [src, *src.resolve().parents]:

        candidate = directory / ".djlint_rules.yaml"

        if candidate.is_file():
            return candidate

    return None


def load_pyproject_settings(src: Path) -> Dict:
    """Load djlint config from pyproject.toml."""

    djlint_content: Dict = {}
    pyproject_file = find_pyproject(src)

    if pyproject_file:
        content = tomlkit.parse(pyproject_file.read_text(encoding="utf8"))
        try:
            djlint_content = content["tool"]["djlint"]  # type: ignore
        except KeyError:
            logger.info("No pyproject.toml found.")

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


class Config:
    """Djling Config."""

    def __init__(
        self,
        src: str,
        ignore: Optional[str] = None,
        extension: Optional[str] = None,
        indent: Optional[int] = None,
        quiet: Optional[bool] = False,
        profile: Optional[str] = None,
    ):

        djlint_settings = load_pyproject_settings(Path(src))

        # custom configuration options
        self.extension: str = str(extension or djlint_settings.get("extension", "html"))
        self.quiet: str = str(quiet or djlint_settings.get("quiet", ""))
        self.custom_blocks: str = str(
            build_custom_blocks(djlint_settings.get("custom_blocks")) or ""
        )

        # ignore is based on input and also profile
        self.ignore: str = str(ignore or djlint_settings.get("ignore", ""))

        # codes to exclude
        profile_dict: Dict[str, List[str]] = {
            "django": ["J", "N", "M"],
            "jinja": ["D", "N", "M"],
            "nunjucks": ["D", "J", "M"],
            "handlebars": ["D", "J", "N"],
            "golang": ["D", "J", "N", "M"],
        }

        self.profile_code: List[str] = profile_dict.get(
            str(profile or djlint_settings.get("profile", "all")).lower(), []
        )
        self.profile: str = str(
            profile or djlint_settings.get("profile", "all")
        ).lower()

        # load linter rules
        rule_set = validate_rules(
            yaml.load(
                (Path(__file__).parent / "rules.yaml").read_text(encoding="utf8"),
                Loader=yaml.SafeLoader,
            )
            + load_custom_rules(Path(src))
        )

        self.linter_rules = list(
            filter(
                lambda x: x["rule"]["name"] not in self.ignore.split(",")
                and x["rule"]["name"][0] not in self.profile_code
                and self.profile not in x["rule"].get("exclude", []),
                rule_set,
            )
        )

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
            | venv
            | \.tox
            | \.eggs
            | \.git
            | \.hg
            | \.mypy_cache
            | \.nox
            | \.svn
            | \.bzr
            | _build
            | buck-out
            | build
            | dist
            | \.pants\.d
            | \.direnv
            | node_modules
            | __pypackages__
        """

        self.exclude: str = djlint_settings.get("exclude", default_exclude)

        extend_exclude: str = djlint_settings.get("extend_exclude", "")

        if extend_exclude:
            self.exclude += r" | " + r" | ".join(
                re.escape(x.strip()) for x in extend_exclude.split(",")
            )

        # add blank line after load tags
        self.blank_line_after_tag: Optional[str] = djlint_settings.get(
            "blank_line_after_tag", None
        )

        # contents of tags will not be formatted
        self.ignored_block_opening: str = r"""
              <style
            | {\*
            | <\?php
            | <script
            | <!--
            | [^\{]{\#
            | <pre
            | <textarea
            | {%[ ]djlint:off[ ]%}
            | {%[ ]+?comment[ ]+?[^(?:%})]*?%}
        """

        self.ignored_block_closing: str = r"""
              </style
            | \*}
            | \?>
            | </script
            |  -->
            | \#}
            | </pre
            | </textarea
            | {%[ ]djlint:on[ ]%}
            | {%[ ]+?endcomment[ ]+?%}
        """

        # all html tags possible
        self.indent_html_tags: str = r"""
              a
            | abbr
            | acronym
            | address
            | applet
            | area
            | article
            | aside
            | audio
            | b
            | base
            | basefont
            | bdi
            | bdo
            | big
            | blockquote
            | body
            | br
            | button
            | canvas
            | caption
            | center
            | cite
            | code
            | col
            | colgroup
            | data
            | datalist
            | dd
            | del
            | details
            | dfn
            | dialog
            | dir
            | div
            | dl
            | dt
            | em
            | embed
            | fieldset
            | figcaption
            | figure
            | font
            | footer
            | form
            | frame
            | frameset
            | h1
            | h2
            | h3
            | h4
            | h5
            | h6
            | head
            | header
            | hr
            | html
            | i
            | iframe
            | icon
            | img
            | input
            | ins
            | kbd
            | label
            | legend
            | li
            | link
            | main
            | map
            | mark
            | meta
            | meter
            | nav
            | noframes
            | noscript
            | object
            | ol
            | optgroup
            | option
            | output
            | p
            | path
            | param
            | picture
            | progress
            | q
            | rp
            | rt
            | ruby
            | s
            | samp
            | script
            | section
            | select
            | small
            | source
            | span
            | strike
            | strong
            | style
            | sub
            | summary
            | sup
            | svg
            | table
            | tbody
            | td
            | template
            | tfoot
            | th
            | thead
            | time
            | title
            | tr
            | track
            | tt
            | u
            | ul
            | var
            | video
            | wbr
        """

        self.indent_template_tags: str = (
            r"""  if
                | for
                | block
                | else
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
            """
            + self.custom_blocks
        )

        # the contents of these tag blocks will be indented, then unindented
        self.tag_indent: str = (
            r"""
              (?:\{\{\#|\{%-?)[ ]*?
                ("""
            + self.indent_template_tags
            + r"""
                )
            | (?:<
                (?:
                    """
            + self.indent_html_tags
            + """
                )\\b
              )
        """
        )

        self.tag_unindent: str = (
            r"""^
              (?:
                  (?:\{\{\/)
                | (?:\{%-?[ ]*?end)
              )
            | (?:</
                (?:
                    """
            + self.indent_html_tags
            + """
                )\\b
              )
        """
        )

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

        self.format_long_attributes = True

        # pattern used to find attributes in a tag
        # order is important.
        # 1. attributes="{% if %}with if or for statement{% endif %}"
        # 2. attributes="{{ stuff in here }}"
        # 3. {% if %}with if or for statement{% endif %}
        # 4. attributes="normal html"
        # 5. require | checked | otherword | other-word
        # 6. {{ stuff }}

        self.template_if_for_pattern = (
            r"(?:{%-?\s?(?:if|for)[^}]*?%}(?:.*?{%\s?end(?:if|for)[^}]*?-?%})+?)"
        )
        self.attribute_pattern: str = (
            r"""
            (?:[^\s]+?=(?:\"[^\"]*?"""
            + self.template_if_for_pattern
            + r"""[^\"]*?\"|\'[^\']*?"""
            + self.template_if_for_pattern
            + r"""[^\']*?\'))
            | (?:[^\s]+?=(?:\"[^\"]*?{{.*?}}[^\"]*?\"|\'[^\']*?{{.*?}}[^\']*?\'))
            | """
            + self.template_if_for_pattern
            + r"""
            | (?:[^\s]+?=(?:\"(?:[^\"]*?{%[^}]*?%}[^\"]*?)+?\"))
            | (?:[^\s]+?=(?:\'(?:[^\']*?{%[^}]*?%}[^\']*?)+?\'))
            | (?:[^\s]+?=(?:\".*?\"|\'.*?\'))
            | required
            | checked
            | [\w|-]+
            | [\w|-]+=[\w|-]+
            | {{.*?}}
        """
        )

        self.attribute_style_pattern: str = r"(.*?)(style=)([\"|'])(([^\"']+?;)+?)\3"

        self.start_template_tags: str = (
            r"""
              if
            | for
            | block
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
            """
            + self.custom_blocks
            + r"""
        """
        )

        self.break_template_tags: str = (
            r"""
              if
            | end
            | for
            | block
            | endblock
            | else
            | spaceless
            | compress
            | load
            | include
            | assets
            | addto
            | language
            | with
            | assets
            | autoescape
            | filter
            | elif
            | resetcycle
            | verbatim
            | each
            """
            + self.custom_blocks
            + r"""
        """
        )

        self.ignored_blocks: str = r"""
              <(script|style|pre|textarea).*?</(\1)>
            | {%[ ]djlint:off[ ]%}.*?{%[ ]djlint:on[ ]%}
            | <!--.*?-->
            | {\*.*?\*}
            | {\#.*?\#}
            | <\?php.*?\?>
            | {\%[ ]trans[ ][^}]*?\%}
            | {%[ ]+?comment[ ]+?[^(?:%})]*?%}.*?{%[ ]+?endcomment[ ]+?%}
        """

        self.ignored_inline_blocks: str = r"""
              <!--.*?-->
            | {\*.*?\*}
            | {\#.*?\#}
            | <\?php.*?\?>
            | {%[ ]+?comment[ ]+?[^(?:%})]*?%}.*?{%[ ]+?endcomment[ ]+?%}
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
        """

        self.always_self_closing_html_tags: str = r"""
              link
            | img
            | meta
            | source
            | br
            | input
        """

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
            | a
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
            | span
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
            + """
        """
        )
