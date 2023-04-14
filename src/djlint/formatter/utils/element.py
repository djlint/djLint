from typing import Optional,List

from .tools import *

class Element:
    def __init__(self,
        type,
        config,
        elements:Optional[List] = [],
        data = ""
        ) -> None:

        self.elements = []
        self.type = type
        self.data = data or ""
        self.appender(elements)
        self.parent = None
        self.previous_element = None
        self.next_element = None

    def __iter__(self):
        for attr in self.elements:
            yield attr

    def appender(self, element):
        new = list_builder(element)

        for x, element in enumerate(new):
            if type(element) in [Group, Indent, Hardline,Softline,Script,Style,Line]:
                element.parent=self

                if x==0 and self.elements:
                    element.previous_element=self.elements[-1]
                    self.elements[-1].next_element=element
                if x > 0:
                    element.previous_element=new[x-1]
                if x+1 < len(new):
                    element.next_element=new[x+1]

        self.elements.extend(new)

    def __len__(self):
        # for x in self.elements:
        #     print("GROUP", type(x), len(x))
        if self.type == Group:
            return sum(len(x) for x in self.elements)

        if self.type == Fill:
            return len(" ".join(self.data))

        if self.type == Script:
            return len(self.data)

        if self.type == Style:
            return sum(len(x) for x in self.elements)
        if self.type == Indent:
            return sum(len(x) for x in self.elements)

        else:
            return len(self.data)

    def print(self):
        print(self.type, self.elements)
        out = ""

        out += self.data

        for child in self.elements:
            out += child.print()

        return out
