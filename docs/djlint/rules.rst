Linter Rules
============

Codes
~~~~~

+--------+-------------------------------------------------------------------------+
| Code   | Meaning                                                                 |
+========+=========================================================================+
| T001   | Variables should be wrapped in a single whitespace. Ex: {{ this }}      |
+--------+-------------------------------------------------------------------------+
| T002   | Double quotes should be used in tags. Ex {% extends "this.html" %}      |
+--------+-------------------------------------------------------------------------+
| T003   | Endblock should have name. Ex: {% endblock body %}.                     |
+--------+-------------------------------------------------------------------------+
| D004   | (Django) Static urls should follow {% static path/to/file %} pattern.   |
+--------+-------------------------------------------------------------------------+
| J004   | (Jinja) Static urls should follow {{ url_for('static'..) }} pattern.    |
+--------+-------------------------------------------------------------------------+
| H005   | Html tag should have lang attribute.                                    |
+--------+-------------------------------------------------------------------------+
| H006   | Img tag should have alt, height and width attributes.                   |
+--------+-------------------------------------------------------------------------+
| H007   | <!DOCTYPE ... > should be present before the html tag.                  |
+--------+-------------------------------------------------------------------------+
| H008   | Attributes should be double quoted.                                     |
+--------+-------------------------------------------------------------------------+
| H009   | Tag names should be lowercase.                                          |
+--------+-------------------------------------------------------------------------+
| H010   | Attribute names should be lowercase.                                    |
+--------+-------------------------------------------------------------------------+
| H011   | Attribute values should be quoted.                                      |
+--------+-------------------------------------------------------------------------+
| H012   | There should be no spaces around attribute =.                           |
+--------+-------------------------------------------------------------------------+
| H014   | More than 2 blank lines.                                                |
+--------+-------------------------------------------------------------------------+
| H015   | Follow h tags with a line break.                                        |
+--------+-------------------------------------------------------------------------+
| H016   | Missing title tag in html.                                              |
+--------+-------------------------------------------------------------------------+
| H017   | Tag should be self closing.                                             |
+--------+-------------------------------------------------------------------------+
| D018   | (Django) Internal links should use the {% url ... %} pattern.           |
+--------+-------------------------------------------------------------------------+
| J018   | (Jinja) Internal links should use the {% url ... %} pattern.            |
+--------+-------------------------------------------------------------------------+

Adding Rules
------------

A good rule consists of

-  Name
-  Code
-  Message - Message to display when error is found.
-  Flags - Regex flags. Defaults to re.DOTALL. ex: re.I|re.M
-  Patterns - regex expressions that will find the error.
-  Exclude - Optional list of profiles to exclude rule from.

Code Patterns
~~~~~~~~~~~~~

The first letter of a code follows the pattern:

- T: applies to template language
- H: applies to html
- D: applies specifically to Django
- J: applies specifically to Jinja
- N: applies specifically to Nunjucks
- M: applies specifically to Handlebars
