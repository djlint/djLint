"""djlint Attribute Parser Overrides.

This class overrides the AttributeParser functions.

The output elements form AttributeParser are converted into Tag
elements that are then used in the builder.
"""
import re
from HtmlTemplateParser import AttributeParser as Atp

from .attribute_tag import AttributeTag as Tag
from .tools import *

class AttributeParser(Atp):
    """Overrides from AttributeParser."""

    def __init__(self, config, parent_tag):
        super(AttributeParser, self).__init__()
        self.config = config
        self.parent_tag = parent_tag
        self.tree = None
        self.tag = Tag("None", self.config, parent_tag)

    def handle_starttag_curly_perc(self, tag, attrs, props):
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = STARTTAG_CURLY_PERC

        # if tag is an acceptable open tag
        # print(self.tag.name)
        if self.tag.name in ['if', 'for', 'with']:
            self.tree.handle_starttag(self.tag)
        else:
            self.tree.handle_statement(self.tag)

    def handle_endtag_curly_perc(self, tag, attrs, props):
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
            properties=props,
        )
        self.tag.type = ENDTAG_CURLY_PERC

        self.tree.handle_endtag(self.tag)

    def handle_starttag_comment_curly_perc(self, tag, attrs, props):
        # django multi line comment {% comment %}{% endcomment %}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = STARTTAG_COMMENT_CURLY_PERC

        self.tree.handle_starttag(self.tag)

    def handle_endtag_comment_curly_perc(self, tag, attrs, props):
        # django multi line comment {% comment %}{% endcomment %}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            properties=props,
        )
        self.tag.type = ENDTAG_COMMENT_CURLY_PERC

        self.tree.handle_endtag(self.tag)

    def handle_comment_curly_hash(self, value):
        # django/jinja comment
        tag = Tag(
            value,
            self.config,
            self.parent_tag,
        )
        tag.type = COMMENT_CURLY_HASH

        self.handle_statement(tag, None)

    def handle_comment_curly_two_exclaim(self, value, props):
        # handlebars comment
        tag = Tag(
            value,
            self.config,
            self.parent_tag,
            properties=props,
        )
        tag.type = CURLY_TWO_EXCAIM

        self.handle_statement(tag, None)

    def handle_comment_at_star(self, value):
        # c# razor pages comment
        tag = Tag(
            value,
            self.config,
            self.parent_tag,
        )
        tag.type = COMMENT_AT_STAR

        self.handle_statement(tag, None)

    def handle_starttag_curly_two_hash(self, tag, attrs, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = STARTTAG_CURLY_TWO_HASH

        self.tree.handle_starttag(self.tag)

    def handle_endtag_curly_two_slash(self, tag, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            properties=props,
        )
        self.tag.type = ENDTAG_CURLY_TWO_SLASH

        self.tree.handle_endtag(self.tag)

    def handle_slash_curly_two(self, tag, attrs):
        # handlebars/mustache inline raw block
        tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
        )
        tag.type = SLASH_CURLY_TWO

        self.tree.handle_statement(tag)

    def handle_endtag_curly_four_slash(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
            properties=props,
        )
        self.tag.type = ENDTAG_CURLY_FOUR_SLASH
        self.tree.handle_endtag(self.tag)

    def handle_starttag_curly_four(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = STARTTAG_CURLY_FOUR

        self.tree.handle_starttag(self.tag)

    def handle_curly_three(self, value):
        # handlebars un-escaped html
        tag = Tag(
            value,
            self.config,
            self.parent_tag,
        )
        tag.type = CURLY_THREE

        self.tree.handle_statement(tag)

    def handle_curly_two(self, tag, attrs, props):
        tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            attributes=attrs,
            properties=props,
        )
        tag.type = CURLY_TWO
        self.tree.handle_statement(tag)

    def handle_name(self, name, props):
        """
        Any free text. If the attribute
        has a value following, there will be a property "has-value".
        """
        # print("name:", name)
        tag = Tag(
            DATA_ATTRIBUTE_NAME,
            self.config,
            self.parent_tag,
            properties=props,
        )
        tag.type = DATA_ATTRIBUTE_NAME
        tag.data.append(name)

        self.tree.handle_statement(tag)

    def handle_value_start(self):
        """
        This will be a quote character where an attribute value starts/ends.
        """
        if self.get_element_text() == '"':
            self.tag = Tag(DOUBLE_QUOTE, self.config, self.parent_tag)
            self.tag.type = DOUBLE_QUOTE

        else:
            self.tag = Tag(SINGLE_QUOTE, self.config, self.parent_tag)
            self.tag.type = SINGLE_QUOTE

        if self.tree.current_tag.type == self.tag.type:
            self.tree.handle_endtag(self.tag)
        else:
            self.tree.handle_starttag(self.tag)

    def handle_space(self, value):
        """
        Any whitespace inside an attribute.
        """
        tag = self.tree._most_recent_tag
        break_type=HAS_TRAILING_BREAK
        space_type=HAS_TRAILING_SPACE

        if (self.tree.current_tag != self.tree._most_recent_tag
            and self.tree.current_tag.children[-1].type in ALL_QUOTES):
            tag = self.tree.current_tag.children[-1]
            break_type=HAS_TRAILING_CLOSE_BREAK
            space_type=HAS_TRAILING_CLOSE_SPACE

        # print("here", self.tree._most_recent_tag, self.tree.current_tag, self.tree.current_tag.children[-1])
        tag.trailing_space.append(value)
        # print(value)
        if re.search(r"\n", value):
            tag.properties.append(break_type)
        tag.properties.append(space_type)
        # pass
