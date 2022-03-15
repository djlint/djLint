import re
from itertools import chain
from typing import Dict, List, Optional, Tuple

from HtmlElementAttributes import html_element_attributes
from HtmlStyles import html_styles
from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements

from ...settings import Config


class Tag:
    def __init__(
        self,
        tag: str,
        config: Config,
        parent: Optional["Tag"] = None,
        attributes: Optional[List] = None,
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
        self.data: Optional[str] = None
        self.type: Optional[str] = None
        self.parent = parent
        self.rawname = tag
        self.namespace, self.name = self.__get_tag_name()
        self.is_pre = self.__tag_is_pre(self.name)
        self.raw_attributes = attributes
        self.is_void = self.name in html_void_elements

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
    def open_tag(self) -> str:
        if self.parent and (
            self.parent.is_indentation_sensitive or self.parent.is_space_sensitive
        ):
            return f"<{self.name}{self.attributes}{self.__get_tag_closing()}"
        else:
            return f"<{self.name}{self.attributes}{self.__get_tag_closing()}"

    @property
    def close_tag(self) -> str:
        if self.is_void:
            return ""

        if self.parent and (
            self.parent.is_indentation_sensitive or self.parent.is_space_sensitive
        ):
            return f"</{self.name}{self.__get_tag_closing()}"
        return f"</{self.name}{self.__get_tag_closing()}"

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
        display = self.__css_display.get(self.name, self.__css_default_display)
        #print(display)
        return self.is_script or not display.startswith("table") and display not in [
            "block",
            "list-item",
            "inline-block"
        ]

    @property
    def is_hidden(self) -> bool:
        return self.__css_display.get(self.name, self.__css_default_display) == "none"
    @property
    def is_indentation_sensitive(self) -> bool:
        return self.__tag_is_pre(self.name)

    def __tag_is_pre(self, tag: str) -> bool:
        return self.__css_whitespace.get(tag, self.__css_default_whitespace).startswith(
            "pre"
        )

    @property
    def is_script(self) -> bool:
        return self.name in ("script", "style", "svg:style")

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

    @property
    def attributes(self) -> str:

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
