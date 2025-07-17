"""Format attributes."""

from __future__ import annotations

import json
from functools import partial
from typing import TYPE_CHECKING

import jsbeautifier
import regex as re
from jsbeautifier.javascript.options import BeautifierOptions

from djlint.helpers import RE_FLAGS_IMX, RE_FLAGS_IX, child_of_ignored_block

if TYPE_CHECKING:
    from djlint.settings import Config


def count_object_properties(config: Config, value: str) -> int:
    """Count the number of properties in a JSON/JS object."""
    try:
        # Try parsing as JSON first
        data = json.loads(value)
        return len(data)
    except Exception:
        # For JS objects, count property-like patterns
        # Simple heuristic: count comma-separated properties
        cleaned = config.js_string_pattern.sub("", value)  # Remove strings
        return len(config.js_property_pattern.findall(cleaned))


def is_json_object(value: str) -> bool:
    """Check if attribute value is a valid JSON object."""
    try:
        json.loads(value)
    except Exception:
        return False
    else:
        return True


def format_json_with_indent(
    config: Config, value: str, base_indent: str
) -> str:
    """Format JSON with proper HTML-relative indentation."""
    try:
        data = json.loads(value)
    except Exception:
        return value
    else:
        # Use indent_size from config for JSON formatting
        indent_size = config.js_config.get("indent_size", 4)
        formatted = json.dumps(data, indent=indent_size)
        # Add base_indent to each line (except first)
        lines = formatted.split("\n")
        if len(lines) > 1:
            indented_lines = [lines[0]]
            for i, line in enumerate(lines[1:], 1):
                if i == len(lines) - 1:  # Last line (closing brace)
                    # Indent closing brace less than properties
                    closing_indent = base_indent[:-2]  # Remove 2 spaces
                    indented_lines.append(closing_indent + line)
                else:
                    indented_lines.append(base_indent + line)
            return "\n".join(indented_lines)
        return formatted


def format_js_with_indent(config: Config, value: str, base_indent: str) -> str:
    """Format JavaScript code/object with proper HTML-relative indentation."""
    try:
        # Use the same JS config as the main JS formatter
        js_config = dict(config.js_config)
        js_config["indent_level"] = 0  # No extra indentation from jsbeautifier

        opts = BeautifierOptions(js_config)
        formatted: str = jsbeautifier.beautify(value, opts)
    except Exception:
        return value
    else:
        # Add base_indent to each line while preserving relative indentation
        lines = formatted.split("\n")
        if len(lines) > 1:
            indented_lines = [
                lines[0].strip()
            ]  # Remove jsbeautifier's indentation from first line

            for i, line in enumerate(lines[1:], 1):
                if not line.strip():  # Handle empty lines
                    indented_lines.append("")
                    continue

                # Preserve the original jsbeautifier indentation structure
                line_indent = len(line) - len(line.lstrip())

                # Check if this is an object (starts and ends with braces)
                is_object = value.strip().startswith(
                    "{"
                ) and value.strip().endswith("}")

                if (
                    is_object and i == len(lines) - 1
                ):  # Last line of object (closing brace)
                    # Indent closing brace less than properties for objects
                    js_indent_size = config.js_config.get("indent_size", 4)
                    closing_indent = base_indent[
                        :-js_indent_size
                    ]  # Remove js_indent_size spaces for JS objects
                    indented_lines.append(
                        closing_indent + (" " * line_indent) + line.strip()
                    )
                else:
                    # For general JS code or object properties, use full base_indent + jsbeautifier indent
                    indented_lines.append(
                        base_indent + (" " * line_indent) + line.strip()
                    )
            return "\n".join(indented_lines)
        return formatted


def format_template_tags(config: Config, attributes: str, spacing: int) -> str:
    """Format template tags in attributes."""
    # find break tags, add breaks + indent
    # find unindent lines and move back
    # put short stuff back on one line

    def add_indentation(config: Config, attributes: str, spacing: int) -> str:
        """Indent template tags.

        |    <form class="this"
        |    ----- attribute name
        |
        |    <form class="this"
        |---^ leading space
        |
        |    <form class="this"
        |    ^----^ base indent
        |
        """
        indent = 0
        indented = ""
        indent_adder = spacing or 0

        for line_number, line in enumerate(attributes.splitlines()):
            # when checking for template tag, use "match" to force start of line check.
            if re.match(
                config.template_unindent, line.strip(), flags=RE_FLAGS_IX
            ):
                indent -= 1
                tmp = (
                    (indent * config.indent)
                    + (indent_adder * " ")
                    + line.strip()
                )

            elif re.match(
                config.tag_unindent_line, line.strip(), flags=RE_FLAGS_IX
            ):
                # if we are leaving an indented group, then remove the indent_adder
                tmp = (
                    max(indent - 1, 0) * config.indent
                    + indent_adder * " "
                    + line.strip()
                )

            elif re.search(
                config.template_indent, line.strip(), flags=RE_FLAGS_IX
            ) and not re.search(
                config.template_unindent, line.strip(), flags=RE_FLAGS_IX
            ):
                # for open tags, search, but then check that they are not closed.
                tmp = (
                    (indent * config.indent)
                    + (indent_adder * " ")
                    + line.strip()
                )
                indent += 1

            else:
                tmp = (
                    (indent * config.indent)
                    + (indent_adder * " ")
                    + line.strip()
                )

            if line_number == 0:
                # don't touch first line
                indented += line.strip()
            elif tmp.strip():
                indented += f"\n{tmp}"

        return indented

    def add_break(pattern: str, match: re.Match[str]) -> str:
        """Make a decision if a break should be added."""
        if pattern == "before":
            return f"\n{match.group()}"

        return f"{match.group(1)}\n{match.group(2).strip()}"

    break_char = config.break_before

    func = partial(add_break, "before")

    attributes = re.sub(
        break_char
        + r".\K((?:{%|{{\#)[ ]*?(?:"
        + config.break_template_tags
        + ")[^}]+?[%|}]})",
        func,
        attributes,
        flags=RE_FLAGS_IMX,
    )

    func = partial(add_break, "after")
    # break after
    attributes = re.sub(
        r"((?:{%|{{\#)[ ]*?(?:"
        + config.break_template_tags
        + ")[^}]+?[%|}]})([^\n]+)$",
        func,
        attributes,
        flags=RE_FLAGS_IMX,
    )
    return add_indentation(config, attributes, spacing)


