import re
from itertools import chain
from typing import Dict, List, Optional, Tuple, Union

from HtmlElementAttributes import html_element_attributes
from HtmlStyles import html_styles
from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements

from djlint.settings import Config


class Tag:
    """
    The base node of a HTML tree.

    Arguments:
        tag (string): The HTML element name, like ``div``, ``a``, ``caption``, etc..
        config (djlint.settings.Conf): The parser config object.

    Keyword Arguments:
        parent (Tag): A tag object of this element parent if any.
        attributes (list): List of element attributes, each attribute a is tuple where
            first item is the attribute name and second item is the attribute value.
        properties (list): Some 'virtual' properties specific to some tags that may
            define special behaviors.
    """
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
        """
        Describe if Tag is an HTML element (as defined from Tag argument).

        This is more of a shortand since this method does not make any assertion and
        only returns what have been set in ``Tag._is_html`` instance attribute. On
        default, a Tag is not assumed as an HTML element, you need to set it yourself
        on the instance attribute.

        TODO: Despite return is typed to string, you may be able to just set instance
        attribute to ``True`` to qualify element as HTML.

        Returns:
            string: The value of ``Tag._is_html`` instance attribute. It may be
            ``False`` if attribute has never be explicitely set.
        """
        return self._is_html

    @is_html.setter
    def is_html(self, val: str) -> None:
        """
        Setter method to define value of ``Tag._is_html`` attribute.

        TODO: Despite typed as a string, the practical usage of is_html is boolean so
        it should be safe enough to type it as a boolean.

        Arguments:
            val (string): Value to set.
        """
        self._is_html = val

    def _spaceless_left(self) -> str:
        """
        Returns possible character to describe a spaceless marker at left position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.

        Returns:
            string: A single hyphen if element have the property ``spaceless-left``
            else return an empty string.
        """
        return "-" if "spaceless-left" in self.raw_properties else ""

    def _spaceless_right(self) -> str:
        """
        Returns possible character to describe a spaceless marker at right position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.

        Returns:
            string: A single hyphen if element have the property ``spaceless-right``
            else return an empty string.
        """
        return "-" if "spaceless-right" in self.raw_properties else ""

    def __get_tag_closing(self) -> str:
        """
        Returns element HTML tag ending syntax.

        Returns:
            string: `` />`` if element is a void HTML element, else ``>``.
        """
        if self.is_void:
            return " />"

        return ">"

    @property
    def open_tag(self) -> str:
        """
        Returns element HTML opening tag including its possible attributes.

        * If element is a HTML element, this will be the HTML opening tag like
          ``<p>``;
        * If element is a curly element with percent, this will be its closing form like
          ``{% endtag %}``;
        * Finally if element is not a HTML or a curly element, this will be an empty
          string.

        Returns:
            string: Opening tag string if available.
        """
        if self._is_html:
            if self.parent and (
                self.parent.is_indentation_sensitive or self.parent.is_space_sensitive
            ):
                return f"<{self.name}{self.attributes}{self.__get_tag_closing()}"
            else:
                return f"<{self.name}{self.attributes}{self.__get_tag_closing()}"

        if self.type == "starttag_curly_perc":
            return (
                f"{{%{self._spaceless_left()} {self.tag}{self._attributes()} "
                f"{self._spaceless_right()}%}}"
            )

        return ""

    @property
    def close_tag(self) -> str:
        """
        Returns element HTML closing tag.

        * If element is a HTML element and not a void HTML element, this will
          be the HTML closing tag like ``</p>``;
        * If element is a curly element with percent, this will be its closing form like
          ``{% endtag %}``;
        * Finally if element is not a HTML or a curly element, this will be an empty
          string.

        Returns:
            string: Closing tag string if available.
        """
        if self.is_void:
            return ""

        if self._is_html:
            if self.parent and (
                self.parent.is_indentation_sensitive or self.parent.is_space_sensitive
            ):
                return f"</{self.name}{self.__get_tag_closing()}"
            return f"</{self.name}{self.__get_tag_closing()}"

        if self.type == "endtag_curly_perc":
            return (
                f"{{%{self._spaceless_left()} end{self.tag}{self._attributes()} "
                f"{self._spaceless_right()}%}}"
            )

        return ""

    @property
    def statement_tag(self) -> str:
        """
        Returns element statement tag.

        Returns:
            string: The statement tag or an empty string, depending if element is a
            curly element or not.
        """
        if self.type == "curly":
            return f"{{{{ {self.tag}{self._attributes()} }}}}"

        return ""

    def __get_tag_style(self, style: str) -> Dict:
        """
        Returns all HTML element default value for given CSS property as defined from
        HTML5 W3C specification.

        Arguments:
            style (string): CSS property name to search for.

        Returns:
            dict: A dictionnary of all HTML element which have a default value for
            given CSS property. Where item key is the element name and item value is
            the default property value.
        """
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

    def __tag_is_pre(self, tag: str) -> bool:
        """
        Describe if Tag have preformatted text behavior.

        Element preformatted text status is determined from default element styles
        according to W3C CSS specifications.

        Whatever status is, if ``Tag._is_html`` is ``False`` this will always return
        ``False``.

        Returns:
            bool: True if element have a preformatted text behavior else ``False``.
        """
        if self._is_html:
            return self.__css_whitespace.get(
                tag, self.__css_default_whitespace
            ).startswith("pre")
        return False

    @property
    def is_space_sensitive(self) -> bool:
        """
        Check if tag is space sensitive.

        Space sensitivity is based on element CSS flow. If element is HTML, have a
        block alike flow and not a script element, it is not considered as sensitive.

        Returns:
            bool: A boolean whether the element is space sensitive or not.
        """
        if self._is_html:
            display = self.__css_display.get(self.name, self.__css_default_display)

            return (
                self.is_script
                or not display.startswith("table")
                and display not in ["block", "list-item", "inline-block"]
            )

        return False

    @property
    def is_indentation_sensitive(self) -> bool:
        """
        Check if tag is indentation sensitive.

        Indentation sensitivity is based on element CSS flow. If element is HTML and
        have a 'pre' alike flow it is considered as sensitive.

        TODO: It seems '__tag_is_pre' have already been used in 'self.is_pre' from
        '__init__' so it should be safe to rely on this instance attribute instead of
        running '__tag_is_pre' again each time 'is_indentation_sensitive' is called.

        Returns:
            bool: A boolean whether the element is indentation sensitive or not.
        """
        if self._is_html:
            return self.__tag_is_pre(self.name)

        return False

    @property
    def is_hidden(self) -> bool:
        """
        Describe if Tag is an hidden element.

        Element hidden status is determined from element CSS flow (block,
        inline, table, etc..) as defined in HTML specifications, element CSS style rules
        is not involved here.

        Whatever hidden status is, if ``Tag._is_html`` is ``False`` this will always
        return ``False``.

        TODO: This property is a little disturbing with the ``Tag.hidden`` attribute
        that does not seem to fullfill the same purpose.

        Returns:
            bool: True if element have a hidden status like body, meta, etc.. else
            ``False``.
        """
        if self._is_html:
            return (
                self.__css_display.get(self.name, self.__css_default_display) == "none"
            )

        return False

    @property
    def is_script(self) -> bool:
        """
        Describe if Tag is assumed as a 'script' element.

        Element script status is determined from the tag name.

        Whatever script status is, if ``Tag._is_html`` is ``False`` this will always
        return ``False``.

        TODO: <template> element should probably be assumed as a script element.

        Returns:
            bool: True if element is assumed as script element else ``False``.
        """
        if self._is_html:
            return self.name in ("script", "style", "svg:style")

        return False

    def __get_tag_name(self) -> Tuple[Optional[str], str]:
        """
        Get HTML element name and its possible namespace.

        Returns:
            tuple: The pair ``namespace, name``, where ``namespace`` can be
            None if no namespace have been found and ``name`` may be
            forced to lowercase if it is a knowed valid HTML element name, else it is
            left unchanged.
        """
        # tags with a namespace
        namespace = None
        tag = self.rawname
        if ":" in self.rawname:
            namespace = self.rawname.split(":")[0]
            tag = (":").join(self.rawname.split(":")[1:])

        return namespace, tag.lower() if tag.lower() in html_tag_names else tag

    def __get_attribute_name(self, tag: str, attribute: str) -> str:
        """
        Returns lowerized attribute name if it is a knowed attribute from
        function ``HtmlElementAttributes.html_element_attributes``.

        Arguments:
            tag (string): The HTML element name.
            attribute (string): The attribute name.

        Returns:
            string: Attribute name.
        """
        return (
            attribute.lower()
            if attribute.lower() in html_element_attributes["*"]
            or attribute.lower() in html_element_attributes.get(tag, [])
            else attribute
        )

    def _attributes(self):
        """
        Return attributes whatever the element is HTML or not.

        No normalization is applied here except whitespace divider between attributes.

        .. Note::
            For this method to work correctly, the attribute ``Tag.raw_attributes``
            must be set to a list of strings, like: ``['class="foo"', 'id="foo"']``.

        Returns:
            string: Empty string if there is no attribute or ``None`` if element is not
            HTML (as returned from ``_is_html``). Else it will return a string
            including all the attributes.
        """
        attribs = []
        if not self.raw_attributes:
            return ""

        for x in self.raw_attributes:
            value = re.sub(r"\s+", " ", x).strip()

            attribs.append(value)

        return " " + (" ").join(attribs) if len(attribs) > 0 else ""

    @property
    def attributes(self) -> str:
        """
        Return normalized attributes for a HTML element.

        Normalization is just about lowercase and whitespace divider between multiple
        attributes.

        .. Note::
            For this method to work correctly, the attribute ``Tag.raw_attributes``
            must be set to a list of tuples, like:
            ``[("class", "foo"), ("id", "foo")]``.

        Returns:
            string: Empty string if there is no attribute or ``None`` if element is not
            HTML (as returned from ``_is_html``). Else it will return a string
            including all the attributes.
        """
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
        """
        Compute final indentation to apply.

        This repeats the indentation string from ``Tag.config.indent`` for each level.
        Zero or negative level will return an empty string.

        Arguments:
            level (integer): Current element level in HTML tree.

        Returns:
            string: Indentation string to apply.
        """
        return level * self.config.indent

    def format_contents(self, level):
        """
        Return formatted output of current element children.

        Arguments:
            level (integer): Current element level in HTML tree.

        Returns:
            string: A string including a recursive output of children.
        """
        s = []
        for child in self.children:
            # print(f"{self.name}'s child: {child.name}")
            s.append(child.format(level))

        return "".join(s)

    def format(self, level=0):
        """
        Return formatted element output.

        This will recursively format current element and all of its children.

        Keyword Arguments:
            level (integer): The current element level, it will impact indentation
                width. Default to zero.

        Returns:
            string: Formatted element output.
        """
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
            # if not self.tag.is_void:
            #     self.last_sibling = self

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
        # self.output += self.current_indent()
        # self.last_sibling = close_tag

        # if close_tag.is_script:
        #     self.last_parent = self.get_open_parent(close_tag)
        # else:
        #     self.last_parent = self.get_open_parent(self.tag.parent)

        # if close_tag.is_script:
        #     self.ignored_level -= 1
        # print(self.current_indent(level) + self.close_tag + "\n")
        self.output += self.current_indent(level) + self.close_tag + "\n"

        return self.output
