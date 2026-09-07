"""Rule H057: Check for a video with no captions track.

A video with sound carries its speech only in the audio, so a deaf or
hard-of-hearing viewer gets nothing from it without captions, which WCAG
1.2.2 requires. A `<track>` whose `kind` is `captions` or `subtitles`
satisfies the rule, and so does one with no `kind` at all, since
subtitles is the default.

Only what the markup says for certain is judged. A `muted` video has no
audio to caption, and the tracks, or the `muted` attribute itself, may be
written by a template tag, so a video whose opening tag or body holds
template syntax is left alone. Template syntax means an opener a template
language actually writes, `{{`, `{%`, `{#` or `${`, rather than any `{`
or `$`, so a jQuery handler, an Alpine `$refs`, a css custom property and
a price written in the fallback text are read as the ordinary text they
are.

Markup is read the way the tag tokenizer reads it, so `muted` written as
an attribute *value*, a `</video>` written inside an attribute value, and
a `<track>` that is commented out or quoted inside a value are text
rather than markup. The element is judged when its `</video>` closes it;
one left open holds no body a browser would end and is left to `H025`.
"""

from __future__ import annotations

from bisect import bisect_left
from operator import itemgetter
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    mask_raw_text_bodies,
    overlaps_ignored_block,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from typing import Final

    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError

_CAPTION_KINDS: Final = frozenset(("captions", "subtitles"))

_position: Final = itemgetter(0)

# the openers a template language writes, so that a lone "{" or "$" -- a
# css brace, a jQuery call, a price -- is not read as one
_TEMPLATE_OPENING_PATTERN: Final = re.compile(
    r"\{[{%#]|\$\{", cache_pattern=False
)

# one attribute of a tag's attribute area: a name, and the value written
# after an "=" in double quotes, single quotes or none at all. The name
# stops where a name has to stop, so an unquoted value is a value rather
# than a second attribute and `class=muted` is not the muted attribute.
_ATTRIBUTE_PATTERN: Final = re.compile(
    r"""(?P<name>[^\s/>="'<]+)"""
    r"""(?:\s*=\s*(?:"(?P<double>[^"]*)"|'(?P<single>[^']*)'"""
    r"""|(?P<bare>[^\s"'=<>`]*)))?""",
    re.S,
    cache_pattern=False,
)


def _attributes(area: str) -> Iterator[tuple[str, str | None]]:
    """Yield each attribute of the area, name lowered, with its raw value.

    An attribute written with no value at all yields None, which is not
    the same as the empty string an `=""` writes.
    """
    for match in _ATTRIBUTE_PATTERN.finditer(area):
        double, single, bare = match.group("double", "single", "bare")
        if double is not None:
            value: str | None = double
        elif single is not None:
            value = single
        else:
            value = bare
        yield match.group("name").lower(), value


def _is_muted(area: str) -> bool:
    """Whether the opening tag carries the muted attribute.

    The word is looked for before the attributes are read, because
    reading them is the expensive half and a tag without the word
    anywhere cannot be writing that attribute.
    """
    if "muted" not in area.casefold():
        return False
    return any(name == "muted" for name, _ in _attributes(area))


def _is_caption_track(area: str) -> bool:
    """Whether the track counts as the captions or subtitles of a video.

    A track with no `kind`, with an empty one, or with one a template tag
    writes is read as the default, subtitles. Only the first `kind` is
    read, as a browser reads it, and it has to name the kind exactly:
    `captionsxyz` is not `captions`.
    """
    for name, value in _attributes(area):
        if name != "kind":
            continue
        if value is None:
            return True
        kind = value.strip()
        return (
            not kind
            or _TEMPLATE_OPENING_PATTERN.search(kind) is not None
            or kind.casefold() in _CAPTION_KINDS
        )
    return True


def _comment_spans(html: str) -> tuple[tuple[int, int], ...]:
    """The html comments of the document, which hold text, not markup.

    Each search starts where the last comment ended, so a document of
    them is read in one pass.
    """
    spans: list[tuple[int, int]] = []
    position = 0
    while (start := html.find("<!--", position)) >= 0:
        end = html.find("-->", start + 4)
        if end < 0:
            spans.append((start, len(html)))
            break
        spans.append((start, end + 3))
        position = end + 3
    return tuple(spans)


def _template_positions(html: str) -> tuple[int, ...]:
    """Where a template tag opens, skipping the ones a comment quotes.

    Both sequences run forward together, so the whole document costs one
    pass rather than a lookup for every opener.
    """
    comments = _comment_spans(html)
    index = 0
    positions: list[int] = []
    for match in _TEMPLATE_OPENING_PATTERN.finditer(html):
        start = match.start()
        while index < len(comments) and comments[index][1] <= start:
            index += 1
        if index < len(comments) and comments[index][0] <= start:
            continue
        positions.append(start)
    return tuple(positions)


def _holds_template(positions: Sequence[int], start: int, end: int) -> bool:
    """Whether a template tag opens in the half open span."""
    index = bisect_left(positions, start)
    return index < len(positions) and positions[index] < end


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for a video with no captions track.

    Every `<video>` is pushed and its `</video>` pops it, so the body is
    whatever the tokenizer read between them and each tag of the document
    is read once however broken the markup is. A caption track satisfies
    every video still open around it, which is counted rather than
    written to each one.
    """
    found: list[tuple[int, LintError]] = []
    masked = mask_raw_text_bodies(html)
    template_positions = _template_positions(masked)
    # a track satisfies every video open around it, so the count at the
    # time a video opened tells whether one was written in its body
    caption_tracks = 0
    open_videos: list[tuple[TagToken, int]] = []

    for token in tokenize_markup(html):
        if token.declaration:
            continue
        name = token.name.casefold()

        if name == "track":
            if not token.closing and not overlaps_ignored_block(
                config, html, token
            ):
                area = html[token.name_end : token.attributes_end]
                caption_tracks += _is_caption_track(area)
            continue

        if name != "video":
            continue

        if not token.closing:
            open_videos.append((token, caption_tracks))
            continue

        if not open_videos:
            continue
        opening, captions_before = open_videos.pop()
        if (
            caption_tracks > captions_before
            or _is_muted(html[opening.name_end : opening.attributes_end])
            or _TEMPLATE_OPENING_PATTERN.search(
                html, opening.start, opening.end
            )
            or _holds_template(template_positions, opening.end, token.start)
            or overlaps_ignored_block(config, html, opening)
            or inside_ignored_rule(config, html, opening, rule["name"])
            or inside_ignored_linter_block(config, html, opening)
        ):
            continue

        found.append((
            opening.start,
            {
                "code": rule["name"],
                "line": get_line(opening.start, line_ends),
                "match": html[opening.start : token.end].strip()[:20],
                "message": rule["message"],
            },
        ))

    # a video nested in another closes first, so the findings are put
    # back into the order the videos are written in
    found.sort(key=_position)
    return tuple(error for _, error in found)
