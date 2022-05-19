import re
from typing import Dict, List, Optional, Tuple

from ..settings import Config

from .utils import Tag, TreeBuilder, TemplateParser

"""
options needed > no
empty-attributes-are-booleans >> required will either be "require =''" or just require
"""

"""
1. run html though the template parser
2. output is in a stack of tags
3. tag stack is formatted

We cannot format directly from the parser as me must know
future tags when formattings.
"""


def indent_html(rawcode: str, config: Config):

    ## pop front mater
    rawcode = rawcode.strip()

    front_matter = re.search(r"^---[\s\S]+?---\S*", rawcode)

    if front_matter:
        front_matter = front_matter.group()
        rawcode = rawcode.replace(front_matter, "")
        front_matter = front_matter.strip() + "\n"
    else:
        front_matter = ""

    def breakbefore(html):

        return bool(re.search(r"\n[ \t]*$", html, re.M))

    def spacebefore(html):

        return bool(re.search(r"[ ]*$", html, re.M))


    p = TreeBuilder(config, rawcode)


    #p = TemplateParser(config)

    #p.feed(rawcode)
    #output = p.close()
    output = p.format()

    output = front_matter + output

    return output

