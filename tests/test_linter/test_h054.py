"""Test linter code H054.

uv run pytest tests/test_linter/test_h054.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<a href="/x"><button>Go</button></a>'),
        (True),
        id="a button inside a link",
    ),
    pytest.param(
        ('<button><a href="/x">Go</a></button>'),
        (True),
        id="a link inside a button",
    ),
    pytest.param(
        ('<a href="/x"><input type="text"></a>'),
        (True),
        id="an input inside a link",
    ),
    pytest.param(
        ("<button><select><option>a</option></select></button>"),
        (True),
        id="a select inside a button",
    ),
    pytest.param(
        ('<a href="{{ url }}"><button type="button">x</button></a>'),
        (True),
        id="an href written by a template tag counts",
    ),
    pytest.param(
        ('<a href="/x"><span><button>deep</button></span></a>'),
        (True),
        id="the control need not be a direct child",
    ),
    pytest.param(
        ("<a href><button>x</button></a>"),
        (True),
        id="a valueless href still makes a link",
    ),
    pytest.param(
        ('<a href="/x"><textarea></textarea></a>'),
        (True),
        id="a textarea inside a link",
    ),
    pytest.param(
        ('<button type="button"><input type="file"></button>'),
        (True),
        id="a file input inside a button",
    ),
    pytest.param(
        ('<a href="/x"><a>plain</a><button>x</button></a>'),
        (True),
        id="closing a plain link does not end the one around it",
    ),
    pytest.param(
        ('<A HREF="/x"><BUTTON>x</BUTTON></A>'),
        (True),
        id="read whatever the case",
    ),
    pytest.param(
        ('<a href="/x">text</a><button>x</button>'), (False), id="siblings"
    ),
    pytest.param(
        ("<a><button>x</button></a>"),
        (False),
        id="a link with no href is not interactive",
    ),
    pytest.param(
        ("<button><span>x</span></button>"),
        (False),
        id="plain content inside a button",
    ),
    pytest.param(
        ('<a href="/x"><input type="hidden" name="t"></a>'),
        (False),
        id="a hidden input is not a control",
    ),
    pytest.param(
        ('<label><input type="checkbox"> x</label>'),
        (False),
        id="a label is not a container the rule watches",
    ),
    pytest.param(
        ('<a href="/x">1</a><a href="/y">2</a>'), (False), id="sibling links"
    ),
    pytest.param(
        ("<button>x</button><button>y</button>"), (False), id="sibling buttons"
    ),
    pytest.param(
        ('<p title="<a href=/x><button>t</button></a>">x</p>'),
        (False),
        id="markup inside an attribute value is text",
    ),
    pytest.param(
        ('<a data-href="/x"><button>x</button></a>'),
        (False),
        id="a name that merely ends in href",
    ),
    pytest.param(
        ('<a href="/x"><input type="{{ t }}"></a>'),
        (False),
        id="a type written by a template tag is unknowable",
    ),
    pytest.param(
        ("<ul><li><button>x</buton></li><li><button>y</button></li></ul>"),
        (False),
        id="a button left open ends with the element around it",
    ),
    pytest.param(
        ('{% comment %}<a href="/x"><button>x</button></a>{% endcomment %}'),
        (False),
        id="a commented out block",
    ),
    pytest.param(
        ('<a href="/x">{# djlint:off #}<button>x</button>{# djlint:on #}</a>'),
        (False),
        id="an ignored region",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h054(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H054" in codes) is reported


def test_h054_reports_the_inner_tag() -> None:
    filename = "test.html"
    config = Config(filename, profile="django")
    source = '<a href="/x">\n  <button>Go</button>\n</a>'

    findings = linter(config, source, filename, filename)[filename]
    reported = [
        (error["line"], error["match"])
        for error in findings
        if error["code"] == "H054"
    ]

    assert reported == [("2:2", "<button>")]
