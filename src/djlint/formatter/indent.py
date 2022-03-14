
import re
from typing import Dict, List, Optional, Tuple

from ..settings import Config
from .parser import HTMLParser
from .utils import Tag

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


    p = MyHTMLParser()
    p.feed(rawcode)
    p.close()

    def breakbefore(html):

        return bool(re.search(r"\n[ \t]*$", html, re.M))

    def spacebefore(html):
        return bool(re.search(r"[ ]*$", html, re.M))

    elements = []

    class MyHTMLParser(HTMLParser):
        def __init__(self, config):

            super(MyHTMLParser, self).__init__()
            self.output = ""
            self.config = config

            self.indent_temp_tags = ["if"]
            self.indent_block = False
            self.current_block = "tag"

            self.indent = self.config.indent
            self.level = 0
            self.ignored_level = 0
            self.inline_level = 0
            self.is_inline = False
            self.last_tag: Optional[Tag] = None
            self.line_length = 0
            self.namespace = ""
            self.tag = Tag("None", self.config)
            self.parents = []

        def get_parent(self):
            if len(self.parents) > 0:
                return self.parents[-1]
            return None

        def current_indent(self):
            indent = ""
            if (
                not self.tag.is_indentation_sensitive
                and self.output != ""
                and self.output[-1] != "\n"
            ):
                indent += "\n"
            return indent + self.indent * self.level

        def handle_decl(self, decl):
            if re.match(r"doctype", decl, re.I):
                self.output += self.current_indent()
                decl = re.sub(r"^doctype", "", decl, flags=re.I | re.M).strip()
                decl = re.sub(r"^html\b", "html", decl, flags=re.I | re.M)
                decl = re.sub(r"\s+", " ", decl)
                self.output += "<!DOCTYPE " + decl + ">" + "\n"
                self.last_tag = "doctype"

        def handle_starttag(self, tag, attrs):
            self.tag = Tag(tag, self.config, parent=self.get_parent(), attributes=attrs)

            # indent = self.current_indent()
            # print("start tag:", tag)

            if self.tag.is_space_sensitive:
                # print("space sensitive")
                self.output += self.current_indent() + self.tag.open_tag()
            #     #print("space sensitive tags")
            #     #if self.ignored_level == 0 and breakbefore(self.output):
            #         #self.output += indent

            #         self.line_length += len(indent)
            #     elif self.ignored_level == 0 and not breakbefore(self.output):
            #         #self.output += "\n" + indent
            #         self.output += indent
            #         self.line_length =len(indent)
            #     self.output += html_tag
            #     if tag not in html_void_elements:
            #         self.ignored_level += 1
            #         self.current_block = "tag"

            elif self.tag.is_indentation_sensitive:
                # print("indent sensitive")
                self.output += self.current_indent() + self.tag.open_tag()

            elif self.tag.is_script:
                self.output += self.current_indent() + self.tag.open_tag()
                self.ignored_level += 1

            # elif self.tag_is_pre(tag):
            #     print("pre blocks")
            #     if self.inline_level == 0 and breakbefore(self.output):
            #         self.output += indent
            #         self.line_length +=len(indent)

            #     if (
            #         self.inline_level == 0
            #         and not breakbefore(self.output)
            #         and self.current_block == "tag"
            #     ):
            #         self.output += "\n" + indent
            #         self.line_length =len(indent)

            #     if tag not in html_void_elements:
            #         self.inline_level += 1
            #     self.output += html_tag
            #     self.line_length +=len(html_tag)

            #     if tag not in html_void_elements:
            #         self.current_block = "tag"
            # else:

            # self.output = self.output.rstrip()
            # if self.output and self.output[-1] != "\n":
            #     self.output = self.output #+ "\n"
            #     self.line_length = 0

            # self.output += indent
            # self.line_length += len(indent)
            else:
                self.output += self.current_indent() + self.tag.open_tag()
            # self.line_length = 0
            # if tag not in html_void_elements:
            #     self.level += 1
            #     self.current_block = "tag"

            # else:
            #     self.output += html_tag

            if not self.tag.is_void:
                self.last_tag = self.tag
                self.parents.append(self.tag)
                self.level += 1

        # def handle_tempstatestarttag(self, tag, attrs):
        #     attribs = " " + (" ").join(attrs) + "" if attrs else ""
        #     if tag in self.indent_temp_tags:
        #         self.output += (
        #             (self.indent * self.level) + "{% " + tag + attribs + " %}\n"
        #         )
        #         self.level += 1

        def handle_endtag(self, tag):
            print("end tag:", tag)
            # do not update the class tag with the endtag.
            tag = Tag(tag, self.config, parent=self.tag.parent)

            # if tag in self.ignored_html_tags:
            #     self.output += "</" + tag + ">"
            #     self.ignored_level -= 1
            #     self.current_block = "tag"

            # elif tag in self.inline_blocks:
            #     self.inline_level -= 1
            #     self.output += "</" + tag + ">"
            #     self.current_block = "tag"
            if not tag.is_void:
                self.level -= 1

            if tag.is_script:
                self.ignored_level -= 1

            print(tag.name, tag.is_space_sensitive, tag.is_indentation_sensitive)

            if not tag.is_space_sensitive:
                self.output += self.current_indent()
            self.output += tag.close_tag()

            self.last_tag = tag
            if self.parents[-1].name == tag.name:
                self.parents.pop()

        # def handle_tempstateendtag(self, tag, attrs):
        #     attribs = " " + (" ").join(attrs) + "" if attrs else ""
        #     if tag in self.indent_temp_tags:
        #         self.level -= 1
        #         self.output += (self.indent * self.level) + "{% end" + tag + " %}\n"

        def handle_data(self, data):
            # print("data")
            # print(self.tag)
            if self.ignored_level > 0:
                self.output += data

            elif self.tag.parent and self.tag.parent.is_space_sensitive:
                # print("space sensitive ", self.tag)

                # long text can be wrapped to meet line length
                data = re.sub(r"\s+", " ", data)
                data = data.split(" ")
                cleaned_data = ""
                for x, chunck in enumerate(data, 1):

                    cleaned_data += chunck
                    if x == len(data):

                        continue
                    if len(cleaned_data.split("\n")[-1]) < self.config.max_line_length:
                        cleaned_data += " "
                    else:
                        cleaned_data += "\n" + self.current_indent()

                if re.search(r"\s$", cleaned_data, flags=re.M):
                    cleaned_data = cleaned_data[:-1] + "\n"

                self.tag.data = cleaned_data
                self.output += cleaned_data

            elif self.tag.parent and self.tag.parent.is_indentation_sensitive:
                # print("indent sensitive ", self.tag)
                data = re.sub(r"\s+", " ", data)
                self.tag.data = data
                self.output += data

            elif data.strip() != "":
                # for example, "." following "</a>"
                if self.tag.is_space_sensitive:
                    data = re.sub(r"\s+", " ", data)
                    self.output += data.rstrip() + "\n"
                else:
                    length = (
                        len(self.output.split("\n")[-1])
                        + len(self.current_indent())
                        + len(data.strip())
                    )

                    if length > self.config.max_line_length:
                        self.tag.data = (
                            "\n" + self.current_indent() + data.strip() + "\n"
                        )
                        self.output += (
                            "\n" + self.current_indent() + data.strip() + "\n"
                        )
                    else:
                        self.tag.data = data.strip()
                        self.output += data.strip()
            # else:
            # print("skipped data")
            # if self.ignored_level > 0 or self.inline_level > 0 and data.strip() != "":
            #     self.output += data
            #     self.current_block = "text"

            # elif data.strip() != "":
            #     data = re.sub(r"\s+$", " ", data.lstrip(), re.M)
            #     # if breakbefore(self.output):
            #     #     self.output += self.indent * self.level
            #     #     self.line_length +=len( self.indent * self.level)
            #     self.output += data
            #     self.line_length += len(data)
            #     self.current_block = "text"

        def handle_comment(self, data):
            # if breakbefore(self.output):
            # self.output += self.indent * self.level
            # elif (
            #     self.ignored_level == 0
            #     and self.inline_level == 0
            #     and not breakbefore(self.output)
            # ):
            # self.output += "\n" + (self.indent * self.level)
            self.output += "<!--" + data + "-->"

        def close(self):
            super(MyHTMLParser, self).close()
            return self.output

    p = MyHTMLParser(config)
    p.feed(rawcode)
    output = p.close()

    output = front_matter + output

    return output
