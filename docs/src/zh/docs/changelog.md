---
description: djLint Changelog. Find updates from recent releases and what feature you can expect on your next upgrade.
title: Changelog
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, changelog
---

{% raw %}

# Changelog

Changelog is now included in the [release](https://github.com/djlint/djLint/releases).

<!--## {{ "next_release" i18n }}-->

## 1.0.2

::: content

- Bug fixes [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- Bug fixes [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- Bug fixes [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- Bug fixes [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- Added `--warn` flag to return return errors as warnings.
  :::

## 0.7.5

::: content

- Bug fixes [#187](https://github.com/djlint/djLint/issues/187)
- Added better support for `yaml` front matter in template files
- Added rule T032 for [#123](https://github.com/djlint/djLint/issues/123)
- Added rule H033 for [#124](https://github.com/djlint/djLint/issues/124)
- Changed linter profiles to be inclusive vs exclusive for [#178](https://github.com/djlint/djLint/issues/178)
- Added alternate config file option `.djlintrc` for [#188](https://github.com/djlint/djLint/issues/188)
  :::

## 0.7.4

::: content

- Bug fixes [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- Bug fixes [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Dropped Py3.6 from `pyproject.toml`.
  :::

## 0.7.2

::: content

- Bug fixes [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- Bug fixes [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- Added config for custom HTML tags
- Bug fixes
  :::

## 0.6.9

::: content

- Added HTML and Angular profiles
- Allowed some entities in rule #H023
- Bug fixes
  :::

## 0.6.8

::: content

- Bug fixes
- Updated docs
  :::

## 0.6.7

::: content

- Added config option `format_attribute_template_tags` as opt-in for template tag formatting inside of attributes
- Added config option `linter_output_format` to customize linter message variable order
- Added rules H030 and H031 to check meta tags
  :::

## 0.6.6

::: content

- Big fixes
  :::

## 0.6.5

::: content

- Updated output paths to be relative to the project root
- Bug fixes
  :::

## 0.6.4

::: content

- Bug fixes
  :::

## 0.6.3

::: content

- Added support for django `blocktrans` tag
- Bug fixes
  :::

## 0.6.2

::: content

- Bug fixes
  :::

## 0.6.1

::: content

- Bug fixes
- Made rule T028 stricter with clearer message
  :::

## 0.6.0

::: content

- Added rule T027 to check for unclosed in template syntax
- Added rule T028 to check for missing spaceless tags in attributes
- Added rule H029 to check for lowercase form method
- Ignored django blocktranslate tags that do not have "trimmed" from formatter
- Bug fixes
  :::

## 0.5.9a

::: content

- Added test support for python 3.10
- Added pre-commit hook
  :::

## 0.5.9

::: content

- Added option `--use-gitignore` to extend the excludes
- Changed default exclude matching
- Fixed windows exclude paths
- Fixed formatting of `{%...%}` tags in attributes
- Fixed formatting for for loops and nested conditions in attributes
  :::

## 0.5.8

::: content

- Added require_pragma option
- Updated DJ018 to catch `data-src` and `action` on inputs
- Fixed inline ignore syntax
- Added `--lint` option as placeholder for default usage
- Bug fixes
  :::

## 0.5.7

::: content

- Bug fixes
  :::

## 0.5.6

::: content

- Added rule H026 to find empty id and class tags
- Bug fixes
  :::

## 0.5.5

::: content

- Consolidated settings and slimmed code
- Bug fixes
  :::

## 0.5.4

::: content

- Added rule H020 to find empty tag pairs
- Added rule H021 to find inline styles
- Added rule H022 to find http links
- Added rule H023 to find entity references
- Added rule H024 to find type on scripts and styles
- Added rule H025 to check for orphan tags. Thanks to https://stackoverflow.com/a/1736801/10265880
- Improved attribute formatting
- Updated `blank_line_after_tag` option to add newline regardless of location
- Fixed django `trans` tag formatting
- Added formatting for inline styles
- Added formatting for template conditions inside attributes
- Added srcset as possible url location in linter rules
- Speed up formatting
- Special thanks to [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- Change stdout for `--reformat/check` options to only print new html when using stdin as the input
  :::

## 0.5.2

::: content

- Split `alt` requirement from H006 to H013
- Added optional custom rules file
- Added `golang` as profile option
- Fixed formatting of ignored blocks containing inline comments
- Added default text to `--indent` and `-e` options
- Update url rules to accept #
- Fixed file encoding on Windows OS
- Fix single line template tag regex
- Fix `blank_line_after_tag` for tags with leading space
  :::

## 0.5.1

::: content

- Added rule H019
- Fixed bugs in DJ018 and H012
  :::

## 0.5.0

::: content

- Fixed several regex matching bugs in linter rules
- Stopped linter from returning errors in ignored blocks
- Added option to ignore code block from linter/formatter with `{% djlint:off %}...{% djlint:on %}` tags
  :::

## 0.4.9

::: content

- Fixed bug [#35](https://github.com/djlint/djLint/issues/35)
  :::

## 0.4.8

::: content

- Fixed bug [#34](https://github.com/djlint/djLint/issues/34)
  :::

## 0.4.7

::: content

- Moved `source` tag to single line tags
  :::

## 0.4.6

::: content

- Fixed bug [#31](https://github.com/djlint/djLint/issues/31)
  :::

## 0.4.5

::: content

- Added best practices to docs
- Add `--profile` option to set default linter/formatter rules
- Added linter rules for jinja url patterns
  :::

## 0.4.4

::: content

- Change indent config from string to int. `--indent 3`
  :::

## 0.4.3

::: content

- Added cli option for indent spacing. `--indent=" "`
  :::

## 0.4.2

::: content

- Added support for additional whitespace after tags with `blank_line_after_tag` option
  :::

## 0.4.1

::: content

- Added support for processing several files or folders at once
  :::

## 0.4.0

::: content

- Fixed formatting of django `{# ... #}` tags
- Added indent support for figcaption, details and summary tags
- Added support for overriding or extending the list of excluded paths in `pyproject.toml`
  :::

## 0.3.9

::: content

- Updated attribute handling
  :::

## 0.3.8

::: content

- Added support for stdin
  :::

## 0.3.7

::: content

- Fixed formatting on `small`, `dt`, and `dd` tags
  :::

## 0.3.6

::: content

- Added formatter support for Nunjucks `{%-` opening blocks
  :::

## 0.3.5

::: content

- Added support for more Django blocks
- Added support for custom blocks
- Added support for config in `pyproject.toml`
  :::

## 0.3.4

::: content

- Fixed Nunjucks spaceless tag `-%}` format
  :::

## 0.3.3

::: content

- Allowed short `div` tags to be single line
  :::

## 0.3.2

::: content

- Fixed Django comment formatting
- Ignored textarea from formatting
  :::

## 0.3.1

::: content

- Updated attribute formatting regex
- Updated lint rule W010
  :::

## 0.3.0

::: content

- Changed exit code to 1 if there were any formatting changes
- Added support for Jinja `asset` tags
  :::

## 0.2.9

::: content

- Updated W018 regex
- Removed duplicate lint messages
- Updated E001 for Handlebars
  :::

## 0.2.8

::: content

- Fixed progress bar error for old Click version
  :::

{% endraw %}
