"""Test linter code H057.

uv run pytest tests/test_linter/test_h057.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
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
        (
            '<video controls src="talk.mp4">\n  <source src="talk.webm">\n</video>'
        ),
        (True),
        id="written over several lines",
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
