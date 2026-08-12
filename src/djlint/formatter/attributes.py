"""Format attributes."""

from __future__ import annotations

import json
from functools import partial
from typing import TYPE_CHECKING

import regex as re

from djlint.formatter.class_attributes import (
    CLASS_ATTRIBUTE_NEWLINE,
    VERBATIM_ATTRIBUTE_NEWLINE,
    decode_class_attribute_newlines,
    restore_verbatim_attribute_newlines,
)
from djlint.helpers import (
    RE_FLAGS_IMX,
    RE_FLAGS_IS,
    RE_FLAGS_IX,
    child_of_ignored_block,
)

if TYPE_CHECKING:
    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config

_QUOTED_VALUE_PATTERN = re.compile(r"\"[^\"]*\"|'[^']*'", cache_pattern=False)

# values spread over several lines are flattened with a space at each line
# break, including the ones against the quotes. These attributes are rewritten
# from stripped parts, so that padding never reaches the output.
_PADDED_VALUE_PATTERN = re.compile(
    r"\b(?:style|srcset|data-srcset|sizes)[ \t]*=[ \t]*([\"'])(.*?)\1",
    RE_FLAGS_IS,
    cache_pattern=False,
)


def _rendered_length(config: Config, attribute_group: str) -> int:
    """Length of the attribute group as it will be written out.

    Measuring padding that the rewrite drops spreads a tag whose attributes
    then fit on one line again on the next run.
    """
    length = len(attribute_group)
    if length < config.max_attribute_length:
        return length

    return length - sum(
        len(value) - len(value.strip())
        for match in _PADDED_VALUE_PATTERN.finditer(attribute_group)
        if (value := match.group(2))
    )


def has_unquoted_template_expression(attribute_group: str) -> bool:
    """Check for a ${...} template expression outside quoted values."""
    return "${" in attribute_group and "${" in _QUOTED_VALUE_PATTERN.sub(
        "", attribute_group
    )


def count_object_properties(config: Config, value: str) -> int:
    """Count the number of properties in a JSON/JS object."""
    try:
        data = json.loads(value)
        return len(data)
    except json.JSONDecodeError:
        # not json, so fall back to counting comma separated properties.
        # strings go first, or a comma inside one counts as a separator.
        cleaned = config.format_attribute_js_json_string_pattern.sub("", value)
        return len(
            config.format_attribute_js_json_property_pattern.findall(cleaned)
        )


def is_json_object(value: str) -> bool:
    """Check if attribute value is a valid JSON object."""
    try:
        json.loads(value)
    except json.JSONDecodeError:
        return False
    else:
        return True


def format_json_with_indent(
    config: Config, value: str, base_indent: str
) -> str:
    """Format JSON with proper HTML-relative indentation."""
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        return value
    else:
        indent_size = config.js_config.get("indent_size", 4)
        formatted = json.dumps(data, indent=indent_size)
        # json.dumps indents from column 0, so the attribute's own indentation
        # goes in front of every line but the first, which follows the quote.
        # the closing brace sits one level back from the properties.
        lines = formatted.split("\n")
        if len(lines) > 1:
            indented_lines = [lines[0]]
            for i, line in enumerate(lines[1:], 1):
                if i == len(lines) - 1:
                    content_indent = base_indent + (" " * indent_size)
                    if len(content_indent) >= indent_size:
                        closing_indent = content_indent[:-indent_size]
                    else:
                        closing_indent = base_indent
                    indented_lines.append(closing_indent + line)
                else:
                    indented_lines.append(base_indent + line)
            return "\n".join(indented_lines)
        return formatted


def format_js_with_indent(config: Config, value: str, base_indent: str) -> str:
    """Format JavaScript code/object with proper HTML-relative indentation."""
    import jsbeautifier  # noqa: PLC0415
    from jsbeautifier.javascript.options import (  # noqa: PLC0415
        BeautifierOptions,
    )

    try:
        # the same config the main js formatter uses, except that the
        # attribute's indentation is added below, so jsbeautifier adds none.
        js_config = dict(config.js_config)
        js_config["indent_level"] = 0

        opts = BeautifierOptions(js_config)
        formatted: str = jsbeautifier.beautify(value, opts)
    except ValueError:
        return value
    else:
        # keep jsbeautifier's relative indentation and put the attribute's own
        # in front of it. the first line follows the quote, so it takes none.
        lines = formatted.split("\n")
        if len(lines) > 1:
            indented_lines = [lines[0].strip()]

            for i, line in enumerate(lines[1:], 1):
                if not line.strip():
                    indented_lines.append("")
                    continue

                line_indent = len(line) - len(line.lstrip())

                is_object = value.strip().startswith(
                    "{"
                ) and value.strip().endswith("}")

                if is_object and i == len(lines) - 1:
                    indented_lines.append(
                        base_indent + (" " * line_indent) + line.strip()
                    )
                else:
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
        template_unindent_pattern = re.compile(
            config.template_unindent, RE_FLAGS_IX
        )
        tag_unindent_line_pattern = re.compile(
            config.tag_unindent_line, RE_FLAGS_IX
        )
        template_indent_pattern = re.compile(
            config.template_indent, RE_FLAGS_IX
        )

        indent = 0
        indented = ""
        indent_adder = spacing or 0

        for line_number, line in enumerate(attributes.splitlines()):
            # when checking for template tag, use "match" to force start of line check.
            if template_unindent_pattern.match(line.strip()):
                indent -= 1
                tmp = (
                    (indent * config.indent)
                    + (indent_adder * " ")
                    + line.strip()
                )

            elif tag_unindent_line_pattern.match(line.strip()):
                # if we are leaving an indented group, then remove the indent_adder
                tmp = (
                    max(indent - 1, 0) * config.indent
                    + indent_adder * " "
                    + line.strip()
                )

            elif template_indent_pattern.search(
                line.strip()
            ) and not template_unindent_pattern.search(line.strip()):
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
        + r"[ \t]\K((?:{%|{{\#)[ ]*?(?:"
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
        + ")[^}]+?[%|}]})(?=[ \t])([^\n]+)$",
        func,
        attributes,
        flags=RE_FLAGS_IMX,
    )
    return add_indentation(config, attributes, spacing)


