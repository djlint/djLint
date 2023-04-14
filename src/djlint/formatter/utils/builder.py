"""Build the new html from the old.

A lot of inspiration coming from an older bs4 release.

https://github.com/waylan/beautifulsoup/blob/480367ce8c8a4d1ada3012a95f0b5c2cce4cf497/bs4/__init__.py#L278
https://github.com/waylan/beautifulsoup/blob/master/COPYING.txt

All sections are a tag, even text blocks.

While text continues, it is added to the same block.
node type of text

"""
import re

from .parser import TemplateParser
from .tag import Tag
from .tools import (
    ALL_CLOSE_TEMPLATE_TYPES,
    ALL_OPEN_TEMPLATE_TYPES,
    DATA_TAG_NAME,
    HAS_TRAILING_BREAK,
    HAS_TRAILING_SPACE,
    ROOT_TAG_NAME,
    HAS_TRAILING_BREAKS
)


class TreeBuilder(Tag):
    """Tree Builder takes tags and assembles them into a hierarchy.

    Formatting of the entire html is achieved by iterating the tags and calling tag.format().
    """

    def __init__(self, config, text):
        self.text = text
        self.config = config
        self.parser = TemplateParser(config)
        self._reset()
        self._feed()

    def _reset(self):
        Tag.__init__(self, ROOT_TAG_NAME, self.config)
        self.hidden = 1
        self.parser.reset()

        self.tagStack = []  # children of current tag
        self.current_tag = None
        self._most_recent_tag = None
        self.current_data = []

        self.pushTag(self)

    def _feed(self):
        self.parser.tree = self
        self.parser.feed(self.text)
        self.parser.close()

        while self.current_tag.name != ROOT_TAG_NAME:
            self.popTag()

        self.endData()

    def endData(self):
        return

    def handle_starttag(self, tag):
        self.endData()

        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        # don't stack void tags
        if tag.is_void:
            self.pushTag(tag, stack=False)
        else:
            self.pushTag(tag)

        return tag

    def popTag(self):
        tag = self.tagStack.pop()

        if self.tagStack:
            self.current_tag = self.tagStack[-1]
        return self.current_tag

    def pushTag(self, tag, stack=True):
        if self.current_tag:
            self.current_tag.children.append(tag)

        if stack:
            self.tagStack.append(tag)

            self.current_tag = self.tagStack[-1]

    def _popToTag(self, name, namespace, type, inclusivePop=True):

        if name == ROOT_TAG_NAME:
            # don't leave me!
            return

        last_pop = None

        stack_size = len(self.tagStack)

        for i in range(stack_size - 1, 0, -1):
            t = self.tagStack[i]

            # we allow non standard html structure.
            # if any prev tags are an open template type tag and the current tag is an html tag
            # do not pop them.
            if (
                t.type in ALL_OPEN_TEMPLATE_TYPES
                and type not in ALL_CLOSE_TEMPLATE_TYPES
            ):
                # last_pop="add-parent" # print('breaking')
                break

            if (
                name == t.name and namespace == t.namespace
            ):  # and t.type = type... curly=curly, html=html etc
                if inclusivePop:
                    last_pop = self.popTag()
                break
            last_pop = self.popTag()

        return last_pop

    def handle_endtag(self, tag):
        """Html tags have no "contents" in the closing tag, so they are not tracked.

        However, we track the closing tag otherwise as their maybe attributes or properties we need to use.
        """
        self.endData()
        status = self._popToTag(tag.name, tag.namespace, tag.type)

        # this case is for closing html tags that are nested in template tags alone.
        # if status == "add-parent":
        tag.parent = self.current_tag

        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        # if tag.is_html is False:
        # but don't push to stack!
        self.pushTag(tag, stack=False)

    def handle_data(self, data):
        # add prop to previous tag
        if self._most_recent_tag:
            # only if most recent tag exists - required for files with leading junk
            if re.match(r"(\s*\n){2,}", data, re.M):
                self._most_recent_tag.raw_properties.append(HAS_TRAILING_BREAKS)

            if re.match(r"\s*\n", data, re.M):
                self._most_recent_tag.raw_properties.append(HAS_TRAILING_BREAK)

            if data.strip() == "":
                self._most_recent_tag.raw_properties.append(HAS_TRAILING_SPACE)
                return self._most_recent_tag

            elif re.match(r"\s", data, re.M):
                self._most_recent_tag.raw_properties.append(HAS_TRAILING_SPACE)

            if self._most_recent_tag.type == DATA_TAG_NAME:
                self._most_recent_tag.data.append(data)

                return self._most_recent_tag

        else:
            if data.strip() == "":
                return

        tag = Tag(DATA_TAG_NAME, self.config)
        tag.type = DATA_TAG_NAME
        tag.data.append(data)
        tag.parent = self.current_tag

        # add prop to current tag
        if re.search(r"(\s*\n){2,}$", data, re.M):

            tag.raw_properties.append(HAS_TRAILING_BREAKS)
        if len(data.rstrip()) != len(data):
            # print("adding trailing break")
            tag.raw_properties.append(HAS_TRAILING_SPACE)

        if self._most_recent_tag != self.current_tag:
            tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        self.pushTag(tag, stack=False)

        return tag

    def handle_statement(self, tag):
        self.endData()
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        self.pushTag(tag, stack=False)

    def handle_decl(self, tag):
        self.endData()
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        self.pushTag(tag)
        self.endData()
        self._popToTag(tag.name, tag.namespace, tag.type)

        return tag
