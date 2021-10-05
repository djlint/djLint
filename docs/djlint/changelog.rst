Changelog
=========

Next Release
------------
- Split ``alt`` requirement from H006 to H013
- Added optional custom rules file
- Added ``golang`` as profile option
- Fixed formatting of ignored blocks containing inline comments
- Added default text to ``--indent`` and ``-e`` options
- Update url rules to accept #

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