def format_attributes(config: Config, html: str, token: TagToken) -> str:
    """Spread long attributes over multiple lines."""
    # check that we are not inside an ignored block
    attribute_group = html[token.name_end : token.attributes_end].strip()
    if (
        has_unquoted_template_expression(attribute_group)
        or (
            _rendered_length(config, attribute_group)
            < config.max_attribute_length
            # a value that keeps a line break of its own spans lines
            # whatever its length, so the tag never fits on one
            and CLASS_ATTRIBUTE_NEWLINE not in attribute_group
            and VERBATIM_ATTRIBUTE_NEWLINE not in attribute_group
        )
    ) or child_of_ignored_block(config, html, token):
        return html[token.start : token.end]

    if not config.format_attribute_template_tags:
        template_depth = 0
        for template_tag in re.finditer(
            config.template_tags, attribute_group, flags=RE_FLAGS_IMX
        ):
            if re.match(
                config.template_unindent,
                template_tag.group(),
                flags=RE_FLAGS_IMX,
            ):
                template_depth = max(template_depth - 1, 0)
            elif re.match(
                config.template_indent, template_tag.group(), flags=RE_FLAGS_IMX
            ):
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

    # the tag is rebuilt from the matched attribute groups, so any
    # non-whitespace byte the pattern cannot match would be dropped. Bail out
    # and leave malformed attributes untouched rather than corrupting them.
    attribute_matches = list(
        re.finditer(config.attribute_pattern, attribute_group, flags=re.X)
    )
    covered = 0
    for attr_grp in attribute_matches:
        if attribute_group[covered : attr_grp.start()].strip():
            return html[token.start : token.end]
        if attr_grp.group(1) is None and attr_grp.group().strip().startswith(
            "="
        ):
            # a nameless "=value" attribute is malformed; leave the tag
            # untouched rather than emitting a bogus "None=" attribute.
            # (template-conditional attributes like "{% if x %}sel{% endif %}"
            # also have no name group but must still be formatted.)
            return html[token.start : token.end]
        covered = attr_grp.end()
    if attribute_group[covered:].strip():
        return html[token.start : token.end]

    # format attributes as groups
    for attr_grp in attribute_matches:
        # Match.group() rebuilds the string from the span on every call, so
        # pull the three groups out once instead of re-slicing per branch.
        attrib_name, raw_value, standalone = attr_grp.group(1, 2, 3)
        first_char = raw_value[0] if raw_value else ""
        is_quoted = first_char in {"'", '"'}
        quote = first_char if is_quoted else '"'

        if is_quoted and first_char == raw_value[-1]:
            attrib_value = raw_value.strip(first_char)
        else:
            attrib_value = raw_value

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

        # format JS/JSON attributes. values with preserved verbatim line
        # breaks are skipped: the beautifier would mangle the marker.
        if (
            config.format_attribute_js_json
            and attrib_name
            and attrib_value
            and VERBATIM_ATTRIBUTE_NEWLINE not in attrib_value
            and config.format_attribute_js_json_pattern.match(attrib_name)
        ):
            if config.format_attribute_js_json_object_pattern.match(
                attrib_value
            ):
                # an object short enough to read on one line is left there.
                if (
                    count_object_properties(config, attrib_value)
                    >= config.format_attribute_js_json_min_props
                ):
                    # the value starts after the attribute name and its quote,
                    # so that is where its content lines up.
                    if is_json_object(attrib_value):
                        json_base_indent = (
                            spacing
                            + (quote_length + len(attrib_name or "")) * " "
                        )
                        attrib_value = format_json_with_indent(
                            config, attrib_value, json_base_indent
                        )
                    else:
                        js_base_indent = (
                            spacing
                            + (quote_length + len(attrib_name or "")) * " "
                        )
                        attrib_value = format_js_with_indent(
                            config, attrib_value, js_base_indent
                        )
            else:
                # not an object, so js code with no property count to check.
                js_code_base_indent = (
                    spacing + (quote_length + len(attrib_name or "")) * " "
                )
                attrib_value = format_js_with_indent(
                    config, attrib_value, js_code_base_indent
                )

        # format template stuff
        if config.format_attribute_template_tags:
            # only spread values whose whitespace collapses when rendered;
            # other values (title, alt, data-*, ...) are shown verbatim and
            # an added line break would change the rendered output.
            if (
                attrib_value
                and attrib_name
                and attrib_name.lower() in {"class", "style"}
                and attrib_name not in config.ignored_attributes
            ):
                attrib_value = format_template_tags(
                    config,
                    attrib_value,
                    len(spacing) + len(attrib_name or "") + quote_length,
                )

            if standalone:
                standalone = format_template_tags(
                    config, standalone, len(spacing) + len(attrib_name or "")
                )

        if (
            config.preserve_class_newlines
            and attrib_name
            and attrib_name.lower() == "class"
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

    # clean trailing spaces added by breaks
    attribute_string = "\n".join(
        x.rstrip() for x in attribute_string.splitlines()
    )

    return f"{attribute_string}"
