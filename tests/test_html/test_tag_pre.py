"""Test html pre tag.

uv run pytest tests/test_html/test_tag_pre.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

# added for https://github.com/djlint/djLint/issues/187
test_data = [
    pytest.param(
        (
            "{% if a %}\n"
            "    <div>\n"
            "        <pre><code>asdf</code></pre>\n"
            "        <pre><code>asdf\n"
            "            </code></pre>\n"
            "        <!-- other html -->\n"
            "        <h2>title</h2>\n"
            "    </div>\n"
            "{% endif %}\n"
        ),
        (
            "{% if a %}\n"
            "    <div>\n"
            "        <pre><code>asdf</code></pre>\n"
            "        <pre><code>asdf\n"
            "            </code></pre>\n"
            "        <!-- other html -->\n"
            "        <h2>title</h2>\n"
            "    </div>\n"
            "{% endif %}\n"
        ),
        id="pre_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output


@pytest.mark.parametrize(
    "source",
    [
        pytest.param(
            "<div>\n    <pre>&lt;!-- x -->\n   indented\ntail</pre>\n</div>\n",
            id="escaped_comment_close",
        ),
        pytest.param(
            "<div>\n"
            "    <pre>{# djlint:off H025 #}\n"
            "{# djlint:on #}\n"
            "<span></pre>\n"
            "</div>\n",
            id="djlint_pragmas_as_content",
        ),
        pytest.param(
            '{{#if}}\n<pre class="language-html">\n{# djlint:on #}\n',
            id="handlebars_section_is_not_a_jinja_comment",
        ),
    ],
)
def test_markers_in_pre_are_content(source: str, basic_config: Config) -> None:
    """Text that looks like a marker must not end the verbatim block.

    Reformatting must reach a fixed point; these used to add an indent
    level to the pre contents on every run.
    """
    once = formatter(basic_config, source)
    twice = formatter(basic_config, once)

    printer(once, source, twice)
    assert once == twice
