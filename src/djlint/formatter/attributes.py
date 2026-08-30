"""Format attributes."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_LOWERCASE_ATTRIBUTE_NAMES
from djlint.formatter.class_attributes import (
    CLASS_ATTRIBUTE_NEWLINE,
    VERBATIM_ATTRIBUTE_NEWLINE,
    decode_class_attribute_newlines,
    restore_verbatim_attribute_newlines,
)
from djlint.helpers import RE_FLAGS_IMX, RE_FLAGS_IS, child_of_ignored_block

if TYPE_CHECKING:
    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config

_QUOTED_VALUE_PATTERN = re.compile(r"\"[^\"]*\"|'[^']*'", cache_pattern=False)
_UNQUOTED_VALUE_PATTERN = re.compile(r"=[ \t]*[^\s\"'=<>]", cache_pattern=False)

_SRCSET_ATTRIBUTE_NAMES = frozenset(("srcset", "data-srcset", "sizes"))
_COLLAPSIBLE_VALUE_ATTRIBUTE_NAMES = frozenset(("class", "style"))

_REWRITTEN_FROM_STRIPPED_PARTS_PATTERN = re.compile(
    r"\b(?:style|srcset|data-srcset|sizes)[ \t]*=[ \t]*([\"'])(.*?)\1",
    RE_FLAGS_IS,
    cache_pattern=False,
)


def _rendered_length(config: Config, attribute_group: str) -> int:
    """Length of the attribute group as it will be written out.

    Values spread over several lines arrive flattened with a space at each
    line break. Measuring padding that the rewrite drops spreads a tag whose
    attributes then fit on one line again on the next run.
    """
    length = len(attribute_group)
    if length < config.max_attribute_length:
        return length

    return length - sum(
        len(value) - len(value.strip())
        for match in _REWRITTEN_FROM_STRIPPED_PARTS_PATTERN.finditer(
            attribute_group
        )
        if (value := match.group(2))
    )


def normalize_attributes(config: Config, attribute_group: str) -> str:
    """Lowercase a known attribute name and quote a bare value.

    Only the names `H010` knows are lowercased, so a framework binding
    such as `viewBox` or an angular input keeps the case it carries.

    A value holding a quote of its own is left as written. It is not valid
    html to begin with, and a browser reads `a=b'c` as the single value
    `b'c`, where the match stops at the quote: writing `a="b"'c` would make
    the rest an attribute of its own.
    """
    quotable = _UNQUOTED_VALUE_PATTERN.search(attribute_group) is not None
    lowerable = not config.ignore_case and not attribute_group.islower()
    if not (quotable or lowerable):
        return attribute_group

    matches = list(config.attribute_pattern.finditer(attribute_group))
    if not _is_fully_matched(attribute_group, matches):
        return attribute_group

    output: list[str] = []
    previous_end = 0

    def rewrite(span: tuple[int, int], text: str) -> None:
        nonlocal previous_end
        output.extend((attribute_group[previous_end : span[0]], text))
        previous_end = span[1]

    for match in matches:
        name, value = match.group(1, 2)
        if not name:
            continue

        if (
            lowerable
            and not name.islower()
            and name.lower() in HTML_LOWERCASE_ATTRIBUTE_NAMES
        ):
            rewrite(match.span(1), name.lower())

        if (
            quotable
            and value
            and not {'"', "'"} & set(value)
            and attribute_group[match.end(2) : match.end(2) + 1]
            in {"", " ", "\t"}
        ):
            rewrite(match.span(2), f'"{value}"')

    output.append(attribute_group[previous_end:])
    return "".join(output)


def has_unquoted_template_expression(attribute_group: str) -> bool:
    """Check for a ${...} template expression outside quoted values."""
    return "${" in attribute_group and "${" in _QUOTED_VALUE_PATTERN.sub(
        "", attribute_group
    )


def count_object_properties(config: Config, value: str) -> int:
    """Count the number of properties in a JSON/JS object."""
    try:
        return len(json.loads(value))
    except json.JSONDecodeError:
        without_strings = config.format_attribute_js_json_string_pattern.sub(
            "", value
        )
        return len(
            config.format_attribute_js_json_property_pattern.findall(
                without_strings
            )
        )


def _indent_below_first_line(formatted: str, base_indent: str) -> str:
    """Add the attribute's own indentation to every line but the first.

    The first line follows the opening quote, so it takes none.
    """
    first, *rest = formatted.split("\n")
    if not rest:
        return formatted
    return "\n".join([
        first.strip(),
        *(base_indent + line if line.strip() else "" for line in rest),
    ])


def format_json_with_indent(
    config: Config, value: str, base_indent: str
) -> str | None:
    """Format JSON with HTML-relative indentation, or None if not JSON."""
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        return None

    formatted = json.dumps(data, indent=config.js_config.get("indent_size", 4))
    return _indent_below_first_line(formatted, base_indent)


def format_js_with_indent(config: Config, value: str, base_indent: str) -> str:
    """Format JavaScript code/object with proper HTML-relative indentation."""
    import jsbeautifier  # noqa: PLC0415
    from jsbeautifier.javascript.options import (  # noqa: PLC0415
        BeautifierOptions,
    )

    js_config = dict(config.js_config)
    js_config["indent_level"] = 0

    try:
        formatted: str = jsbeautifier.beautify(
            value, BeautifierOptions(js_config)
        )
    except ValueError:
        return value

    return _indent_below_first_line(formatted, base_indent)


def format_template_tags(config: Config, attributes: str, spacing: int) -> str:
    """Format template tags in attributes."""

    def add_indentation(config: Config, attributes: str, spacing: int) -> str:
        """Indent template tags below the column the value starts at."""
        template_unindent_pattern = config.template_unindent_ix_pattern
        tag_unindent_line_pattern = config.tag_unindent_line_ix_pattern
        template_indent_pattern = config.template_indent_ix_pattern

        indent = 0
        lines = []
        base_indent = (spacing or 0) * " "

        for line_number, raw_line in enumerate(attributes.splitlines()):
            line = raw_line.strip()
            if template_unindent_pattern.match(line):
                indent -= 1
                level = indent
            elif tag_unindent_line_pattern.match(line):
                level = max(indent - 1, 0)
            else:
                level = indent
                if template_indent_pattern.search(
                    line
                ) and not template_unindent_pattern.search(line):
                    indent += 1

            if line_number == 0:
                lines.append(line)
            elif line:
                lines.append(f"{level * config.indent}{base_indent}{line}")

        return "\n".join(lines)

    def add_break_before(match: re.Match[str]) -> str:
        return f"\n{match.group()}"

    def add_break_after(match: re.Match[str]) -> str:
        return f"{match.group(1)}\n{match.group(2).strip()}"

    attributes = re.sub(
        config.break_before
        + r"[ \t]\K((?:{%|{{\#)[ ]*?(?:"
        + config.break_template_tags
        + ")[^}]+?[%|}]})",
        add_break_before,
        attributes,
        flags=RE_FLAGS_IMX,
    )

    attributes = re.sub(
        r"((?:{%|{{\#)[ ]*?(?:"
        + config.break_template_tags
        + ")[^}]+?[%|}]})(?=[ \t])([^\n]+)$",
        add_break_after,
        attributes,
        flags=RE_FLAGS_IMX,
    )
    return add_indentation(config, attributes, spacing)


def _is_fully_matched(
    attribute_group: str, attribute_matches: list[re.Match[str]]
) -> bool:
    """Whether the matches account for every non-space byte of the group.

    The tag is rebuilt from the matched groups, so anything the pattern
    misses would be dropped. A nameless "=value" attribute is malformed
    the same way, and would be written back out as "None=value"; template
    conditionals such as "{% if x %}sel{% endif %}" also have no name group
    but must still be formatted.
    """
    covered = 0
    for match in attribute_matches:
        if attribute_group[covered : match.start()].strip():
            return False
        if match.group(1) is None and match.group().strip().startswith("="):
            return False
        covered = match.end()
    return not attribute_group[covered:].strip()


def format_attributes(config: Config, html: str, token: TagToken) -> str:
    """Spread long attributes over multiple lines."""
    attribute_group = html[token.name_end : token.attributes_end].strip()
    if (
        has_unquoted_template_expression(attribute_group)
        or (
            _rendered_length(config, attribute_group)
            < config.max_attribute_length
            and CLASS_ATTRIBUTE_NEWLINE not in attribute_group
            and VERBATIM_ATTRIBUTE_NEWLINE not in attribute_group
        )
    ) or child_of_ignored_block(config, html, token):
        return html[token.start : token.end]

    if not config.format_attribute_template_tags:
        template_depth = 0
        for template_tag in config.template_tags_imx_pattern.finditer(
            attribute_group
        ):
            if config.template_unindent_imx_pattern.match(template_tag.group()):
                template_depth = max(template_depth - 1, 0)
            elif config.template_indent_imx_pattern.match(template_tag.group()):
                template_depth += 1
                if template_depth > 1:
                    return html[token.start : token.end]

    leading_start = token.start
    while leading_start and html[leading_start - 1] in " \t":
        leading_start -= 1
    leading_space = html[leading_start : token.start]

    tag = f"<{token.name} "

    spacing = (
        leading_space + config.indent
        if config.single_attribute_per_line
        else leading_space + len(tag) * " "
    )

    attributes = []

    attribute_matches = list(config.attribute_pattern.finditer(attribute_group))
    if not _is_fully_matched(attribute_group, attribute_matches):
        return html[token.start : token.end]

    for attr_grp in attribute_matches:
        attrib_name, raw_value, standalone = attr_grp.group(1, 2, 3)
        first_char = raw_value[0] if raw_value else ""
        is_quoted = first_char in {"'", '"'}
        quote = first_char if is_quoted else '"'

        if is_quoted and first_char == raw_value[-1]:
            attrib_value = raw_value.strip(first_char)
        else:
            attrib_value = raw_value

        value_offset = len('="') if attrib_name and attrib_value else len('"')

        join_space = (
            f"\n{spacing}"
            if config.format_attribute_template_tags
            else (
                f"\n{spacing}" + (value_offset + len(attrib_name or "")) * " "
            )
        )

        lowered_name = attrib_name.lower() if attrib_name else ""

        if lowered_name == "style":
            attrib_value = f";{join_space}".join(
                stripped
                for value in attrib_value.split(";")
                if (stripped := value.strip())
            )

        elif lowered_name in _SRCSET_ATTRIBUTE_NAMES:
            for descriptor in ("w", "x"):
                attrib_value = f"{descriptor},{join_space}".join(
                    stripped
                    for value in attrib_value.split(f"{descriptor},")
                    if (stripped := value.strip())
                )

        if (
            config.format_attribute_js_json
            and attrib_name
            and attrib_value
            and VERBATIM_ATTRIBUTE_NEWLINE not in attrib_value
            and config.format_attribute_js_json_pattern.match(attrib_name)
        ):
            value_indent = spacing + (value_offset + len(attrib_name)) * " "

            if not config.format_attribute_js_json_object_pattern.match(
                attrib_value
            ):
                attrib_value = format_js_with_indent(
                    config, attrib_value, value_indent
                )
            elif (
                count_object_properties(config, attrib_value)
                >= config.format_attribute_js_json_min_props
            ):
                as_json = format_json_with_indent(
                    config, attrib_value, value_indent
                )
                attrib_value = (
                    as_json
                    if as_json is not None
                    else format_js_with_indent(
                        config, attrib_value, value_indent
                    )
                )

        if config.format_attribute_template_tags:
            if (
                attrib_value
                and attrib_name
                and lowered_name in _COLLAPSIBLE_VALUE_ATTRIBUTE_NAMES
                and attrib_name not in config.ignored_attributes
            ):
                attrib_value = format_template_tags(
                    config,
                    attrib_value,
                    len(spacing) + len(attrib_name) + value_offset,
                )

            if standalone:
                standalone = format_template_tags(
                    config, standalone, len(spacing) + len(attrib_name or "")
                )

        if (
            config.preserve_class_newlines
            and lowered_name == "class"
            and attrib_value
        ):
            attrib_value = decode_class_attribute_newlines(
                attrib_value, join_space
            )

        if attrib_value:
            attrib_value = restore_verbatim_attribute_newlines(attrib_value)

        if (attrib_name and attrib_value) or is_quoted:
            attrib_value = attrib_value or ""
            attributes.append(f"{attrib_name}={quote}{attrib_value}{quote}")
        else:
            attributes.append(
                (attrib_name or "") + (attrib_value or "") + (standalone or "")
            )
    attribute_string = f"\n{spacing}".join(x for x in attributes if x)

    close = " />" if token.self_closing else ">"

    if config.single_attribute_per_line:
        attribute_string = (
            f"{leading_space}<{token.name}"
            f"\n{spacing}{attribute_string}"
            f"\n{leading_space}{close.strip()}"
        )
    else:
        attribute_string = f"{leading_space}{tag}{attribute_string}{close}"

    return "\n".join(x.rstrip() for x in attribute_string.splitlines())
