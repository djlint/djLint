"""Lossless HTML tag tokenization."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Final


@final
@dataclass(
    repr=False,
    eq=False,
    frozen=True,
    match_args=False,
    kw_only=True,
    slots=True,
)
class TagToken:
    """Source positions for one HTML tag."""

    start: int
    end: int
    name_start: int
    name_end: int
    attributes_end: int
    name: str
    closing: bool
    declaration: bool
    self_closing: bool

    def span(self) -> tuple[int, int]:
        """Return the source span."""
        return self.start, self.end


_TEMPLATE_DELIMITERS: Final = MappingProxyType({"{%": "%}", "{#": "#}"})


def _after_mako_expression(source: str, start: int) -> int | None:
    """Return the end of a balanced Mako expression."""
    depth = 1
    quote: str | None = None
    cursor = start + 2
    while cursor < len(source):
        char = source[cursor]
        if quote is not None:
            if char == "\\":
                cursor += 2
                continue
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return cursor + 1
        cursor += 1
    return None


def _after_template(source: str, start: int) -> int | None:
    if source.startswith("${", start):
        return _after_mako_expression(source, start)

    if source.startswith("{{", start):
        # Handlebars allows a variable-length brace run: {{ }}, {{{ }}}
        # (triple stache) and {{{{ }}}} (raw blocks). Match the opening run
        # with an equal-length closing run so a leftover brace does not
        # abort the surrounding tag scan.
        open_length = 2
        while source[start + open_length : start + open_length + 1] == "{":
            open_length += 1
        closing = "}" * open_length
        end = source.find(closing, start + open_length)
        return end + open_length if end >= 0 else None

    closing = _TEMPLATE_DELIMITERS.get(source[start : start + 2])
    if not closing:
        return None
    end = source.find(closing, start + 2)
    return end + len(closing) if end >= 0 else None


def _next_template_opener(source: str, start: int, stop: int) -> int:
    """Return the next "{" or "$" position in [start, stop), or -1."""
    brace = source.find("{", start, stop)
    dollar = source.find("$", start, stop)
    if brace < 0:
        return dollar
    if dollar < 0:
        return brace
    return min(brace, dollar)


def _enclosing_template_end(source: str, start: int, lt: int) -> int | None:
    """End of a template expression opening in [start, lt) that spans lt.

    A "<" used as a less-than operator inside a template expression
    ({{ }}, {% %}, {# #}, ${ }) is not a tag start.
    """
    cursor = start
    while cursor < lt:
        opener = _next_template_opener(source, cursor, lt)
        if opener < 0:
            return None
        after = _after_template(source, opener)
        if after is None:
            cursor = opener + 1
        elif after > lt:
            return after
        else:
            cursor = after
    return None


def tokenize_tags(source: str) -> Iterator[TagToken]:
    """Yield tags without normalizing or copying their contents."""
    has_templates = "{" in source or "$" in source
    search_from = 0
    while (start := source.find("<", search_from)) >= 0:
        if has_templates:
            enclosing_end = _enclosing_template_end(source, search_from, start)
            if enclosing_end is not None:
                search_from = enclosing_end
                continue
        if source.startswith("<!--", start):
            comment_end = source.find("-->", start + 4)
            if comment_end < 0:
                # An unterminated "<!--" (e.g. a stray one inside a {# #}
                # template comment or a <textarea>) must not swallow the
                # rest of the document; skip the marker and keep scanning.
                search_from = start + 4
                continue
            search_from = comment_end + 3
            continue
        if source.startswith("<![CDATA[", start):
            cdata_end = source.find("]]>", start + 9)
            if cdata_end < 0:
                search_from = start + 9
                continue
            search_from = cdata_end + 3
            continue

        name_start = start + 1
        closing = source[name_start : name_start + 1] == "/"
        declaration = source[name_start : name_start + 1] == "!"
        if closing or declaration:
            name_start += 1
        if name_start >= len(source) or not source[name_start].isalpha():
            search_from = start + 1
            continue

        name_end = name_start
        while (
            name_end < len(source)
            and not source[name_end].isspace()
            and source[name_end] not in "/>{"
        ):
            name_end += 1

        quote: str | None = None
        cursor = name_end
        while cursor < len(source):
            char = source[cursor]
            # Skip over template expressions so their contents cannot end the
            # tag. Inside a quoted value, ">" / "{" / "}" are already quote
            # guarded, so only the brace-balancing "${...}" scanner runs
            # there; the naive "{{"/"{%"/"{#" search is skipped to keep a
            # quoted literal like a="{{" from consuming later "}}" content.
            if char == "$" or (char == "{" and quote is None):
                template_end = _after_template(source, cursor)
                if template_end is not None:
                    cursor = template_end
                    continue

            if char in "\"'":
                quote = (
                    None if quote == char else char if quote is None else quote
                )
            elif char in "{}" and quote is None:
                search_from = start + 1
                break
            elif char == ">" and quote is None:
                attributes_end = cursor
                while (
                    attributes_end > name_end
                    and source[attributes_end - 1].isspace()
                ):
                    attributes_end -= 1
                self_closing = (
                    source[attributes_end - 1 : attributes_end] == "/"
                )
                if self_closing:
                    attributes_end -= 1
                    while (
                        attributes_end > name_end
                        and source[attributes_end - 1].isspace()
                    ):
                        attributes_end -= 1
                yield TagToken(
                    start=start,
                    end=cursor + 1,
                    name_start=name_start,
                    name_end=name_end,
                    attributes_end=attributes_end,
                    name=source[name_start:name_end],
                    closing=closing,
                    declaration=declaration,
                    self_closing=self_closing,
                )
                search_from = cursor + 1
                break
            cursor += 1
        else:
            return
