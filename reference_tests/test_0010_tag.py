"""
Describing Tag object behaviors
"""
import pytest

from src.djlint.formatter.utils import Tag


def test_failure_tag_spaceless_left_without_props(basic_config) -> None:
    """
    Demonstrate that a Tag with a curly type and without properties will raise an
    exception in methods 'Tag._spaceless_left' and 'Tag._spaceless_right'.

    Some methods like 'open_tag' and 'close_tag' are affected with this behavior.

    TODO:
        'Tag._spaceless_left' and 'Tag._spaceless_right' should be safer and/or at least
        'Tag.properties' should be set to an empty list if not given.
    """
    current_tag = Tag("div", basic_config)
    current_tag.type = "starttag_curly_perc"

    with pytest.raises(TypeError):
        current_tag.open_tag


@pytest.mark.parametrize("source, expected", [
    (
        "foo",
        (None, "foo"),
    ),
    (
        "FoO",
        (None, "FoO"),
    ),
    (
        "Div",
        (None, "div"),
    ),
    (
        "namespace:p",
        ("namespace", "p"),
    ),
])
def test_tag_get_tag_name(basic_config, source, expected) -> None:
    """
    Method should correctly split HTML element name and its possible namespace.
    """
    tag = Tag(source, basic_config)

    assert tag._Tag__get_tag_name() == expected


@pytest.mark.parametrize("element, attribute, expected", [
    (
        "foo",
        "class",
        "class",
    ),
    (
        "foo",
        "Class",
        "class",
    ),
    (
        "foo",
        "Href",
        "Href",
    ),
    (
        "a",
        "Href",
        "href",
    ),
    (
        "foo",
        "Klass",
        "Klass",
    ),
    (
        "div",
        "Data-attr-foo",
        "Data-attr-foo",
    ),
])
def test_tag_get_attribute_name(basic_config, element, attribute, expected) -> None:
    """
    Method should lowerize attribute name if it is knowed attribute.

    Note than this method is stateless, it don't care about class arguments or instance
    attributes.
    """
    tag = Tag("dummy", basic_config)

    assert tag._Tag__get_attribute_name(element, attribute) == expected


@pytest.mark.parametrize("source, attributes, is_html, expected", [
    (
        "p",
        [],
        True,
        "",
    ),
    (
        "p",
        [("foo", "bar"),],
        False,
        None,
    ),
    (
        "p",
        [("foo", " bar"),],
        True,
        " foo=\"bar\"",
    ),
    (
        "p",
        [
            ("FOO", "bar"),
            ("CLASS", "plop"),
            ("zip", "zap"),
        ],
        True,
        " FOO=\"bar\" class=\"plop\" zip=\"zap\"",
    ),
    # TODO: Tag.attributes property method lack of a returns when is_html is False. In
    # this case it just always returns None despite method describes a string return.
    (
        "p",
        None,
        False,
        None,
    ),
])
def test_tag_attributes_property(
    basic_config, source, attributes, is_html, expected
) -> None:
    """
    Property should returns normalized attributes for a HTML element.
    """
    tag = Tag(source, basic_config, attributes=attributes)
    tag.is_html = is_html

    assert tag.attributes == expected


@pytest.mark.parametrize("source, attributes, expected", [
    (
        "p",
        None,
        "",
    ),
    (
        "p",
        [],
        "",
    ),
    (
        "p",
        ['foo'],
        ' foo',
    ),
    (
        "p",
        ['foo="bar"'],
        ' foo="bar"',
    ),
    (
        "p",
        [" foo=\"bar\"", "selected", "ping='pong'", "ZIP=\"Zap\"",],
        " foo=\"bar\" selected ping='pong' ZIP=\"Zap\"",
    ),
])
def test_tag_attributes_method(basic_config, source, attributes, expected) -> None:
    """
    Method should join attributes correctly.
    """
    tag = Tag(source, basic_config, attributes=attributes)

    assert tag._attributes() == expected


@pytest.mark.parametrize("source", [
    "foo",
    "p",
    "namespace:div",
])
def test_tag_is_html(basic_config, source) -> None:
    """
    Tag is assumed to be an HTML element only if it has been set to.
    """
    tag = Tag(source, basic_config)

    # Initialy, none tag are assumed as HTML
    assert tag.is_html is False

    # The tag need to be informed explicitely
    tag.is_html = True
    assert tag.is_html is True


@pytest.mark.parametrize("source, is_html, expected", [
    ("p", False, False),
    ("b", False, False,),
    ("caption", True, False),
    ("head", True, True),
    # TODO: Is '<script>' a real visible element ???
    ("script", True, False),
])
def test_tag_is_hidden(basic_config, source, is_html, expected) -> None:
    """
    Tag is assumed to be hidden if it is an hidden element such as <head>, this is not
    related to any CSS rule.
    """
    tag = Tag(source, basic_config)
    tag.is_html = is_html

    assert tag.is_hidden == expected


