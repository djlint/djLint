{% raw %}

```bash
Usage: djlint [OPTIONS] SRC ...

  djLint · HTML template linter and formatter.

Options:
  --version                       Show the version and exit.
  --lsp                           Run as a language server over stdio, for
                                  editors.
  -e, --extension EXT             Extension of the files to look for in folders.
                                  [default: html]
  -i, --ignore CODES              Linter codes to skip, comma-separated, for
                                  example H014,H017.
  --reformat                      Format the files in place.
  --check                         Show what formatting would change, without
                                  changing the files.
  --stdin-filename PATH           Path that stands for stdin in messages,
                                  excludes and per-file ignores. [default: -]
  --indent N                      Spaces per indent level. [default: 4, or
                                  indent_size from .editorconfig]
  --quiet                         Do not print diffs, the progress bar or the
                                  summary.
  --profile NAME                  Template language: html, django, jinja,
                                  nunjucks, handlebars, liquid, golang, angular,
                                  tera, askama or all. It decides which linter
                                  rules run and how template syntax is
                                  formatted. [default: html]
  --require-pragma                Only format or lint files whose first line is
                                  a djlint:on comment.
  --lint                          Lint the files. This is the default when
                                  neither --reformat nor --check is given.
  --use-gitignore                 Also skip the paths that .gitignore lists.
  --allow-empty-input             Exit with 0 instead of 2 when the given paths
                                  match no files.
  --warn                          Exit with 0 instead of 1 when there are lint
                                  errors or files to reformat.
  --preserve-leading-space        Keep the leading spaces of text lines where
                                  possible.
  --preserve-blank-lines          Keep blank lines where possible.
  --preserve-class-newlines       Keep the line breaks in class attributes
                                  written across lines.
  --format-css                    Also format the contents of <style> tags, with
                                  css-beautify.
  --format-js                     Also format JavaScript and JSON in <script>
                                  tags, with js-beautify.
  --format-attribute-js-json      Also format JavaScript and JSON in attributes
                                  such as onclick and x-data.
  --format-attribute-js-json-pattern REGEX
                                  Regex for the names of the attributes to
                                  format as JavaScript or JSON. [default: on*
                                  event handlers and Alpine, Vue, Angular and
                                  Aurelia bindings]
  --format-attribute-js-json-min-props N
                                  Format an object only when it has at least
                                  this many properties. [default: 2]
  --configuration FILE            Global config file: a pyproject.toml,
                                  djlint.toml or .djlintrc. The project's own
                                  config file wins where both set an option.
  --prefer-configuration          Let the --configuration file win over the
                                  project's own config file.
  --rules FILE                    Custom linter rules, in the .djlint_rules.yaml
                                  format.
  --statistics                    After linting, print how many times each code
                                  was found.
  --include CODES                 Linter codes to turn on that are off by
                                  default, comma-separated, for example H017.
  --ignore-case                   Do not fix the case of known HTML tags.
  --ignore-blocks TAGS            Template blocks that do not indent their
                                  contents, comma-separated.
  --blank-line-after-tag TAGS     Template tags to follow with a blank line,
                                  comma-separated, for example load,extends.
  --blank-line-before-tag TAGS    Template tags to precede with a blank line,
                                  comma-separated, for example load,extends.
  --line-break-after-multiline-tag
                                  When a tag's attributes are spread over lines,
                                  start its content on a new line.
  --custom-blocks TAGS            Names of the custom template blocks to indent,
                                  comma-separated, for example toc.
  --custom-html TAGS              Names of the custom HTML tags to indent,
                                  comma-separated, for example mjml.
  --exclude PATHS                 Paths to skip, comma-separated, in place of
                                  the default list.
  --extend-exclude PATHS          Paths to skip on top of the default list,
                                  comma-separated.
  --linter-output-format FORMAT   Layout of each lint message, from {filename},
                                  {line}, {end}, {code}, {message} and {match}.
                                  [default: {code} {line} {message} {match}]
  --max-line-length N             Join tags onto one line only when the line
                                  fits within this length. [default: 120, or
                                  max_line_length from .editorconfig]
  --max-attribute-length N        Spread a tag's attributes over lines once they
                                  are longer than this. [default: 70]
  --format-attribute-template-tags
                                  Format template syntax inside tag attributes.
  --single-attribute-per-line     When an opening tag wraps, put each attribute
                                  on its own line.
  --per-file-ignores <PATTERN CODES>...
                                  Skip linter codes in the files whose path
                                  matches a regex. Can be repeated.
  --indent-css N                  Indent width inside <style> tags, for
                                  --format-css. [default: 4]
  --indent-js N                   Indent width inside <script> tags, for
                                  --format-js. [default: 4]
  --close-void-tags               Close void tags with a slash, so <img> becomes
                                  <img />.
  --no-line-after-yaml            Do not add a blank line after YAML front
                                  matter.
  --name-endblocks                Name the block in its {% endblock %} when the
                                  block spans lines.
  --sort-attributes               Sort attributes by name, with id first and
                                  class second.
  --sort-load-tags                Sort the libraries in {% load %} tags and drop
                                  repeated ones.
  --no-indent-inner-html          Do not indent <head> and <body> inside <html>.
  --no-function-formatting        Do not format the arguments of function calls
                                  inside {{ }}.
  --no-set-formatting             Do not format the contents of {% set %} tags.
  --keep-br-inline                Keep <br> on the line of the text it breaks.
  --no-entity-formatting          Do not rewrite entity references such as
                                  &copy; as the characters they name.
  --quote-style [double|single]   Quotes for strings inside template tags.
                                  [default: double]
  --max-blank-lines N             Keep at most this many blank lines in a row.
                                  [default: 0]
  --github-output / --no-github-output
                                  Print results as GitHub Actions annotations.
                                  On by default inside GitHub Actions.
  --sarif                         Print findings as a SARIF 2.1.0 JSON document,
                                  for GitHub code scanning and other tools.
  -h, --help                      Show this message and exit.
```

{% endraw %}
