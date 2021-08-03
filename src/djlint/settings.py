"""Settings for reformater."""
# pylint: disable=C0301,C0103
# flake8: noqa

# default indentation
indent = "    "

break_html_tags = ["a", "abbr"]


# indicates tags whose contents should not be formatted
ignored_tag_opening = r"<script|<style|<!--|{\*|<\?php|<pre"

# indicates when to stop ignoring
ignored_tag_closing = r"</script|</style|-->|\*}|\?>|</pre"

# the contents of these tag blocks will be indented
tag_indent = r"(?:\{\{\#)|\{% +?(if|for|block|else|spaceless|compress|addto|language|with)|(?:{% verbatim %})|(?:<(?:html|head|body|div|a|nav|ul|ol|dl|li|table|thead|tbody|tr|th|td|blockquote|textarea|select|form|option|cache|optgroup|fieldset|legend|label|header|main|section|aside|footer|figure|video|span|p|g|svg|h\d|button|img|path|script|style|source))"

# this signals when tags should be unindented (see tags above)
tag_unindent = r"(?:\{\{\/)|\{% end|(?:{% endverbatim %})|(?:</(?:html|head|body|div|a|nav|ul|ol|dl|li|table|thead|tbody|tr|th|td|blockquote|select|form|option|optgroup|fieldset|legend|label|textarea|header|cache|main|section|aside|footer|figure|video|span|p|g|svg|h\d|button|img|path|script|style|source))"

# these tags should be unindented and next line will be indented
tag_unindent_line = r"(?:\{% el)|(?:\{\{ *?(?:else|\^) *?\}\})"

# these tags use raw code and should flatten to column 1
# tabs will be removed inside these tags! use spaces for spacing if needed!
# flatten starting with this tag...
tag_raw_flat_opening = r"[^\{]{#"

# ...stop flattening when you encounter this tag
tag_raw_flat_closing = r"#}[^\}]"

# reduce empty lines greater than  x to 1 line
reduce_extralines_gt = 2

# if lines are longer than x
max_line_length = 120
format_long_attributes = True

# pattern used to find attributes in a tag
attribute_pattern = r"(.+?=(?:\".*?\"|\'.*?\')|required|checked)\s*"
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

start_template_tags = (
    r"{% ?(?:if|for|block|spaceless|compress|load|assets|addto|language|with)[^}]+?%}"
)

break_template_tags = [
    r"{% ?(?:if|end|for|block|endblock|else|spaceless|compress|load|include|assets|addto|language|with)[^}]+?%}",
]

unformated_html_tags = ["script"]

ignored_blocks = [
    r"<(script|style|pre).*?(?:%s).*?</(\1)>",
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
    "textarea",
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
    "pre",
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
    "textarea",
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
