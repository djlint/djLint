"""Build the new html from the old.

A lot of inspiration coming from an older bs4 release.

https://github.com/waylan/beautifulsoup/blob/480367ce8c8a4d1ada3012a95f0b5c2cce4cf497/bs4/__init__.py#L278
https://github.com/waylan/beautifulsoup/blob/master/COPYING.txt

"""
from .parser import TemplateParser
from .tag import Tag

class TreeBuilder(Tag):

    ROOT_TAG_NAME = "djlint"

    def __init__(self, config, text):
        self.text = text
        self.config = config
        self.parser = TemplateParser(config)
        self._reset()
        self._feed()

    def _reset(self):
        Tag.__init__(self,self.ROOT_TAG_NAME, self.config)
        self.hidden = 1
        self.parser.reset()

        self.tagStack = [] # children of current tag
        self.current_tag = None
        self._most_recent_tag = None
        self.current_data = []


        self.pushTag(self)

    def _feed(self):
        self.parser.tree = self
        self.parser.feed(self.text)
        self.parser.close()

        while self.current_tag.name != self.ROOT_TAG_NAME:
            self.popTag()

        self.endData()

    def endData(self):
        return

    def handle_starttag(self, tag):
        self.endData()
        #print("start")
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        self.pushTag(tag)

        return tag

    def popTag(self):
        tag = self.tagStack.pop()
        #print("pop: ", tag.name)

        if self.tagStack:
            self.current_tag = self.tagStack[-1]
        return self.current_tag

    def pushTag(self, tag):
        if self.current_tag:
            self.current_tag.children.append(tag)
        self.tagStack.append(tag)

        self.current_tag = self.tagStack[-1]

    def _popToTag(self, name, namespace, inclusivePop=True):

        if name == self.ROOT_TAG_NAME:
            # don't leave me!
            return

        last_pop = None

        stack_size = len(self.tagStack)

        for i in range(stack_size - 1, 0, -1):
            t = self.tagStack[i]
            if (name == t.name and namespace == t.namespace): # and t.type = type... curly=curly, html=html etc
                if inclusivePop:
                    last_pop = self.popTag()
                break
            last_pop = self.popTag()

        return last_pop

    def handle_endtag(self, tag):
        self.endData()
        self._popToTag(tag.name, tag.namespace)


    def handle_data(self):
        print("data")
