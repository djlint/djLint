Changelog
=========

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
