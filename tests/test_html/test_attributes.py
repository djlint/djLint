"""Tests for attributes.

uv run pytest tests/test_html/test_attributes.py
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
            "<img\n"
            "    {% image value.image fill-640x360   as block_image_640 %}\n"
            "    {% image value.image fill-768x432   as block_image_768 %}\n"
            "    {% image value.image fill-1024x576  as block_image_1024 %}\n"
            "    {% image value.image fill-1600x900  as block_image_1600 %}\n"
            '    data-src="{{ block_image_640.url }}"\n'
            '    data-srcset="{{ block_image_640.url }} 640w,\n'
            "              {{ block_image_768.url }} 768w,\n"
            "              {{ block_image_1024.url }} 1024w,\n"
            '              {{ block_image_1600.url }} 1600w"\n'
            '    sizes="(min-width: 1200px) 458px,\n'
            "        (min-width: 992px) 374px,\n"
            "        (min-width: 768px) 720px,\n"
            '        calc(100vw - 30px)"\n'
            '    class="richtext-image imageblock overflow {{ value.image_position }} lazy"\n'
            '    title="{{ value.image.title }}"\n'
            '    alt="Block image"/>\n'
        ),
        (
            "<img {% image value.image fill-640x360   as block_image_640 %}\n"
            "     {% image value.image fill-768x432   as block_image_768 %}\n"
            "     {% image value.image fill-1024x576  as block_image_1024 %}\n"
            "     {% image value.image fill-1600x900  as block_image_1600 %}\n"
            '     data-src="{{ block_image_640.url }}"\n'
            '     data-srcset="{{ block_image_640.url }} 640w,\n'
            "                  {{ block_image_768.url }} 768w,\n"
            "                  {{ block_image_1024.url }} 1024w,\n"
            '                  {{ block_image_1600.url }} 1600w"\n'
            '     sizes="(min-width: 1200px) 458px,\n'
            "            (min-width: 992px) 374px,\n"
            "            (min-width: 768px) 720px,\n"
            '            calc(100vw - 30px)"\n'
            '     class="richtext-image imageblock overflow {{ value.image_position }} lazy"\n'
            '     title="{{ value.image.title }}"\n'
            '     alt="Block image" />\n'
        ),
        id="srcset",
    ),
    pytest.param(
        (
            '<input type="text" class="class one class two" disabled="true" value="something pretty long goes here"\n'
            '   style="width:100px;cursor: text;border:1px solid pink"\n'
            '   required="true" />\n'
        ),
        (
            '<input type="text"\n'
            '       class="class one class two"\n'
            '       disabled="true"\n'
            '       value="something pretty long goes here"\n'
            '       style="width:100px;\n'
            "              cursor: text;\n"
            '              border:1px solid pink"\n'
            '       required="true" />\n'
        ),
        id="long_attributes",
    ),
    pytest.param(
        (
            "<div\n"
            '    class="my long classes"\n'
            '    required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            '<div class="my long classes"\n'
            '     required="true"\n'
            '     checked="checked"\n'
            '     data-attr="some long junk"\n'
            '     style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem">\n'
        ),
        id="style_attributes",
    ),
    pytest.param(
        (
            "<div>\n"
            '   <div style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem"\n'
            '     data-attr="stuff"\n'
            '     class="my long class goes here">\n'
            "    </div>\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    <div style="margin-left: 90px;\n'
            "                display: contents;\n"
            "                font-weight: bold;\n"
            '                font-size: 1.5rem"\n'
            '         data-attr="stuff"\n'
            '         class="my long class goes here"></div>\n'
            "</div>\n"
        ),
        id="style_before_others",
    ),
    # attributes with space around = are not broken
    # https://github.com/djlint/djLint/issues/317
    # https://github.com/djlint/djLint/issues/330
    pytest.param(
        (
            '<a href = "http://test.test:3000/testtesttesttesttesttesttesttesttesttest">Test</a>\n'
        ),
        (
            '<a href="http://test.test:3000/testtesttesttesttesttesttesttesttesttest">Test</a>\n'
        ),
        id="space_around_equals",
    ),
    pytest.param(
        (
            "<div\n"
            '    class="a long list of meaningless classes"\n'
            '    id="something_meaning_less_is_here"\n'
            "    required\n"
            '    checked="checked"\n'
            '    json-data=\'{"menu":{"header":"SVG Viewer","items":[{"id":"Open"}]}}\'>\n'
            "</div>\n"
        ),
        (
            '<div class="a long list of meaningless classes"\n'
            '     id="something_meaning_less_is_here"\n'
            "     required\n"
            '     checked="checked"\n'
            '     json-data=\'{"menu":{"header":"SVG Viewer","items":[{"id":"Open"}]}}\'></div>\n'
        ),
        id="ignored_attributes",
    ),
    pytest.param(
        (
            "<select\n"
            "   multiple\n"
            '  class="selectpicker show-tick"\n'
            '  id="device-select"\n'
            '  title="">\n'
            "</select>\n"
        ),
        (
            '<select multiple class="selectpicker show-tick" id="device-select" title=""></select>\n'
        ),
        id="boolean_attribute",
    ),
    pytest.param(
        (
            "<select\n"
            "   multiple\n"
            '    class="selectpicker show-tick"\n'
            '    id="device-select"\n'
            '    title=""\n'
            '     value="something pretty long goes here"\n'
            '     style="width:100px;cursor: text;border:1px solid pink">\n'
            "   </select>\n"
        ),
        (
            "<select multiple\n"
            '        class="selectpicker show-tick"\n'
            '        id="device-select"\n'
            '        title=""\n'
            '        value="something pretty long goes here"\n'
            '        style="width:100px;\n'
            "               cursor: text;\n"
            '               border:1px solid pink"></select>\n'
        ),
        id="boolean_after_tag",
    ),
    pytest.param(
        (
            "<input readonly\n"
            '   class="form-control"\n'
            '   type="text"\n'
            '   name="driver_id"\n'
            "   value=\"{{ id|default(' sample_text ') }}\"/>\n"
        ),
        (
            "<input readonly\n"
            '       class="form-control"\n'
            '       type="text"\n'
            '       name="driver_id"\n'
            '       value="{{ id|default(" sample_text ") }}" />\n'
        ),
        id="another_boolean_after_tag",
    ),
    pytest.param(
        (
            '<button id="test"\n'
            '        name="test"\n'
            '        type="submit"\n'
            "        one=\"isTrue ? 'True' : 'False'\"\n"
            "        two=\"'Test' .\"\n"
            "        three=\"'Test'\"></button>\n"
        ),
        (
            '<button id="test"\n'
            '        name="test"\n'
            '        type="submit"\n'
            "        one=\"isTrue ? 'True' : 'False'\"\n"
            "        two=\"'Test' .\"\n"
            "        three=\"'Test'\"></button>\n"
        ),
        id="attributes_with_quoted_values",
    ),
    pytest.param(
        (
            "<input name=address maxlength=200>\n"
            "<input name='address' maxlength='200'>\n"
            '<input name="address" maxlength="200">\n'
            '<div class="foo"></div>\n'
            '<div   class="foo"   ></div>\n'
            '<div class="foo bar"></div>\n'
            '<div class="foo bar" id="header"></div>\n'
            '<div   class="foo bar"   id="header"   ></div>\n'
            "<div data-prettier></div>\n"
            '<div data-prettier="true"></div>\n'
            '<meta property="og:description" content="The Mozilla Developer Network (MDN) provides\n'
            "information about Open Web technologies including HTML, CSS, and APIs for both Web sites\n"
            'and HTML5 Apps. It also documents Mozilla products, like Firefox OS.">\n'
            "<div attribute>String</div>\n"
            '<div attribute="">String</div>\n'
            "<div attribute=''>String</div>\n"
            "<div attribute >String</div>\n"
            '<div attribute = "" >String</div>\n'
            "<div attribute = '' >String</div>\n"
            "<div  attribute  >String</div>\n"
            '<div  attribute  =  ""  >String</div>\n'
            "<div  attribute  =  ''  >String</div>\n"
            '<div attribute="attribute = attribute"></div>\n'
            "<div ATTRIBUTE>String</div>\n"
            '<div ATTRIBUTE="">String</div>\n'
            "<div ATTRIBUTE=''>String</div>\n"
            "<article\n"
            '  id="electriccars"\n'
            '  data-columns="3"\n'
            '  data-index-number="12314"\n'
            '  data-parent="cars">\n'
            "</article>\n"
            "<article\n"
            '  id="electriccars"\n'
            '  data-columns="3"\n'
            '  data-index-number="12314"\n'
            '  data-parent="cars">...</article>\n'
            "<article\n"
            '  id="electriccars"\n'
            '  data-columns="3"\n'
            '  data-index-number="12314"\n'
            '  data-parent="cars">\n'
            "  ...\n"
            "</article>\n"
            "<article\n"
            '  id="electriccars"\n'
            '  data-columns="3"\n'
            '  data-index-number="12314"\n'
            '  data-parent="cars">\n'
            "</article>\n"
            "<article\n"
            '  id="electriccars"\n'
            '  data-columns="3"\n'
            '  data-index-number="12314"\n'
            '  data-parent="cars">\n'
            "</article>\n"
            "<X>\n"
            "</X>\n"
            '<X a="1">\n'
            "</X>\n"
            '<X a="1" b="2">\n'
            "</X>\n"
            '<X a="1" b="2" c="3">\n'
            "</X>\n"
            "<p\n"
            '  class="\n'
            "    foo\n"
            "    bar\n"
            "    baz\n"
            '  "\n'
            ">\n"
            "</p>\n"
        ),
        (
            "<input name=address maxlength=200>\n"
            "<input name='address' maxlength='200'>\n"
            '<input name="address" maxlength="200">\n'
            '<div class="foo"></div>\n'
            '<div class="foo"></div>\n'
            '<div class="foo bar"></div>\n'
            '<div class="foo bar" id="header"></div>\n'
            '<div class="foo bar"   id="header"></div>\n'
            "<div data-prettier></div>\n"
            '<div data-prettier="true"></div>\n'
            '<meta property="og:description"\n'
            '      content="The Mozilla Developer Network (MDN) provides information about Open Web technologies including HTML, CSS, and APIs for both Web sites and HTML5 Apps. It also documents Mozilla products, like Firefox OS.">\n'
            "<div attribute>String</div>\n"
            '<div attribute="">String</div>\n'
            "<div attribute=''>String</div>\n"
            "<div attribute>String</div>\n"
            '<div attribute = "">String</div>\n'
            "<div attribute = ''>String</div>\n"
            "<div attribute>String</div>\n"
            '<div attribute  =  "">String</div>\n'
            "<div attribute  =  ''>String</div>\n"
            '<div attribute="attribute = attribute"></div>\n'
            "<div ATTRIBUTE>String</div>\n"
            '<div ATTRIBUTE="">String</div>\n'
            "<div ATTRIBUTE=''>String</div>\n"
            '<article id="electriccars"\n'
            '         data-columns="3"\n'
            '         data-index-number="12314"\n'
            '         data-parent="cars"></article>\n'
            '<article id="electriccars"\n'
            '         data-columns="3"\n'
            '         data-index-number="12314"\n'
            '         data-parent="cars">...</article>\n'
            '<article id="electriccars"\n'
            '         data-columns="3"\n'
            '         data-index-number="12314"\n'
            '         data-parent="cars">...</article>\n'
            '<article id="electriccars"\n'
            '         data-columns="3"\n'
            '         data-index-number="12314"\n'
            '         data-parent="cars"></article>\n'
            '<article id="electriccars"\n'
            '         data-columns="3"\n'
            '         data-index-number="12314"\n'
            '         data-parent="cars"></article>\n'
            "<X>\n"
            "</X>\n"
            '<X a="1">\n'
            "</X>\n"
            '<X a="1" b="2">\n'
            "</X>\n"
            '<X a="1" b="2" c="3">\n'
            "</X>\n"
            '<p class=" foo bar baz "></p>\n'
        ),
        id="long_attributes",
    ),
    pytest.param(
        (
            '<button type="submit">This is valid.</button>\n'
            '<button type="submit" disabled>This is valid.</button>\n'
            '<button type="submit" disabled="">This is valid.</button>\n'
            '<button type="submit" disabled="disabled">This is valid.</button>\n'
            '<button type="submit" disabled=true>This is valid. This will be disabled.</button>\n'
            "<button type=\"submit\" disabled='true'>This is valid. This will be disabled.</button>\n"
            '<button type="submit" disabled="true">This is valid. This will be disabled.</button>\n'
            '<button type="submit" disabled=false>This is valid. This will be disabled.</button>\n'
            '<button type="submit" disabled="false">This is valid. This will be disabled.</button>\n'
            "<button type=\"submit\" disabled='false'>This is valid. This will be disabled.</button>\n"
            '<button type="submit" disabled=hahah>This is valid. This will be disabled.</button>\n'
            "<button type=\"submit\" disabled='hahah'>This is valid. This will be disabled.</button>\n"
            '<button type="submit" disabled="hahah">This is valid. This will be disabled.</button>\n'
            '<input type="checkbox" checked disabled name="cheese">\n'
            '<input type="checkbox" checked="checked" disabled="disabled" name="cheese">\n'
            '<input type=\'checkbox\' checked="" disabled="" name=cheese >\n'
            '<div lang=""></div>\n'
        ),
        (
            '<button type="submit">This is valid.</button>\n'
            '<button type="submit" disabled>This is valid.</button>\n'
            '<button type="submit" disabled="">This is valid.</button>\n'
            '<button type="submit" disabled="disabled">This is valid.</button>\n'
            '<button type="submit" disabled=true>This is valid. This will be disabled.</button>\n'
            "<button type=\"submit\" disabled='true'>This is valid. This will be disabled.</button>\n"
            '<button type="submit" disabled="true">This is valid. This will be disabled.</button>\n'
            '<button type="submit" disabled=false>This is valid. This will be disabled.</button>\n'
            '<button type="submit" disabled="false">This is valid. This will be disabled.</button>\n'
            "<button type=\"submit\" disabled='false'>This is valid. This will be disabled.</button>\n"
            '<button type="submit" disabled=hahah>This is valid. This will be disabled.</button>\n'
            "<button type=\"submit\" disabled='hahah'>This is valid. This will be disabled.</button>\n"
            '<button type="submit" disabled="hahah">This is valid. This will be disabled.</button>\n'
            '<input type="checkbox" checked disabled name="cheese">\n'
            '<input type="checkbox" checked="checked" disabled="disabled" name="cheese">\n'
            '<input type=\'checkbox\' checked="" disabled="" name=cheese>\n'
            '<div lang=""></div>\n'
        ),
        id="boolean",
    ),
    pytest.param(
        (
            "<div CaseSensitive></div>\n"
            '    """\n'
            "    )\n"
            "\n"
            "    html_out = (\n"
            '        """\n'
            "<div CaseSensitive></div>\n"
            '        """\n'
        ),
        (
            "<div CaseSensitive></div>\n"
            '"""\n'
            ")\n"
            "html_out = (\n"
            '"""\n'
            "<div CaseSensitive></div>\n"
            '"""\n'
        ),
        id="CaseSensitive",
    ),
    pytest.param(
        (
            '<div class="ProviderMeasuresContainer__heading-row\n'
            "  d-flex\n"
            "  flex-column flex-lg-row\n"
            "  justify-content-start justify-content-lg-between\n"
            '  align-items-start align-items-lg-center">Foo</div>\n'
            '<div  class="a-bem-block a-bem-block--with-modifier ">\n'
            '<div  class="a-bem-block__element a-bem-block__element--with-modifier also-another-block" >\n'
            '<div  class="a-bem-block__element a-bem-block__element--with-modifier also-another-block__element">\n'
            "</div></div> </div>\n"
        ),
        (
            '<div class="ProviderMeasuresContainer__heading-row d-flex flex-column flex-lg-row justify-content-start justify-content-lg-between align-items-start align-items-lg-center">\n'
            "    Foo\n"
            "</div>\n"
            '<div class="a-bem-block a-bem-block--with-modifier ">\n'
            '    <div class="a-bem-block__element a-bem-block__element--with-modifier also-another-block">\n'
            '        <div class="a-bem-block__element a-bem-block__element--with-modifier also-another-block__element"></div>\n'
            "    </div>\n"
            "</div>\n"
        ),
        id="class_bem1",
    ),
    pytest.param(
        (
            '<div class="news__header widget__content">\n'
            '  <div class="news__tabs">\n'
            '    <h1 class="news__tab-wrapper news__head-item">\n'
            "      <a\n"
            '        class="home-link home-link_blue_yes news__tab news__tab_selected_yes mix-tabber__tab mix-tabber__tab_selected_yes"\n'
            '        tabindex="0"\n'
            '        aria-selected="true"\n'
            '        aria-controls="news_panel_news"\n'
            '        data-key="news"\n'
            '        id="news_tab_news"\n'
            '        data-stat-link="news.tab.link.news"\n'
            '        data-stat-select="news.tab.select.news"\n'
            '        target="_blank"\n'
            '        role="tab"\n'
            '        href="https://yandex.ru/news?msid=1581089780.29024.161826.172442&mlid=1581088893.glob_225"\n'
            '        rel="noopener"\n'
            "        >...</a\n"
            "      >\n"
            "    </h1>\n"
            "  </div>\n"
            "</div>\n"
        ),
        (
            '<div class="news__header widget__content">\n'
            '    <div class="news__tabs">\n'
            '        <h1 class="news__tab-wrapper news__head-item">\n'
            '            <a class="home-link home-link_blue_yes news__tab news__tab_selected_yes mix-tabber__tab mix-tabber__tab_selected_yes"\n'
            '               tabindex="0"\n'
            '               aria-selected="true"\n'
            '               aria-controls="news_panel_news"\n'
            '               data-key="news"\n'
            '               id="news_tab_news"\n'
            '               data-stat-link="news.tab.link.news"\n'
            '               data-stat-select="news.tab.select.news"\n'
            '               target="_blank"\n'
            '               role="tab"\n'
            '               href="https://yandex.ru/news?msid=1581089780.29024.161826.172442&mlid=1581088893.glob_225"\n'
            '               rel="noopener">...</a>\n'
            "        </h1>\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="class_bem2",
    ),
    pytest.param(
        (
            '<my-tag class="md:foo-bg md:foo-color md:foo--sub-bg md:foo--sub-color xl:foo xl:prefix2 --prefix2--something-else unrelated_class_to_fill_80_chars"></my-tag>'
        ),
        (
            '<my-tag class="md:foo-bg md:foo-color md:foo--sub-bg md:foo--sub-color xl:foo xl:prefix2 --prefix2--something-else unrelated_class_to_fill_80_chars"></my-tag>\n'
        ),
        id="class_colon",
    ),
    pytest.param(
        (
            '<my-tag class="__prefix1__foo __prefix1__bar __prefix2__foo prefix2 prefix2--something --prefix2--something-else"></my-tag>\n'
            '<my-tag class="--prefix1--foo --prefix1--bar --prefix2--foo prefix2 prefix2__something __prefix2__something_else"></my-tag>'
        ),
        (
            '<my-tag class="__prefix1__foo __prefix1__bar __prefix2__foo prefix2 prefix2--something --prefix2--something-else"></my-tag>\n'
            '<my-tag class="--prefix1--foo --prefix1--bar --prefix2--foo prefix2 prefix2__something __prefix2__something_else"></my-tag>\n'
        ),
        id="class_leading_dashes",
    ),
    pytest.param(
        (
            '<div aria-hidden="true" class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none d-on-nav-focus js-jump-to-badge-jump">\n'
            "  Jump to\n"
            '  <span class="d-inline-block ml-1 v-align-middle">x</span>\n'
            "</div>\n"
        ),
        (
            '<div aria-hidden="true"\n'
            '     class="border rounded-1 flex-shrink-0 bg-gray px-1 text-gray-light ml-1 f6 d-none d-on-nav-focus js-jump-to-badge-jump">\n'
            "    Jump to\n"
            '    <span class="d-inline-block ml-1 v-align-middle">x</span>\n'
            "</div>\n"
        ),
        id="class_many_short_names",
    ),
    pytest.param(
        (
            '<img class="\n'
            "                     foo\n"
            "bar\n"
            '">\n'
            '<img class="  ">\n'
            "<img class>\n"
            '<img class="\n'
            "looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong\n"
            "a-long-long-long-long-long-class-name\n"
            "another-long-long-long-class-name\n"
            "                     foo bar\n"
            "foo bar\n"
            "                     foo bar\n"
            "foo bar\n"
            "                     foo bar\n"
            "foo bar\n"
            "                     foo bar\n"
            "foo bar\n"
            "                     foo bar\n"
            "foo bar\n"
            "                     foo bar\n"
            "foo bar\n"
            "                     foo bar\n"
            '">\n'
            "<img\n"
            'class="{{ ...classes }}">\n'
            "<img\n"
            'class="foo bar {{ otherClass }}">\n'
            "<!-- escaped -->\n"
            "<!-- from: https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape#Basic_results -->\n"
            '<img class="\n'
            "\\.foo\\#bar\n"
            "\\(\\)\\[\\]\\{\\}\n"
            "--a\n"
            "\\30\n"
            "\\ufffd\n"
            '">\n'
            "<!-- from yahoo website -->\n"
            '<div id="header-wrapper" class="Bgc(#fff) Bdbc(t) Bdbs(s) Bdbw(1px) D(tb) Pos(f) Tbl(f) W(100%) Z(4)\n'
            "has-scrolled_Bdc($c-fuji-grey-d) Scrolling_Bdc($c-fuji-grey-d) has-scrolled_Bxsh($headerShadow)\n"
            'Scrolling_Bxsh($headerShadow) ">\n'
            '<div class="Bgc(#fff) M(a) Maw(1301px) Miw(1000px) Pb(12px) Pt(22px) Pos(r) TranslateZ(0) Z(6)"\n'
            '><h1 class="Fz(0) Pstart(15px) Pos(a)"><a id="header-logo"\n'
            'href="https://www.yahoo.com/" class="D(b) Pos(r)" data-ylk="elm:img;elmt:logo;sec:hd;slk:logo">\n'
            '<img class="H(27px)!--sm1024 Mt(9px)!--sm1024 W(90px)!--sm1024"\n'
            'src="https://s.yimg.com/rz/p/yahoo_frontpage_en-US_s_f_p_205x58_frontpage_2x.png" height="58px"\n'
            'width="205px" alt="Yahoo"/></a></h1></div></div>\n'
        ),
        (
            '<img class=" foo bar ">\n'
            '<img class="  ">\n'
            "<img class>\n"
            '<img class=" looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong a-long-long-long-long-long-class-name another-long-long-long-class-name foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo bar ">\n'
            '<img class="{{ ...classes }}">\n'
            '<img class="foo bar {{ otherClass }}">\n'
            "<!-- escaped -->\n"
            "<!-- from: https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape#Basic_results -->\n"
            '<img class=" \\.foo\\#bar \\(\\)\\[\\]\\{\\} --a \\30 \\ufffd ">\n'
            "<!-- from yahoo website -->\n"
            '<div id="header-wrapper"\n'
            '     class="Bgc(#fff) Bdbc(t) Bdbs(s) Bdbw(1px) D(tb) Pos(f) Tbl(f) W(100%) Z(4) has-scrolled_Bdc($c-fuji-grey-d) Scrolling_Bdc($c-fuji-grey-d) has-scrolled_Bxsh($headerShadow) Scrolling_Bxsh($headerShadow) ">\n'
            '    <div class="Bgc(#fff) M(a) Maw(1301px) Miw(1000px) Pb(12px) Pt(22px) Pos(r) TranslateZ(0) Z(6)">\n'
            '        <h1 class="Fz(0) Pstart(15px) Pos(a)">\n'
            '            <a id="header-logo"\n'
            '               href="https://www.yahoo.com/"\n'
            '               class="D(b) Pos(r)"\n'
            '               data-ylk="elm:img;elmt:logo;sec:hd;slk:logo">\n'
            '                <img class="H(27px)!--sm1024 Mt(9px)!--sm1024 W(90px)!--sm1024"\n'
            '                     src="https://s.yimg.com/rz/p/yahoo_frontpage_en-US_s_f_p_205x58_frontpage_2x.png"\n'
            '                     height="58px"\n'
            '                     width="205px"\n'
            '                     alt="Yahoo" />\n'
            "            </a>\n"
            "        </h1>\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="class_names",
    ),
    pytest.param(
        (
            '<div aria-hidden="true" class="border rounded-1 flex-shrink-0 bg-gray px-1 loooooooooooooooooooooooong">\n'
            "</div>\n"
            "\n"
            "    )\n"
            "\n"
            "    html_out = (\n"
            "\n"
            '<div aria-hidden="true"\n'
            '     class="border rounded-1 flex-shrink-0 bg-gray px-1 loooooooooooooooooooooooong"\n'
            "></div>\n"
        ),
        (
            '<div aria-hidden="true"\n'
            '     class="border rounded-1 flex-shrink-0 bg-gray px-1 loooooooooooooooooooooooong"></div>\n'
            ")\n"
            "html_out = (\n"
            '<div aria-hidden="true"\n'
            '     class="border rounded-1 flex-shrink-0 bg-gray px-1 loooooooooooooooooooooooong"></div>\n'
        ),
        id="print_width_edge",
    ),
    pytest.param(
        ('<img src="test.png" alt="John \'ShotGun\' Nelson">\n'),
        ('<img src="test.png" alt="John \'ShotGun\' Nelson">\n'),
        id="double_quotes",
    ),
    pytest.param(
        ('<a href="1" href="2">123</a>'),
        ('<a href="1" href="2">123</a>\n'),
        id="duplicate",
    ),
    pytest.param(
        ('<img src="test.png" alt=\'John "ShotGun" Nelson\'>'),
        ('<img src="test.png" alt=\'John "ShotGun" Nelson\'>\n'),
        id="single_quotes",
    ),
    pytest.param(
        (
            "<div\n"
            "    smart-quotes='123 \" 456'\n"
            '    smart-quotes="123 \' 456"\n'
            "    smart-quotes='123 &apos;&quot; 456'\n"
            "></div>\n"
        ),
        (
            "<div smart-quotes='123 \" 456'\n"
            '     smart-quotes="123 \' 456"\n'
            "     smart-quotes='123 &apos;&quot; 456'></div>\n"
        ),
        id="smart_quotes",
    ),
    pytest.param(
        (
            '<img src="/assets/visual.png"\n'
            'srcset="/assets/visual@0.5.png  400w, /assets/visual.png      805w"\n'
            'sizes="(max-width: 66rem) 100vw, 66rem" alt=""/>\n'
            '<img src="/assets/visual.png"\n'
            'srcset="/assets/visual@0.5.png  400w, /assets/visual.png      805w, /assets/visual@2x.png   1610w,  /assets/visual@3x.png   2415w"\n'
            'sizes="(max-width: 66rem) 100vw, 66rem" alt=""/>\n'
            '<img src="/assets/visual.png"\n'
            'srcset="/assets/visual@0.5.png  0.5x, /assets/visual.png      1111x,    /assets/visual@2x.png   2x, /assets/visual@3x.png   3.3333x"\n'
            'sizes="(max-width: 66rem) 100vw, 66rem" alt=""/>\n'
            "<img\n"
            'srcset="\n'
            "             /media/examples/surfer-240-200.jpg\n"
            '">\n'
            "<!-- #8150 -->\n"
            "<img\n"
            'sizes="(max-width: 1400px) 100vw, 1400px"\n'
            'srcset="\n'
            "_20200401_145009_szrhju_c_scale,w_200.jpg 200w,\n"
            "_20200401_145009_szrhju_c_scale,w_379.jpg 379w,\n"
            "_20200401_145009_szrhju_c_scale,w_515.jpg 515w,\n"
            "_20200401_145009_szrhju_c_scale,w_630.jpg 630w,\n"
            "_20200401_145009_szrhju_c_scale,w_731.jpg 731w,\n"
            "_20200401_145009_szrhju_c_scale,w_828.jpg 828w,\n"
            "_20200401_145009_szrhju_c_scale,w_921.jpg 921w,\n"
            "_20200401_145009_szrhju_c_scale,w_995.jpg 995w,\n"
            "_20200401_145009_szrhju_c_scale,w_1072.jpg 1072w,\n"
            "_20200401_145009_szrhju_c_scale,w_1145.jpg 1145w,\n"
            "_20200401_145009_szrhju_c_scale,w_1216.jpg 1216w,\n"
            "_20200401_145009_szrhju_c_scale,w_1284.jpg 1284w,\n"
            "_20200401_145009_szrhju_c_scale,w_1350.jpg 1350w,\n"
            "_20200401_145009_szrhju_c_scale,w_1398.jpg 1398w,\n"
            '_20200401_145009_szrhju_c_scale,w_1400.jpg 1400w"\n'
            'src="_20200401_145009_szrhju_c_scale,w_1400.jpg"\n'
            'alt="">\n'
            "\n"
            "    )\n"
            "\n"
            "    html_out = (\n"
            "\n"
            "<img\n"
            '  src="/assets/visual.png"\n'
            '  srcset="/assets/visual@0.5.png 400w, /assets/visual.png 805w"\n'
            '  sizes="(max-width: 66rem) 100vw, 66rem"\n'
            '  alt=""\n'
            "/>\n"
            "<img\n"
            '  src="/assets/visual.png"\n'
            '  srcset="\n'
            "    /assets/visual@0.5.png  400w,\n"
            "    /assets/visual.png      805w,\n"
            "    /assets/visual@2x.png  1610w,\n"
            "    /assets/visual@3x.png  2415w\n"
            '  "\n'
            '  sizes="(max-width: 66rem) 100vw, 66rem"\n'
            '  alt=""\n'
            "/>\n"
            "<img\n"
            '  src="/assets/visual.png"\n'
            '  srcset="\n'
            "    /assets/visual@0.5.png    0.5x,\n"
            "    /assets/visual.png     1111x,\n"
            "    /assets/visual@2x.png     2x,\n"
            "    /assets/visual@3x.png     3.3333x\n"
            '  "\n'
            '  sizes="(max-width: 66rem) 100vw, 66rem"\n'
            '  alt=""\n'
            "/>\n"
            '<img srcset="/media/examples/surfer-240-200.jpg" />\n'
            "<!-- #8150 -->\n"
            "<img\n"
            '  sizes="(max-width: 1400px) 100vw, 1400px"\n'
            '  srcset="\n'
            "    _20200401_145009_szrhju_c_scale,w_200.jpg   200w,\n"
            "    _20200401_145009_szrhju_c_scale,w_379.jpg   379w,\n"
            "    _20200401_145009_szrhju_c_scale,w_515.jpg   515w,\n"
            "    _20200401_145009_szrhju_c_scale,w_630.jpg   630w,\n"
            "    _20200401_145009_szrhju_c_scale,w_731.jpg   731w,\n"
            "    _20200401_145009_szrhju_c_scale,w_828.jpg   828w,\n"
            "    _20200401_145009_szrhju_c_scale,w_921.jpg   921w,\n"
            "    _20200401_145009_szrhju_c_scale,w_995.jpg   995w,\n"
            "    _20200401_145009_szrhju_c_scale,w_1072.jpg 1072w,\n"
            "    _20200401_145009_szrhju_c_scale,w_1145.jpg 1145w,\n"
            "    _20200401_145009_szrhju_c_scale,w_1216.jpg 1216w,\n"
            "    _20200401_145009_szrhju_c_scale,w_1284.jpg 1284w,\n"
            "    _20200401_145009_szrhju_c_scale,w_1350.jpg 1350w,\n"
            "    _20200401_145009_szrhju_c_scale,w_1398.jpg 1398w,\n"
            "    _20200401_145009_szrhju_c_scale,w_1400.jpg 1400w\n"
            '  "\n'
            '  src="_20200401_145009_szrhju_c_scale,w_1400.jpg"\n'
            '  alt=""\n'
            "/>\n"
        ),
        (
            '<img src="/assets/visual.png"\n'
            '     srcset="/assets/visual@0.5.png  400w,\n'
            '             /assets/visual.png      805w"\n'
            '     sizes="(max-width: 66rem) 100vw,\n'
            '            66rem"\n'
            '     alt="" />\n'
            '<img src="/assets/visual.png"\n'
            '     srcset="/assets/visual@0.5.png  400w,\n'
            "             /assets/visual.png      805w,\n"
            "             /assets/visual@2x.png   1610w,\n"
            '             /assets/visual@3x.png   2415w"\n'
            '     sizes="(max-width: 66rem) 100vw,\n'
            '            66rem"\n'
            '     alt="" />\n'
            '<img src="/assets/visual.png"\n'
            '     srcset="/assets/visual@0.5.png  0.5x,\n'
            "             /assets/visual.png      1111x,\n"
            "             /assets/visual@2x.png   2x,\n"
            '             /assets/visual@3x.png   3.3333x"\n'
            '     sizes="(max-width: 66rem) 100vw,\n'
            '            66rem"\n'
            '     alt="" />\n'
            '<img srcset=" /media/examples/surfer-240-200.jpg ">\n'
            "<!-- #8150 -->\n"
            '<img sizes="(max-width: 1400px) 100vw,\n'
            '            1400px"\n'
            '     srcset="_20200401_145009_szrhju_c_scale,w_200.jpg 200w,\n'
            "             _20200401_145009_szrhju_c_scale,w_379.jpg 379w,\n"
            "             _20200401_145009_szrhju_c_scale,w_515.jpg 515w,\n"
            "             _20200401_145009_szrhju_c_scale,w_630.jpg 630w,\n"
            "             _20200401_145009_szrhju_c_scale,w_731.jpg 731w,\n"
            "             _20200401_145009_szrhju_c_scale,w_828.jpg 828w,\n"
            "             _20200401_145009_szrhju_c_scale,w_921.jpg 921w,\n"
            "             _20200401_145009_szrhju_c_scale,w_995.jpg 995w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1072.jpg 1072w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1145.jpg 1145w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1216.jpg 1216w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1284.jpg 1284w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1350.jpg 1350w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1398.jpg 1398w,\n"
            '             _20200401_145009_szrhju_c_scale,w_1400.jpg 1400w"\n'
            '     src="_20200401_145009_szrhju_c_scale,w_1400.jpg"\n'
            '     alt="">\n'
            ")\n"
            "html_out = (\n"
            '<img src="/assets/visual.png"\n'
            '     srcset="/assets/visual@0.5.png 400w,\n'
            '             /assets/visual.png 805w"\n'
            '     sizes="(max-width: 66rem) 100vw,\n'
            '            66rem"\n'
            '     alt="" />\n'
            '<img src="/assets/visual.png"\n'
            '     srcset="/assets/visual@0.5.png  400w,\n'
            "             /assets/visual.png      805w,\n"
            "             /assets/visual@2x.png  1610w,\n"
            '             /assets/visual@3x.png  2415w"\n'
            '     sizes="(max-width: 66rem) 100vw,\n'
            '            66rem"\n'
            '     alt="" />\n'
            '<img src="/assets/visual.png"\n'
            '     srcset="/assets/visual@0.5.png    0.5x,\n'
            "             /assets/visual.png     1111x,\n"
            "             /assets/visual@2x.png     2x,\n"
            '             /assets/visual@3x.png     3.3333x"\n'
            '     sizes="(max-width: 66rem) 100vw,\n'
            '            66rem"\n'
            '     alt="" />\n'
            '<img srcset="/media/examples/surfer-240-200.jpg" />\n'
            "<!-- #8150 -->\n"
            '<img sizes="(max-width: 1400px) 100vw,\n'
            '            1400px"\n'
            '     srcset="_20200401_145009_szrhju_c_scale,w_200.jpg   200w,\n'
            "             _20200401_145009_szrhju_c_scale,w_379.jpg   379w,\n"
            "             _20200401_145009_szrhju_c_scale,w_515.jpg   515w,\n"
            "             _20200401_145009_szrhju_c_scale,w_630.jpg   630w,\n"
            "             _20200401_145009_szrhju_c_scale,w_731.jpg   731w,\n"
            "             _20200401_145009_szrhju_c_scale,w_828.jpg   828w,\n"
            "             _20200401_145009_szrhju_c_scale,w_921.jpg   921w,\n"
            "             _20200401_145009_szrhju_c_scale,w_995.jpg   995w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1072.jpg 1072w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1145.jpg 1145w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1216.jpg 1216w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1284.jpg 1284w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1350.jpg 1350w,\n"
            "             _20200401_145009_szrhju_c_scale,w_1398.jpg 1398w,\n"
            '             _20200401_145009_szrhju_c_scale,w_1400.jpg 1400w"\n'
            '     src="_20200401_145009_szrhju_c_scale,w_1400.jpg"\n'
            '     alt="" />\n'
        ),
        id="src_set",
    ),
    pytest.param(
        (
            '<div style="\n'
            "color:\n"
            "#fFf\n"
            '"></div>\n'
            '<div style=" "></div>\n'
            "<div style></div>\n"
            '<div style="\n'
            "all: initial;display: block;\n"
            "contain: content;text-align: center;\n"
            "background: linear-gradient(to left, hotpink, #FFF00F, #ccc, hsla(240, 100%, 50%, .05), transparent);\n"
            "background: linear-gradient(to left, hsla(240, 100%, 50%, .05), red);\n"
            "max-width: 500px;margin: 0 auto;\n"
            "border-radius: 8px;transition: transform .2s ease-out;\n"
            '"></div>\n'
            '<div style="\n'
            "background: linear-gradient(to left, hotpink, hsla(240, 100%, 50%, .05), transparent);\n"
            '"></div>\n'
            '<div style="   color : red;\n'
            '            display    :inline ">\n'
            "  </div>\n"
            '<div style="\n'
            "color: green;\n"
            "display: inline\n"
            '">\n'
            "  </div>\n"
            "<div attribute-1 attribute-2 attribute-3 attribute-4 attribute-5 attribute-6 attribute-7\n"
            'style="css-prop-1: css-value;css-prop-2: css-value;css-prop-3: css-value;css-prop-4: css-value;"\n'
            " attribute-1 attribute-2 attribute-3 attribute-4 attribute-5 attribute-6 attribute-7 >\n"
            "  </div>\n"
            '<div style="{{ ...styles }}"\n'
            "></div>\n"
            '<div style="color: red; {{ otherStyles }}"\n'
            "></div>\n"
        ),
        (
            '<div style=" color: #fFf "></div>\n'
            '<div style=" "></div>\n'
            "<div style></div>\n"
            '<div style="all: initial;\n'
            "            display: block;\n"
            "            contain: content;\n"
            "            text-align: center;\n"
            "            background: linear-gradient(to left, hotpink, #FFF00F, #ccc, hsla(240, 100%, 50%, .05), transparent);\n"
            "            background: linear-gradient(to left, hsla(240, 100%, 50%, .05), red);\n"
            "            max-width: 500px;\n"
            "            margin: 0 auto;\n"
            "            border-radius: 8px;\n"
            '            transition: transform .2s ease-out"></div>\n'
            '<div style="background: linear-gradient(to left, hotpink, hsla(240, 100%, 50%, .05), transparent)"></div>\n'
            '<div style="   color : red; display    :inline "></div>\n'
            '<div style=" color: green; display: inline "></div>\n'
            "<div attribute-1\n"
            "     attribute-2\n"
            "     attribute-3\n"
            "     attribute-4\n"
            "     attribute-5\n"
            "     attribute-6\n"
            "     attribute-7\n"
            '     style="css-prop-1: css-value;\n'
            "            css-prop-2: css-value;\n"
            "            css-prop-3: css-value;\n"
            '            css-prop-4: css-value"\n'
            "     attribute-1\n"
            "     attribute-2\n"
            "     attribute-3\n"
            "     attribute-4\n"
            "     attribute-5\n"
            "     attribute-6\n"
            "     attribute-7></div>\n"
            '<div style="{{ ...styles }}"></div>\n'
            '<div style="color: red; {{ otherStyles }}"></div>\n'
        ),
        id="style",
    ),
    pytest.param(
        ("<p title=Title>String</p>"),
        ("<p title=Title>String</p>\n"),
        id="without_quotes",
    ),
    pytest.param(
        ('<select data-html="<div></div>" data-normal="hello"></select>'),
        ('<select data-html="<div></div>" data-normal="hello"></select>\n'),
        id="with_html_tag_in_attribute",
    ),
    pytest.param(
        (
            '<select data-json=\'{"html": "<div></div>"}\' data-normal="hello"></select>'
        ),
        (
            '<select data-json=\'{"html": "<div></div>"}\' data-normal="hello"></select>\n'
        ),
        id="with_json_html_tag_in_attribute",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output


# was disabled