@pytest.mark.parametrize("source, is_html, expected", [
    ("p", False, False),
    ("pre", False, False,),
    ("div", True, False),
    ("pre", True, True),
])
def test_tag_tag_is_pre(basic_config, source, is_html, expected) -> None:
    """
    Tag is assumed to have preformatted text behavior if its HTML element is
    registered as so from W3C CSS specification.
    """
    tag = Tag(source, basic_config)
    tag.is_html = is_html

    assert tag._Tag__tag_is_pre(source) == expected


@pytest.mark.parametrize("source, is_html, expected", [
    ("foo", True, True),
    ("div", True, False),
    ("namespace:div", True, False),
    ("pre", True, False),
    ("blockquote", True, False),
    ("td", True, False),
    ("script", True, True),
    ("script", False, False),
    ("area", True, True),
    ("area", False, False),
])
def test_tag_is_space_sensitive(basic_config, source, is_html, expected) -> None:
    """
    Space sensitivity should be correctly determined from element nature and CSS flow.
    """
    tag = Tag(source, basic_config)
    tag.is_html = is_html

    assert tag.is_space_sensitive is expected


@pytest.mark.parametrize(
    (
        "current_name, current_is_html, current_type, current_kwargs, "
        "parent_name, parent_is_html, parent_type, parent_kwargs, "
        "expected"
    ),
    [
        (
            # The current tag name, is_html, type and kwargs to pass to Tag
            "div",
            False,
            None,
            {},
            # The same for the parent tag if any
            None,
            False,
            None,
            {},
            # Expected resulting output
            "",
        ),
        (
            "div",
            True,
            None,
            {},
            None,
            False,
            None,
            {},
            "<div>",
        ),
        (
            "div",
            True,
            None,
            {
                "attributes": [("class", "foo")],
            },
            None,
            False,
            None,
            {},
            "<div class=\"foo\">",
        ),
        (
            "div",
            False,
            "starttag_curly_perc",
            {
                "attributes": [("class=\"foo\"")],
                "properties": [],
            },
            None,
            False,
            None,
            {},
            "{% div class=\"foo\" %}",
        ),
        # TODO: Defining a Tag as both HTML and curly tag will lead to unexpected
        # behavior
        (
            "div",
            True,
            "starttag_curly_perc",
            {
                "attributes": [("class=\"foo\"")],
                "properties": [],
            },
            None,
            False,
            None,
            {},
            "<div c=\"l\">",
        ),
        (
            "div",
            True,
            "starttag_curly_perc",
            {
                "attributes": [("class", "foo"),],
                "properties": [],
            },
            None,
            False,
            None,
            {},
            "<div class=\"foo\">",
        ),
    ]
)
def test_tag_open_tag(
    basic_config, current_name, current_is_html, current_type, current_kwargs,
    parent_name, parent_is_html, parent_type, parent_kwargs, expected
) -> None:
    """
    Opening element tag should be correctly built from its nature and options.

    NOTE:
        Although ready, 'parent' argument is not really used here yet in practice since
        there is currently no real implementation differences with or without a parent.
    """
    # Create parent element tag if any from parameters
    if parent_name:
        parent_tag = Tag(parent_name, basic_config, **parent_kwargs)
        parent_tag.is_html = parent_is_html
        parent_tag.type = parent_type
        current_kwargs["parent"] = parent_tag

    current_tag = Tag(current_name, basic_config, **current_kwargs)
    current_tag.is_html = current_is_html
    current_tag.type = current_type

    assert current_tag.open_tag == expected


@pytest.mark.parametrize(
    (
        "current_name, current_is_html, current_type, current_kwargs, "
        "parent_name, parent_is_html, parent_type, parent_kwargs, "
        "expected"
    ),
    [
        (
            # The current tag name, is_html, type and kwargs to pass to Tag
            "div",
            False,
            None,
            {},
            # The same for the parent tag if any
            None,
            False,
            None,
            {},
            # Expected string
            "",
        ),
        (
            "div",
            True,
            None,
            {},
            None,
            False,
            None,
            {},
            "</div>",
        ),
        (
            "div",
            True,
            None,
            {
                "attributes": [("class", "foo")],
            },
            None,
            False,
            None,
            {},
            "</div>",
        ),
        # Defining a Tag as both HTML and curly, the HTML nature always wins against
        # curly types
        (
            "div",
            True,
            "endtag_curly_perc",
            {
                "attributes": [("class=\"foo\"")],
                "properties": [],
            },
            None,
            False,
            None,
            {},
            "</div>",
        ),
        (
            "div",
            True,
            "endtag_curly_perc",
            {
                "attributes": [("class", "foo"),],
                "properties": [],
            },
            None,
            False,
            None,
            {},
            "</div>",
        ),
        # TODO: It does not seems right to include attributes in ending tag
        (
            "div",
            False,
            "endtag_curly_perc",
            {
                "attributes": [("class=\"foo\"")],
                "properties": [],
            },
            None,
            False,
            None,
            {},
            "{% enddiv class=\"foo\" %}",
        ),
    ]
)
def test_tag_close_tag(
    basic_config, current_name, current_is_html, current_type, current_kwargs,
    parent_name, parent_is_html, parent_type, parent_kwargs, expected
) -> None:
    """
    Closing element tag should be correctly built from its nature and options.

    NOTE:
        Although ready, 'parent' argument is not really used yet in practice since
        there is currently no real differences with or without a parent
    """
    # Create parent element tag if any from parameters
    if parent_name:
        parent_tag = Tag(parent_name, basic_config, **parent_kwargs)
        parent_tag.is_html = parent_is_html
        parent_tag.type = parent_type
        current_kwargs["parent"] = parent_tag

    current_tag = Tag(current_name, basic_config, **current_kwargs)
    current_tag.is_html = current_is_html
    current_tag.type = current_type

    assert current_tag.close_tag == expected


