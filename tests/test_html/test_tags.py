"""Djlint tests for tags.

Many tests from from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   pytest tests/test_html/test_tags.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_tags.py::test_long_attributes --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_case_sensitive(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<CaseSensitive CaseSensitive="true">hello world</CaseSensitive>
    """
    ).strip()

    html_out = (
        """
<CaseSensitive CaseSensitive="true">hello world</CaseSensitive>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_close_at_start(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<div>
    aaaaaaaaaa
    <a
      href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"
      >bbbbbbbbbb</a
    >
    cccccccccc
</div>
<div>
    aaaaaaaaaa
    <a
      href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"
      >bbbbbbbbbb</a
    >cccccccccc
</div>
    """
    ).strip()

    html_out = (
        """
<div>
  aaaaaaaaaa
  <a
    href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"
    >bbbbbbbbbb</a
  >
  cccccccccc
</div>
<div>
  aaaaaaaaaa
  <a
    href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"
    >bbbbbbbbbb</a
  >cccccccccc
</div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_custom_element(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<app-foo></app-foo>
<app-bar></app-bar>
    """
    ).strip()

    html_out = (
        """
<app-foo></app-foo>
<app-bar></app-bar>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_opening_at_end(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<p
  >Want to write us a letter? Use our<a
    ><b
      ><a>mailing address</a></b
    ></a
  >.</p
>

<p
  >Want to write us a letter? Use our<a
  href="contacts.html#Mailing_address"
    ><b
      ><a>mailing address</a></b
    ></a
  >.</p
>

<p
  >Want to write us a letter? Use our<a
  href="contacts.html#Mailing_address"
  href1="contacts.html#Mailing_address"
  href2="contacts.html#Mailing_address"
  href3="contacts.html#Mailing_address"
  href4="contacts.html#Mailing_address"
    ><b
      ><a>mailing address</a></b
    ></a
  >.</p
>
    """
    ).strip()

    html_out = (
        """
<p>
  Want to write us a letter? Use our<a
    ><b><a>mailing address</a></b></a
  >.
</p>

<p>
  Want to write us a letter? Use our<a href="contacts.html#Mailing_address"
    ><b><a>mailing address</a></b></a
  >.
</p>

<p>
  Want to write us a letter? Use our<a
    href="contacts.html#Mailing_address"
    href1="contacts.html#Mailing_address"
    href2="contacts.html#Mailing_address"
    href3="contacts.html#Mailing_address"
    href4="contacts.html#Mailing_address"
    ><b><a>mailing address</a></b></a
  >.
</p>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_option(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<select><option>Blue</option><option>Green</option><optgroup label="Darker"><option>Dark Blue</option><option>Dark Green</option></optgroup></select>
<input list=colors>
<datalist id=colors><option>Blue</option><option>Green</option></datalist>
    """
    ).strip()

    html_out = (
        """
<select>
  <option>Blue</option>
  <option>Green</option>
  <optgroup label="Darker">
    <option>Dark Blue</option>
    <option>Dark Green</option>
  </optgroup>
</select>
<input list="colors" />
<datalist id="colors">
  <option>Blue</option>
  <option>Green</option>
</datalist>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_pre(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<pre>
--------------------------------------------------------------------------------


                                      *         *       *
                                     **        **      ***
                                     **        **       *
   ****    ***  ****               ********  ********                   ***  ****
  * ***  *  **** **** *    ***    ********  ********  ***        ***     **** **** *
 *   ****    **   ****    * ***      **        **      ***      * ***     **   ****
**    **     **          *   ***     **        **       **     *   ***    **
**    **     **         **    ***    **        **       **    **    ***   **
**    **     **         ********     **        **       **    ********    **
**    **     **         *******      **        **       **    *******     **
**    **     **         **           **        **       **    **          **
*******      ***        ****    *    **        **       **    ****    *   ***
******        ***        *******      **        **      *** *  *******     ***
**                        *****                          ***    *****
**
**
 **

--------------------------------------------------------------------------------
</pre>
<pre>

        Text in a pre element

    is displayed in a fixed-width

   font, and it preserves

   both             spaces and

   line breaks

</pre>
<pre>     Foo     Bar     </pre>
<pre>
     Foo     Bar
</pre>
<pre>Foo     Bar
</pre>
<pre>
     Foo     Bar</pre>
<figure role="img" aria-labelledby="cow-caption">
  <pre>
___________________________
< I'm an expert in my field. >
---------------------------
     \\   ^__^
      \\  (oo)\\_______
         (__)\\       )\\/\\
             ||----w |
             ||     ||
___________________________
  </pre>
  <figcaption id="cow-caption">
    A cow saying, "I'm an expert in my field." The cow is illustrated using preformatted text characters.
  </figcaption>
</figure>
<pre data-attr-1="foo" data-attr-2="foo" data-attr-3="foo" data-attr-4="foo" data-attr-5="foo" data-attr-6="foo">
     Foo     Bar
</pre>
<div>
  <div>
    <div>
      <div>
        <pre>
          ______
          STRING
          ______
        </pre>
      </div>
    </div>
  </div>
</div>
<pre></pre>

<pre><code #foo></code></pre>

<details>
  <pre><!--Comments-->
  </pre></details>

<details><pre>
  <!--Comments-->
</pre>
</details>

<!-- #6028 -->
<pre><br></pre>
<PRE><HR></PRE>
<pre><br/></pre>
<PRE><HR/></PRE>
<pre><br /></pre>
<PRE><HR /></PRE>
<pre><span></span></pre>
<PRE><DIV></DIV></PRE>
<pre><br/>long long long text long long long text long long long text long long long text <br></pre>
<pre><br>long long long text long long long text long long long text long long long text <BR/></pre>

    """
    ).strip()

    html_out = (
        """
<pre>
--------------------------------------------------------------------------------


                                      *         *       *
                                     **        **      ***
                                     **        **       *
   ****    ***  ****               ********  ********                   ***  ****
  * ***  *  **** **** *    ***    ********  ********  ***        ***     **** **** *
 *   ****    **   ****    * ***      **        **      ***      * ***     **   ****
**    **     **          *   ***     **        **       **     *   ***    **
**    **     **         **    ***    **        **       **    **    ***   **
**    **     **         ********     **        **       **    ********    **
**    **     **         *******      **        **       **    *******     **
**    **     **         **           **        **       **    **          **
*******      ***        ****    *    **        **       **    ****    *   ***
******        ***        *******      **        **      *** *  *******     ***
**                        *****                          ***    *****
**
**
 **

--------------------------------------------------------------------------------
</pre>
<pre>

        Text in a pre element

    is displayed in a fixed-width

   font, and it preserves

   both             spaces and

   line breaks

</pre>
<pre>     Foo     Bar     </pre>
<pre>
     Foo     Bar
</pre>
<pre>
Foo     Bar
</pre>
<pre>     Foo     Bar</pre>
<figure role="img" aria-labelledby="cow-caption">
  <pre>
___________________________
< I'm an expert in my field. >
---------------------------
     \\   ^__^
      \\  (oo)\\_______
         (__)\\       )\\/\\
             ||----w |
             ||     ||
___________________________
  </pre>
  <figcaption id="cow-caption">
    A cow saying, "I'm an expert in my field." The cow is illustrated using
    preformatted text characters.
  </figcaption>
</figure>
<pre
  data-attr-1="foo"
  data-attr-2="foo"
  data-attr-3="foo"
  data-attr-4="foo"
  data-attr-5="foo"
  data-attr-6="foo"
>
     Foo     Bar
</pre>
<div>
  <div>
    <div>
      <div>
        <pre>
          ______
          STRING
          ______
        </pre>
      </div>
    </div>
  </div>
</div>
<pre></pre>

<pre><code #foo></code></pre>

<details>
  <pre><!--Comments-->
  </pre>
</details>

<details>
  <pre>
  <!--Comments-->
</pre>
</details>

<!-- #6028 -->
<pre><br></pre>
<pre><HR></pre>
<pre><br/></pre>
<pre><HR/></pre>
<pre><br /></pre>
<pre><HR /></pre>
<pre><span></span></pre>
<pre><DIV></DIV></pre>
<pre><br/>long long long text long long long text long long long text long long long text <br></pre>
<pre><br>long long long text long long long text long long long text long long long text <BR/></pre>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_tags(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<br/>
<br />
<br  />
<br
/>
<br attribute-a />
<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute />
<br attribute-a="value" />
<br
  attribute-a="value"
/>
<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value" />
<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value" />
<br attribute-a="value" attribute-b="value" attribute-c="value" attribute-d="value" attribute-e="value" attribute-f="value" />
<div>string</div>
<div>very very very very very very very very very very very very very very very very long string</div>
<div very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute>string</div>
<div very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value">string</div>
<div attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value">string</div>
<div attribute="value">very very very very very very very very very very very very very very very very long string</div>
<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">string</div>
<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">very very very very very very very very very very very very very very very very long string</div>
<video width="320" height="240" controls>
  <source src="movie.mp4" type="video/mp4">
  <source src="movie.ogg" type="video/ogg">
  Your browser does not support the video tag.
</video>
<div><div>string</div></div>
<div><div>string</div><div>string</div></div>
<div><div><div>string</div></div><div>string</div></div>
<div><div>string</div><div><div>string</div></div></div>
<div><div></div></div>
<div><div></div><div></div></div>
<div><div><div><div><div><div><div>string</div></div></div></div></div></div></div>
<div>
  <div>string</div>
</div>
<div>

  <div>string</div>

</div>
<div>

  <div>string</div>

  <div>string</div>

</div>
<ul
  >123<li
    class="foo"
    id="bar"
  >First</li
  >456<li
    class="baz"
  >Second</li
  >789</ul
>
<span>*<b>200</b></span>
<img src="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong" />123
<div>123<meta attr/>456</div>
<p>x<span a="b"></span></p>
<p>x<meta a></p>
<p>x<meta></p>
<span></span>

<label aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa></label> |
<span></span>
<br />
<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  >12345678901234567890</button
> <br /><br />

<button bind-disabled="isUnchanged" on-click="onSave($event)"
  >Disabled Cancel</button
>
<br /><br />
<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  >12345678901234567890</button
> <br /><br />

<button bind-disabled="isUnchanged" on-click="onSave($event)"
  >Disabled Cancel</button
>
<br /><br />
<p>"<span [innerHTML]="title"></span>" is the <i>property bound</i> title.</p>
<li>12345678901234567890123456789012345678901234567890123456789012345678901234567890</li>
<div>
<app-nav></app-nav>
<router-outlet></router-outlet>
<app-footer></app-footer>

<app-nav [input]="something"></app-nav>
<router-outlet></router-outlet>
<app-footer></app-footer>

<app-primary-navigation></app-primary-navigation>
<router-outlet></router-outlet>
<app-footer [input]="something"></app-footer>
</div>
<x:root><SPAN>tag name in other namespace should also lower cased</SPAN></x:root>
<div>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit,
  "<strong>seddoeiusmod</strong>".
</div>
<div>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit,
  <strong>seddoeiusmod</strong>.
</div>
<span>
  <i class="fa fa-refresh fa-spin" />
  <i class="fa fa-refresh fa-spin" />
  <i class="fa fa-refresh fa-spin" />
</span>

<!-- #5810 -->
<table><tr>
</tr>
</table><div>Should not insert empty line before this div</div>

<!-- self-closing -->
<span><input type="checkbox"/> </span>
<span><span><input type="checkbox"/></span></span>
<span><input type="checkbox"/></span>
    """
    ).strip()

    html_out = (
        """
<br />
<br />
<br />
<br />
<br attribute-a />
<br
  very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute
/>
<br attribute-a="value" />
<br attribute-a="value" />
<br
  very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value"
/>
<br
  very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value"
/>
<br
  attribute-a="value"
  attribute-b="value"
  attribute-c="value"
  attribute-d="value"
  attribute-e="value"
  attribute-f="value"
/>
<div>string</div>
<div>
  very very very very very very very very very very very very very very very
  very long string
</div>
<div
  very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute
>
  string
</div>
<div
  very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value"
>
  string
</div>
<div
  attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value"
>
  string
</div>
<div attribute="value">
  very very very very very very very very very very very very very very very
  very long string
</div>
<div
  attribute="value"
  attributea="value"
  attributeb="value"
  attributec="value"
  attributed="value"
  attributef="value"
>
  string
</div>
<div
  attribute="value"
  attributea="value"
  attributeb="value"
  attributec="value"
  attributed="value"
  attributef="value"
>
  very very very very very very very very very very very very very very very
  very long string
</div>
<video width="320" height="240" controls>
  <source src="movie.mp4" type="video/mp4" />
  <source src="movie.ogg" type="video/ogg" />
  Your browser does not support the video tag.
</video>
<div><div>string</div></div>
<div>
  <div>string</div>
  <div>string</div>
</div>
<div>
  <div><div>string</div></div>
  <div>string</div>
</div>
<div>
  <div>string</div>
  <div><div>string</div></div>
</div>
<div><div></div></div>
<div>
  <div></div>
  <div></div>
</div>
<div>
  <div>
    <div>
      <div>
        <div>
          <div><div>string</div></div>
        </div>
      </div>
    </div>
  </div>
</div>
<div>
  <div>string</div>
</div>
<div>
  <div>string</div>
</div>
<div>
  <div>string</div>

  <div>string</div>
</div>
<ul>
  123
  <li class="foo" id="bar">First</li>
  456
  <li class="baz">Second</li>
  789
</ul>
<span>*<b>200</b></span>
<img
  src="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"
/>123
<div>123<meta attr />456</div>
<p>x<span a="b"></span></p>
<p>x<meta a /></p>
<p>x<meta /></p>
<span></span>

<label
  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
></label>
|
<span></span>
<br />
<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>12345678901234567890</button>
<br /><br />

<button bind-disabled="isUnchanged" on-click="onSave($event)">
  Disabled Cancel
</button>
<br /><br />
<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>12345678901234567890</button>
<br /><br />

<button bind-disabled="isUnchanged" on-click="onSave($event)">
  Disabled Cancel
</button>
<br /><br />
<p>"<span [innerHTML]="title"></span>" is the <i>property bound</i> title.</p>
<li>
  12345678901234567890123456789012345678901234567890123456789012345678901234567890
</li>
<div>
  <app-nav></app-nav>
  <router-outlet></router-outlet>
  <app-footer></app-footer>

  <app-nav [input]="something"></app-nav>
  <router-outlet></router-outlet>
  <app-footer></app-footer>

  <app-primary-navigation></app-primary-navigation>
  <router-outlet></router-outlet>
  <app-footer [input]="something"></app-footer>
</div>
<x:root
  ><span>tag name in other namespace should also lower cased</span></x:root
>
<div>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit,
  "<strong>seddoeiusmod</strong>".
</div>
<div>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit,
  <strong>seddoeiusmod</strong>.
</div>
<span>
  <i class="fa fa-refresh fa-spin" />
  <i class="fa fa-refresh fa-spin" />
  <i class="fa fa-refresh fa-spin" />
</span>

<!-- #5810 -->
<table>
  <tr></tr>
</table>
<div>Should not insert empty line before this div</div>

<!-- self-closing -->
<span><input type="checkbox" /> </span>
<span
  ><span><input type="checkbox" /></span
></span>
<span><input type="checkbox" /></span>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_tags2(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<div>before<noscript>noscript long long long long long long long long</noscript>after</div>

<div>before<details><summary>summary long long long long </summary>details</details>after</div>

<div>before<dialog open>dialog long long long long  long long long long </dialog>after</div>

<div>before<object data="horse.wav"><param name="autoplay" value="true"/><param name="autoplay" value="true"/></object>after</div>

<div>before<meter min="0" max="1" low=".4" high=".7" optimum=".5" value=".2"></meter>after</div>

<div>before<progress value=".5" max="1"></progress>after</div>
    """
    ).strip()

    html_out = (
        """
<div>
  before<noscript>noscript long long long long long long long long</noscript
  >after
</div>

<div>
  before
  <details>
    <summary>summary long long long long</summary>
    details
  </details>
  after
</div>

<div>
  before
  <dialog open>dialog long long long long long long long long</dialog>
  after
</div>

<div>
  before<object data="horse.wav">
    <param name="autoplay" value="true" />
    <param name="autoplay" value="true" /></object
  >after
</div>

<div>
  before<meter
    min="0"
    max="1"
    low=".4"
    high=".7"
    optimum=".5"
    value=".2"
  ></meter
  >after
</div>

<div>before<progress value=".5" max="1"></progress>after</div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_textarea(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<div>
  <div>
    <div>
      <div>
        <div>
          <div>
            <div>
              <div>
                <div>
                  <div>
                    <div>
                      <div>
                        <textarea rows="10" cols="45" name="text">
                        String
                        </textarea>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<textarea></textarea>

<div><textarea>lorem ipsum</textarea></div>
    """
    ).strip()

    html_out = (
        """
<div>
  <div>
    <div>
      <div>
        <div>
          <div>
            <div>
              <div>
                <div>
                  <div>
                    <div>
                      <div>
                        <textarea rows="10" cols="45" name="text">
                        String
                        </textarea>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<textarea></textarea>

<div><textarea>lorem ipsum</textarea></div>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)


def test_unsupported(runner: CliRunner, tmp_file: TextIO) -> None:

    html_in = (
        b"""
<center></center>
    """
    ).strip()

    html_out = (
        """
<center></center>
        """
    ).strip()

    output = reformat(tmp_file, runner, html_in)
