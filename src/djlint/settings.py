"""Settings for reformater."""
# pylint: disable=C0301,C0103
# flake8: noqa

# default indentation
indent = "    "

# contents of tags will not be formatted, but tags will be formatted
ignored_block_opening = [r"<style" r"{\*", r"<\?php", r"<script"]

ignored_block_closing = [r"</style" r"\*}", r"\?>", r"</script"]


# contents of tags will not be formated and tags will not be formatted
ignored_group_opening = [r"<!--", r"[^\{]{#", r"<pre", r"<textarea"]

ignored_group_closing = [r"-->", r"#}", r"</pre", r"</textarea"]


# the contents of these tag blocks will be indented, then unindented
tag_indent = r"(?:\{\{\#)|\{% +?(if|for|block|else|spaceless|compress|addto|language|with|assets)|(?:{% verbatim %})|(?:<(?:html|head|body|div|a|nav|ul|ol|dl|li|table|thead|tbody|tr|th|td|blockquote|select|form|option|cache|optgroup|fieldset|legend|label|header|main|section|aside|footer|figure|video|span|p|g|svg|h\d|button|img|path|script|style|source))"
tag_unindent = r"(?:\{\{\/)|\{% end|(?:{% endverbatim %})|(?:</(?:html|head|body|div|a|nav|ul|ol|dl|li|table|thead|tbody|tr|th|td|blockquote|select|form|option|optgroup|fieldset|legend|label|header|cache|main|section|aside|footer|figure|video|span|p|g|svg|h\d|button|img|path|script|style|source))"

# these tags should be unindented and next line will be indented
tag_unindent_line = r"(?:\{% el)|(?:\{\{ *?(?:else|\^) *?\}\})"


# reduce empty lines greater than  x to 1 line
reduce_extralines_gt = 2

# if lines are longer than x
max_line_length = 120
format_long_attributes = True

# pattern used to find attributes in a tag
attribute_pattern = r"(?:{%[^}]*?%}(?:.*?{%[^}]*?%})+?)|(?:[^\s]+?=(?:\"{{.*?}}\"|\'{{.*?}}\'))|(?:[^\s]+?=(?:\".*?\"|\'.*?\'))|required|checked|[\w|-]+|[\w|-]+=[\w|-]+|{{.*?}}"
tag_pattern = r"(<\w+?[^>]*?)((?:\n[^>]+?)+?)(/?\>)"
ignored_attributes = [
    "data-json",
]

ignored_paths = [
    ".venv",
    "venv",
    ".tox",
    ".eggs",
    ".git",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".svn",
    ".bzr",
    "_build",
    "buck-out",
    "build",
    "dist",
    ".pants.d",
    ".direnv",
    "node_modules",
    "__pypackages__",
]

start_template_tags = r"{% ?(?:if|for|block|spaceless|compress|load|assets|addto|language|with|assets)[^}]+?%}"

break_template_tags = [
    r"{% ?(?:if|end|for|block|endblock|else|spaceless|compress|load|include|assets|addto|language|with|assets)[^}]+?%}",
]

unformated_html_tags = ["script"]

ignored_blocks = [
    r"<(script|style|pre|textarea).*?(?:%s).*?</(\1)>",
    r"<!--.*?(?:%s).*?-->",
    r"{\*.*?(?:%s).*?\*}",
    r"{#.*?(?:%s).*?#}",
    r"<\?php.*?(?:%s).*?\?>",
]

ignored_inline_blocks = [
    r"<!--.*?-->",
    r"{\*.*?\*}",
    r"{#.*?#}",
    r"<\?php.*?\?>",
]

single_line_html_tags = [
    "button",
    "a",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "td",
    "th",
    "strong",
    "em",
    "icon",
    "span",
    "title",
    "link",
    "path",
    "label",
    "div",
]

always_single_line_html_tags = ["link", "img", "meta"]

single_line_template_tags = ["if", "for", "block", "with"]

break_html_tags = [
    "a",
    "abbr",
    "acronym",
    "address",
    "applet",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "basefont",
    "bdi",
    "bdo",
    "big",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "center",
    "cite",
    "code",
    "col",
    "colgroup",
    "data",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "dialog",
    "dir",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "font",
    "footer",
    "form",
    "frame",
    "frameset",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hr",
    "html",
    "i",
    "iframe",
    "icon",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "legend",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "meta",
    "meter",
    "nav",
    "noframes",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "path",
    "param",
    "picture",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "section",
    "select",
    "small",
    "source",
    "span",
    "strike",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "svg",
    "table",
    "tbody",
    "td",
    "template",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "tt",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
]
