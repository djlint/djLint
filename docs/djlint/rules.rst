Linter Rules
============

Error Codes
~~~~~~~~~~~

+--------+----------------------------------------------------------------------+
| Code   | Meaning                                                              |
+========+======================================================================+
| E001   | Variables should be wrapped in a single whitespace. Ex: {{ this }}   |
+--------+----------------------------------------------------------------------+
| E002   | Double quotes should be used in tags. Ex {% extends "this.html" %}   |
+--------+----------------------------------------------------------------------+

Warning Codes
~~~~~~~~~~~~~

+--------+----------------------------------------------------------------+
| Code   | Meaning                                                        |
+========+================================================================+
| W003   | Endblock should have name. Ex: {% endblock body %}.            |
+--------+----------------------------------------------------------------+
| W004   | Status urls should follow {% static path/to/file %} pattern.   |
+--------+----------------------------------------------------------------+
| W005   | Html tag should have lang attribute.                           |
+--------+----------------------------------------------------------------+
| W006   | Img tag should have alt, height and width attributes.          |
+--------+----------------------------------------------------------------+
| W007   | <!DOCTYPE ... > should be present before the html tag.         |
+--------+----------------------------------------------------------------+
| W008   | Attributes should be double quoted.                            |
+--------+----------------------------------------------------------------+
| W009   | Tag names should be lowercase.                                 |
+--------+----------------------------------------------------------------+
| W010   | Attribute names should be lowercase.                           |
+--------+----------------------------------------------------------------+
| W011   | Attirbute values should be quoted.                             |
+--------+----------------------------------------------------------------+
| W012   | There should be no spaces around attribute =.                  |
+--------+----------------------------------------------------------------+
| W013   | Line is longer than 120 chars.                                 |
+--------+----------------------------------------------------------------+
| W014   | More than 2 blank lines.                                       |
+--------+----------------------------------------------------------------+
| W015   | Follow h tags with a blank line.                               |
+--------+----------------------------------------------------------------+
| W016   | Missging title tag in html.                                    |
+--------+----------------------------------------------------------------+
| W017   | Tag should be self closing.                                    |
+--------+----------------------------------------------------------------+
| W018   | Internal links should use the {% url ... %} pattern.           |
+--------+----------------------------------------------------------------+

Adding Rules
------------

A good rule consists of

-  Name
-  Code - Codes beginning with "E" signify error, and "W" warning.
-  Message - Message to display when error is found.
-  Flags - Regex flags. Defaults to re.DOTALL. ex: re.I|re.M
-  Patterns - regex expressions that will find the error.