def format_attributes(config: Config, html: str, match: re.Match[str]) -> str:
    """Spread long attributes over multiple lines."""
    # check that we are not inside an ignored block
    if len(
        match.group(3).strip()
    ) < config.max_attribute_length or child_of_ignored_block(
        config, html, match
    ):
        return match.group()

    leading_space = match.group(1)

    tag = match.group(2) + " "

    spacing = leading_space + len(tag) * " "

    attributes = []

    # format attributes as groups
    for attr_grp in re.finditer(
        config.attribute_pattern, match.group(3).strip(), flags=re.X
    ):
        attrib_name = attr_grp.group(1)
        is_quoted = attr_grp.group(2) and attr_grp.group(2)[0] in {"'", '"'}
        quote = attr_grp.group(2)[0] if is_quoted else '"'

        attrib_value = None

        if attr_grp.group(2) and attr_grp.group(2)[0] == attr_grp.group(2)[-1]:
            if attr_grp.group(2)[0] == "'":
                attrib_value = attr_grp.group(2).strip("'")

            elif attr_grp.group(2)[0] == '"':
                attrib_value = attr_grp.group(2).strip('"')

            else:
                attrib_value = attr_grp.group(2)
        else:
            attrib_value = attr_grp.group(2)

        standalone = attr_grp.group(3)

        quote_length = 1

        if attrib_name and attrib_value:
            # for the equals sign
            quote_length += 1

        join_space = (
            f"\n{spacing}"
            if config.format_attribute_template_tags
            else (
                f"\n{spacing}" + (quote_length + len(attrib_name or "")) * " "
            )
        )

        # format style attribute
        if attrib_name and attrib_name.lower() == "style":
            attrib_value = f";{join_space}".join(
                stripped
                for value in attrib_value.split(";")
                if (stripped := value.strip())
            )

        elif attrib_name and attrib_name.lower() in {
            "srcset",
            "data-srcset",
            "sizes",
        }:
            # vw
            attrib_value = f"w,{join_space}".join(
                stripped
                for value in attrib_value.split("w,")
                if (stripped := value.strip())
            )
            # px
            attrib_value = f"x,{join_space}".join(
                stripped
                for value in attrib_value.split("x,")
                if (stripped := value.strip())
            )

        # format JS/JSON attributes
        if (
            config.format_js_attributes
            and attrib_name
            and attrib_value
            and config.js_attribute_pattern.match(attrib_name)
        ):
            # Check if it's an object or general JavaScript code
            if config.object_braces_pattern.match(attrib_value):
                # Skip objects with fewer than minimum properties
                if (
                    count_object_properties(config, attrib_value)
                    >= config.js_attribute_minimum_properties
                ):
                    # Format JSON objects first, then JavaScript objects
                    if is_json_object(attrib_value):
                        # Calculate proper base indentation for JSON content
                        json_base_indent = (
                            spacing
                            + (quote_length + len(attrib_name or "") + 2) * " "
                        )
                        attrib_value = format_json_with_indent(
                            config, attrib_value, json_base_indent
                        )
                    else:
                        # Calculate proper base indentation for JavaScript objects
                        js_indent_size = config.js_config.get("indent_size", 4)
                        js_base_indent = (
                            spacing
                            + (
                                quote_length
                                + len(attrib_name or "")
                                + js_indent_size
                            )
                            * " "
                        )
                        # Format JavaScript objects
                        attrib_value = format_js_with_indent(
                            config, attrib_value, js_base_indent
                        )
            else:
                # Format general JavaScript code (non-objects)
                # Calculate base indentation for general JS code
                js_code_base_indent = (
                    spacing + (quote_length + len(attrib_name or "") + 0) * " "
                )
                attrib_value = format_js_with_indent(
                    config, attrib_value, js_code_base_indent
                )

        # format template stuff
        if config.format_attribute_template_tags:
            if attrib_value and attrib_name not in config.ignored_attributes:
                attrib_value = format_template_tags(
                    config,
                    attrib_value,
                    len(spacing) + len(attrib_name or "") + quote_length,
                )

            if standalone:
                standalone = format_template_tags(
                    config, standalone, len(spacing) + len(attrib_name or "")
                )

        if (attrib_name and attrib_value) or is_quoted:
            attrib_value = attrib_value or ""
            attributes.append(f"{attrib_name}={quote}{attrib_value}{quote}")
        else:
            attributes.append(
                (attrib_name or "") + (attrib_value or "") + (standalone or "")
            )
    attribute_string = f"\n{spacing}".join(x for x in attributes if x)

    close = match.group(4)

    attribute_string = f"{leading_space}{tag}{attribute_string}{close}"

    # clean trailing spaces added by breaks
    attribute_string = "\n".join(
        x.rstrip() for x in attribute_string.splitlines()
    )

    return f"{attribute_string}"
