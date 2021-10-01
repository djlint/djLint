"""Settings for reformater."""
# pylint: disable=C0301,C0103
# flake8: noqa


import logging
import re

## get pyproject.toml settings
from pathlib import Path
from typing import Dict, List, Optional, Union

import tomlkit

logger = logging.getLogger(__name__)


def find_pyproject(src: Path) -> Optional[Path]:
    """Search upstream for a pyprojec.toml file."""

    for directory in [src, *src.resolve().parents]:

        candidate = directory / "pyproject.toml"

        if candidate.is_file():
            return candidate

    return None


def load_pyproject_settings(src: Path) -> Dict:
    """Load djlint config from pyproject.toml."""

    djlint_content: Dict = {}
    pyproject_file = find_pyproject(src)

    if pyproject_file:
        content = tomlkit.parse(pyproject_file.read_text())
        try:
            djlint_content = content["tool"]["djlint"]  # type: ignore
        except KeyError:
            logger.info("No pyproject.toml found.")

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
        }

        self.profile_code: List[str] = profile_dict.get(
            str(profile or djlint_settings.get("profile", "all")).lower(), []
        )
        self.profile: str = str(
            profile or djlint_settings.get("profile", "all")
        ).lower()

        # base options
        self.indent: str = (indent or int(djlint_settings.get("indent", 4))) * " "

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

        # contents of tags will not be formatted, but tags will be formatted
        self.ignored_block_opening: str = r"""
              <style
            | {\*
            | <\?php
            | <script
        """

        self.ignored_block_closing: str = r"""
              </style
            | \*}
            | \?>
            | </script
        """

        # contents of tags will not be formated and tags will not be formatted
        self.ignored_group_opening: str = r"""
              <!--
            | [^\{]{\#
            | <pre
            | <textarea
        """

        self.ignored_group_closing: str = r"""
              -->
            | \#}
            | </pre
            | </textarea
        """

        # the contents of these tag blocks will be indented, then unindented
        self.tag_indent: str = (
            r"""
              (?:\{\{\#|\{%-?)[ ]*?
                (
                      if
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
                    | comment
                    | filter
                    | each
                    """
            + self.custom_blocks
            + r"""
                )
            | (?:<
                (?:
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
                    | cache
                    | optgroup
                    | fieldset
                    | legend
                    | label
                    | header
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
                    | img
                    | path
                    | script
                    | style
                    | details
                    | summary
                )
              )
        """
        )

        self.tag_unindent: str = r"""^
              (?:
                  (?:\{\{\/)
                | (?:\{%-?[ ]*?end)
              )
            | (?:</
                (?:
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
                    | img
                    | path
                    | script
                    | style
                    | details
                    | summary
                )
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

        # reduce empty lines greater than  x to 1 line
        self.reduce_extralines_gt = 2

        # if lines are longer than x
        self.max_line_length = 120
        self.format_long_attributes = True

        # pattern used to find attributes in a tag
        # order is important.
        # 1. attributes="{% if %}with if or for statement{% endif %}"
        # 2. attributes="{{ stuff in here }}"
        # 3. {% if %}with if or for statement{% endif %}
        # 4. attributes="normal html"
        # 5. require | checked | otherword | other-word
        # 6. {{ stuff }}
        template_if_for_pattern = (
            r"(?:{%-?\s?(?:if|for)[^}]*?%}(?:.*?{%\s?end(?:if|for)[^}]*?-?%})+?)"
        )
        self.attribute_pattern: str = (
            r"""
            (?:[^\s]+?=(?:\"[^\"]*?"""
            + template_if_for_pattern
            + r"""[^\"]*?\"|\'[^\']*?"""
            + template_if_for_pattern
            + r"""[^\']*?\'))
            | (?:[^\s]+?=(?:\"[^\"]*?{{.*?}}[^\"]*?\"|\'[^\']*?{{.*?}}[^\']*?\'))
            | """
            + template_if_for_pattern
            + r"""
            | (?:[^\s]+?=(?:\".*?\"|\'.*?\'))
            | required
            | checked
            | [\w|-]+
            | [\w|-]+=[\w|-]+
            | {{.*?}}
        """
        )

        self.tag_pattern: str = r"""
            (<\w+?[^>]*?)((?:\n[^>]+?)+?)(/?\>)
        """

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
            | comment
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
            | comment
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
            | <!--.*?-->
            | {\*.*?\*}
            | {\#.*?\#}
            | <\?php.*?\?>
        """

        self.ignored_inline_blocks: str = r"""
              <!--.*?-->
            | {\*.*?\*}
            | {\#.*?\#}
            | <\?php.*?\?>
        """

        self.single_line_html_tags: str = r"""
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
        """

        self.always_single_line_html_tags: str = r"""
              link
            | img
            | meta
            | source
        """

        self.single_line_template_tags: str = r"""
              if
            | for
            | block
            | with
            | comment
        """

        self.break_html_tags: str = r"""
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
