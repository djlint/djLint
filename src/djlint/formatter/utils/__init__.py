from .builder import TreeBuilder
from .parser import TemplateParser
from .tag import Tag
from .writer import Writer

"""
Need to define break types.

The tag.format() method should return a list of stuff:

["<html",">",hardbreak, "<p", ">", softbreak, "text", softbreak, "<p", ">"]

where the softbreaks will become real line breaks of the allowed line length is exceeded.
"""
