from typing import List, Dict
import jsbeautifier
from jsbeautifier.javascript.options import BeautifierOptions as JsBeautifierOptions
from cssbeautifier.css.options import BeautifierOptions as CssBeautifierOptions
import cssbeautifier
from HtmlStyles import html_styles
from itertools import chain

ROOT_TAG_NAME = "djlint"
DATA_TAG_NAME = "djlint-data"

ROOT_ATTRIBUTE_NAME ="djlint-attribute"
DATA_ATTRIBUTE_NAME = "djlint-attribute-data"

VOID = "void"
CLOSE = "close"
DOCTYPE = "doctype"
ENDTAG_CURLY_PERC = "endtag_curly_perc"
ENDTAG_CURLY_TWO_SLASH = "endtag_curly_two_slash"
ENDTAG_CURLY_FOUR_SLASH = "endtag_curly_four_slash"
ENDTAG_COMMENT_CURLY_PERC = "endtag_comment_curly_perc"
OPEN = "open"
STARTTAG_CURLY_PERC = "starttag_curly_perc"
STARTTAG_CURLY_FOUR = "starttag_curly_four"
STARTTAG_CURLY_TWO_HASH = "starttag_curly_two_hash"
STARTTAG_COMMENT_CURLY_PERC = "starttag_comment_curly_perc"

COMMENT_CURLY_HASH = "comment_curly_hash"
COMMENT_AT_STAR = "comment_at_star"
COMMENT = "comment"

SINGLE_QUOTE="djlint-single-quote"
DOUBLE_QUOTE="djlint-double-quote"
ALL_QUOTES = [SINGLE_QUOTE,DOUBLE_QUOTE]

CURLY_TWO_EXCAIM = "curly_two_exlaim"
CURLY_TWO = "curly_two"
SLASH_CURLY_TWO = "slash_curly_two"
CURLY_THREE = "curly_three"

ALL_CLOSE_TYPES = [
    CLOSE,
    ENDTAG_CURLY_PERC,
    ENDTAG_CURLY_TWO_SLASH,
    ENDTAG_CURLY_FOUR_SLASH,
    ENDTAG_COMMENT_CURLY_PERC,
]
ALL_CLOSE_TEMPLATE_TYPES = [
    ENDTAG_CURLY_PERC,
    ENDTAG_CURLY_TWO_SLASH,
    ENDTAG_CURLY_FOUR_SLASH,
    ENDTAG_COMMENT_CURLY_PERC,
]
ALL_OPEN_TYPES = [
    OPEN,
    STARTTAG_CURLY_PERC,
    STARTTAG_CURLY_FOUR,
    STARTTAG_CURLY_TWO_HASH,
    STARTTAG_COMMENT_CURLY_PERC,
]
ALL_OPEN_TEMPLATE_TYPES = [
    STARTTAG_CURLY_PERC,
    STARTTAG_CURLY_FOUR,
    STARTTAG_CURLY_TWO_HASH,
    STARTTAG_COMMENT_CURLY_PERC,
]
ALL_COMMENT_TYPES = [COMMENT, COMMENT_CURLY_HASH, COMMENT_AT_STAR]
ALL_STATEMENT_TYPES = [CURLY_TWO_EXCAIM, CURLY_TWO, SLASH_CURLY_TWO, CURLY_THREE]

# property values must match html-attribute-formatter prop names
HAS_TRAILING_SPACE = "has-trailing-space"
HAS_TRAILING_BREAK = "has-trailing-break"
HAS_TRAILING_BREAKS = "has-trailing-breaks"
HAS_TRAILING_CLOSE_BREAK="has-trailing-close-break"
HAS_TRAILING_CLOSE_SPACE="has-trailing-close-space"
SPACELESS_LEFT_DASH = "spaceless-left-dash"
SPACELESS_LEFT_TILDE = "spaceless-left-tilde"
SPACELESS_LEFT_PLUS = "spaceless-left-plus"
SAFE_LEFT = "safe-left"
PARTIAL = "partial"
SPACELESS_RIGHT_DASH = "spaceless-right-dash"
SPACELESS_RIGHT_TILDE = "spaceless-right-tilde"
SPACELESS_RIGHT_PLUS = "spaceless-right-plus"
HAS_VALUE = "has-value"

CSS_DEFAULT_WHITESPACE = "normal"
CSS_DEFAULT_DISPLAY = "inline"

