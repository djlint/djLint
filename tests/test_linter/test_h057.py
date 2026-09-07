"""Test linter code H057.

uv run pytest tests/test_linter/test_h057.py
"""

from __future__ import annotations

import time

import pytest

from djlint.lint import linter
from djlint.rules import H057
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<video src="a.mp4"></video>'), (True), id="a video with no track"
    ),
    pytest.param(
        ('<video controls><source src="a.mp4" type="video/mp4"></video>'),
        (True),
        id="a source is not a track",
    ),
    pytest.param(
        (
            '<video controls><source src="a.mp4"><track kind="chapters" src="c.vtt"></video>'
        ),
        (True),
        id="chapters are not captions",
    ),
    pytest.param(
        (
            '<video controls><track kind="metadata" src="m.vtt"><track kind="descriptions" src="d.vtt"></video>'
        ),
        (True),
        id="nor are metadata and descriptions",
    ),
    pytest.param(
        ('<video controls><track kind="captionsxyz" src="c.vtt"></video>'),
        (True),
        id="nor is a kind that merely starts with captions",
    ),
    pytest.param(
        ('<video controls><track kind="subtitles-en" src="c.vtt"></video>'),
        (True),
        id="nor one that merely starts with subtitles",
    ),
    pytest.param(
        ('<video data-muted="true" src="a.mp4"></video>'),
        (True),
        id="a name that merely ends in muted",
    ),
    pytest.param(
        ('<video title="a muted clip" src="a.mp4"></video>'),
        (True),
        id="muted written inside a value",
    ),
    pytest.param(
        ('<video class=muted src="a.mp4"></video>'),
        (True),
        id="muted written as an unquoted value",
    ),
    pytest.param(
        ('<video data-state=muted src="a.mp4"></video>'),
        (True),
        id="and as an unquoted value of a data attribute",
    ),
    pytest.param(
        (
            '<video controls src="talk.mp4">\n  <source src="talk.webm">\n</video>'
        ),
        (True),
        id="written over several lines",
    ),
    pytest.param(
        ('<video src="a.mp4"></video >'),
        (True),
        id="an end tag with a space before its bracket",
    ),
    pytest.param(
        ('<video src="a.mp4"></video\n>'),
        (True),
        id="an end tag with a line break before its bracket",
    ),
    pytest.param(
        ('<video src="a.mp4"></video\t>'),
        (True),
        id="an end tag with a tab before its bracket",
    ),
    pytest.param(
        ('<video src="a.mp4" onclick="$(this).play()"></video>'),
        (True),
        id="a jquery handler is not a template tag",
    ),
    pytest.param(
        ('<video x-on:click="$refs.v.play()" src="a.mp4"></video>'),
        (True),
        id="nor is an alpine magic",
    ),
    pytest.param(
        ('<video @click="$emit(\'play\')" src="a.mp4"></video>'),
        (True),
        id="nor is a vue handler",
    ),
    pytest.param(
        ('<video :style="{width: w}" src="a.mp4"></video>'),
        (True),
        id="nor is a vue binding",
    ),
    pytest.param(
        ('<video src="a.mp4" style="--ratio:{16/9}"></video>'),
        (True),
        id="nor is a brace in a css value",
    ),
    pytest.param(
        ('<video src="a.mp4" data-cost="$5"></video>'),
        (True),
        id="nor is a price in a value",
    ),
    pytest.param(
        ('<video src="a.mp4">Only $5 a month</video>'),
        (True),
        id="nor is a price in the fallback text",
    ),
    pytest.param(
        ('<video src="a.mp4"><p>Cost: $9.99</p></video>'),
        (True),
        id="nor is one written in a paragraph",
    ),
    pytest.param(
        ('<video src="a.mp4"><style>.v{color:red}</style></video>'),
        (True),
        id="nor is a brace in a style block",
    ),
    pytest.param(
        ('<video src="a.mp4">Use the {menu} to play</video>'),
        (True),
        id="nor is a brace in the fallback text",
    ),
    pytest.param(
        ('<video src="a.mp4"><a href="a.mp4?x=1&amp;y={2}">dl</a></video>'),
        (True),
        id="nor is a brace in a url",
    ),
    pytest.param(
        ('<video controls><!-- <track kind="captions"> --></video>'),
        (True),
        id="a track that is commented out is not a track",
    ),
    pytest.param(
        (
            '<video controls><source src="a.mp4" data-note="<track kind=captions>"></video>'
        ),
        (True),
        id="nor is one written inside a value",
    ),
    pytest.param(
        (
            '<video controls><source src="a.mp4"><track kind="captions" src="c.vtt"></video>'
        ),
        (False),
        id="a captions track",
    ),
    pytest.param(
        ("<video controls><track kind='subtitles' src=\"c.vtt\"></video>"),
        (False),
        id="a subtitles track in single quotes",
    ),
    pytest.param(
        ('<video controls><track kind=captions src="c.vtt"></video>'),
        (False),
        id="a kind written without quotes",
    ),
    pytest.param(
        ('<video controls><track kind="CAPTIONS" src="c.vtt"></video>'),
        (False),
        id="the kind is read whatever its case",
    ),
    pytest.param(
        ('<video controls><track src="c.vtt"></video>'),
        (False),
        id="a track with no kind is subtitles by default",
    ),
    pytest.param(
        (
            '<video controls><track kind="chapters" src="c.vtt"><track kind="subtitles" src="s.vtt"></video>'
        ),
        (False),
        id="a subtitles track among others",
    ),
    pytest.param(
        (
            '<video controls><source src="a.mp4" data-x="</video>"><track kind="captions" src="c.vtt"></video>'
        ),
        (False),
        id="an end tag written inside a value ends nothing",
    ),
    pytest.param(
        ('<video muted autoplay loop src="bg.mp4"></video>'),
        (False),
        id="a muted video has no audio to caption",
    ),
    pytest.param(
        ('<video muted="muted" src="bg.mp4"></video>'),
        (False),
        id="muted written with a value",
    ),
    pytest.param(
        (
            '<video controls>{% for t in tracks %}<track kind="captions" src="{{ t }}">{% endfor %}</video>'
        ),
        (False),
        id="tracks written by a template loop",
    ),
    pytest.param(
        ('<video controls>{% include "tracks.html" %}</video>'),
        (False),
        id="tracks written by an include",
    ),
    pytest.param(
        ('<video {% if bg %}muted{% endif %} src="a.mp4"></video>'),
        (False),
        id="a template tag among the attributes",
    ),
    pytest.param(
        (
            '<video title="a>b" {% if v.silent %}muted{% endif %} src="{{ v.url }}"></video>'
        ),
        (False),
        id="a bracket in a value hides no template tag",
    ),
    pytest.param(
        (
            '<video controls aria-label="Home > Videos" poster="{{ v.poster }}"></video>'
        ),
        (False),
        id="nor does one written in a label",
    ),
    pytest.param(
        ('<video-js src="a.mp4"></video-js>'),
        (False),
        id="a custom element whose name starts with video",
    ),
    pytest.param(
        ('<p title="<video></video>">x</p>'),
        (False),
        id="markup written inside an attribute value",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h057(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H057" in codes) is reported


def test_h057_reads_unclosed_videos_in_one_pass() -> None:
    """A video left open must not send the scan over the rest of the file.

    Every opening tag used to re-scan everything after it, twice, so a
    74 kb file of them took five seconds and a 144 kb one took twenty two.
    """
    filename = "test.html"
    config = Config(filename, profile="django")
    source = (
        '<video controls preload="none" src="/media/clip.mp4"'
        ' poster="/img/p.jpg">\n'
    ) * 1000
    rule = {"name": "H057", "message": "Video should have a captions track."}

    start = time.perf_counter()
    findings = H057.run(rule, config, source, filename, [])

    assert findings == ()
    assert time.perf_counter() - start < 2


def test_h057_reads_a_run_of_opening_tags_in_one_pass() -> None:
    """A bare tag repeated costs no more than the tags themselves."""
    filename = "test.html"
    config = Config(filename, profile="django")
    source = "<video>" * 8000
    rule = {"name": "H057", "message": "Video should have a captions track."}

    start = time.perf_counter()
    findings = H057.run(rule, config, source, filename, [])

    assert findings == ()
    assert time.perf_counter() - start < 2
