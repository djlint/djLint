import re

from ..settings import Config
from .parser import HTMLParser
from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements
from HtmlStyles import html_styles
from HtmlElementAttributes import html_element_attributes
from itertools import chain
"""
options needed > no
empty-attributes-are-booleans >> required will either be "require =''" or just require
"""
def indent_html(rawcode: str, config: Config):

    ## pop front mater
    rawcode = rawcode.strip()

    front_matter = re.search(r"^---[\s\S]+?---\S*", rawcode)

    if front_matter:
        front_matter = front_matter.group()
        rawcode = rawcode.replace(front_matter, "")
        front_matter = front_matter.strip() + "\n"
    else:
        front_matter = ""

    def breakbefore(html):

        return bool(re.search(r"\n[ \t]*$", html, re.M))

    def spacebefore(html):

        return bool(re.search(r"[ ]*$", html, re.M))

    elements = []


    class MyHTMLParser(HTMLParser):
        @staticmethod
        def get_tag_style(style):
            return dict(
                chain(
                    *map(
                        dict.items,
                        [
                            {y: x["style"].get(style) for y in x["selectorText"].split(",")}
                            for x in list(
                                filter(lambda x: x["style"].get(style) is not None, html_styles)
                            )
                        ],
                    )
                )
            )

        #def should_ignore_content(self, tag):

        def tag_is_space_sensitive(self, tag):
            display = self.css_display.get('tag', self.css_default_display)
            return not display.startswith('table') and display not in ['block', 'list-item', 'inline-block']

        def tag_is_pre(self, tag):
            return self.css_whitespace.get(tag, self.css_default_whitespace).startswith('pre')

        def get_tag_closing(self, tag):
            return " />" if tag in html_void_elements else ">"

        def get_tag_name(self, tag):
            return tag.lower() if tag in html_tag_names else tag

        def get_attribute_name(self, tag, attribute):
            return attribute.lower() if attribute in html_element_attributes["*"] or attribute in html_element_attributes[tag] else attribute

        def get_tag_attributes(self, tag, attributes):

            attribs = []

            for x in attributes:
                key=self.get_attribute_name(tag, x[0])
                value=(f"=\"{x[1]}\"" if x[1] else "")

                attribs.append(f"{key}{value}")

            return (" ").join(attribs) if len(attribs) else ""
        def __init__(self, config):


            super(MyHTMLParser, self).__init__()
            self.output = ""
            self.config = config
            self.indent_html_tags = ["div", "p", "dd"]
            self.ignored_html_tags = ["pre", "code", "textarea", "script"]
            self.inline_blocks = [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "a",
                "span",
                "small"
            ]

            self.css_display = dict(**self.get_tag_style('display'),**{
                  "button": "inline-block",
                  "template": "inline",
                  "source": "block",
                  "track": "block",
                  "script": "block",
                  "param": "block",
                  "details": "block",
                  "summary": "block",
                  "dialog": "block",
                  "meter": "inline-block",
                  "progress": "inline-block",
                  "object": "inline-block",
                  "video": "inline-block",
                  "audio": "inline-block",
                  "select": "inline-block",
                  "option": "block",
                  "optgroup": "block"
                })
            self.css_default_display = "inline"
            self.css_whitespace = self.get_tag_style('whitespace')
            self.css_default_whitespace = 'normal'

            self.indent_temp_tags = ["if"]
            self.indent_block = False
            self.current_block = "tag"

            self.indent = self.config.indent
            self.level = 0
            self.ignored_level = 0
            self.inline_level = 0
            self.is_inline = False
            self.last_tag = ""
            self.line_length= 0

        def handle_decl(self,decl):
            if re.match(r'doctype', decl, re.I):
                self.output += self.indent * self.level
                decl = re.sub(r'^doctype', "", decl, flags=re.I | re.M).strip()
                decl = re.sub(r'^html\b', "html", decl, flags=re.I | re.M)
                decl = re.sub(r'\s+', " ", decl)
                self.output += "<!DOCTYPE " + decl + self.get_tag_closing('doctype')
                self.last_tag = 'doctype'

        def handle_starttag(self, tag, attrs):
            tag = self.get_tag_name(tag)

            #print("opening: ", tag)

            attributes = ""

            if attrs:
                attributes = " " + self.get_tag_attributes(tag, attrs)

            html_closing = self.get_tag_closing(tag)
            html_tag = f"<{tag}{attributes}{html_closing}"

            indent = self.indent * self.level

            if self.tag_is_space_sensitive(tag):
                # print("ignored html tags")
                if self.ignored_level == 0 and breakbefore(self.output):
                    self.output += indent
                elif self.ignored_level == 0 and not breakbefore(self.output):
                    self.output += "\n" + indent
                self.output += html_tag
                if tag not in html_void_elements:
                    self.ignored_level += 1
                    self.current_block = "tag"

            elif self.tag_is_pre(tag):
                # print("inline blocks")
                if self.inline_level == 0 and breakbefore(self.output):
                    self.output += self.indent * self.level

                if (
                    self.inline_level == 0
                    and not breakbefore(self.output)
                    and self.current_block == "tag"
                ):
                    self.output += "\n" + indent

                if tag not in html_void_elements:
                    self.inline_level += 1
                self.output += html_tag

                if tag not in html_void_elements:
                    self.current_block = "tag"
            else:
                # print("else")
                # if tag in self.indent_html_tags:
                self.output = self.output.rstrip()
                if self.output and self.output[-1] != "\n":
                    self.output = self.output + "\n"

                self.output += indent

                self.output += html_tag + "\n"
                if tag not in html_void_elements:
                    self.level += 1
                    self.current_block = "tag"

            # else:
            #     self.output += html_tag

            self.last_tag = tag

        def handle_tempstatestarttag(self, tag, attrs):
            attribs = " " + (" ").join(attrs) + "" if attrs else ""
            if tag in self.indent_temp_tags:
                self.output += (
                    (self.indent * self.level) + "{% " + tag + attribs + " %}\n"
                )
                self.level += 1

        def handle_endtag(self, tag):
            tag = self.get_tag_name(tag)

            if tag in self.ignored_html_tags:
                self.output += "</" + tag + ">"
                self.ignored_level -= 1
                self.current_block = "tag"

            elif tag in self.inline_blocks:
                self.inline_level -= 1
                self.output += "</" + tag + ">"
                self.current_block = "tag"
            elif tag not in html_void_elements:
                self.output = self.output.rstrip()
                if self.output != "":
                    self.output = self.output + "\n"

                # print("end")
                self.level -= 1
                self.output += (self.indent * self.level) + "</" + tag + ">\n"
                self.current_block = "tag"

            self.last_tag = tag

        def handle_tempstateendtag(self, tag, attrs):
            attribs = " " + (" ").join(attrs) + "" if attrs else ""
            if tag in self.indent_temp_tags:
                self.level -= 1
                self.output += (self.indent * self.level) + "{% end" + tag + " %}\n"

        def handle_data(self, data):
            if self.ignored_level > 0 or self.inline_level > 0 and data.strip() != "":
                self.output += data
                self.current_block = "text"
            elif data.strip() != "":

                if breakbefore(self.output):
                    self.output += self.indent * self.level
                self.output += re.sub(r"\s+$", " ", data.lstrip(), re.M)
                self.current_block = "text"

        def handle_comment(self, data):
            if breakbefore(self.output):
                self.output += self.indent * self.level
            elif (
                self.ignored_level == 0
                and self.inline_level == 0
                and not breakbefore(self.output)
            ):
                self.output += "\n" + (self.indent * self.level)
            self.output += "<!--" + data + "-->"

        def close(self):
            super(MyHTMLParser, self).close()
            return self.output

    p = MyHTMLParser(config)
    p.feed(rawcode)
    output = p.close()

    output = front_matter + output

    return output
