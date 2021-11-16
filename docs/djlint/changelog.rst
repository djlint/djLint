Changelog
=========

next release
------------
- Bug fixes

0.6.0
-----
- Added rule T027 to check for unclosed in template syntax
- Added rule T028 to check for missing spaceless tags in attributes
- Added rule H029 to check for lowercase form method
- Ignored djagno blocktranslate tags that do not have "trimmed" from formatter
- Bug fixes

0.5.9a
------
- Added test support for python 3.10
- Added pre-commit hook

0.5.9
-----
- Added option ``--use-gitignore`` to extend the excludes
- Changed default exclude matching
- Fixed windows exclude paths
- Fixed formatting of ``{%...%}`` tags in attributes
- Fixed formatting for for loops and nested conditions in attributes

0.5.8
-----
- Added require_pragma option
- Updated DJ018 to catch ``data-src`` and ``action`` on inputs
- Fixed inline ignore syntax
- Added ``--lint`` option as placeholder for default usage
- Bug fixes

0.5.7
-----
- Bug fixes

0.5.6
-----
- Added rule H026 to find empty id and class tags
- Bug fixes

0.5.5
-----
- Consolidated settings and slimmed code
- Bug fixes

0.5.4
-----
- Added rule H020 to find empty tag pairs
- Added rule H021 to find inline styles
- Added rule H022 to find http links
- Added rule H023 to find entity references
- Added rule H024 to find type on scripts and styles
- Added rule H025 to check for orphan tags. Thanks to https://stackoverflow.com/a/1736801/10265880
- Improved attribute formatting
- Updated ``blank_line_after_tag`` option to add newline regardless of location
- Fixed django ``trans`` tag formatting
- Added formatting for inline styles
- Added formatting for template conditions inside attributes
- Added srcset as possible url location in linter rules
- Speed up formatting
- Special thanks to `jayvdb <https://github.com/jayvdb>`_

0.5.3
-----
- Change stdout for ``--reformat/check`` options to only print new html when using stdin as the input

0.5.2
-----
- Split ``alt`` requirement from H006 to H013
- Added optional custom rules file
- Added ``golang`` as profile option
- Fixed formatting of ignored blocks containing inline comments
- Added default text to ``--indent`` and ``-e`` options
- Update url rules to accept #
- Fixed file encoding on Windows OS
- Fix single line template tag regex
- Fix ``blank_line_after_tag`` for tags with leading space

0.5.1
-----
- Added rule H019
- Fixed bugs in DJ018 and H012

0.5.0
-----
- Fixed several regex matching bugs in linter rules
- Stopped linter from returning errors in ignored blocks
- Added option to ignore code block from linter/formatter with ``{% djlint:off %}...{% djlint:on %}`` tags

0.4.9
-----
- Fixed bug `#35 <https://github.com/Riverside-Healthcare/djLint/issues/35>`_

0.4.8
-----
- Fixed bug `#34 <https://github.com/Riverside-Healthcare/djLint/issues/34>`_

0.4.7
-----
- Moved ``source`` tag to single line tags

0.4.6
-----
- Fixed bug `#31 <https://github.com/Riverside-Healthcare/djLint/issues/31>`_

0.4.5
-----
- Added best practices to docs
- Add ``--profile`` option to set default linter/formatter rules
- Added linter rules for jinja url patterns

0.4.4
-----
- Change indent config from string to int. ``--indent 3``

0.4.3
-----
- Added cli option for indent spacing. ``--indent="  "``

0.4.2
-----
- Added support for additional whitespace after tags with ``blank_line_after_tag`` option

0.4.1
-----
- Added support for processing several files or folders at once

0.4.0
-----
- Fixed formatting of django ``{# ... #}`` tags
- Added indent support for figcaption, details and summary tags
- Added support for overriding or extending the list of excluded paths in  ``pyproject.toml``

0.3.9
-----
- Updated attribute handling

0.3.8
-----
- Added support for stdin

0.3.7
-----
- Fixed formatting on ``small``, ``dt``, and ``dd`` tags

0.3.6
-----
- Added formatter support for Nunjucks ``{%-`` opening blocks

0.3.5
-----
- Added support for more Django blocks
- Added support for custom blocks
- Added support for config in ``pyproject.toml``

0.3.4
-----
- Fixed Nunjucks spaceless tag ``-%}`` format

0.3.3
-----
- Allowed short ``div`` tags to be single line

0.3.2
-----
- Fixed Django comment formatting
- Ignored textarea from formatting

0.3.1
-----
- Updated attribute formatting regex
- Updated lint rule W010

0.3.0
-----
- Changed exit code to 1 if there were any formatting changes
- Added support for Jinja ``asset`` tags

0.2.9
-----
- Updated W018 regex
- Removed duplicate lint messages
- Updated E001 for Handlebars

0.2.8
-----
- Fixed progress bar error for old Click version
