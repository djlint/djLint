"""Base tag class.

A tag represents any html/template element.
"""

import re

from typing import Dict, List, Optional, Tuple, Union, TypeVar


from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements

from djlint.settings import Config

from .attribute_builder import AttributeTreeBuilder
from .tools import *

Self = TypeVar("Self", bound="Tag")

class Tag:
    """
    The base node of a HTML tree.

    Arguments:
        tag (string): The HTML element name, like ``div``, ``a``, ``caption``, etc..
        config (djlint.settings.Conf): The parser config object.

    Keyword Arguments:
        parent (Tag): A tag object of this element parent if any.
        attributes (str): string of potential attributes for an html element or
            template tag.
        properties (list): Some 'virtual' properties specific to some tags that may
            define special behaviors.
    """

    def __init__(
        self,
        tag: str,
        config: Config,
        parent: Optional["Tag"] = None,
        attributes: Optional[str] = None,
        properties: Optional[List] = [],
    ) -> None:

        self._data: List[str] = [] # data is updated/accessed with the getter/setter functions
        self._type: Optional[str] = None # type is updated/access with the getter/setter functions.
        self._is_html = False # is_html is updated/access with the getter/setter functions.
        self.parent = parent
        self.config = config
        self.previous_tag = None
        self.next_tag = None
        self.rawname = tag
        self.children = []
        self.output = []
        self.hidden = False
        self.tag = tag
        self.namespace, self.name = self.__get_tag_name()
        self.raw_attributes = attributes
        self.raw_properties = properties or []
        self.is_void = self.name in html_void_elements + ["extends", "load", "include"]
        self.css_display=CSS_DISPLAY.get(self.name,CSS_DEFAULT_DISPLAY)


    def __str__(self) -> str:
        """
        String representation of the tag.

        returns name (type). ex "div (open)"
        """
        return f"{self.name} ({self.type})"

    @property
    def data(self) -> Optional[str]:
        """
        Hold any data content for the Tag here. Generally html/template
        tags will have not data, but the data will be in a data type tag
        that is a child of the html/template tag.

        data getter function.
        """
        return self._data

    @data.setter
    def data(self, val: str) -> None:
        """
        Add data to a tag.

        Setter method to define value of ``Tag.data`` attribute.

        Arguments:
            val (string): Value to set.
        """
        self._data = val

    @property
    def type(self) -> Optional[str]:
        """
        Describe the Tag type, eg open, close, curly_two, etc

        type getter function.
        """
        return self._type

    @type.setter
    def type(self, val: str) -> None:
        """
        Setter method to define value of ``Tag.type`` attribute.

        Arguments:
            val (string): Value to set.
        """
        self._type = val

    @property
    def is_html(self) -> bool:
        """
        Describe if Tag is an HTML element (as defined from Tag argument).

        is_html getter function.
        """
        return self._is_html

    @is_html.setter
    def is_html(self, val: str) -> None:
        """
        Setter method to define value of ``Tag.is_html`` attribute.

        Arguments:
            val (string): Value to set.
        """
        self._is_html = val

    def first_child(self) -> Optional[Self]:
        """
        Method to return the first child of the current Tag.

        A child is any tag type, including data, template tags, and close tags.
        """
        if self.children:
            return self.children[0]

        return None

    def last_child(self) -> Optional[Self]:
        """
        Method to return the last child of the current Tag.

        A child is any tag type, including data, template tags, and close tags.
        """
        if self.children:
            return self.children[-1]

        return None

    def first_element(self) -> Optional[Self]:
        """
        Method to return the first element of the current Tag.

        An element is considered any non-close tag.
        """
        if self.children:
            for child in self.children:
                if child not in ALL_CLOSE_TYPES:
                    return child

        return None

    def last_element(self) -> Optional[Self]:
        """
        Method to return the last element of the current Tag.

        An element is considered any non-close tag.
        """
        if self.children:
            for child in reversed(self.children):
                if child not in ALL_CLOSE_TYPES:
                    return child

        return None

    def is_last_child(self) -> bool:
        return self.parent and self.parent.last_element() == self

    @property
    def elements(self) -> List[Self]:
        """
        Property to return the all child element of the current Tag.

        An element is considered any non-close tag.
        """
        if self.children:
            return [x for x in self.children if x.type not in ALL_CLOSE_TYPES]
        return []

    def set_profile(self, profile) -> str:
        # todo: add config setting to disable profile guessing
        if self.config.profile == "all":
            self.config.profile = profile

        # set all parents
        if self.parent:
            self.parent.set_profile(profile)

    def get_profile(self) -> str:
        if self.config.profile != "all":
            return self.config.profile

        if self.parent:
            return self.parent.get_profile()

        return self.config.profile

    def __get_template_space(self) -> str:
        """
        Returns a possible whitespace character that will be include inside the
        template tag on the left and right position of the tag.
        """
        # if profile == handlebars or mustache, exclude the spaces.
        # we should try to guess the profile......

        return " " if self.get_profile() != "handlebars" else ""

    def __get_partial(self) -> str:
        """
        Returns possible character to describe a partial marker at left position
        inside an element tag.

        This is only for the curly tag syntax which support it like Handlebars.
        """

        return "> " if PARTIAL in self.raw_properties else ""

    def __get_safe_left(self) -> str:
        if SAFE_LEFT in self.raw_properties:
            return "--"

        return ""

    def __get_spaceless_left(self) -> str:
        """
        Returns possible character to describe a spaceless marker at left position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.
        """
        if SPACELESS_LEFT_DASH in self.raw_properties:
            return "-"

        if SPACELESS_LEFT_TILDE in self.raw_properties:
            return "~"

        if SPACELESS_LEFT_PLUS in self.raw_properties:
            return "+"

        return ""

    def __get_spaceless_right(self) -> str:
        """
        Returns possible character to describe a spaceless marker at right position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.
        """
        if SPACELESS_RIGHT_DASH in self.raw_properties:
            return "-"

        if SPACELESS_RIGHT_TILDE in self.raw_properties:
            return "~"

        if SPACELESS_RIGHT_PLUS in self.raw_properties:
            return "+"

        return ""

    def __get_tag_closing(self) -> str:
        """
        Returns tag ending syntax.

        For example, an html ending `` />`` or template ``%}``.
        """
        if self.is_void:
            return "/>"

        if self.is_html:
            if self.type == COMMENT:
                return "-->"
            return ">"

        if self.type in [STARTTAG_CURLY_PERC, ENDTAG_CURLY_PERC]:
            return self.__get_spaceless_right() + "%}"

        if self.type in [STARTTAG_CURLY_FOUR, ENDTAG_CURLY_FOUR_SLASH]:
            return self.__get_spaceless_right() + "}}}}"

        if self.type in [
            CURLY_TWO_EXCAIM,
            CURLY_TWO,
            STARTTAG_CURLY_TWO_HASH,
            ENDTAG_CURLY_TWO_SLASH,
            SLASH_CURLY_TWO,
        ]:
            return self.__get_spaceless_right() + "}}"

        if self.type == CURLY_THREE:
            return self.__get_spaceless_right() + "}}}"
        if self.type == COMMENT_CURLY_HASH:
            return self.__get_spaceless_right() + "#}"
        return ""

    def __get_tag_opening(self) -> str:
        """
        Returns tag opening syntax.

        For example, an html start ``<`` or template ``{%``.
        """
        if self.type in [STARTTAG_CURLY_PERC, ENDTAG_CURLY_PERC]:
            return "{%" + self.__get_spaceless_left()

        if self.type == STARTTAG_CURLY_FOUR:
            return "{{{{" + self.__get_spaceless_left()

        if self.type == CURLY_THREE:
            return "{{{" + self.__get_spaceless_left()

        if self.type == STARTTAG_CURLY_TWO_HASH:
            return f"{{{{{self.__get_spaceless_left()}#"

        if self.type == ENDTAG_CURLY_FOUR_SLASH:
            return f"{{{{{{{{{self.__get_spaceless_left()}/"

        if self.type == ENDTAG_CURLY_TWO_SLASH:
            return f"{{{{{self.__get_spaceless_left()}/"

        if self.type == CURLY_TWO:
            return "{{" + self.__get_spaceless_left()

        if self.type == CURLY_TWO_EXCAIM:
            return "{{!" + self.__get_spaceless_left()

        if self.type == COMMENT and self.is_html:
            return "<!--"

        if self.type == SLASH_CURLY_TWO:
            return "\\{{" + self.__get_spaceless_left()

        if self.type == COMMENT_CURLY_HASH:
            return "{#" + self.__get_spaceless_left()

        if self.type == DOCTYPE:
            return "<!"

        if self.type == OPEN or self.type == VOID:
            return "<"

        return "</"

    def __get_tag_modifier(self) -> str:
        """
        Returns tag name modifier.

        Used specifically for django/jinja end tags.
        """
        if self.type == ENDTAG_CURLY_PERC:
            return "end"
        return ""

    @property
    def open_tag_opening(self) -> str:
        """
        Returns opening tag including its possible attributes.

        * If element is a HTML element, this will be the HTML opening tag like
          ``<p>``;
        * If element is a curly element with percent, this will be its closing form like
          ``{% endtag %}``;
        """
        if self.tag in [ROOT_TAG_NAME, DATA_TAG_NAME]:
            # Root tag does not have opening tag.
            return ""

        if self.type in ALL_CLOSE_TYPES:
            # Close tags is not an opening tag.
            return ""

        if self.is_html:
            if self.type in COMMENT:
                start = f"{self.__get_tag_opening()}{self.tag}"
            else:
                start = f"{self.__get_tag_opening()}{self.name}"
            # self.indent_padding = len(start)

            if self.is_void:
                # print("Here! open tag opening void")

                return [start, self._attributes, " "]#, Line()]

            return [start, self._attributes]

        start = f"{self.__get_tag_opening()}{self.__get_partial()}{self.__get_template_space()}{self.tag}"

        # self.indent_padding = len(start)

        return [start, self._attributes, self.__get_template_space()]


    @property
    def close_tag_opening(self) -> str:
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
        # print(self, self.last_child())

        if self.previous_tag and self.previous_tag.needs_to_borrow_parent_closing_tag_start_marker:
            # if self.is_pre:
            #     return Hardline()
            return Softline()

        if self.tag in [DOCTYPE, ROOT_TAG_NAME]:
            return ""

        if self.type in ALL_OPEN_TYPES:
            return ""

        if self.is_void or self.type in [COMMENT]:
            return ""

        if self.is_html:
            if self.parent and (
                self.parent.is_indentation_sensitive
                or self.parent.is_whitespace_sensitive
            ):
                return f"{self.__get_tag_opening()}{self.name}"
            return f"{self.__get_tag_opening()}{self.name}"

        if self.type in ALL_CLOSE_TEMPLATE_TYPES:
            return [
                self.__get_tag_opening(),
                self.__get_partial(),
                self.__get_safe_left(),
                self.__get_template_space(),
                self.__get_tag_modifier(),
                self.tag,
                self._attributes,
                self.__get_template_space(),
            ]

        return ""

    @property
    def open_tag_closing(self) -> str:
        """
        Returns closing tag including its possible attributes.
        """
        if self.next_tag and self.next_tag.needs_to_borrow_last_child_closing_tag_end_marker:
            return ""

        if self.tag in [ROOT_TAG_NAME, DATA_TAG_NAME]:
            return ""

        if self.type in ALL_CLOSE_TYPES:
            return ""

        if (
            self.next_tag
            and self.next_tag.needs_to_borrow_prev_closing_tag_end_marker
            and self.is_void is False
        ):
            return ""

        if self.first_child() and self.first_child().needs_to_borrow_parent_opening_tag_end_marker and self.is_void is False:
            return Softline()


        return self.__get_tag_closing()


    @property
    def close_tag_closing(self) -> str:
        if self.tag in [DOCTYPE, ROOT_TAG_NAME]:
            return ""

        if self.type in ALL_OPEN_TYPES:
            return ""

        if self.is_void or self.type in [COMMENT]:
            return ""

        if self.next_tag and self.next_tag.needs_to_borrow_prev_closing_tag_end_marker:
            return ""

        if self.is_html:
            return self.__get_tag_closing()

        if self.type in ALL_CLOSE_TEMPLATE_TYPES:
            return self.__get_tag_closing()

        return ""

    @property
    def parent_tag_close_opening(self) -> str:
        if self.needs_to_borrow_parent_closing_tag_start_marker:
            return f"{self.next_tag.__get_tag_opening()}{self.next_tag.name}"
        return ""

    @property
    def last_child_close_closing(self) -> str:
        if self.needs_to_borrow_last_child_closing_tag_end_marker:
            return [Softline(), f"{self.previous_tag.__get_tag_closing()}"]

    @property
    def parent_tag_open_tag_closing(self) -> str:
        if self.needs_to_borrow_parent_opening_tag_end_marker:
            return self.parent.__get_tag_closing()

    @property
    def previous_tag_close_tag_closing(self) -> str:
        # if self.tag == DATA_TAG_NAME:
        #     return ""
        # print(self, self.needs_to_borrow_parent_opening_tag_end_marker)


        if not self.previous_tag:
            return ""

        if self.previous_tag.tag in [DOCTYPE, ROOT_TAG_NAME]:
            return ""

        if self.previous_tag.is_void or self.previous_tag.type in [COMMENT]:
            return ""

        if self.needs_to_borrow_prev_closing_tag_end_marker:
            # print("sending")
            return self.previous_tag.__get_tag_closing()

        return ""

    @property
    def statement_tag(self) -> str:
        """
        Returns element statement tag.

        Returns:
            string: The statement tag or an empty string, depending if element is a
            curly element or not.
        """
        return [
            self.__get_tag_opening(),
            self.__get_partial(),
            self.__get_safe_left(),
            self.__get_template_space(),
            self.tag,
            self._attributes,
            self.__get_template_space(),
            self.__get_tag_closing(),
        ]

    @property
    def is_pre(self) -> bool:
        """
        Describe if Tag have preformatted text behavior.

        Element preformatted text status is determined from default element styles
        according to W3C CSS specifications.

        Whatever status is, if ``Tag._is_html`` is ``False`` this will always return
        ``False``.

        Returns:
            bool: True if element have a preformatted text behavior else ``False``.
        """
        if self.is_html:
            return CSS_WHITESPACE.get(
                self.name, CSS_DEFAULT_WHITESPACE
            ).startswith("pre")
        return False

    @property
    def is_whitespace_sensitive(self) -> bool:
        """
        Check if tag is space sensitive.

        Space sensitivity is based on element CSS flow. If element is HTML, have a
        block alike flow and not a script element, it is not considered as sensitive.

        Returns:
            bool: A boolean whether the element is space sensitive or not.
        """

        # if self.is_html:
        #     display = self.css_display

        return (
            self.is_script
            or not self.is_html
            # or not display.startswith("table")
            # and display not in ["block", "list-item", "inline-block"]
            or self.is_indentation_sensitive
        )

        # return False

    @property
    def is_first_child_leading_space_sensitive_css_display(self) -> bool:
        return not self.is_display_block_like and self.css_display != "inline-block"

    @property
    def is_next_leading_space_sensitive_css_display(self) -> bool:
        return not self.is_display_block_like and not self.is_display_none

    @property
    def has_surrounding_breaks(self) -> bool:
        if self.has_trailing_break and self.has_leading_break:
            return True

        if self.parent.name == ROOT_TAG_NAME and self.previous_tag is None and self.has_trailing_break:
            return True

    @property
    def is_prefer_hardline_as_surrounding_space(self) -> bool:
        if self.is_html and self.name == 'br' or self.has_surrounding_breaks:
            return True

        return False

    @property
    def is_leading_space_sensitive(self) -> bool:
        """
        Check if tag is sensitive to leading space.
        """
        if self.type == COMMENT:
            return False

        if self.type in ALL_CLOSE_TYPES and self.is_display_block_like or self.css_display == "inline-block":
            return False

        if (self.type == DATA_TAG_NAME
            and self.previous_tag
            and self.previous_tag.type == DATA_TAG_NAME
        ):
            return True

        if not self.parent or self.parent.css_display=='none':
            return False

        if self.parent.is_pre:
            return True

        if (not self.previous_tag
            and (
                (self.parent and self.parent.tag == ROOT_TAG_NAME)
                or (self.is_pre and self.parent)
                or (self.parent and self.parent.is_script)
                or not self.parent.is_first_child_leading_space_sensitive_css_display
        )):
            return False

        if (
            self.previous_tag
            and not self.previous_tag.is_next_leading_space_sensitive_css_display
        ):
            return False

        if self.is_display_block_like:
            return False

        return True

    @property
    def is_trailing_space_sensitive(self) -> bool:
        if (
            self.type == DATA_TAG_NAME
            and self.next_tag
            and (self.next_tag == DATA_TAG_NAME or self.next_tag.type in ALL_CLOSE_TYPES)
        ):

            return True

        if not self.parent or self.parent.is_display_none:
            return False

        if self.is_pre:
            return True

        if (self.is_last_child #not self.next_tag
          and (
            (self.parent and self.parent.tag == ROOT_TAG_NAME)
            or (self.is_pre and self.parent)
            or (self.parent and self.parent.is_script)
            or not self.parent.is_last_child_trailing_space_sensitive_css_display
        )):
            return False

        if (
            self.next_tag
            and self.next_tag.type not in ALL_CLOSE_TYPES
            and not self.next_tag.is_prev_trailing_space_sensitive_css_display
        ):
            # print("sending false")
            return False

        return True

    @property
    def is_indentation_sensitive(self) -> bool:
        """
        Check if tag is indentation sensitive.

        Indentation sensitivity is based on element CSS flow. If element is HTML and
        have a 'pre' alike flow it is considered as sensitive.

        Returns:
            bool: A boolean whether the element is indentation sensitive or not.
        """
        if self.is_html:
            return self.is_pre

        return False

    @property
    def is_dangling_space_sensitive(self) -> bool:
        return (
            not self.is_script
            and self.css_display != "inline-block"
            and not self.is_display_block_like
        )

    @property
    def is_display_none(self) -> bool:
        """
        Describe if Tag is an hidden element.

        Element hidden status is determined from element CSS flow (block,
        inline, table, etc..) as defined in HTML specifications, element CSS style rules
        is not involved here.

        Whatever hidden status is, if ``Tag.is_html`` is ``False`` this will always
        return ``False``.

        TODO: This property is a little disturbing with the ``Tag.hidden`` attribute
        that does not seem to fullfill the same purpose.

        Returns:
            bool: True if element have a hidden status like body, meta, etc.. else
            ``False``.
        """
        if self.is_html:
            return (
                self.css_display == "none"
            )

        return False

    @property
    def is_display_block_like(self) -> bool:
        return self.css_display in ["block", "list-item"] or self.css_display.startswith("table")

    @property
    def has_trailing_space(self) -> bool:
        return HAS_TRAILING_SPACE in self.raw_properties

    @property
    def has_trailing_break(self) -> bool:
        return HAS_TRAILING_BREAK in self.raw_properties or HAS_TRAILING_BREAKS in self.raw_properties

    @property
    def has_trailing_breaks(self) -> bool:
        return HAS_TRAILING_BREAKS in self.raw_properties

    @property
    def has_leading_breaks(self) -> bool:
        return (
            self.previous_tag and HAS_TRAILING_BREAKS in self.previous_tag.raw_properties
        )

    @property
    def is_last_child_trailing_space_sensitive_css_display(self) -> bool:
        return not self.is_display_block_like and self.css_display != "inline-block"

    @property
    def is_prev_trailing_space_sensitive_css_display(self) -> bool:
        return not self.is_display_block_like



    @property
    def is_script(self) -> bool:
        """
        Describe if Tag is assumed as a 'script' element.

        Element script status is determined from the tag name.

        Whatever script status is, if ``Tag.is_html`` is ``False`` this will always
        return ``False``.

        TODO: <template> element should probably be assumed as a script element.

        Returns:
            bool: True if element is assumed as script element else ``False``.
        """
        if self.is_html:
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

        if tag.lower() in html_tag_names:
            tag = tag.lower()
        if tag.lower() == "doctype":
            tag = "DOCTYPE"
        return namespace, tag

    @property
    def _attributes(self) -> str:
        """
        Return normalized attributes for a HTML element.

        Normalization is just about lowercase and whitespace divider between multiple
        attributes.

        Returns:
            string: Empty string if there is no attribute or ``None`` if element is not
            HTML (as returned from ``is_html``). Else it will return a string
            including all the attributes.
        """
        if not self.raw_attributes:
            return ""

        if self.is_html:
            p = AttributeTreeBuilder(
                self.config, self.raw_attributes, self.tag, 0
            )
            return p.format()

        # template attributes
        return " " + self.raw_attributes

    def format_contents(self):
        """
        Return formatted output of current element children.

        Returns:
            string: A string including a recursive output of children.
        """
        s = []
        for child in self.children:


            formated = child.format()

            if child.type in ALL_CLOSE_TYPES and len(s) > 0 and isinstance(s[-1], Group) and formated:
                # merge the close tag with the previous group
                # print(type(s[-1]), s, formated, formated[0].elements)
                s[-1].appender(formated[0])

                formated = formated[1:]
                # print(formated)
            #     s[-1] = s[-1].appender(list_builder(formated))
            # else:
            s.extend(list_builder(formated))
            # print(s)

        return s

    @property
    def has_empty_data(self) -> bool:
        return not any(x.strip() for x in self.data)
    @property
    def has_nontext_child(self) -> bool:
        return any(x for x in self.children if x.type != DATA_TAG_NAME)

    @property
    def has_next_element(self) -> bool:
        return self.parent and self.parent.last_element() != self

    @property
    def has_leading_space(self) -> bool:
        return self.previous_tag and (
            HAS_TRAILING_BREAK in self.previous_tag.raw_properties
            or HAS_TRAILING_SPACE in self.previous_tag.raw_properties
        )

    @property
    def has_leading_break(self) -> bool:
        return (
            self.previous_tag and HAS_TRAILING_BREAK in self.previous_tag.raw_properties
        )

    @property
    def should_hug_content(self) -> bool:
        return (
            len(self.children) == 1
            and self.first_child().type in ALL_STATEMENT_TYPES
            and self.first_child().is_leading_space_sensitive
            and not self.first_child().has_leading_space
            and self.last_child().is_trailing_space_sensitive
            and not self.last_child().has_trailing_space
        )

    @property
    def should_force_break_children(self) -> bool:
        return (
            self.type != DATA_TAG_NAME
            and self.children
            and (
                self.name in ["html", "head", "ul", "ol", "select"]
                or (
                    self.css_display.startswith("table")
                    and self.css_display != "table-cell"
                )
            )
        )

    @property
    def should_force_break(self) -> bool:
        return (
            self.should_force_break_children
            or (
                self.type != DATA_TAG_NAME
                and self.children
                and (
                    self.name in ["body", "script", "style"]
                    or self.children
                    and any(x.has_nontext_child or x.is_pre
                     for x in self.children)
                )
            )
            or (
                self.first_element()
                and (
                    # first is open tag, last is close tag.
                    self.first_element().name == self.last_element().name
                    )
                and self.first_element().type != DATA_TAG_NAME
                and self.first_element().has_leading_break
                and (
                    not self.last_element().is_trailing_space_sensitive
                    or self.last_element().has_trailing_break
                )
            )
        )

    @property
    def break_before_children(self) -> str:
        # print("should force", self, self.should_force_break)
        return self.should_force_break and self.tag != ROOT_TAG_NAME


    def print_line_before_children(self) -> str:
        # print(self.tag, self.tag == ROOT_TAG_NAME)
        if self.tag == ROOT_TAG_NAME:
            # print("skipping")
            return ""

        if not self.children:
            return ""

        if self.should_hug_content:
            return ""

        if (
            self.first_child()
            and self.first_child().has_leading_space
            and self.first_child().is_leading_space_sensitive
        ):
            """
            <a> <span>
               ^> this needs to stay.
            """
            if self.has_trailing_breaks:
                return Hardline()
            return Line()

        if (
            self.first_child()
            and self.first_child().type == DATA_TAG_NAME
            and self.is_whitespace_sensitive
            and self.is_indentation_sensitive
        ):
            return ""

        if self.is_dangling_space_sensitive and self.has_trailing_space is False:
            return ""

        if self.break_before_children:
            # print(self.break_before_children)
            # print("hard")
            return Hardline()

        return Softline()

    @property
    def needs_to_borrow_parent_closing_tag_start_marker(self) -> bool:
        return (not self.has_next_element and
                not self.has_leading_space and
                self.next_tag and self.next_tag.is_leading_space_sensitive and
                self.type==DATA_TAG_NAME)

    @property
    def needs_to_borrow_parent_opening_tag_end_marker(self) -> bool:
        # print(self, self.previous_tag, self.is_leading_space_sensitive)
        return ((not self.previous_tag
            or self.parent.first_child() == self)
            and self.is_leading_space_sensitive and not self.has_leading_space and not self.parent.has_trailing_space)

    @property
    def needs_to_borrow_next_opening_tag_marker(self) -> bool:
        return self.next_tag and not self.next_tag.type == DATA_TAG_NAME and self.type == DATA_TAG_NAME and self.is_trailing_space_sensitive and not self.has_trailing_space

    @property
    def needs_to_borrow_last_child_closing_tag_end_marker(self) -> bool:
        # print(self, self.previous_tag, self.children)
        # if self.previous_tag:
        #     print(self.is_leading_space_sensitive, self.is_trailing_space_sensitive, self.previous_tag.is_trailing_space_sensitive, self.previous_tag.has_trailing_space)

        return (#self.children and (close tag has no children)
             self.type == CLOSE
            and self.previous_tag
            and (self.previous_tag.is_trailing_space_sensitive or self.is_leading_space_sensitive)
            and not self.previous_tag.has_trailing_space
            and self.previous_tag.type != DATA_TAG_NAME and not self.is_pre)

    @property
    def needs_to_borrow_prev_closing_tag_end_marker(self) -> bool:
        # print(self, self.is_leading_space_sensitive)
        return (
            self.previous_tag and self.previous_tag.first_child() != self # not if we are the first child
            and self.previous_tag.tag != DOCTYPE
            # and self.previous_tag.tag != DATA_TAG_NAME
            and self.previous_tag.type not in [STARTTAG_CURLY_PERC]
            and self.is_leading_space_sensitive
            and self.type != CLOSE  # closing tags are not leading sensitive.
            and not self.has_leading_space
        )

    def print_line_between_children(self) -> str:
        # print(self, self.data, self.has_empty_data)
        if self.parent and len(self.parent.elements) == 1:
            return ""

        # print(self, self.parent, self.parent.last_child() if self.parent else None)
        if not self.has_next_element:
            return ""

        if self.type == DOCTYPE:
            if self.next_tag:
                return Hardline()
            return ""

        if self.type in [OPEN]:
            return ""

        if self.type == DATA_TAG_NAME and self.has_empty_data:
            return ""

        if self.should_force_break_children:

            return Hardline()


        if (
            self.is_void
            and self.has_next_element
            and self.is_prefer_hardline_as_surrounding_space
        ):
            if self.has_trailing_breaks:
                return [Hardline(), Hardline()]

            return Hardline()

        if (self.type == DATA_TAG_NAME
            and self.next_tag and self.next_tag.type == DATA_TAG_NAME):
            if self.is_trailing_space_sensitive:
                if self.has_trailing_space:
                    if self.is_prefer_hardline_as_surrounding_space:

                        return Hardline()

                    return Line()
                if self.is_prefer_hardline_as_surrounding_space:
                    return Hardline()
            return SoftLine()


        if self.needs_to_borrow_next_opening_tag_marker and (self.next_tag.first_child() or self.next_tag.is_void or (self.next_tag.type == OPEN and self.next_tag.attributes)
            or self.is_void and self.needs_to_borrow_prev_closing_tag_end_marker):
            return ""

        # print(self.next_tag,  self.next_tag.is_leading_space_sensitive if self.next_tag else None)

        if self.next_tag and not self.next_tag.is_leading_space_sensitive:
            if self.has_trailing_breaks:
                return [Hardline(), Hardline()]
            # print("hardline")

            return Hardline()

        if self.next_tag and self.next_tag.has_leading_space and self.next_tag.is_leading_space_sensitive:
            if self.has_trailing_breaks:
                return [Hardline(), Hardline()]
            if self.has_trailing_break:
                print("harline", self.data)
                return Hardline()
            # print(self.next_tag)
            # print("sending line!")
            return Line()

        if self.tag == ROOT_TAG_NAME:
            return ""

        return Softline()


        # if (
        #     self.next_tag
        #     and self.next_tag.type in [OPEN, VOID]
        #     and self.type in [CLOSE, COMMENT]
        #     and self.parent.last_child() != self
        # ):
        #     if self.next_tag.needs_to_borrow_prev_closing_tag_end_marker:
        #         return Softline()
        #     return Hardline()

        # if self.is_dangling_space_sensitive and self.parent and self.parent.last_child() != self and (
        #     self.has_trailing_space or self.has_trailing_break
        # ):
        #     # line will enforce either a break or a space.
        #     if self.is_prefer_hardline_as_surrounding_space:
        #         return Hardline()
        #     return Line()

        # if (
        #     self.is_void
        #     and self.next_tag
        #     and not self.next_tag.is_dangling_space_sensitive
        # ):
        #     return Hardline()

        # if not self.is_dangling_space_sensitive and self.type != CLOSE:
        #     return Softline()


        # return ""

    def print_line_after_children(self) -> str:
        # this function is only for the LAST child
        # if not the last child, then get out.
        if self.type in ALL_CLOSE_TYPES:
            return ""


        # if the last child is not beside a close tag then skip.
        # structure is like:
        # parent (self)
        #    child one
        #    child two (last_child())
        # close tag (last_child().next_tag)
        if self.last_child() and self.last_child().next_tag and self.last_child().next_tag.type not in ALL_CLOSE_TYPES:
            return ""

        # print(self)

        if self.tag == ROOT_TAG_NAME:
            # always end the file with a hard line break.
            return Hardline()

        if self.type in [OPEN, COMMENT] and not self.children:
            # print(self, self.is_trailing_space_sensitive, self.next_tag and self.next_tag.is_leading_space_sensitive, self.css_display)
            if self.has_trailing_space and (self.is_trailing_space_sensitive or (self.next_tag and self.next_tag.is_leading_space_sensitive)):
                # empty tag containing space <x> </x>
                return Line()
            return ""

        if self.type == DATA_TAG_NAME and self.has_empty_data:
            return ""

        needs_to_borrow = False
        if self.next_tag:
            needs_to_borrow = self.next_tag.needs_to_borrow_prev_closing_tag_end_marker
        elif self.parent:
            needs_to_borrow = self.parent.needs_to_borrow_prev_closing_tag_end_marker

        if needs_to_borrow:
            if (
                self.last_child()
                and self.last_child().has_trailing_space
                and self.last_child().is_trailing_space_sensitive
            ):
                return " "

            return ""

        if self.should_hug_content:

            return ""

        if (
            self.last_child()
            and self.last_child().has_trailing_space
            and self.last_child().is_trailing_space_sensitive
            and self.is_leading_space_sensitive
        ):
            if self.last_child().has_trailing_breaks:
                return [Hardline(), Hardline()]
            return Hardline()

        if self.last_child() and (
            self.last_child().type in [COMMENT, OPEN]
            or (
                self.last_child().type == DATA_TAG_NAME
                and self.is_whitespace_sensitive
                and self.is_indentation_sensitive
            )
        ):
            return ""

        if self.type == DATA_TAG_NAME:
            return ""

        # skip dangling
        if (
            self.is_dangling_space_sensitive
            and self.last_child()
            and not self.last_child().has_trailing_space
        ):
            return ""

        if self.break_before_children:
            return Hardline()

        return Softline()

    def appender(self, stuff):
        self.output.extend(list_builder(stuff))

    def format(self):
        """
        Return formatted element output.

        This will recursively format current element and all of its children.

        Returns:
            string: Formatted element output.

        """
        # print(self.tag, self.parent.tag if self.parent else None)
        # print(self.type, (self.parent.type if self.parent else None))
        # print(self.previous_tag.type if self.previous_tag else None )
        # print([self.previous_tag_close_tag_closing, self.open_tag_opening, self.open_tag_closing])
        # print(self.tag, self.raw_properties, self.has_trailing_space)

        group = self

        # if self.type in ALL_OPEN_TYPES:
            # start a new group
        group = Group()

        group.appender(
            Group(
                [
                    self.previous_tag_close_tag_closing,
                    self.parent_tag_open_tag_closing,
                    self.last_child_close_closing,
                    self.open_tag_opening,
                    self.open_tag_closing,
                ]
            )
        )

        if not self.is_void and self.tag != DATA_TAG_NAME:
            # group.appender(self.break_before_children())
            group.appender(self.print_line_before_children())
            if self.tag in ROOT_TAG_NAME:
                contents = Group()
            else:
                contents = Indent(self.config)
            contents_group = Group()
            contents_group.appender(self.format_contents())
            contents.appender(contents_group)
            group.appender(contents)
            group.appender(self.print_line_after_children())


        if self.tag == DATA_TAG_NAME and self.data:
            if self.parent.name == "script":
                # format with jsbeautify or cssbeautify.
                script = Script(self.data, self.config)
                group.appender(script)
            elif self.parent.name == "style":
                style = Style(self.config, self.data)
                group.appender(style)
            else:
                # print(self.parent, self.parent.css_display,  self.parent.is_pre)
                if self.parent.is_pre:
                    if self.data:
                        self.data[-1] = self.data[-1] + self.parent_tag_close_opening
                    else:
                        self.data=[self.parent_tag_close_opening]
                    group.appender(Fill(self.data))
                else:
                    # consolidate breaks
                    data = [re.sub(r"\s+"," ", x.strip()) for x in self.data if x.strip()!=""]

                    # print(self, data, self.raw_properties)

                    # this should be added to the prev tag.
                    # if self.has_leading_breaks:
                    #     if data:
                    #         data[0]= data[0] + "\n"
                    #     else:
                    #         data = ["\n"]

                    # if self.has_trailing_breaks:
                    #     # preserve trailing breaks around text
                    #     if data:
                    #         data[-1]= data[-1] + "\n"
                    #     else:
                    #         data = ["\n"]
                    if (self.has_trailing_space) and self.next_tag and self.next_tag.name == DATA_TAG_NAME:#self.next_tag.is_leading_space_sensitive:
                        if data:
                            data[-1]= data[-1].rstrip() + " "
                        else:
                            data = [' ']

                    if data:
                        data[-1] = data[-1] + self.parent_tag_close_opening
                    else:
                        data = [self.parent_tag_close_opening]
                    group.appender(Fill(data))

        group.appender([self.close_tag_opening, self.close_tag_closing])

        if group != self:
            self.appender(group)

        self.appender(self.print_line_between_children())

        return self.output