@pytest.mark.parametrize("property_name, expected", [
    (
        "foo",
        {},
    ),
    (
        "flex",
        {},
    ),
    (
        "color",
        {
            "dialog": "black",
            ":link": "#0000EE",
            ":visited": "#551A8B",
            ":link:active": "#FF0000",
            ":visited:active": "#FF0000",
            "mark": "black",
            "hr": "gray"
        },
    ),
])
def test_tag_get_tag_style(basic_config, property_name, expected) -> None:
    """
    Method should returns all default values of HTML elements for given CSS property.

    Note than this method is stateless, it don't care about class arguments or instance
    attributes.
    """
    tag = Tag("div", basic_config)

    assert tag._Tag__get_tag_style(property_name) == expected


def test_tag_format_contents(basic_config) -> None:
    """
    Basic test for element children formatting that should be recursively formatted.
    """
    body = Tag("body", basic_config)
    body.is_html = True
    body.type = "open"

    heading = Tag("h1", basic_config)
    heading.is_html = True
    heading.type = "open"

    container = Tag("div", basic_config)
    container.is_html = True
    container.type = "open"

    paragraph = Tag("p", basic_config)
    paragraph.is_html = True
    paragraph.type = "open"

    horizontal_rule = Tag("hr", basic_config)
    horizontal_rule.is_html = True
    horizontal_rule.type = "void"

    container.children.append(paragraph)
    container.children.append(horizontal_rule)
    body.children.append(heading)
    body.children.append(container)

    output = body.format_contents(0)

    expected = (
        "<h1>\n"
        "</h1>\n"
        "<div>\n"
        "    <p>\n"
        "    </p>\n"
        "    <hr />    \n"
        "</div>\n"
    )

    assert output == expected


@pytest.mark.parametrize("source, is_html, type_attr, kwargs, expected", [
    (
        "div",
        False,
        "open",
        {},
        "\n\n"
    ),
    (
        "div",
        True,
        "open",
        {},
        "<div>\n</div>\n"
    ),
    (
        "div",
        True,
        "void",
        {},
        "<div>\n</div>\n"
    ),
    (
        "div",
        True,
        "void",
        {
            "attributes": [("class", "foo")],
        },
        "<div class=\"foo\">\n</div>\n"
    ),
    (
        "div",
        False,
        "starttag_curly_perc",
        {
            "properties": [],
        },
        "{% div %}\n"
    ),
    (
        "div",
        False,
        "endtag_curly_perc",
        {
            "properties": [],
        },
        "{% enddiv %}\n"
    ),
    (
        "div",
        False,
        "starttag_curly_perc",
        {
            "attributes": [("class=\"foo\"")],
            "properties": [],
        },
        "{% div class=\"foo\" %}\n"
    ),
    # TODO: As stated in 'test_tag_close_tag', attributes are propagated in closing tag
    (
        "div",
        False,
        "endtag_curly_perc",
        {
            "attributes": [("class=\"foo\"")],
            "properties": [],
        },
        "{% enddiv class=\"foo\" %}\n"
    ),
    # TODO: As stated in 'test_tag_open_tag' and 'test_tag_close_tag', the HTML nature
    # always wins against curly types
    (
        "div",
        True,
        "starttag_curly_perc",
        {},
        "<div></div>\n"
    ),
    # TODO: Weird behavior when type is incorrect but it's not clear what it should be
    # instead
    (
        "div",
        True,
        None,
        {},
        "</div>\n"
    ),
])
def test_tag_format(
    basic_config, source, is_html, type_attr, kwargs, expected
) -> None:
    """
    TODO: To. Do.

    NOTE: Tag suffers of too many required attributes settings to return correct
    formatting while it should be self sufficient to determine if it is an HTML element,
    hidden, type, etc.. or at least it should be enough to determine them from Tag
    keyword arguments.
    """
    tag = Tag(source, basic_config, **kwargs)
    tag.is_html = is_html
    tag.type = type_attr

    assert tag.format() == expected
