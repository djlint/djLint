import re
from typing import Dict, List, Optional, Tuple

from HtmlTemplateParser import Htp

from .tag import Tag


class TemplateParser(Htp):
    def __init__(self, config):

        super(TemplateParser, self).__init__()
        self.output = ""
        self.config = config
        self.tree = None
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

        self.open_types = ["open", "void", "starttag_curly_perc"]
        self.close_types = ["close", "endtag_curly_perc"]

    def get_parent(self):
        if len(self.parents) > 0:
            return self.parents[-1]
        return None

    def current_indent(self) -> str:
        indent = ""
        spacing = self.indent * self.level

        if self.tag.type in self.open_types:
            if (
                not self.tag.is_indentation_sensitive
                and not self.tag.is_space_sensitive
                and not (self.tag.parent and self.tag.parent.is_space_sensitive)
                or self.tag.parent
                and self.tag.parent.is_display_none
            ):
                if self.tag.data is None and self.output and self.output[-1] != "\n":
                    return "\n" + spacing

                return spacing

            elif (
                self.tag.data is None
                and self.last_sibling
                and self.last_sibling.data is None
                and not self.tag.is_indentation_sensitive
                and self.output
                and self.output[-1] != "\n"
                and not (
                    self.tag.parent
                    and self.tag.parent.type == "open"
                    and self.tag.parent.is_space_sensitive
                )
            ):
                return "\n" + spacing
            elif not self.tag.is_indentation_sensitive and self.tag.data is not None:

                return ""
            elif (
                self.output
                and self.output[-1] != "\n"
                and (self.tag.data and len(self.tag.data) > 0)
            ):

                return ""
            elif self.tag.is_display_none and not (
                self.tag.parent and self.tag.parent.is_space_sensitive
            ):
                if self.output and self.output[-1] == "\n":
                    return spacing
                else:
                    return "\n" + spacing
            elif self.tag.is_script:
                return spacing
            return ""
        elif self.tag.type in self.close_types:

            if not (
                self.tag.parent
                and self.tag.parent.type in self.open_types
                and self.tag.parent.is_space_sensitive
            ):

                if self.output and self.output[-1] == "\n":

                    return spacing

                # do not add empty space to empty tags
                elif (
                    self.tag.name == self.last_sibling.name
                    and self.tag.type != self.last_sibling.type
                    and self.last_parent.data is None
                ):

                    return ""
                else:
                    return "\n" + spacing
            elif not (self.tag.parent.type in self.open_types):

                return spacing
            else:

                if self.tag.is_display_none and not self.last_parent.is_display_none:
                    if self.output and self.output[-1] == "\n":
                        return spacing
                    else:
                        return "\n" + spacing
                if self.output[-1] == "\n":
                    return spacing
                return ""

        return ""

    def get_open_parent(self, tag: Tag) -> Optional[Tag]:
        while tag and tag.parent:
            if tag.parent.type in self.open_types:
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

        self.tag = Tag(tag, self.config, attributes=attrs)
        self.tag.is_html = True

        if not self.tag.is_void:
            self.tag.type = "open"
        else:
            self.tag.type = "void"

        self.tree.handle_starttag(self.tag)

    # def handle_tempstatestarttag(self, tag, attrs):
    #     attribs = " " + (" ").join(attrs) + "" if attrs else ""
    #     if tag in self.indent_temp_tags:
    #         self.output += (
    #             (self.indent * self.level) + "{% " + tag + attribs + " %}\n"
    #         )
    #         self.level += 1

    def handle_starttag_curly_perc(self, tag, attrs, props):

        self.last_sibling = self.tag
        self.tag = Tag(
            tag,
            self.config,
            parent=self.last_parent,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_perc"

        self.tree.handle_starttag(self.tag)
       # self.output += self.current_indent()
       # self.level += 1
       # self.output += self.tag.open_tag
       # self.last_parent = self.tag


    def handle_starttag_curly_hash(self, tag, attrs):
        print("starttag_curly_hash", tag, attrs)

    def handle_starttag_curly_four(self, tag, attrs):
        print("starttag_curly_four", tag, attrs)

    def handle_endtag_curly_perc(self, tag, attrs, props):

        last_tag = self.tag

        self.tag = Tag(
            tag,
            self.config,
            parent=self.last_parent,
            attributes=attrs,
            properties=props,
        )
        self.tag.type = "endtag_curly_perc"
        self.level -= 1
        self.output += self.current_indent()
        self.output += self.tag.close_tag

        # if closed a short block, it can be inline
        # if (self.tag.name == self.last_sibling.name and self.tag.type != self.last_sibling.type
        #     and self.last_parent.data is None):

        self.last_sibling = self.tag
        self.last_parent = self.get_open_parent(self.tag.parent)

    def handle_endtag_curly_hash(self, tag):
        print("endtag_curly_hash", tag)

    def handle_endtag_curly_four(self, tag):
        print("endtag_curly_four", tag)

    def handle_comment_curly_hash(self, data):
        self.output = self.current_indent() + f"{{# {data.strip()} #}}"
        print("comment_curly_hash", data)

    def handle_comment_curly_exlaim(self, data):
        print("comment_curly_exlaim", data)

    def handle_comment_curly_exlaim_dash(self, data):
        print("comment_curly_exlaim_dash", data)

    def handle_comment_at_star(self, data):
        print("comment_at_star", data)

    def handle_comment_curly_perc(self, data, attrs, props):
        print("comment_curly_perc", data, attrs, props)

    def handle_comment_curly_perc_close(self, data, props):
        print("comment_curly_perc_close", data, props)

    def handle_charref(self, data):
        print("charref", data)

    def handle_decl(self, data):
        print("decl", data)

    def handle_entityref(self, data):
        print("entityref", data)

    def handle_pi(self, data):
        print("pi", data)

    def unknown_decl(self, decl):
        print("unknown decl", decl)

    def handle_endtag(self, tag: str) -> None:
        """Handle end tag.

        Create a tag object. Do not update the class property
        unless it is not a void tag.

        If the tag is not void, update the last sibling.
        """
        close_tag = Tag(tag, self.config, parent=self.last_parent)
        close_tag.type = "close"
        close_tag.is_html = True

        if not close_tag.is_void:
            self.level -= 1
            self.tag = close_tag

            self.tree.handle_endtag(self.tag)
        else:
            # void tags are handled in the open tag block.
            return

    def handle_curly(self, data, attrs):

        # curly handles as data. build the tag and pass it to the
        # data processor.
        tag = Tag(data, self.config, attributes=attrs)
        tag.type = "curly"

        self.handle_data(tag.statement_tag)

    def handle_data(self, data: str) -> None:
        self.tag.data.append(data.strip())
        print(data.strip())
        # if self.ignored_level > 0:

        #     self.output += data

        # elif self.tag.parent and self.tag.parent.is_space_sensitive:

        #     # long text can be wrapped to meet line length
        #     data = re.sub(r"\s+", " ", data)
        #     data_split = data.split(" ")
        #     cleaned_data = ""
        #     for x, chunck in enumerate(data_split, 1):

        #         cleaned_data += chunck
        #         if x == len(data_split):

        #             continue
        #         if len(cleaned_data.split("\n")[-1]) < self.config.max_line_length:
        #             cleaned_data += " "
        #         else:
        #             cleaned_data += "\n" + self.current_indent()

        #     if re.search(r"\s$", cleaned_data, flags=re.M):
        #         cleaned_data = cleaned_data[:-1] + "\n"

        #     self.tag.data = cleaned_data
        #     self.output += cleaned_data

        # elif self.tag.parent and self.tag.parent.is_indentation_sensitive:

        #     data = re.sub(r"\s+", " ", data)
        #     self.tag.data = data
        #     self.output += data

        # elif data.strip() != "":
        #     # for example, "." following "</a>"
        #     if self.tag.is_void:
        #         data = re.sub(r"\s+", " ", data).lstrip()
        #         self.output += self.current_indent() + data.rstrip() + "\n"
        #     elif self.tag.is_space_sensitive:
        #         data = re.sub(r"\s+", " ", data)
        #         self.output += data.rstrip() + "\n"
        #     elif self.tag.data is None:
        #         self.tag.data = "\n" + self.current_indent() + data.strip()
        #         self.output += "\n" + self.current_indent() + data.strip()
        #     else:
        #         self.tag.data = " " + data.strip()
        #         self.output += " " + data.strip()
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
        super(TemplateParser, self).close()
        return self.output