def get_tag_styles(style: str) -> Dict:
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
CSS_DISPLAY = dict(
            list(get_tag_styles("display").items())
            + list(
                {
                    "button": "inline-block",
                    "template": "block",
                    "source": "inline",
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


CSS_WHITESPACE = get_tag_styles("white-space")


class Softline:
    parent = None
    previous_element = None
    next_element = None
    indent = 0
    sibling_length = 0
    force_hardbreak = False

    def __str__(self):
        return __class__.__name__

    def __repr__(self):
        return self.__str__()

    def resolve(self, indent=""):
        #if hard_break and self.next_element:
        if self.force_hardbreak:# and self.next_element:
            # print("breaking", len(indent))
            return "\n" + indent
        # if not self.next_element:
        #     print("missing next", self.previous_element)
        return ""

    def __len__(self):
        return 0




    def has_child_type(self, search_type):
        return isinstance(self,search_type)

    def flatten(self, config):
        # count indent parents
        el = self.parent
        indent = 0
        while el:
            if isinstance(el,Indent):
                indent += 1

            el= el.parent

        # get sibling indent from parents
        el = self

        while el.parent:
            if isinstance(el.next_element, Indent):
                indent+=1
                break
            el = el.parent

        self.indent = indent
        return self


class Line:
    parent=None
    previous_element = None
    next_element = None
    indent = 0
    def __init__(self, nested=False):
        self.nested=nested



    def __str__(self):
        return __class__.__name__

    def __repr__(self):
        return self.__str__()

    def resolve(self, hard_break=True, indent=""):
        if hard_break == True:
            return "\n" + indent
        if self.next_element:
            return " "
        return ""

    def __len__(self):
        return 1

    def closest(self,search_type):
        el = self.parent
        while el:
            if isinstance(el,search_type):
                return el
            el = el.parent
        return 0

    def has_child_type(self, search_type):
        return isinstance(self,search_type)

    def flatten(self, config):
        el = self.parent
        indent = 0
        while el:
            if isinstance(el,Indent):
                indent += 1

            el= el.parent
        self.indent = indent
        return self

class BreakParent:
    parent=None
    previous_element = None
    next_element = None
    def __str__(self):
        return __class__.__name__

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return 0

    def has_child_type(self, search_type):
        return isinstance(self,search_type)

class Hardline:
    parent=None
    previous_element = None
    next_element = None
    indent = 0
    def __str__(self):
        return __class__.__name__

    def __repr__(self):
        return self.__str__()

    def resolve(self, indent=""):
        return "\n" + indent

    def __len__(self):
        return 0

    @property
    def has_next_element(self):
        if self.next_element:
            return True
        return False

    def has_child_type(self, search_type):
        return isinstance(self,search_type)

    def flatten(self, config):
        el = self.parent
        indent = 0
        while el:
            if isinstance(el,Indent):
                indent += 1

            el= el.parent
        if isinstance(self.next_element, Indent):
            indent+=1
        self.indent = indent
        return self

def list_builder(elements):
    processed = []
    if isinstance(elements, List):
        for element in elements:
            processed.extend(list_builder(element))

    elif (
        elements
        or isinstance(elements, Softline)
        or isinstance(elements, Hardline)
        or isinstance(elements, BreakParent)
        or isinstance(elements, Line)
    ):
        processed.append(elements)

    return processed


class Group:
    def __init__(self, elements=[]):
        self.parent=None
        self.previous_element = None
        self.next_element = None
        self.elements = []
        self.appender(elements)

    def appender(self, elements):

        new = list_builder(elements)
        # print('calling appender', self.elements, new)

        for x, element in enumerate(new):
            if type(element) in [Group, Indent, Hardline,Softline,Script,Style,Line, Fill]:
                element.parent=self
                if x==0 and self.elements:
                    element.previous_element=self.elements[-1]
                    if not isinstance(self.elements[-1],str):
                        self.elements[-1].next_element=element
                if x > 0:
                    element.previous_element=new[x-1]
                if x+1 < len(new):
                    element.next_element=new[x+1]

        self.elements.extend(new)

    def resolve(self):
        return "".join(self.elements)

    def __str__(self, level=0):
        out = []

        for x, element in enumerate(self.elements):

            if isinstance(element, Indent) or isinstance(element, Group):
                out.append(element.__repr__(level).strip())
            else:
                if isinstance(element,str) and element.strip() == "":
                    out.append(str("<space>"))
                else:
                    out.append(str(element))
        spacing = "\n" + level * "  "
        less_spacing = "\n" + max(level - 1, 0) * "  "
        contents = spacing + (spacing).join(out) + less_spacing
        return f"{__class__.__name__}([{contents}])"

    def __repr__(self, level=1):
        spacing = "\n" + level * "  "
        return f"{spacing}{self.__str__(level+1)}\n"

    def __iter__(self):
        for attr in self.elements:
            yield attr

    def __len__(self):
        return sum(len(x) for x in self.elements)

    def __getitem__(self, item):
        return self.elements[item]

    def get_elements(self):
        return self.elements

    def has_immediate_child_type(self, search_type):
        return any(isinstance(x, search_type) for x in self.elements)



    def find_first_child_of_type(self, mytype):
        for element in self.elements:
            # print(type(element))
            if isinstance(element,mytype):
                # print("returning", element)
                return element
            elif type(element) in [Group,Indent]:
                # print("searching child", type(element))
                el = element.find_first_child_of_type(mytype)
                if el:
                    return el

        return None

    @property
    def has_hardline(self):
        return any(isinstance(x,Hardline) for x in self.elements)

    def has_child_type(self, search_type):
        if isinstance(self, search_type):
            return True

        return any(not isinstance(x,str) and x.has_child_type(search_type) for x in self.elements)


    def flatten(self, config):
        flattened = []

        # if a child hardline, set the immediate breaks to forced.
        # breaks are one group deep

        # if self.has_child_type(Hardline) and self.has_immediate_child_type(Softline) and not self.has_immediate_child_type(Hardline):
        #     for x in self.elements:
        #         if isinstance(x,Softline):
        #             x.force_hardbreak = True

        # print(self.__len__())
        if self.__len__() > config.max_line_length:

            els = self.elements
            while els:
                found=False
                new_els = []
                for x in els:
                    if isinstance(x,Softline):
                        x.force_hardbreak = True
                        found = True

                    if type(x) in [Indent, Group]:
                        new_els.extend(x.elements)
                if found == True:
                    break
                # print(new_els)
                els = new_els

        # if self.has_child_type(Hardline) and not self.has_immediate_child_type(Hardline):
        #     els = self.elements
        #     while els:
        #         found=False
        #         new_els = []
        #         for x in els:
        #             if type(x) in [Indent, Group]:
        #                 new_els.extend(x.elements)
        #                 if x.has_immediate_child_type(Hardline):
        #                     break

        #             if isinstance(x,Softline):
        #                 x.force_hardbreak = True
        #                 found = True


        #         if found == True:
        #             break
        #         # print(new_els)
        #         els = new_els

        for x in self.elements:
            if isinstance(x, str):
                flattened.append(x)
            else:

                flat_child = x.flatten(config)

                if isinstance(flat_child,List):
                    flattened.extend(flat_child)
                else:
                    flattened.append(flat_child)
        return flattened


class Fill:
    type = "Fill"

    def __init__(self, data):
        self.data = data
        self.parent = None
        self.previous_element = None
        self.next_element = None
        self.indent = 0
    def appender(self, element):
        self.data.extend(list_builder(element))
    def __str__(self):
        return f"{__class__.__name__}({self.data})"

    def __repr__(self):
        return "\n  " + self.__str__() + "\n"

    def __len__(self):
        return len(" ".join(self.data))

    def resolve(self, indent, end, first_line_length):
        start = len(indent)
        if isinstance(self.data, List):
            data = " ".join(self.data)
        else:
            data = self.data


        allowed_length = end - (first_line_length or start)

        # print(len(data),first_line_length, end, allowed_length)

        if len(data) < allowed_length:
            return data

        data = data.split(" ")

        chunk_list = []
        chunk = ""
        for x in data:

            if len(chunk) + len(x) > allowed_length:
                chunk_list.append(chunk)
                chunk = x.lstrip()
                allowed_length = end - start
            elif chunk != "":
                chunk += " " + x
            else:
                chunk = x.lstrip()

        chunk_list.append(chunk)
        # spacing = f"{start * ' '}"
        return  (f"\n{indent}").join(chunk_list)

    def has_child_type(self, search_type):
        return isinstance(self,search_type)

    def flatten(self, config):
        indent = 0
        el = self.parent
        while el:
            if isinstance(el,Indent):
                indent += 1

            el= el.parent
        self.indent = indent
        return self

class Script:
    def __init__(self, data, config):
        self.data=" ".join(data)
        self.config = config
        self.parent = None
        self.previous_element = None
        self.next_element = None
        self.indent = 0
    def __str__(self):
        return __class__.__name__

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.data)



    def resolve(self):
        # use config to set if indentation is tab, space, and size of it.
        # indent is passed from the writer as the base indent size.
        opts = JsBeautifierOptions({"indent_size":self.config.indent, "indent_level":self.indent})
        return jsbeautifier.beautify(self.data, opts)
    def has_child_type(self, search_type):
        return isinstance(self,search_type)

    def flatten(self, config):
        indent=0
        el = self.parent
        while el:
            if isinstance(el,Indent):
                indent += 1

            el= el.parent
        self.indent = indent
        return self


class Style:
    def __init__(self, config, elements=[]):
        self.elements=elements
        self.config = config
        self.parent = None
        self.previous_element = None
        self.next_element = None
    def appender(self, element):
        self.elements.extend(list_builder(element))
    def __str__(self):
        return __class__.__name__

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return sum(len(x) for x in self.elements)


    def resolve(self):
        # use config to set if indentation is tab, space, and size of it.
        # indent is passed from the writer as the base indent size.
        opts = CssBeautifierOptions({"indent_size":self.config.indent, "indent_level":self.indent})
        return cssbeautifier.beautify(" ".join(self.elements), opts)
    def has_child_type(self, search_type):
        return isinstance(self,search_type)

    def flatten(self, config):
        indent=0
        el = self.parent
        while el:
            if isinstance(el,Indent):
                indent += 1

            el= el.parent
        self.indent = indent
        return self

class String:
    pass
class Indent:
    def __init__(self, config):
        self.elements = []
        self.config = config
        self.parent = None
        self.previous_element = None
        self.next_element = None

    def __str__(self, level=0):
        out = []

        for x, element in enumerate(self.elements):

            if isinstance(element, Indent):
                out.append(element.__repr__(level).strip())
            elif isinstance(element, Group):
                out.append(element.__repr__(level).strip())
            else:
                if isinstance(element,str) and element.strip() == "":
                    out.append(str("<space>"))
                else:
                    out.append(str(element))
        spacing = "\n" + level * "  "
        less_spacing = "\n" + max(level - 1, 0) * "  "
        contents = spacing + (spacing).join(out) + less_spacing
        return f"{__class__.__name__}([{contents}])"

    def __repr__(self, level=1):
        spacing = "\n" + level * "  "
        return f"{spacing}{self.__str__(level+1)}\n"

    def appender(self, element):
        new = list_builder(element)

        for x, element in enumerate(new):
            if type(element) in [Group, Indent, Hardline,Softline,Script,Style,Line, Fill]:
                element.parent=self

                if x==0 and self.elements:
                    element.previous_element=self.elements[-1]
                    self.elements[-1].next_element=element
                if x > 0:
                    element.previous_element=new[x-1]
                if x+1 < len(new):
                    element.next_element=new[x+1]

        self.elements.extend(new)

    def get_elements(self):
        return self.elements
    def has_immediate_child_type(self, search_type):
        return any(isinstance(x, search_type) for x in self.elements)

    @property
    def has_hardline(self):
        return any(isinstance(x,Hardline) for x in self.elements)

    def has_child_type(self, search_type):
        if isinstance(self, search_type):
            return True

        return  any(not isinstance(x,str) and x.has_child_type(search_type) for x in self.elements)

    def __len__(self):
        # also need to add in the current indent. If type is a tab do tab * width?
        return sum(len(x) for x in self.elements)



    def find_first_child_of_type(self, mytype):
        for element in self.elements:
            if isinstance(element,mytype):
                return element
            elif type(element) in [Group,Indent]:
                el = element.find_first_child_of_type(mytype)
                if el:
                    return el

        return None
    def flatten(self, config):
        flattened = []

        for x in self.elements:
            if isinstance(x, str):
                flattened.append(x)
            else:
                if isinstance(x, Softline):
                    # pass content length to softline
                    x.sibling_length = self.__len__()

                flat_child = x.flatten(config)
                if isinstance(flat_child,List):
                    flattened.extend(flat_child)
                else:
                    flattened.append(flat_child)
        return flattened

