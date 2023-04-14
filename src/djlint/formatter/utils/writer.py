from typing import List

from .tools import *

from itertools import groupby

class Writer:
    def __init__(self, config, indent=0, current_length=0,force_hardbreak=False, force_linebreak=False, processed_length=0, group_length=0):
        self.config = config
        self.current_length = current_length
        self.indent = indent
        self.force_hardbreak=force_hardbreak
        self.processed_length=processed_length
        self.force_linebreak=force_linebreak
        self.group_length=group_length
        self.doc_list = []
        # print('setting force hardbreak', self.force_hardbreak)

    # def doc_pusher(self, stuff):
    #     if isinstance(stuff, str):
    #         if isinstance(self.doc_list[-1], str):
    #             self.doc_list[-1] = self.doc_list[-1] + stuff
    #             return

    #     self.doc_list.append(stuff)
    #     return



    def write(self, contents
       #, parent=None
       ):

        doc=""
        doc_list = []
        # split into chunks by hard breaks
        # then count the length of the chunk
        # if chunk length > max line,
        # then softline = hard break
        # else softline = no break

        current_contents = []
        # print(contents)

        for x, element in enumerate(contents):
            flattened = element.flatten(self.config)
            if isinstance(flattened,List):
                doc_list.extend(element.flatten(self.config))
            else:
                doc_list.append(element.flatten(self.config))

        print(doc_list)
        def get_len_before_break(doc_list):
            length = 0
            for x in doc_list:
                if isinstance(x,Hardline) or isinstance(x,Softline):
                    return length
                length += len(x)

            return length

        line_length = 0
        for x, element in enumerate(doc_list):

            len_before_break = get_len_before_break(doc_list[x:])
            indent=(element.indent  * (self.config.indent * self.config.indent_type)) if hasattr(element, "indent") else ""

            if isinstance(element,Hardline):
                line_length = 0

                if doc_list[x+1:] and type(doc_list[x+1]) in [Script,Style]:
                    indent=""
                doc += element.resolve(indent=indent )
            elif isinstance(element, Softline):
                if element.force_hardbreak:
                    line_length = 0

                doc += element.resolve(indent=indent)
            elif isinstance(element, Line):
                # print(element.nested, len(element.closest(Group)), line_length)
                # print(element.next_element, element.parent)
                hard_break = False
                line_length += len(element)
                # print(line_length)
                if line_length + len_before_break > self.config.max_line_length and element.nested is False:
                    hard_break=True

                if element.nested and len(element.closest(Group)) > self.config.max_line_length:
                    hard_break=True
                    # line_length=0
                # print("line!", len(element.resolve(hard_break=hard_break, indent=indent )))
                doc += element.resolve(hard_break=hard_break, indent=indent )
                # print(doc)

            elif isinstance(element,Fill):
                # print(len(doc.splitlines()[-1]) if doc else 0, len(indent))
                line_length += len(element)
                # print(len(doc.splitlines()[-1]) if doc else 0, len(element))
                doc += element.resolve(indent=indent,end=self.config.max_line_length, first_line_length=len(doc.splitlines()[-1]) if doc else 0)


            elif isinstance(element,Script):
                doc += element.resolve()

            elif isinstance(element,Style):
                doc += element.resolve()

            else:
                line_length += len(element)
                doc += element


        return doc


    def get_indent(self):
        return self.indent * (self.config.indent * self.config.indent_type)
