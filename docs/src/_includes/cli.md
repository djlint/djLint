{% raw %}

```bash
Usage: djlint [OPTIONS] SRC ...

  djLint · HTML template linter and formatter.

Options:
  --version                       Show the version and exit.
  -e, --extension TEXT            File extension to check [default: html]
  -i, --ignore TEXT               Codes to ignore. ex: "H014,H017"
  --reformat                      Reformat the file(s).
  --check                         Check formatting on the file(s).
  --indent INTEGER                Indent spacing. [default: 4]
  --quiet                         Do not print diff when reformatting.
  --profile TEXT                  Enable defaults by template language. ops:
                                  django, jinja, nunjucks, handlebars, golang,
                                  angular, html [default: html]
  --require-pragma                Only format or lint files that starts with a
                                  comment with the text 'djlint:on'
  --lint                          Lint for common issues. [default option]
  --use-gitignore                 Use .gitignore file to extend excludes.
  --warn                          Return errors as warnings.
  --preserve-leading-space        Attempt to preserve leading space on text.
  --preserve-blank-lines          Attempt to preserve blank lines.
  --format-css                    Also format contents of <style> tags.
  --format-js                     Also format contents of <script> tags.
  --configuration FILE            Path to global configuration file in
                                  djlint.toml or .djlintrc format
  --statistics                    Count the number of occurrences of each
                                  error/warning code.
  --include TEXT                  Codes to include. ex: "H014,H017"
  --ignore-case                   Do not fix case on known html tags.
  --ignore-blocks TEXT            Comma list of template blocks to not indent.
  --blank-line-after-tag TEXT     Add an additional blank line after {% <tag>
                                  ... %} tag groups.
  --blank-line-before-tag TEXT    Add an additional blank line before {% <tag>
                                  ... %} tag groups.
  --line-break-after-multiline-tag
                                  Do not condense the content of multi-line
                                  tags into the line of the last attribute.
  --custom-blocks TEXT            Indent custom template blocks. For example
                                  {% toc %}...{% endtoc %}
  --custom-html TEXT              Indent custom HTML tags. For example <mjml>
  --exclude TEXT                  Override the default exclude paths.
  --extend-exclude TEXT           Add additional paths to the default exclude.
  --linter-output-format TEXT     Customize order of linter output message.
  --max-line-length INTEGER       Max line length. [default: 120]
  --max-attribute-length INTEGER  Max attribute length. [default: 70]
  --format-attribute-template-tags
                                  Attempt to format template syntax inside of
                                  tag attributes.
  --per-file-ignores <TEXT TEXT>...
                                  Ignore linter rules on a per-file basis.
  --indent-css INTEGER            Set CSS indent level.
  --indent-js INTEGER             Set JS indent level.
  --close-void-tags               Add closing mark on known void tags. Ex:
                                  <img> becomes <img />
  --no-line-after-yaml            Do not add a blank line after yaml front
                                  matter.
  --no-function-formatting        Do not attempt to format function contents.
  --no-set-formatting             Do not attempt to format set contents.
  --max-blank-lines INTEGER       Consolidate blank lines down to x lines.
                                  [default: 0]
  -h, --help                      Show this message and exit.
```

{% endraw %}
