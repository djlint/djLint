"""Attribute tag additions to the base Tag class.

The only purpose of this class is to keep logic that is
dedicated to the attributes separated from the standard
Tag logic.

Also formatting of attribute is done slightly differently than
the html tag formatting.
"""
import re
from typing import Dict, List, Optional, Tuple, Union, TypeVar

from HtmlElementAttributes import html_element_attributes

from djlint.settings import Config

from .tools import *
from HtmlElementAttributes import html_element_attributes

Self = TypeVar("Self", bound="Tag")

class AttributeTag:
    # any override methods here.
    def __init__(
        self,
        tag: str,
        config: Config,
        parent_tag: str,
        attributes: Optional[List] = None,
        properties: Optional[List] = None,
    ):

        self.tag = tag
        self.config = config
        self.parent = None
        self.parent_tag = parent_tag or ""
        self.previous_tag = None
        self.next_tag = None
        self.raw_attributes = attributes
        self.properties = properties or []
        self.children = []
        self.data: List[str] = []
        self.base_level = 0
        self.output = []
        self.trailing_space=[]
        self.has_quoted_value = False

        self.namespace = None
        self.type: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.type} ({self.data} props:{self.properties})"

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, val: str) -> None:
        self._type = val

    def get_next_element(self):

        if self.parent:

            for x, child in enumerate(self.parent.children):
                if child == self and self.parent.children[x+1:]:
                    return self.parent.children[x+1]

    @property
    def name(self):
        if self.data:
            return self.data[0]

        return self.tag

    def get_last_data(self):
        if self.data:
            return "".join(self.data)[-1]
        return None

    def get_first_data(self):
        if self.data:
            return "".join(self.data)[0]
        return None


    def _previous_with_prop(self, prop):

        if self.previous_tag:
            if prop in self.previous_tag.properties:
                return self.previous_tag

            return self.previous_tag._previous_with_prop(prop)
        return None

    def _next_with_prop(self, prop):

        if self.next_tag:
            if prop in self.next_tag.properties:
                return self.next_tag

            return self.next_tag._next_with_prop(prop)
        return None

    def _nested_quote_level(self, level=0):

        if self.parent:
            if self.parent.type in ALL_QUOTES:
                level += 1

            level += self.parent._nested_quote_level(level)

        return level

    def has_nested_quote(self):
        if self.children:
            for child in self.children:
                if child.type in ALL_QUOTES:
                    return True
                if child.has_nested_quote():
                    return True
        return False



    @property
    def _get_quote(self):
        # check the nested level of the quote.
        # print(self, self.previous_tag)
        # if (self.type in ALL_QUOTES
        #     or (self.previous_tag and self.previous_tag._has_value and self.parent.type not in ALL_QUOTES)
        #     and self.has_nested_quote):
        #     if self.type == SINGLE_QUOTE:
        #         return "'"
        #     if self.type == DOUBLE_QUOTE:
        #         return '"'

        # else:
        #     return '"'

        if (self.type in ALL_QUOTES
            or (self.previous_tag and self.previous_tag._has_value and self.parent.type not in ALL_QUOTES)):
            # print("getting quote")
            if self.has_nested_quote:
                if self.type == SINGLE_QUOTE:
                    return "'"
                if self.type == DOUBLE_QUOTE:
                    return '"'
            return '"'
            # level = self._nested_quote_level()

            # if level == 0:
            #     return '"'
            # elif level == 1:
            #     return "'"
            # elif level % 2 == 0:
            #     return '"'
            # return "'"

        return ""

    @property
    def is_space_sensitive(self) -> bool:
        if self.name in ['class', 'style']:
            return False
        return True

    @property
    def _has_leading_space(self) -> bool:
        if self.previous_tag and self.previous_tag._has_trailing_space:
            return True

        # or if we are the first child of a parent w/ trailing space
        if (
            self.parent
            and self.parent._has_trailing_space
            and self.parent.children[0] == self
        ):
            return True

    @property
    def _has_trailing_space(self) -> bool:
        return HAS_TRAILING_SPACE in self.properties

    @property
    def _has_trailing_close_space(self) -> bool:
        return HAS_TRAILING_CLOSE_SPACE in self.properties

    @property
    def _has_trailing_break(self) -> bool:
        return HAS_TRAILING_BREAK in self.properties

    @property
    def _has_value(self) -> bool:
        return HAS_VALUE in self.properties

    @property
    def _break_before(self) -> bool:
        if (
            HAS_TRAILING_SPACE in self.previous_tag.properties
        ):  # and self._is_in_attribute_value is False:
            return ""  # return "\n"

        return ""

    @property
    def _break_after(self) -> str:
        return ""
        if self.name == ROOT_ATTRIBUTE_NAME and self.children:
            return Softline()

    @property
    def _space_before(self) -> str:
        """
        Handles space before text.
        """
        if (
            self.parent
            and self.parent.name == ROOT_ATTRIBUTE_NAME
            and not self.previous_tag
        ):
            if self.parent_tag == DOCTYPE:
                return " "

            return Line()

        if self._has_leading_space:
            if self.previous_tag and self.previous_tag._has_trailing_space:
                # print("skipping")
                return ""
            if (
                self.parent
                and self.parent.name in ALL_QUOTES
                and self.parent.previous_tag
                and not self.parent.previous_tag._has_value
            ):
                return " "


    def last_child(self):
        if self.children:
            return self.children[-1]

        return None

    def first_child(self):
        if self.children:
            return self.children[0]

        return None

    @property
    def _space_after(self) -> str:
        # print(self)
        if (
            not self.next_tag
            and self.tag != ROOT_ATTRIBUTE_NAME
            and self.parent
            and self.parent.name not in ALL_QUOTES
        ):
            return "" #Softline()

        if self._has_value and not self.is_attribute_value:
            return ""

        # print(self.name[-1], self.next_tag.name if self.next_tag else "")
        # if self.name[-1] in [":"]:
        #     """
        #     Keep nice formatting on spread out attributes.

        #     attrib="{ this: true, that:false }"
        #              ^     ^     ^
        #     """
        #     return " "
        if self.name[-1] in [";", ","]:
            """
            Keep nice formatting on spread out attributes.

            attrib="{ this: true; that:false }"
                                 ^
            """
            if self.get_attribute_tag().name in ['style']:
                return ""
            if self.get_attribute_tag().name in ['data-srcset', 'sizes', 'srcset']:
                return Line(nested=True)
            return " "

        if self.next_tag and self.parent and self.parent.type not in ALL_QUOTES and self.next_tag.name[0] in ["}"]:
            """
            Keep nice formatting on spread out attributes.

            attrib="{ this: true }"
                                ^
            """
            # print(self, self.parent)
            return " "

        if self._has_trailing_break and self.is_attribute_value and self.parent.last_child() != self and self.get_attribute_tag().is_space_sensitive:

            # print(self, len(self.trailing_space))
            # print(self.is_attribute_value )
            # (
            # self.parent and
            # self.parent.tag in ALL_QUOTES or
            # (
            #     self.previous_tag and
            #     self.previous_tag._has_value and
            #     self.type not in ALL_QUOTES
            # ))


            return "".join(self.trailing_space)

        if self._has_trailing_space:
            # print(self)
            if (
                self.parent
                and self.parent.name in ALL_QUOTES
                and self.parent.previous_tag
                and not self.parent.previous_tag._has_value
                and self.parent.last_child() != self
            ):

                return " "

            if self._nested_quote_level() < 1:
                if self.parent_tag == DOCTYPE:
                    return " "

                return Line()

            if self.next_tag and self.parent and self.parent.last_child() != self:
                if self.parent_tag == DOCTYPE:
                    return " "
                if self.name in ALL_QUOTES and self.get_next_element().get_first_data() in [',']:
                    # verify what is following the quotes.. if in json return nothing
                    return ""

                if self.is_attribute_value:
                    if self.get_attribute_tag().name == "style" and self.next_tag.name.startswith(":"):
                        return ""
                    return " "

                # if self.is_attribute_value and self.get_attribute_tag().name in ['data-srcset', "sizes"]:# self.get_next_element().get_first_data() in [',']
                #     return " "

                # if self.is_attribute_value and self.get_attribute_tag().is_space_sensitive:
                #     return " "

                # if (self.is_attribute_value and
                #     (
                #         self.get_next_element().get_last_data() in [',']
                #         or  self.get_next_element() and not self.get_next_element().get_next_element() and self.get_attribute_tag().name in ['data-srcset']
                #     )
                #     ):
                #     """
                #     data-srcset="a.png 100w,
                #                       ^
                #                  b.png 200w"
                #                       ^
                #     """
                #     return " "

                # print(self, self.get_next_element().get_next_element())
                return Line()

            # if self.parent.last_child() != self:
            #     return " "
            # print(self)
            # if self.parent and self.parent.last_child() == self and self.parent.type in ALL_QUOTES and self.parent.is_attribute_value :
            #     print(self)
            #     return " "
            # if self.parent:
            #     if self.parent.is_attribute_value:
            #         return Line(nested=True)
            #     return Line()

        if self._has_trailing_close_space:
            return " "
        if (
            self.name in ALL_QUOTES
            and self.last_child()
            and not self.last_child().next_tag
            and not self.is_attribute_value
        ):
            # if the last item
            return ""

        if self.name in ALL_QUOTES:
            if self._nested_quote_level() < 1:
                if self.parent_tag == DOCTYPE:
                    return " "
                # print("adding line here")
                return Line()


        # if (self.type in ALL_QUOTES
        #     and self.is_attribute_value and self.last_child()._has_trailing_space):
        #     return " "
        # print("skipping")
        return ""


    def get_profile(self) -> str:
        if self.config.profile != "all":
            return self.config.profile

        if self.parent:
            return self.parent.get_profile()

        return self.config.profile
    def __get_spaceless_left(self) -> str:
        """
        Returns possible character to describe a spaceless marker at left position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.
        """
        if SPACELESS_LEFT_DASH in self.properties:
            return "-"

        if SPACELESS_LEFT_TILDE in self.properties:
            return "~"

        if SPACELESS_LEFT_PLUS in self.properties:
            return "+"

        return ""

    def __get_spaceless_right(self) -> str:
        """
        Returns possible character to describe a spaceless marker at right position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.
        """
        if SPACELESS_RIGHT_DASH in self.properties:
            return "-"

        if SPACELESS_RIGHT_TILDE in self.properties:
            return "~"

        if SPACELESS_RIGHT_PLUS in self.properties:
            return "+"

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

        return ""

    def __get_tag_closing(self) -> str:
        """
        Returns tag ending syntax.

        For example, an html ending `` />`` or template ``%}``.
        """
        if self.type == COMMENT:
            return "-->"

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

    def __get_template_space(self) -> str:
        """
        Returns a possible whitespace character that will be include inside the
        template tag on the left and right position of the tag.
        """
        # if profile == handlebars or mustache, exclude the spaces.
        # we should try to guess the profile......

        return " " if self.get_profile() != "handlebars" else ""

    def __get_attribute_name(self, tag) -> str:
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
            tag.lower()
            if tag.lower() in html_element_attributes["*"]
            or tag.lower() in html_element_attributes.get(self.parent_tag.lower(), [])
            else tag
        )

    def __get_attribute_value(self) -> str:
        # should do some cleanup here.
        if self.raw_attributes:
            return " " + self.raw_attributes.strip()
        return ""

    def _clean_data(self):
        style = " ".join(self.data)
        # print(style)
        # return style

        # clean up space
        # style = re.sub(r'\s*(:|;|,)\s*(?!$)',r'\1 ',style, re.M)

        # if self.next_tag and self.next_tag.type in ALL_QUOTES and not self._has_trailing_space:
        #     style = re.sub(r'\s*(:|;|,)\s*',r'\1 ',style, re.M)

        # else:
        #     style = re.sub(r'\s*(:|;|,)\s*(?!$)',r'\1 ',style, re.M)

        # if not self._has_trailing_space or self.next_tag and self.next_tag.type in ALL_QUOTES:
        #     print(self.next_tag)
        #     style= style.strip()


        return style

    def _clean_style(self):
        style = " ".join(self.data).strip()

        # clean up space
        style = re.sub(r'\s*(:|;|,)\s*',r'\1 ',style)

        style = style.rstrip(" ") # semi and space. if the attribute was not fed with spaces they will be a solid line.

        return style

    @property
    def is_attribute_value(self) -> bool:
        return (
            self.parent and
            self.parent.tag in ALL_QUOTES or
            (
                self.previous_tag and
                self.previous_tag._has_value and
                self.type not in ALL_QUOTES
            ))

    def get_attribute_tag(self) -> Self:
        if self.is_attribute_value:
            if(
            self.parent and
            self.parent.tag in ALL_QUOTES
            and self.parent.previous_tag
            and self.parent.previous_tag._has_value
            ):
                return self.parent.previous_tag

            if (
                self.previous_tag and
                self.previous_tag._has_value and
                self.type not in ALL_QUOTES
            ):
                return self.previous_tag

        return None

    def _get_data(self):
        # if inside quotes, don't need to fix case
        if (
            self.type in [DATA_ATTRIBUTE_NAME,ROOT_ATTRIBUTE_NAME, SINGLE_QUOTE,DOUBLE_QUOTE]
            and
            (
            self.is_attribute_value
        )):
            if self.parent.previous_tag and self.parent.previous_tag.name == "style":
                data = []
                raw_data = self._clean_style()

                trailing_semi = False
                if raw_data.endswith(";") and self.parent.last_child() != self:
                    trailing_semi=True
                    raw_data= raw_data.rstrip(";")

                # print(raw_data)
                # if self.parent.first_child() == self:
                #     data.append(Softline())

                if self.parent.last_child() == self:
                    raw_data = raw_data.rstrip(";")
                split_data = raw_data.split(";")

                for x, el in enumerate(split_data):

                    data.append(el.strip() if not el.strip().endswith(",") else el.strip() + " ")
                    if x+1 <len(split_data):
                        data.extend([';',Line(nested=True)])

                if trailing_semi:
                    data.extend([";", Line(nested=True)])
                return data

            # if self.parent.previous_tag and self.parent.previous_tag.name == "srcset":
            return self._clean_data()

        # if self.type == CURLY_TWO:
        #     # print(self.get_attribute_tag().name)
        #     return f"{self.__get_tag_opening()}{self.__get_template_space()}{self.name}{self.__get_template_space()}{self.__get_tag_closing()}"

        if (self.type in ALL_OPEN_TEMPLATE_TYPES
            or self.type in ALL_CLOSE_TEMPLATE_TYPES
            or self.type in ALL_STATEMENT_TYPES
            or self.type in ALL_COMMENT_TYPES):
            # print(self.raw_attributes)
            return f"{self.__get_tag_opening()}{self.__get_template_space()}{self.name}{self.__get_attribute_value()}{self.__get_template_space()}{self.__get_tag_closing()}"

        return " ".join([self.__get_attribute_name(x) for x in self.data])

    def format_contents(self, level=0):
        """
        Return formatted output of current element children.

        Arguments:
            level (integer): Current element level in HTML tree.

        Returns:
            string: A string including a recursive output of children.
        """
        s = []
        for child in self.children:
            formated = list_builder(child.format())

            # print(child, child.is_attribute_value or child.type in ALL_QUOTES)
            if len(s) > 0 and isinstance(s[-1], Group) and (child.is_attribute_value or child.type in ALL_QUOTES):
                if isinstance(formated[-1],Line):
                    s[-1].appender(formated[:-1])
                    s.extend(formated[-1:])
                else:
                    # print(s[-1])
                    s[-1].appender(formated)
            else:
                s.extend(formated)

        return s

    def appender(self, stuff):
        self.output.extend(list_builder(stuff))

    def format(self, level=0):

        # print(self)
        quote = self._get_quote

        group = self

        group.appender(self._space_before)

        if self._has_value:
            group = Group()


        if self.type not in ALL_QUOTES:
            group.appender(quote)

        group.appender(self._get_data())

        if self._has_value:
            if self._has_trailing_space and self.is_attribute_value:
                group.appender(" ")
            group.appender("=")

        if self.type in ALL_QUOTES:
            group.appender(quote)

        if self.tag in ALL_QUOTES:# or self.is_attribute_value:# previous_tag and self.previous_tag._has_value:
            contents = Indent(self.config)
        else:
            contents = Indent(self.config)

        contents.appender(self.format_contents())

        group.appender(contents)
        group.appender(quote)

        if group != self:
            self.appender(group
)
        self.appender(self._space_after)

        self.appender(self._break_after)

        return self.output

    @property
    def statement_tag(self):
        return self.tag
