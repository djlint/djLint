
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
            self.last_sibling: Optional[Tag] = None
            self.last_parent: Optional[Tag] = None
            self.line_length = 0
            self.namespace = ""
            self.tag = Tag("None", self.config)
            self.parents = []

        def get_parent(self):
            if len(self.parents) > 0:
                return self.parents[-1]
            return None

        def current_indent(self) -> str:
            indent = ""
            spacing =self.indent * self.level

            if self.tag.type in ["open", "void"]:

                if (
                    not self.tag.is_indentation_sensitive
                    and not self.tag.is_space_sensitive
                    and not (self.tag.parent and self.tag.parent.is_space_sensitive)
                    or self.tag.parent and self.tag.parent.is_hidden
                ):

                    if (self.tag.data is None  and self.output
                    and self.output[-1] != "\n"):
                        return "\n" + spacing
                    return spacing

                elif (self.tag.data is None and self.last_sibling.data is None
                    and not self.tag.is_indentation_sensitive
                    and self.output
                    and self.output[-1] != "\n"
                    and not( self.tag.parent.type == "open" and self.tag.parent.is_space_sensitive)
                    ):
                    return "\n" + spacing
                elif (
                    not self.tag.is_indentation_sensitive
                    and self.tag.data is not None
                    ):

                    return ""
                elif (self.output and self.output[-1] != "\n" and
                     (self.tag.data and len(self.tag.data) > 0)):

                    return ""
                elif self.tag.is_hidden and not self.tag.parent.is_space_sensitive:
                    if self.output and self.output[-1] == "\n":
                        return spacing
                    else:
                        return "\n" + spacing
                elif self.tag.is_script:
                    return spacing
                return ""
            elif self.tag.type == "close":
                if not ( self.tag.parent.type == "open" and self.tag.parent.is_space_sensitive) :
                    if self.output and self.output[-1] == "\n":
                        return spacing
                    else:
                        return "\n" + spacing
                elif not ( self.tag.parent.type == "open"):

                    return spacing
                else:
                    if self.tag.is_hidden and not self.last_parent.is_hidden:
                        if self.output and self.output[-1] == "\n":
                            return spacing
                        else:
                            return "\n" + spacing
                    if self.output[-1] == "\n":
                        return spacing
                    return ""

            return ""

        def get_open_parent(self,tag: Tag) -> Optional[Tag]:
            while tag and tag.parent:
                if tag.parent.type == "open":
                    return tag.parent
                tag = tag.parent

            return None

        def handle_decl(self, decl: str) -> None:
            if re.match(r"doctype", decl, re.I):
                self.output += self.current_indent()
                decl = re.sub(r"^doctype", "", decl, flags=re.I | re.M).strip()
                decl = re.sub(r"^html\b", "html", decl, flags=re.I | re.M)
                decl = re.sub(r"\s+", " ", decl)
                self.output += "<!DOCTYPE " + decl + ">" + "\n"

        def handle_starttag(self, tag: str, attrs: List) -> None:
            """Handle start tag.

            Create a tag object.

            If the tag is not void, update last parent.
            """
            if self.tag.type == "open":
                self.last_sibling = self.tag

            self.tag = Tag(tag, self.config, parent=self.last_parent, attributes=attrs)
            if not self.tag.is_void:
                self.tag.type = "open"
            else:
                self.tag.type = "void"

            if self.tag.is_space_sensitive:
                self.output += self.current_indent() + self.tag.open_tag

            elif self.tag.is_indentation_sensitive:
                self.output += self.current_indent() + self.tag.open_tag

            elif self.tag.is_script:
                self.output += self.current_indent() + self.tag.open_tag
                self.ignored_level += 1

            else:
                self.output += self.current_indent() + self.tag.open_tag

            if not self.tag.is_void:
                self.level += 1
            self.last_sibling = self.tag

            if self.last_parent is None:
                self.last_parent = self.tag
            elif not self.tag.is_void and not self.tag.is_script:
                self.last_parent = self.tag
            elif self.tag.is_script:
                self.last_parent = self.last_parent
            else:
                self.last_parent = self.tag.parent

        # def handle_tempstatestarttag(self, tag, attrs):
        #     attribs = " " + (" ").join(attrs) + "" if attrs else ""
        #     if tag in self.indent_temp_tags:
        #         self.output += (
        #             (self.indent * self.level) + "{% " + tag + attribs + " %}\n"
        #         )
        #         self.level += 1

        def handle_endtag(self, tag: str) -> None:
            """Handle end tag.

            Create a tag object. Do not update the class property
            unless it is not a void tag.

            If the tag is not void, update the last sibling.
            """
            close_tag = Tag(tag, self.config, parent=self.last_parent)
            close_tag.type = "close"

            if not close_tag.is_void:
                self.level -= 1
                self.tag = close_tag

            self.last_sibling = close_tag

            if close_tag.is_script:
                self.last_parent = self.get_open_parent(close_tag)
            else:
                self.last_parent = self.get_open_parent(self.tag.parent)

            if close_tag.is_script:
                self.ignored_level -= 1

            self.output += self.current_indent()
            self.output += close_tag.close_tag


        # def handle_tempstateendtag(self, tag, attrs):
        #     attribs = " " + (" ").join(attrs) + "" if attrs else ""
        #     if tag in self.indent_temp_tags:
        #         self.level -= 1
        #         self.output += (self.indent * self.level) + "{% end" + tag + " %}\n"

        def handle_data(self, data: str) -> None:

            if self.ignored_level > 0:

                self.output += data

            elif self.tag.parent and self.tag.parent.is_space_sensitive:
                # long text can be wrapped to meet line length
                data = re.sub(r"\s+", " ", data)
                data_split = data.split(" ")
                cleaned_data = ""
                for x, chunck in enumerate(data_split, 1):

                    cleaned_data += chunck
                    if x == len(data_split):

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

                data = re.sub(r"\s+", " ", data)
                self.tag.data = data
                self.output += data

            elif data.strip() != "":

                # for example, "." following "</a>"
                if self.tag.is_void:
                    data = re.sub(r"\s+", " ", data).lstrip()
                    self.output += self.current_indent() + data.rstrip() + "\n"
                elif self.tag.is_space_sensitive:
                    data = re.sub(r"\s+", " ", data)
                    self.output += data.rstrip() + "\n"
                else:
                    self.tag.data = (
                        "\n" + self.current_indent() + data.strip()
                    )
                    self.output += (
                        "\n" + self.current_indent() + data.strip()
                    )
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

        def handle_comment(self, data: str) -> None:
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
