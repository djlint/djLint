"""Test html tags.

uv run pytest tests/test_html/test_tags.py
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
        ('<CaseSensitive CaseSensitive="true">hello world</CaseSensitive>\n'),
        ('<CaseSensitive CaseSensitive="true">hello world</CaseSensitive>\n'),
        id="case_sensitive",
    ),
    pytest.param(
        (
            "<div>\n"
            "    aaaaaaaaaa\n"
            "    <a\n"
            '      href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"\n'
            "      >bbbbbbbbbb</a\n"
            "    >\n"
            "    cccccccccc\n"
            "</div>\n"
            "<div>\n"
            "    aaaaaaaaaa\n"
            "    <a\n"
            '      href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"\n'
            "      >bbbbbbbbbb</a\n"
            "    >cccccccccc\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            "    aaaaaaaaaa\n"
            '    <a href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong">bbbbbbbbbb</a>\n'
            "    cccccccccc\n"
            "</div>\n"
            "<div>\n"
            "    aaaaaaaaaa\n"
            '    <a href="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong">bbbbbbbbbb</a>cccccccccc\n'
            "</div>\n"
        ),
        id="close_at_start",
    ),
    pytest.param(
        ("<app-foo></app-foo>\n<app-bar></app-bar>\n"),
        ("<app-foo></app-foo>\n<app-bar></app-bar>\n"),
        id="custom_element",
    ),
    pytest.param(
        (
            "<p\n"
            "  >Want to write us a letter? Use our<a\n"
            "    ><b\n"
            "      ><a>mailing address</a></b\n"
            "    ></a\n"
            "  >.</p\n"
            ">\n"
            "\n"
            "<p\n"
            "  >Want to write us a letter? Use our<a\n"
            '  href="contacts.html#Mailing_address"\n'
            "    ><b\n"
            "      ><a>mailing address</a></b\n"
            "    ></a\n"
            "  >.</p\n"
            ">\n"
            "\n"
            "<p\n"
            "  >Want to write us a letter? Use our<a\n"
            '  href="contacts.html#Mailing_address"\n'
            '  href1="contacts.html#Mailing_address"\n'
            '  href2="contacts.html#Mailing_address"\n'
            '  href3="contacts.html#Mailing_address"\n'
            '  href4="contacts.html#Mailing_address"\n'
            "    ><b\n"
            "      ><a>mailing address</a></b\n"
            "    ></a\n"
            "  >.</p\n"
            ">\n"
        ),
        (
            "<p>\n"
            "    Want to write us a letter? Use our<a><b><a>mailing address</a></b></a>.\n"
            "</p>\n"
            "<p>\n"
            '    Want to write us a letter? Use our<a href="contacts.html#Mailing_address"><b><a>mailing address</a></b></a>.\n'
            "</p>\n"
            "<p>\n"
            '    Want to write us a letter? Use our<a href="contacts.html#Mailing_address"\n'
            '   href1="contacts.html#Mailing_address"\n'
            '   href2="contacts.html#Mailing_address"\n'
            '   href3="contacts.html#Mailing_address"\n'
            '   href4="contacts.html#Mailing_address"><b><a>mailing address</a></b></a>.\n'
            "</p>\n"
        ),
        id="opening_at_end",
    ),
    pytest.param(
        (
            '<select><option>Blue</option><option>Green</option><optgroup label="Darker"><option>Dark Blue</option><option>Dark Green</option></optgroup></select>\n'
            "<input list=colors>\n"
            "<datalist id=colors><option>Blue</option><option>Green</option></datalist>\n"
        ),
        (
            "<select>\n"
            "    <option>Blue</option>\n"
            "    <option>Green</option>\n"
            '    <optgroup label="Darker">\n'
            "        <option>Dark Blue</option>\n"
            "        <option>Dark Green</option>\n"
            "    </optgroup>\n"
            "</select>\n"
            "<input list=colors>\n"
            "<datalist id=colors>\n"
            "    <option>Blue</option>\n"
            "    <option>Green</option>\n"
            "</datalist>\n"
        ),
        id="option",
    ),
    pytest.param(
        (
            "<pre>\n"
            "--------------------------------------------------------------------------------\n"
            "\n"
            "\n"
            "                                      *         *       *\n"
            "                                     **        **      ***\n"
            "                                     **        **       *\n"
            "   ****    ***  ****               ********  ********                   ***  ****\n"
            "  * ***  *  **** **** *    ***    ********  ********  ***        ***     **** **** *\n"
            " *   ****    **   ****    * ***      **        **      ***      * ***     **   ****\n"
            "**    **     **          *   ***     **        **       **     *   ***    **\n"
            "**    **     **         **    ***    **        **       **    **    ***   **\n"
            "**    **     **         ********     **        **       **    ********    **\n"
            "**    **     **         *******      **        **       **    *******     **\n"
            "**    **     **         **           **        **       **    **          **\n"
            "*******      ***        ****    *    **        **       **    ****    *   ***\n"
            "******        ***        *******      **        **      *** *  *******     ***\n"
            "**                        *****                          ***    *****\n"
            "**\n"
            "**\n"
            " **\n"
            "\n"
            "--------------------------------------------------------------------------------\n"
            "</pre>\n"
            "<pre>\n"
            "\n"
            "        Text in a pre element\n"
            "\n"
            "    is displayed in a fixed-width\n"
            "\n"
            "   font, and it preserves\n"
            "\n"
            "   both             spaces and\n"
            "\n"
            "   line breaks\n"
            "\n"
            "</pre>\n"
            "<pre>     Foo     Bar     </pre>\n"
            "<pre>\n"
            "     Foo     Bar\n"
            "</pre>\n"
            "<pre>Foo     Bar\n"
            "</pre>\n"
            "<pre>\n"
            "     Foo     Bar</pre>\n"
            '<figure role="img" aria-labelledby="cow-caption">\n'
            "  <pre>\n"
            "___________________________\n"
            "< I'm an expert in my field. >\n"
            "---------------------------\n"
            "     \\   ^__^\n"
            "      \\  (oo)\\_______\n"
            "         (__)\\       )\\/\\\n"
            "             ||----w |\n"
            "             ||     ||\n"
            "___________________________\n"
            "  </pre>\n"
            '  <figcaption id="cow-caption">\n'
            '    A cow saying, "I\'m an expert in my field." The cow is illustrated using preformatted text characters.\n'
            "  </figcaption>\n"
            "</figure>\n"
            '<pre data-attr-1="foo" data-attr-2="foo" data-attr-3="foo" data-attr-4="foo" data-attr-5="foo" data-attr-6="foo">\n'
            "     Foo     Bar\n"
            "</pre>\n"
            "<div>\n"
            "  <div>\n"
            "    <div>\n"
            "      <div>\n"
            "        <pre>\n"
            "          ______\n"
            "          STRING\n"
            "          ______\n"
            "        </pre>\n"
            "      </div>\n"
            "    </div>\n"
            "  </div>\n"
            "</div>\n"
            "<pre></pre>\n"
            "\n"
            "<pre><code #foo></code></pre>\n"
            "\n"
            "<details>\n"
            "  <pre><!--Comments-->\n"
            "  </pre></details>\n"
            "\n"
            "<details><pre>\n"
            "  <!--Comments-->\n"
            "</pre>\n"
            "</details>\n"
            "\n"
            "<!-- #6028 -->\n"
            "<pre><br></pre>\n"
            "<PRE><HR></PRE>\n"
            "<pre><br/></pre>\n"
            "<PRE><HR/></PRE>\n"
            "<pre><br /></pre>\n"
            "<PRE><HR /></PRE>\n"
            "<pre><span></span></pre>\n"
            "<PRE><DIV></DIV></PRE>\n"
            "<pre><br/>long long long text long long long text long long long text long long long text <br></pre>\n"
            "<pre><br>long long long text long long long text long long long text long long long text <BR/></pre>\n"
        ),
        (
            "<pre>\n"
            "--------------------------------------------------------------------------------\n"
            "\n"
            "\n"
            "                                      *         *       *\n"
            "                                     **        **      ***\n"
            "                                     **        **       *\n"
            "   ****    ***  ****               ********  ********                   ***  ****\n"
            "  * ***  *  **** **** *    ***    ********  ********  ***        ***     **** **** *\n"
            " *   ****    **   ****    * ***      **        **      ***      * ***     **   ****\n"
            "**    **     **          *   ***     **        **       **     *   ***    **\n"
            "**    **     **         **    ***    **        **       **    **    ***   **\n"
            "**    **     **         ********     **        **       **    ********    **\n"
            "**    **     **         *******      **        **       **    *******     **\n"
            "**    **     **         **           **        **       **    **          **\n"
            "*******      ***        ****    *    **        **       **    ****    *   ***\n"
            "******        ***        *******      **        **      *** *  *******     ***\n"
            "**                        *****                          ***    *****\n"
            "**\n"
            "**\n"
            " **\n"
            "\n"
            "--------------------------------------------------------------------------------\n"
            "</pre>\n"
            "<pre>\n"
            "\n"
            "        Text in a pre element\n"
            "\n"
            "    is displayed in a fixed-width\n"
            "\n"
            "   font, and it preserves\n"
            "\n"
            "   both             spaces and\n"
            "\n"
            "   line breaks\n"
            "\n"
            "</pre>\n"
            "<pre>     Foo     Bar     </pre>\n"
            "<pre>\n"
            "     Foo     Bar\n"
            "</pre>\n"
            "<pre>Foo     Bar\n"
            "</pre>\n"
            "<pre>\n"
            "     Foo     Bar</pre>\n"
            '<figure role="img" aria-labelledby="cow-caption">\n'
            "    <pre>\n"
            "___________________________\n"
            "< I'm an expert in my field. >\n"
            "---------------------------\n"
            "     \\   ^__^\n"
            "      \\  (oo)\\_______\n"
            "         (__)\\       )\\/\\\n"
            "             ||----w |\n"
            "             ||     ||\n"
            "___________________________\n"
            "  </pre>\n"
            '    <figcaption id="cow-caption">\n'
            '        A cow saying, "I\'m an expert in my field." The cow is illustrated using preformatted text characters.\n'
            "    </figcaption>\n"
            "</figure>\n"
            '<pre data-attr-1="foo" data-attr-2="foo" data-attr-3="foo" data-attr-4="foo" data-attr-5="foo" data-attr-6="foo">\n'
            "     Foo     Bar\n"
            "</pre>\n"
            "<div>\n"
            "    <div>\n"
            "        <div>\n"
            "            <div>\n"
            "                <pre>\n"
            "          ______\n"
            "          STRING\n"
            "          ______\n"
            "        </pre>\n"
            "            </div>\n"
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
            "<pre></pre>\n"
            "<pre><code #foo></code></pre>\n"
            "<details>\n"
            "    <pre><!--Comments-->\n"
            "      </pre>\n"
            "</details>\n"
            "<details>\n"
            "    <pre>\n"
            "  <!--Comments-->\n"
            "</pre>\n"
            "</details>\n"
            "<!-- #6028 -->\n"
            "<pre><br></pre>\n"
            "<pre><hr></pre>\n"
            "<pre><br /></pre>\n"
            "<pre><hr /></pre>\n"
            "<pre><br /></pre>\n"
            "<pre><hr /></pre>\n"
            "<pre><span></span></pre>\n"
            "<pre><div></div></pre>\n"
            "<pre><br />long long long text long long long text long long long text long long long text <br></pre>\n"
            "<pre><br>long long long text long long long text long long long text long long long text <br /></pre>\n"
        ),
        id="pre",
    ),
    pytest.param(
        (
            "<br/>\n"
            "<br />\n"
            "<br  />\n"
            "<br\n"
            "/>\n"
            "<br attribute-a />\n"
            "<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute />\n"
            '<br attribute-a="value" />\n'
            "<br\n"
            '  attribute-a="value"\n'
            "/>\n"
            '<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value" />\n'
            '<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value" />\n'
            '<br attribute-a="value" attribute-b="value" attribute-c="value" attribute-d="value" attribute-e="value" attribute-f="value" />\n'
            "<div>string</div>\n"
            "<div>very very very very very very very very very very very very very very very very long string</div>\n"
            "<div very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute>string</div>\n"
            '<div very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value">string</div>\n'
            '<div attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value">string</div>\n'
            '<div attribute="value">very very very very very very very very very very very very very very very very long string</div>\n'
            '<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">string</div>\n'
            '<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">very very very very very very very very very very very very very very very very long string</div>\n'
            '<video width="320" height="240" controls>\n'
            '  <source src="movie.mp4" type="video/mp4">\n'
            '  <source src="movie.ogg" type="video/ogg">\n'
            "  Your browser does not support the video tag.\n"
            "</video>\n"
            "<div><div>string</div></div>\n"
            "<div><div>string</div><div>string</div></div>\n"
            "<div><div><div>string</div></div><div>string</div></div>\n"
            "<div><div>string</div><div><div>string</div></div></div>\n"
            "<div><div></div></div>\n"
            "<div><div></div><div></div></div>\n"
            "<div><div><div><div><div><div><div>string</div></div></div></div></div></div></div>\n"
            "<div>\n"
            "  <div>string</div>\n"
            "</div>\n"
            "<div>\n"
            "\n"
            "  <div>string</div>\n"
            "\n"
            "</div>\n"
            "<div>\n"
            "\n"
            "  <div>string</div>\n"
            "\n"
            "  <div>string</div>\n"
            "\n"
            "</div>\n"
            "<ul\n"
            "  >123<li\n"
            '    class="foo"\n'
            '    id="bar"\n'
            "  >First</li\n"
            "  >456<li\n"
            '    class="baz"\n'
            "  >Second</li\n"
            "  >789</ul\n"
            ">\n"
            "<span>*<b>200</b></span>\n"
            '<img src="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong" />123\n'
            "<div>123<meta attr/>456</div>\n"
            '<p>x<span a="b"></span></p>\n'
            "<p>x<meta a></p>\n"
            "<p>x<meta></p>\n"
            "<span></span>\n"
            "\n"
            "<label aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa></label> |\n"
            "<span></span>\n"
            "<br />\n"
            "<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"
            "  >12345678901234567890</button\n"
            "> <br /><br />\n"
            "\n"
            '<button bind-disabled="isUnchanged" on-click="onSave($event)">Disabled Cancel</button>\n'
            "<br /><br />\n"
            "<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"
            "  >12345678901234567890</button\n"
            "> <br /><br />\n"
            "\n"
            '<button bind-disabled="isUnchanged" on-click="onSave($event)">Disabled Cancel</button>\n'
            "<br /><br />\n"
            '<p>"<span [innerHTML]="title"></span>" is the <i>property bound</i> title.</p>\n'
            "<li>12345678901234567890123456789012345678901234567890123456789012345678901234567890</li>\n"
            "<div>\n"
            "<app-nav></app-nav>\n"
            "<router-outlet></router-outlet>\n"
            "<app-footer></app-footer>\n"
            "\n"
            '<app-nav [input]="something"></app-nav>\n'
            "<router-outlet></router-outlet>\n"
            "<app-footer></app-footer>\n"
            "\n"
            "<app-primary-navigation></app-primary-navigation>\n"
            "<router-outlet></router-outlet>\n"
            '<app-footer [input]="something"></app-footer>\n'
            "</div>\n"
            "<x:root><SPAN>tag name in other namespace should also lower cased</SPAN></x:root>\n"
            "<div>\n"
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit,\n"
            '  "<strong>seddoeiusmod</strong>".\n'
            "</div>\n"
            "<div>\n"
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit,\n"
            "  <strong>seddoeiusmod</strong>.\n"
            "</div>\n"
            "<span>\n"
            '  <i class="fa fa-refresh fa-spin" />\n'
            '  <i class="fa fa-refresh fa-spin" />\n'
            '  <i class="fa fa-refresh fa-spin" />\n'
            "</span>\n"
            "\n"
            "<!-- #5810 -->\n"
            "<table><tr>\n"
            "</tr>\n"
            "</table><div>Should not insert empty line before this div</div>\n"
            "\n"
            "<!-- self-closing -->\n"
            '<span><input type="checkbox"/> </span>\n'
            '<span><span><input type="checkbox"/></span></span>\n'
            '<span><input type="checkbox"/></span>\n'
        ),
        (
            "<br />\n"
            "<br />\n"
            "<br />\n"
            "<br />\n"
            "<br attribute-a />\n"
            "<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute />\n"
            '<br attribute-a="value" />\n'
            '<br attribute-a="value" />\n'
            '<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value" />\n'
            '<br very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value" />\n'
            '<br attribute-a="value"\n'
            '    attribute-b="value"\n'
            '    attribute-c="value"\n'
            '    attribute-d="value"\n'
            '    attribute-e="value"\n'
            '    attribute-f="value" />\n'
            "<div>string</div>\n"
            "<div>very very very very very very very very very very very very very very very very long string</div>\n"
            "<div very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute>\n"
            "    string\n"
            "</div>\n"
            '<div very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-attribute="value">\n'
            "    string\n"
            "</div>\n"
            '<div attribute="very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-very-long-value">\n'
            "    string\n"
            "</div>\n"
            '<div attribute="value">\n'
            "    very very very very very very very very very very very very very very very very long string\n"
            "</div>\n"
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">string</div>\n'
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">\n'
            "    very very very very very very very very very very very very very very very very long string\n"
            "</div>\n"
            '<video width="320" height="240" controls>\n'
            '    <source src="movie.mp4" type="video/mp4">\n'
            '    <source src="movie.ogg" type="video/ogg">\n'
            "    Your browser does not support the video tag.\n"
            "</video>\n"
            "<div>\n"
            "    <div>string</div>\n"
            "</div>\n"
            "<div>\n"
            "    <div>string</div>\n"
            "    <div>string</div>\n"
            "</div>\n"
            "<div>\n"
            "    <div>\n"
            "        <div>string</div>\n"
            "    </div>\n"
            "    <div>string</div>\n"
            "</div>\n"
            "<div>\n"
            "    <div>string</div>\n"
            "    <div>\n"
            "        <div>string</div>\n"
            "    </div>\n"
            "</div>\n"
            "<div>\n"
            "    <div></div>\n"
            "</div>\n"
            "<div>\n"
            "    <div></div>\n"
            "    <div></div>\n"
            "</div>\n"
            "<div>\n"
            "    <div>\n"
            "        <div>\n"
            "            <div>\n"
            "                <div>\n"
            "                    <div>\n"
            "                        <div>string</div>\n"
            "                    </div>\n"
            "                </div>\n"
            "            </div>\n"
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
            "<div>\n"
            "    <div>string</div>\n"
            "</div>\n"
            "<div>\n"
            "    <div>string</div>\n"
            "</div>\n"
            "<div>\n"
            "    <div>string</div>\n"
            "    <div>string</div>\n"
            "</div>\n"
            "<ul>\n"
            "    123\n"
            '    <li class="foo" id="bar">First</li>\n'
            "    456\n"
            '    <li class="baz">Second</li>\n'
            "    789\n"
            "</ul>\n"
            "<span>*<b>200</b></span>\n"
            '<img src="longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong" />\n'
            "123\n"
            "<div>\n"
            "    123\n"
            "    <meta attr />\n"
            "    456\n"
            "</div>\n"
            "<p>\n"
            '    x<span a="b"></span>\n'
            "</p>\n"
            "<p>\n"
            "    x\n"
            "    <meta a>\n"
            "</p>\n"
            "<p>\n"
            "    x\n"
            "    <meta>\n"
            "</p>\n"
            "<span></span>\n"
            "<label aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa></label>\n"
            "|\n"
            "<span></span>\n"
            "<br />\n"
            "<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>12345678901234567890</button>\n"
            "<br />\n"
            "<br />\n"
            '<button bind-disabled="isUnchanged" on-click="onSave($event)">Disabled Cancel</button>\n'
            "<br />\n"
            "<br />\n"
            "<button xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>12345678901234567890</button>\n"
            "<br />\n"
            "<br />\n"
            '<button bind-disabled="isUnchanged" on-click="onSave($event)">Disabled Cancel</button>\n'
            "<br />\n"
            "<br />\n"
            "<p>\n"
            '    "<span [innerHTML]="title"></span>" is the <i>property bound</i> title.\n'
            "</p>\n"
            "<li>12345678901234567890123456789012345678901234567890123456789012345678901234567890</li>\n"
            "<div>\n"
            "    <app-nav></app-nav>\n"
            "    <router-outlet></router-outlet>\n"
            "    <app-footer></app-footer>\n"
            '    <app-nav [input]="something"></app-nav>\n'
            "    <router-outlet></router-outlet>\n"
            "    <app-footer></app-footer>\n"
            "    <app-primary-navigation></app-primary-navigation>\n"
            "    <router-outlet></router-outlet>\n"
            '    <app-footer [input]="something"></app-footer>\n'
            "</div>\n"
            "<x:root><span>tag name in other namespace should also lower cased</span></x:root>\n"
            "<div>\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit,\n"
            '    "<strong>seddoeiusmod</strong>".\n'
            "</div>\n"
            "<div>\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit,\n"
            "    <strong>seddoeiusmod</strong>.\n"
            "</div>\n"
            "<span>\n"
            '    <i class="fa fa-refresh fa-spin" />\n'
            '    <i class="fa fa-refresh fa-spin" />\n'
            '    <i class="fa fa-refresh fa-spin" />\n'
            "</span>\n"
            "<!-- #5810 -->\n"
            "<table>\n"
            "    <tr></tr>\n"
            "</table>\n"
            "<div>Should not insert empty line before this div</div>\n"
            "<!-- self-closing -->\n"
            "<span>\n"
            '    <input type="checkbox" />\n'
            "</span>\n"
            "<span><span>\n"
            '    <input type="checkbox" />\n'
            "</span></span>\n"
            "<span>\n"
            '    <input type="checkbox" />\n'
            "</span>\n"
        ),
        id="tags",
    ),
    pytest.param(
        (
            "<div>before<noscript>noscript long long long long long long long long</noscript>after</div>\n"
            "\n"
            "<div>before<details><summary>summary long long long long </summary>details</details>after</div>\n"
            "\n"
            "<div>before<dialog open>dialog long long long long  long long long long </dialog>after</div>\n"
            "\n"
            '<div>before<object data="horse.wav"><param name="autoplay" value="true"/><param name="autoplay" value="true"/></object>after</div>\n'
            "\n"
            '<div>before<meter min="0" max="1" low=".4" high=".7" optimum=".5" value=".2"></meter>after</div>\n'
            "\n"
            '<div>before<progress value=".5" max="1"></progress>after</div>\n'
            "    )\n"
            "\n"
            "    html_out = (\n"
            "<div>\n"
            "    before<noscript>noscript long long long long long long long long</noscript\n"
            "    >after\n"
            "</div>\n"
            "\n"
            "<div>\n"
            "    before\n"
            "    <details>\n"
            "        <summary>summary long long long long</summary>\n"
            "        details\n"
            "    </details>\n"
            "    after\n"
            "</div>\n"
            "\n"
            "<div>\n"
            "    before\n"
            "    <dialog open>dialog long long long long long long long long</dialog>\n"
            "    after\n"
            "</div>\n"
            "\n"
            "<div>\n"
            '    before<object data="horse.wav">\n'
            '        <param name="autoplay" value="true" />\n'
            '        <param name="autoplay" value="true" /></object\n'
            "    >after\n"
            "</div>\n"
            "\n"
            "<div>\n"
            "    before<meter\n"
            '        min="0"\n'
            '        max="1"\n'
            '        low=".4"\n'
            '        high=".7"\n'
            '        optimum=".5"\n'
            '        value=".2"\n'
            "        ></meter\n"
            "    >after\n"
            "</div>\n"
            "\n"
            '<div>before<progress value=".5" max="1"></progress>after</div>\n'
        ),
        (
            "<div>\n"
            "    before<noscript>noscript long long long long long long long long</noscript>after\n"
            "</div>\n"
            "<div>\n"
            "    before\n"
            "    <details>\n"
            "        <summary>summary long long long long</summary>\n"
            "        details\n"
            "    </details>\n"
            "    after\n"
            "</div>\n"
            "<div>\n"
            "    before<dialog open>dialog long long long long  long long long long </dialog>after\n"
            "</div>\n"
            "<div>\n"
            '    before<object data="horse.wav">\n'
            '    <param name="autoplay" value="true" />\n'
            '    <param name="autoplay" value="true" />\n'
            "</object>after\n"
            "</div>\n"
            "<div>\n"
            '    before<meter min="0" max="1" low=".4" high=".7" optimum=".5" value=".2"></meter>after\n'
            "</div>\n"
            "<div>\n"
            '    before<progress value=".5" max="1"></progress>after\n'
            "</div>\n"
            ")\n"
            "html_out = (\n"
            "<div>\n"
            "    before<noscript>noscript long long long long long long long long</noscript>after\n"
            "</div>\n"
            "<div>\n"
            "    before\n"
            "    <details>\n"
            "        <summary>summary long long long long</summary>\n"
            "        details\n"
            "    </details>\n"
            "    after\n"
            "</div>\n"
            "<div>\n"
            "    before\n"
            "    <dialog open>dialog long long long long long long long long</dialog>\n"
            "    after\n"
            "</div>\n"
            "<div>\n"
            '    before<object data="horse.wav">\n'
            '    <param name="autoplay" value="true" />\n'
            '    <param name="autoplay" value="true" />\n'
            "</object>after\n"
            "</div>\n"
            "<div>\n"
            '    before<meter min="0" max="1" low=".4" high=".7" optimum=".5" value=".2"></meter>after\n'
            "</div>\n"
            "<div>\n"
            '    before<progress value=".5" max="1"></progress>after\n'
            "</div>\n"
        ),
        id="tags_2",
    ),
    pytest.param(
        (
            "<div>\n"
            "  <div>\n"
            "    <div>\n"
            "      <div>\n"
            "        <div>\n"
            "          <div>\n"
            "            <div>\n"
            "              <div>\n"
            "                <div>\n"
            "                  <div>\n"
            "                    <div>\n"
            "                      <div>\n"
            '                        <textarea rows="10" cols="45" name="text">\n'
            "                        String\n"
            "                        </textarea>\n"
            "                      </div>\n"
            "                    </div>\n"
            "                  </div>\n"
            "                </div>\n"
            "              </div>\n"
            "            </div>\n"
            "          </div>\n"
            "        </div>\n"
            "      </div>\n"
            "    </div>\n"
            "  </div>\n"
            "</div>\n"
            "<textarea></textarea>\n"
            "\n"
            "<div><textarea>lorem ipsum</textarea></div>\n"
        ),
        (
            "<div>\n"
            "    <div>\n"
            "        <div>\n"
            "            <div>\n"
            "                <div>\n"
            "                    <div>\n"
            "                        <div>\n"
            "                            <div>\n"
            "                                <div>\n"
            "                                    <div>\n"
            "                                        <div>\n"
            "                                            <div>\n"
            '                                                <textarea rows="10" cols="45" name="text">\n'
            "                        String\n"
            "                        </textarea>\n"
            "                                            </div>\n"
            "                                        </div>\n"
            "                                    </div>\n"
            "                                </div>\n"
            "                            </div>\n"
            "                        </div>\n"
            "                    </div>\n"
            "                </div>\n"
            "            </div>\n"
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
            "<textarea></textarea>\n"
            "<div>\n"
            "    <textarea>lorem ipsum</textarea>\n"
            "</div>\n"
        ),
        id="textarea",
    ),
    pytest.param(
        ("<center></center>\n"), ("<center></center>\n"), id="unsupported"
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
