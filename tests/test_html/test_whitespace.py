"""Test whitespace.

uv run pytest tests/test_html/test_whitespace.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        (
            "<a>Lorem</a>, ispum dolor sit <strong>amet</strong>.\n"
            "<div><a>Lorem</a>, ispum dolor sit <strong>amet</strong>.</div>\n"
            "<div><div><a>Lorem</a>, ispum dolor sit <strong>amet</strong>.</div></div>\n"
        ),
        (
            "<a>Lorem</a>, ispum dolor sit <strong>amet</strong>.\n"
            "<div>\n"
            "    <a>Lorem</a>, ispum dolor sit <strong>amet</strong>.\n"
            "</div>\n"
            "<div>\n"
            "    <div>\n"
            "        <a>Lorem</a>, ispum dolor sit <strong>amet</strong>.\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="break_tags",
    ),
    pytest.param(
        (
            "<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "<button>\n"
            "Click here! Click here! Click here! Click here! Click here! Click here!\n"
            "</button>\n"
            "<div>\n"
            "<button>Click here! Click here! Click here! Click here! Click here! Click here!</button><button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "</div>\n"
            "<div>\n"
            "<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "</div>\n"
            '<video src="brave.webm"><track kind=subtitles src=brave.en.vtt srclang=en label="English"><track kind=subtitles src=brave.en.vtt srclang=en label="English"></video>\n'
        ),
        (
            "<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "<div>\n"
            "    <button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "    <button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "</div>\n"
            "<div>\n"
            "    <button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "    <button>Click here! Click here! Click here! Click here! Click here! Click here!</button>\n"
            "</div>\n"
            '<video src="brave.webm">\n'
            '    <track kind=subtitles src=brave.en.vtt srclang=en label="English">\n'
            '    <track kind=subtitles src=brave.en.vtt srclang=en label="English">\n'
            "</video>\n"
        ),
        id="display_inline_block",
    ),
    pytest.param(
        (
            '<!DOCTYPE html><HTML CLASS="no-js mY-ClAsS"><HEAD><META CHARSET="utf-8"><TITLE>My tITlE</TITLE><META NAME="description" content="My CoNtEnT"></HEAD></HTML>\n'
        ),
        (
            "<!DOCTYPE html>\n"
            '<html CLASS="no-js mY-ClAsS">\n'
            "    <head>\n"
            '        <meta CHARSET="utf-8">\n'
            "        <title>My tITlE</title>\n"
            '        <meta NAME="description" content="My CoNtEnT">\n'
            "    </head>\n"
            "</html>\n"
        ),
        id="display_none",
    ),
    pytest.param(
        (
            "<p>\n"
            "  <img\n"
            '    src="/images/pansies.jpg"\n'
            '    alt="about fedco bottom image"\n'
            '    style="float: left;"\n'
            "  /><strong>We are a cooperative</strong>, one of the few seed companies so organized\n"
            "  in the United States. Because we do not have an individual owner or beneficiary,\n"
            "  profit is not our primary goal. Consumers own 60% of the cooperative and worker\n"
            "  members 40%. Consumer and worker members share proportionately in the cooperative&#8217;s\n"
            "  profits through our annual patronage dividends.\n"
            "</p>\n"
        ),
        (
            "<p>\n"
            '    <img src="/images/pansies.jpg"\n'
            '         alt="about fedco bottom image"\n'
            '         style="float: left" />\n'
            "    <strong>We are a cooperative</strong>, one of the few seed companies so organized\n"
            "    in the United States. Because we do not have an individual owner or beneficiary,\n"
            "    profit is not our primary goal. Consumers own 60% of the cooperative and worker\n"
            "    members 40%. Consumer and worker members share proportionately in the cooperative&#8217;s\n"
            "    profits through our annual patronage dividends.\n"
            "</p>\n"
        ),
        id="fill",
    ),
    pytest.param(
        ("<span> 321 </span>\n\n<span> <a>321</a> </span>\n"),
        ("<span>321</span>\n<span> <a>321</a> </span>\n"),
        id="inline_leading_trailing_spaces",
    ),
    pytest.param(
        (
            "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa vel augue\n"
            "vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet urna consectetur dignissim.\n"
            "Sam vitae neque quis ex dapibus faucibus at sed ligula. Nulla sit amet aliquet nibh.\n"
            "Vestibulum at congue mi. Suspendisse vitae odio vitae massa hendrerit mattis sed eget dui.\n"
            "Sed eu scelerisque neque. Donec <b>maximus</b> rhoncus pellentesque. Aenean purus turpis, vehicula\n"
            "euismod ante vel, ultricies eleifend dui. Class aptent taciti sociosqu ad litora torquent per\n"
            "conubia nostra, per inceptos himenaeos. Donec in ornare velit.</p>\n"
            "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa vel augue\n"
            "vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet urna consectetur dignissim.\n"
            "Sam vitae neque quis ex dapibus faucibus at sed ligula. Nulla sit amet aliquet nibh.\n"
            "Vestibulum at congue mi. Suspendisse vitae odio vitae massa hendrerit mattis sed eget dui.\n"
            'Sed eu scelerisque neque. Donec <a href="#"><b>maximus</b></a> rhoncus pellentesque. Aenean purus turpis, vehicula\n'
            "euismod ante vel, ultricies eleifend dui. Class aptent taciti sociosqu ad litora torquent per\n"
            "conubia nostra, per inceptos himenaeos. Donec in ornare velit.</p>\n"
        ),
        (
            "<p>\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa vel augue\n"
            "    vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet urna consectetur dignissim.\n"
            "    Sam vitae neque quis ex dapibus faucibus at sed ligula. Nulla sit amet aliquet nibh.\n"
            "    Vestibulum at congue mi. Suspendisse vitae odio vitae massa hendrerit mattis sed eget dui.\n"
            "    Sed eu scelerisque neque. Donec <b>maximus</b> rhoncus pellentesque. Aenean purus turpis, vehicula\n"
            "    euismod ante vel, ultricies eleifend dui. Class aptent taciti sociosqu ad litora torquent per\n"
            "    conubia nostra, per inceptos himenaeos. Donec in ornare velit.\n"
            "</p>\n"
            "<p>\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa vel augue\n"
            "    vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet urna consectetur dignissim.\n"
            "    Sam vitae neque quis ex dapibus faucibus at sed ligula. Nulla sit amet aliquet nibh.\n"
            "    Vestibulum at congue mi. Suspendisse vitae odio vitae massa hendrerit mattis sed eget dui.\n"
            '    Sed eu scelerisque neque. Donec <a href="#"><b>maximus</b></a> rhoncus pellentesque. Aenean purus turpis, vehicula\n'
            "    euismod ante vel, ultricies eleifend dui. Class aptent taciti sociosqu ad litora torquent per\n"
            "    conubia nostra, per inceptos himenaeos. Donec in ornare velit.\n"
            "</p>\n"
        ),
        id="inline_nodes",
    ),
    pytest.param(
        (
            '    <a href="/wiki/Help:IPA/English" title="Help:IPA/English">/<span style="border-bottom:1px dotted"><span title="/ˌ/: secondary stress follows">ˌ</span\n'
            '><span title="/ɪ/: &#39;i&#39; in &#39;kit&#39;">ɪ</span\n'
            '><span title="&#39;l&#39; in &#39;lie&#39;">l</span\n'
            '><span title="/ə/: &#39;a&#39; in &#39;about&#39;">ə</span\n'
            '><span title="/ˈ/: primary stress follows">ˈ</span\n'
            '><span title="&#39;n&#39; in &#39;nigh&#39;">n</span\n'
            '><span title="/ɔɪ/: &#39;oi&#39; in &#39;choice&#39;">ɔɪ</span></span>/</a>\n'
            '<span class="word"><span class="syllable"><span class="letter vowel">i</span><span class="letter consonant">p</span></span\n'
            '><span class="syllable"><span class="letter consonant onset">s</span><span class="letter vowel">u</span><span class="letter consonant">m</span></span></span>\n'
        ),
        (
            '<a href="/wiki/Help:IPA/English" title="Help:IPA/English">/<span style="border-bottom:1px dotted"><span title="/ˌ/: secondary stress follows">ˌ</span><span title="/ɪ/: &#39;i&#39; in &#39;kit&#39;">ɪ</span><span title="&#39;l&#39; in &#39;lie&#39;">l</span><span title="/ə/: &#39;a&#39; in &#39;about&#39;">ə</span><span title="/ˈ/: primary stress follows">ˈ</span><span title="&#39;n&#39; in &#39;nigh&#39;">n</span><span title="/ɔɪ/: &#39;oi&#39; in &#39;choice&#39;">ɔɪ</span></span>/</a>\n'
            '<span class="word"><span class="syllable"><span class="letter vowel">i</span><span class="letter consonant">p</span></span><span class="syllable"><span class="letter consonant onset">s</span><span class="letter vowel">u</span><span class="letter consonant">m</span></span></span>\n'
        ),
        id="nested_inline_without_whitespace",
    ),
    pytest.param(
        (
            "<!-- normal whitespaces -->\n"
            "<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span>\n"
            "<!-- non-breaking whitespaces -->\n"
            "<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span>\n"
            "<!-- non-breaking narrow whitespaces -->\n"
            "<span>Prix : 32 €</span>\n"
            "    )\n"
            "\n"
            "    html_out = (\n"
            "<!-- normal whitespaces -->\n"
            "<span\n"
            "    >Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores\n"
            "    voluptas quaerat ut qui sunt vitae error.</span\n"
            ">\n"
            "<!-- non-breaking whitespaces -->\n"
            "<span\n"
            "    >Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span\n"
            ">\n"
            "<!-- non-breaking narrow whitespaces -->\n"
            "<span>Prix : 32 €</span>\n"
        ),
        (
            "<!-- normal whitespaces -->\n"
            "<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span>\n"
            "<!-- non-breaking whitespaces -->\n"
            "<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span>\n"
            "<!-- non-breaking narrow whitespaces -->\n"
            "<span>Prix : 32 €</span>\n"
            ")\n"
            "html_out = (\n"
            "<!-- normal whitespaces -->\n"
            "<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores\n"
            "voluptas quaerat ut qui sunt vitae error.</span>\n"
            "<!-- non-breaking whitespaces -->\n"
            "<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span>\n"
            "<!-- non-breaking narrow whitespaces -->\n"
            "<span>Prix : 32 €</span>\n"
        ),
        id="non_breaking_whitespace",
    ),
    pytest.param(("<div> </div>\n"), ("<div></div>\n"), id="snippet_18"),
    pytest.param(
        ("<div>          </div>\n"), ("<div></div>\n"), id="snippet_19"
    ),
    pytest.param(
        ("<div>           </div>\n"), ("<div></div>\n"), id="snippet_20"
    ),
    pytest.param(
        ("<div>                   </div>\n"), ("<div></div>\n"), id="snippet_21"
    ),
    pytest.param(("<span> </span>\n"), ("<span></span>\n"), id="snippet_22"),
    pytest.param(
        ("<span>          </span>\n"), ("<span></span>\n"), id="snippet_23"
    ),
    pytest.param(
        ("<span>           </span>\n"), ("<span></span>\n"), id="snippet_24"
    ),
    pytest.param(
        ("<span>                   </span>\n"),
        ("<span></span>\n"),
        id="snippet_25",
    ),
    pytest.param(("<img/> <img/>\n"), ("<img /> \n<img />\n"), id="snippet_26"),
    pytest.param(
        ("<img/>          <img/>\n"), ("<img />  \n<img />\n"), id="snippet_27"
    ),
    pytest.param(
        ("<img/>           <img/>\n"),
        ("<img />          \n<img />\n"),
        id="snippet_28",
    ),
    pytest.param(
        ("<img/>                   <img/>\n"),
        ("<img />                  \n<img />\n"),
        id="snippet_29",
    ),
    pytest.param(
        ("<i />   |   <i />\n"), ("<i />   |   <i />\n"), id="snippet_30"
    ),
    pytest.param(
        ("<p><span>X</span>   or   <span>Y</span></p><p>X   or   Y</p>\n"),
        (
            "<p>\n"
            "    <span>X</span>   or   <span>Y</span>\n"
            "</p>\n"
            "<p>X   or   Y</p>\n"
        ),
        id="snippet_31",
    ),
    pytest.param(
        (
            "<!-- U+2005 -->\n"
            "<div>before<span> </span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter</div>\n"
            "<!-- U+005F -->\n"
            "<div>before<span>_</span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter</div>\n"
            "<!-- U+0020 -->\n"
            "<div>before<span> </span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter</div>\n"
        ),
        (
            "<!-- U+2005 -->\n"
            "<div>\n"
            "    before<span></span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter\n"
            "</div>\n"
            "<!-- U+005F -->\n"
            "<div>\n"
            "    before<span>_</span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter\n"
            "</div>\n"
            "<!-- U+0020 -->\n"
            "<div>\n"
            "    before<span></span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter\n"
            "</div>\n"
        ),
        id="snippet_2005",
    ),
    pytest.param(
        (
            "<!-- U+2005 -->\n"
            '<script type="text/unknown" lang="unknown">\n'
            "        // comment\n"
            "          // comment\n"
            "          // comment\n"
            "          // comment\n"
            "</script>\n"
            "<!-- U+005F -->\n"
            '<script type="text/unknown" lang="unknown">\n'
            "   _    // comment\n"
            "          // comment\n"
            "          // comment\n"
            "          // comment\n"
            "</script>\n"
            "<!-- U+0020 -->\n"
            '<script type="text/unknown" lang="unknown">\n'
            "        // comment\n"
            "          // comment\n"
            "          // comment\n"
            "          // comment\n"
            "</script>\n"
        ),
        (
            "<!-- U+2005 -->\n"
            '<script type="text/unknown" lang="unknown">\n'
            "        // comment\n"
            "          // comment\n"
            "          // comment\n"
            "          // comment\n"
            "</script>\n"
            "<!-- U+005F -->\n"
            '<script type="text/unknown" lang="unknown">\n'
            "   _    // comment\n"
            "          // comment\n"
            "          // comment\n"
            "          // comment\n"
            "</script>\n"
            "<!-- U+0020 -->\n"
            '<script type="text/unknown" lang="unknown">\n'
            "        // comment\n"
            "          // comment\n"
            "          // comment\n"
            "          // comment\n"
            "</script>\n"
        ),
        id="snippet_2005_2",
    ),
    pytest.param(
        (
            "<span>123</span>\n"
            "<span>\n"
            "123</span>\n"
            "<span>123\n"
            "</span>\n"
            "<span>\n"
            "123\n"
            "</span>\n"
            "<div>123</div>\n"
            "<div>\n"
            "123</div>\n"
            "<div>123\n"
            "</div>\n"
            "<div>\n"
            "123\n"
            "</div>\n"
        ),
        (
            "<span>123</span>\n"
            "<span>123</span>\n"
            "<span>123</span>\n"
            "<span>123</span>\n"
            "<div>123</div>\n"
            "<div>123</div>\n"
            "<div>123</div>\n"
            "<div>123</div>\n"
        ),
        id="surrounding_linebreak",
    ),
    pytest.param(
        (
            "<table>\n"
            "  <thead>\n"
            "    <tr>\n"
            "      <th>A</th>\n"
            "      <th>B</th>\n"
            "      <th>C</th>\n"
            "    </tr>\n"
            "  </thead>\n"
            "</table>\n"
            "\n"
            "<table><thead><tr><th>A</th><th>B</th><th>C</th></tr></thead></table>\n"
            "\n"
            "<table> <thead> <tr> <th> A </th> <th> B </th> <th> C </th> </tr> </thead> </table>\n"
            "\n"
            "<table>\n"
            "  <thead>\n"
            "    <tr>\n"
            "    </tr>\n"
            "  </thead>\n"
            "</table>\n"
        ),
        (
            "<table>\n"
            "    <thead>\n"
            "        <tr>\n"
            "            <th>A</th>\n"
            "            <th>B</th>\n"
            "            <th>C</th>\n"
            "        </tr>\n"
            "    </thead>\n"
            "</table>\n"
            "<table>\n"
            "    <thead>\n"
            "        <tr>\n"
            "            <th>A</th>\n"
            "            <th>B</th>\n"
            "            <th>C</th>\n"
            "        </tr>\n"
            "    </thead>\n"
            "</table>\n"
            "<table>\n"
            "    <thead>\n"
            "        <tr>\n"
            "            <th>A</th>\n"
            "            <th>B</th>\n"
            "            <th>C</th>\n"
            "        </tr>\n"
            "    </thead>\n"
            "</table>\n"
            "<table>\n"
            "    <thead>\n"
            "        <tr></tr>\n"
            "    </thead>\n"
            "</table>\n"
        ),
        id="table",
    ),
    pytest.param(
        (
            "<template>\n"
            "  <template>foo</template>\n"
            "</template>\n"
            "<template>\n"
            "  <template>foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo</template>\n"
            "</template>\n"
        ),
        (
            "<template>\n"
            "    <template>foo</template>\n"
            "</template>\n"
            "<template>\n"
            "    <template>foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo</template>\n"
            "</template>\n"
        ),
        id="template",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
