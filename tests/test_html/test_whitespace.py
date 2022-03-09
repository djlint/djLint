"""Djlint tests for whitespace.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_whitespace.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_whitespace.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_break_tags(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<a>Lorem</a>, ispum dolor sit <strong>amet</strong>.
<div><a>Lorem</a>, ispum dolor sit <strong>amet</strong>.</div>
<div><div><a>Lorem</a>, ispum dolor sit <strong>amet</strong>.</div></div>
    """
    ).strip()

    html_out = (
        """
<a>Lorem</a>, ispum dolor sit <strong>amet</strong>.
<div><a>Lorem</a>, ispum dolor sit <strong>amet</strong>.</div>
<div>
  <div><a>Lorem</a>, ispum dolor sit <strong>amet</strong>.</div>
</div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_display_inline_block(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>
<button>
Click here! Click here! Click here! Click here! Click here! Click here!
</button>
<div>
<button>Click here! Click here! Click here! Click here! Click here! Click here!</button><button>Click here! Click here! Click here! Click here! Click here! Click here!</button>
</div>
<div>
<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>
<button>Click here! Click here! Click here! Click here! Click here! Click here!</button>
</div>
<video src="brave.webm"><track kind=subtitles src=brave.en.vtt srclang=en label="English"><track kind=subtitles src=brave.en.vtt srclang=en label="English"></video>
    """
    ).strip()

    html_out = (
        """
<button>
  Click here! Click here! Click here! Click here! Click here! Click here!
</button>
<button>
  Click here! Click here! Click here! Click here! Click here! Click here!
</button>
<div>
  <button>
    Click here! Click here! Click here! Click here! Click here! Click here!</button
  ><button>
    Click here! Click here! Click here! Click here! Click here! Click here!
  </button>
</div>
<div>
  <button>
    Click here! Click here! Click here! Click here! Click here! Click here!
  </button>
  <button>
    Click here! Click here! Click here! Click here! Click here! Click here!
  </button>
</div>
<video src="brave.webm">
  <track kind="subtitles" src="brave.en.vtt" srclang="en" label="English" />
  <track kind="subtitles" src="brave.en.vtt" srclang="en" label="English" />
</video>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_display_none(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<!DOCTYPE html><HTML CLASS="no-js mY-ClAsS"><HEAD><META CHARSET="utf-8"><TITLE>My tITlE</TITLE><META NAME="description" content="My CoNtEnT"></HEAD></HTML>
    """
    ).strip()

    html_out = (
        """
<!DOCTYPE html>
<html class="no-js mY-ClAsS">
  <head>
    <meta charset="utf-8" />
    <title>My tITlE</title>
    <meta name="description" content="My CoNtEnT" />
  </head>
</html>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_fill(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<p>
  <img
    src="/images/pansies.jpg"
    alt="about fedco bottom image"
    style="float: left;"
  /><strong>We are a cooperative</strong>, one of the few seed companies so organized
  in the United States. Because we do not have an individual owner or beneficiary,
  profit is not our primary goal. Consumers own 60% of the cooperative and worker
  members 40%. Consumer and worker members share proportionately in the cooperative&#8217;s
  profits through our annual patronage dividends.
</p>
    """
    ).strip()

    html_out = (
        """
<p>
  <img
    src="/images/pansies.jpg"
    alt="about fedco bottom image"
    style="float: left"
  /><strong>We are a cooperative</strong>, one of the few seed companies so
  organized in the United States. Because we do not have an individual owner or
  beneficiary, profit is not our primary goal. Consumers own 60% of the
  cooperative and worker members 40%. Consumer and worker members share
  proportionately in the cooperative&#8217;s profits through our annual
  patronage dividends.
</p>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_inline_leading_trailing_spaces(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<span> 321 </span>

<span> <a>321</a> </span>
    """
    ).strip()

    html_out = (
        """
<span> 321 </span>

<span> <a>321</a> </span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_inline_nodes(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa vel augue
vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet urna consectetur dignissim.
Sam vitae neque quis ex dapibus faucibus at sed ligula. Nulla sit amet aliquet nibh.
Vestibulum at congue mi. Suspendisse vitae odio vitae massa hendrerit mattis sed eget dui.
Sed eu scelerisque neque. Donec <b>maximus</b> rhoncus pellentesque. Aenean purus turpis, vehicula
euismod ante vel, ultricies eleifend dui. Class aptent taciti sociosqu ad litora torquent per
conubia nostra, per inceptos himenaeos. Donec in ornare velit.</p>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa vel augue
vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet urna consectetur dignissim.
Sam vitae neque quis ex dapibus faucibus at sed ligula. Nulla sit amet aliquet nibh.
Vestibulum at congue mi. Suspendisse vitae odio vitae massa hendrerit mattis sed eget dui.
Sed eu scelerisque neque. Donec <a href="#"><b>maximus</b></a> rhoncus pellentesque. Aenean purus turpis, vehicula
euismod ante vel, ultricies eleifend dui. Class aptent taciti sociosqu ad litora torquent per
conubia nostra, per inceptos himenaeos. Donec in ornare velit.</p>
    """
    ).strip()

    html_out = (
        """
<p>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa
  vel augue vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet
  urna consectetur dignissim. Sam vitae neque quis ex dapibus faucibus at sed
  ligula. Nulla sit amet aliquet nibh. Vestibulum at congue mi. Suspendisse
  vitae odio vitae massa hendrerit mattis sed eget dui. Sed eu scelerisque
  neque. Donec <b>maximus</b> rhoncus pellentesque. Aenean purus turpis,
  vehicula euismod ante vel, ultricies eleifend dui. Class aptent taciti
  sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec
  in ornare velit.
</p>
<p>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce cursus massa
  vel augue vestibulum facilisis in porta turpis. Ut faucibus lectus sit amet
  urna consectetur dignissim. Sam vitae neque quis ex dapibus faucibus at sed
  ligula. Nulla sit amet aliquet nibh. Vestibulum at congue mi. Suspendisse
  vitae odio vitae massa hendrerit mattis sed eget dui. Sed eu scelerisque
  neque. Donec <a href="#"><b>maximus</b></a> rhoncus pellentesque. Aenean purus
  turpis, vehicula euismod ante vel, ultricies eleifend dui. Class aptent taciti
  sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec
  in ornare velit.
</p>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_nested_inline_without_whitespace(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        (
            """
<a href="/wiki/Help:IPA/English" title="Help:IPA/English">/<span style="border-bottom:1px dotted"><span title="/ˌ/: secondary stress follows">ˌ</span
><span title="/ɪ/: &#39;i&#39; in &#39;kit&#39;">ɪ</span
><span title="&#39;l&#39; in &#39;lie&#39;">l</span
><span title="/ə/: &#39;a&#39; in &#39;about&#39;">ə</span
><span title="/ˈ/: primary stress follows">ˈ</span
><span title="&#39;n&#39; in &#39;nigh&#39;">n</span
><span title="/ɔɪ/: &#39;oi&#39; in &#39;choice&#39;">ɔɪ</span></span>/</a>
<span class="word"><span class="syllable"><span class="letter vowel">i</span><span class="letter consonant">p</span></span
><span class="syllable"><span class="letter consonant onset">s</span><span class="letter vowel">u</span><span class="letter consonant">m</span></span></span>
    """
        )
        .strip()
        .str.encode()
    )

    html_out = (
        """
<a href="/wiki/Help:IPA/English" title="Help:IPA/English"
  >/<span style="border-bottom: 1px dotted"
    ><span title="/ˌ/: secondary stress follows">ˌ</span
    ><span title="/ɪ/: &#39;i&#39; in &#39;kit&#39;">ɪ</span
    ><span title="&#39;l&#39; in &#39;lie&#39;">l</span
    ><span title="/ə/: &#39;a&#39; in &#39;about&#39;">ə</span
    ><span title="/ˈ/: primary stress follows">ˈ</span
    ><span title="&#39;n&#39; in &#39;nigh&#39;">n</span
    ><span title="/ɔɪ/: &#39;oi&#39; in &#39;choice&#39;">ɔɪ</span></span
  >/</a
>
<span class="word"
  ><span class="syllable"
    ><span class="letter vowel">i</span
    ><span class="letter consonant">p</span></span
  ><span class="syllable"
    ><span class="letter consonant onset">s</span
    ><span class="letter vowel">u</span
    ><span class="letter consonant">m</span></span
  ></span
>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_non_breaking_whitespace(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<!-- normal whitespaces -->
<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span>
<!-- non-breaking whitespaces -->
<span>Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span>
<!-- non-breaking narrow whitespaces -->
<span>Prix : 32 €</span>
    """
    ).strip()

    html_out = (
        """
<!-- normal whitespaces -->
<span
  >Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores
  voluptas quaerat ut qui sunt vitae error.</span
>
<!-- non-breaking whitespaces -->
<span
  >Nihil aut odit omnis. Quam maxime est molestiae. Maxime dolorem dolores voluptas quaerat ut qui sunt vitae error.</span
>
<!-- non-breaking narrow whitespaces -->
<span>Prix : 32 €</span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)



def test_snippet_18(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<div> </div>
    """
    ).strip()

    html_out = (
        """
<div> </div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_19(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<div>          </div>
    """
    ).strip()

    html_out = (
        """
<div> </div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_20(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<div>           </div>
    """
    ).strip()

    html_out = (
        """
<div>  </div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_21(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<div>                   </div>
    """
    ).strip()

    html_out = (
        """
<div>   </div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_22(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<span> </span>
    """
    ).strip()

    html_out = (
        """
<span> </span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_23(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<span>          </span>
    """
    ).strip()

    html_out = (
        """
<span>   </span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_24(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<span>           </span>
    """
    ).strip()

    html_out = (
        """
<span>    </span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_25(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<span>                   </span>
    """
    ).strip()

    html_out = (
        """
<span>     </span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_26(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<img/> <img/>
    """
    ).strip()

    html_out = (
        """
<img /> <img />
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_27(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<img/>          <img/>
    """
    ).strip()

    html_out = (
        """
<img />   <img />
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_28(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<img/>           <img/>
    """
    ).strip()

    html_out = (
        """
<img />    <img />
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_29(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<img/>                   <img/>
    """
    ).strip()

    html_out = (
        """
<img />     <img />
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_30(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<i />   |   <i />
    """
    ).strip()

    html_out = (
        """
<i />   |   <i />
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_31(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<p><span>X</span>   or   <span>Y</span></p><p>X   or   Y</p>
    """
    ).strip()

    html_out = (
        """
<p><span>X</span>   or   <span>Y</span></p>
<p>X   or   Y</p>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_2005(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<!-- U+2005 -->
<div>before<span> </span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter</div>
<!-- U+005F -->
<div>before<span>_</span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter</div>
<!-- U+0020 -->
<div>before<span> </span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter</div>
    """
    ).strip()

    html_out = (
        """
<!-- U+2005 -->
<div>
  before<span> </span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter
</div>
<!-- U+005F -->
<div>
  before<span>_</span>afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter
</div>
<!-- U+0020 -->
<div>
  before<span
  > </span
  >afterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafterafter
</div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_snippet_2005_2(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = str.encode(
        """
<!-- U+2005 -->
<script type="text/unknown" lang="unknown">
        // comment
          // comment
          // comment
          // comment
</script>
<!-- U+005F -->
<script type="text/unknown" lang="unknown">
   _    // comment
          // comment
          // comment
          // comment
</script>
<!-- U+0020 -->
<script type="text/unknown" lang="unknown">
        // comment
          // comment
          // comment
          // comment
</script>
    """
    ).strip()

    html_out = (
        """
<!-- U+2005 -->
<script type="text/unknown" lang="unknown">
       // comment
         // comment
         // comment
         // comment
</script>
<!-- U+005F -->
<script type="text/unknown" lang="unknown">
  _    // comment
         // comment
         // comment
         // comment
</script>
<!-- U+0020 -->
<script type="text/unknown" lang="unknown">
  // comment
    // comment
    // comment
    // comment
</script>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)



def test_surrounding_linebreak(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<span>123</span>
<span>
123</span>
<span>123
</span>
<span>
123
</span>
<div>123</div>
<div>
123</div>
<div>123
</div>
<div>
123
</div>
    """
    ).strip()

    html_out = (
        """
<span>123</span>
<span> 123</span>
<span>123 </span>
<span> 123 </span>
<div>123</div>
<div>123</div>
<div>123</div>
<div>123</div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_table(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<table>
  <thead>
    <tr>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
</table>

<table><thead><tr><th>A</th><th>B</th><th>C</th></tr></thead></table>

<table> <thead> <tr> <th> A </th> <th> B </th> <th> C </th> </tr> </thead> </table>

<table>
  <thead>
    <tr>
    </tr>
  </thead>
</table>
    """
    ).strip()

    html_out = (
        """
<table>
  <thead>
    <tr>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
</table>

<table>
  <thead>
    <tr>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
</table>

<table>
  <thead>
    <tr>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
</table>

<table>
  <thead>
    <tr></tr>
  </thead>
</table>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_template(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<template>
  <template>foo</template>
</template>
<template>
  <template>foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo</template>
</template>
    """
    ).strip()

    html_out = (
        """
<template>
  <template>foo</template>
</template>
<template>
  <template
    >foooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo</template
  >
</template>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
