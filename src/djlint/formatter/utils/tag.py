import re
from itertools import chain
from typing import Dict, List, Optional, Tuple, Union

from HtmlElementAttributes import html_element_attributes
from HtmlStyles import html_styles
from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements

from djlint.settings import Config


class Tag:
    def __init__(
        self,
        tag: str,
        config: Config,
        parent: Optional["Tag"] = None,
        attributes: Optional[List] = None,
        properties: Optional[List] = None,
    ) -> None:

        self.__css_default_whitespace = "normal"
        self.__css_default_display = "inline"
        self.__css_whitespace = self.__get_tag_style("white-space")

        self.__css_display = dict(
            list(self.__get_tag_style("display").items())
            + list(
                {
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
                    "optgroup": "block",
                }.items()
            ),
        )
        self.data: List[str] = []
        self.type: Optional[str] = None
        self._is_html = False
        self.parent = parent
        self.config = config
        self.previous_tag = None
        self.next_tag = None
        self.rawname = tag
        self.children = []
        self.output = ""
        self.hidden = False
        self.tag = tag
        self.namespace, self.name = self.__get_tag_name()
        self.is_pre = self.__tag_is_pre(self.name)
        self.raw_attributes = attributes
        self.raw_properties = properties
        self.is_void = self.name in html_void_elements + ["extends", "load", "include"]

    def __str__(self) -> str:
        return self.name

    @property
    def data(self) -> Optional[str]:
        return self._data

    @data.setter
    def data(self, val: str) -> None:
        self._data = val

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, val: str) -> None:
        self._type = val

    @property
    def is_html(self) -> Optional[str]:
        return self._is_html

    @is_html.setter
    def is_html(self, val: str) -> None:
        self._is_html = val

    @property
    def open_tag(self) -> str:
        if self._is_html:
            if self.parent and (
                self.parent.is_indentation_sensitive or self.parent.is_space_sensitive
            ):
                return f"<{self.name}{self.attributes}{self.__get_tag_closing()}"
            else:
                return f"<{self.name}{self.attributes}{self.__get_tag_closing()}"

        if self.type == "starttag_curly_perc":
            return f"{{%{self._spaceless_left()} {self.tag}{self._attributes()} {self._spaceless_right()}%}}"
        return ""

    @property
    def close_tag(self) -> str:
        if self.is_void:
            return ""
        if self._is_html:
            if self.parent and (
                self.parent.is_indentation_sensitive or self.parent.is_space_sensitive
            ):
                return f"</{self.name}{self.__get_tag_closing()}"
            return f"</{self.name}{self.__get_tag_closing()}"

        if self.type == "endtag_curly_perc":
            return f"{{%{self._spaceless_left()} end{self.tag}{self._attributes()} {self._spaceless_right()}%}}"

        return ""

    @property
    def statement_tag(self):
        if self.type == "curly":
            return f"{{{{ {self.tag}{self._attributes()} }}}}"

        return ""

    def __get_tag_closing(self) -> str:
        if self.is_void:
            return " />"

        return ">"

    def __get_tag_style(self, style: str) -> Dict:
        return dict(
            chain(
                *map(
                    dict.items,
                    [
                        {
                            y.strip(): x["style"].get(style)
                            for y in x["selectorText"].split(",")
                        }
                        for x in list(
                            filter(
                                lambda x: x["style"].get(style) is not None,
                                html_styles,
                            )
                        )
                    ],
                )
            )
        )

    @property
    def is_space_sensitive(self) -> bool:
        """Check if tag is space sensitive."""
        if self._is_html:
            display = self.__css_display.get(self.name, self.__css_default_display)
            # print(display)
            return (
                self.is_script
                or not display.startswith("table")
                and display not in ["block", "list-item", "inline-block"]
            )
        return False

    @property
    def is_hidden(self) -> bool:
        if self._is_html:
            return (
                self.__css_display.get(self.name, self.__css_default_display) == "none"
            )
        return False

    @property
    def is_indentation_sensitive(self) -> bool:
        if self._is_html:
            return self.__tag_is_pre(self.name)
        return False

    def __tag_is_pre(self, tag: str) -> bool:
        if self._is_html:
            return self.__css_whitespace.get(
                tag, self.__css_default_whitespace
            ).startswith("pre")
        return False

    @property
    def is_script(self) -> bool:
        if self._is_html:
            return self.name in ("script", "style", "svg:style")
        return False

    def __get_tag_name(self) -> Tuple[Optional[str], str]:
        # tags with a namespace
        namespace = None
        tag = self.rawname
        if ":" in self.rawname:
            namespace = self.rawname.split(":")[0]
            tag = (":").join(self.rawname.split(":")[1:])

        return namespace, tag.lower() if tag.lower() in html_tag_names else tag

    def __get_attribute_name(self, tag: str, attribute: str) -> str:
        return (
            attribute.lower()
            if attribute.lower() in html_element_attributes["*"]
            or attribute.lower() in html_element_attributes.get(tag, [])
            else attribute
        )

    def _spaceless_left(self):
        return "-" if "spaceless-left" in self.raw_properties else ""

    def _spaceless_right(self):
        return "-" if "spaceless-right" in self.raw_properties else ""

    def _attributes(self):
        attribs = []
        if not self.raw_attributes:
            return ""

        for x in self.raw_attributes:
            value = re.sub(r"\s+", " ", x).strip()

            attribs.append(value)

        return " " + (" ").join(attribs) if len(attribs) > 0 else ""

    @property
    def attributes(self) -> str:
        if self._is_html:
            attribs = []
            if not self.raw_attributes:
                return ""

            for x in self.raw_attributes:
                key = self.__get_attribute_name(self.name, x[0])
                value = ""

                if x[1]:

                    value = re.sub(r"\s+", " ", x[1]).strip()

                    value = f'="{value}"'

                attribs.append(f"{key}{value}")

            return " " + (" ").join(attribs) if len(attribs) > 0 else ""

    def current_indent(self, level):
        return level * self.config.indent

    def format(self, level=0):

        if not self.hidden:

            if self.type in ["open", "void"]:
                if self.is_space_sensitive:
                    self.output += self.current_indent(level) + self.open_tag

                elif self.is_indentation_sensitive:
                    self.output += self.current_indent(level) + self.open_tag

                elif self.is_script:
                    self.output += self.current_indent(level) + self.open_tag
                    # self.ignored_level += 1

                else:
                    self.output += self.current_indent(level) + self.open_tag

                if not self.is_void:
                    level += 1
                    self.output += "\n"

            if self.type == "starttag_curly_perc":
                # print("here")
                # print(self.open_tag)
                self.output += self.current_indent(level) + self.open_tag

            self.output += ''.join(self.data)
#            if not self.tag.is_void:
            # self.last_sibling = self

            # if self.last_parent is None:
            #     self.last_parent = self
            # elif not self.is_void and not self.is_script:
            #     self.last_parent = self
            # elif self.is_script:
            #     self.last_parent = self.last_parent
            # else:
            #     self.last_parent = self.parent
            # print(self.name)

            # print(self.output)

        self.output += self.format_contents(level)
        if not self.is_void:
            level -= 1
        #self.output += self.current_indent()
        # self.last_sibling = close_tag

        # if close_tag.is_script:
        #     self.last_parent = self.get_open_parent(close_tag)
        # else:
        #     self.last_parent = self.get_open_parent(self.tag.parent)

        # if close_tag.is_script:
        #     self.ignored_level -= 1
        print(self.current_indent(level) + self.close_tag + "\n")
        self.output += self.current_indent(level) + self.close_tag + "\n"

        return self.output

    def format_contents(self, level):
        s = []
        for child in self.children:
            #print(f"{self.name}'s child: {child.name}")
            s.append(child.format(level))

        return "".join(s)
