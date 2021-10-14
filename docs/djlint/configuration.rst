Configuration
=============

Configuration is done through your projects `pyproject.toml` file. Command line args will always override any settings in `pyproject.toml`.

.. code:: ini

   [tool.djlint]
   <config options>

ignore
------

Ignore linter codes.

Usage:

.. code:: ini

   ignore = "H014"

extension
---------

Use to only find files with a specific extension.

Usage:

.. code:: ini

   extension = "html.dj"

custom_blocks
-------------

Use to indent custom code blocks. For example ``{% toc %}...{% endtoc %}``

Usage:

.. code:: ini

   custom_blocks = "toc,example"

indent
------

Use to change the code indentation. Default is 4 (four spaces).

Usage:

.. code:: ini

   indent = 3 # change indentation level

exclude
-------

Override the default exclude paths.

Usage:

.. code:: ini

   exclude = ".venv,venv,.tox,.eggs,..."


extend_exclude
--------------

Add additional paths to the default exclude.

Usage:

.. code:: ini

   extend_exclude = ".custom"

blank_line_after_tag
--------------------

Add an additional blank line after ``{% <tag> ... %}`` tag groups.

Usage:

.. code:: ini

   blank_line_after_tag = "load,extends,include"

profile
-------

Set a default profile for the template language. The profile will disable linter rules that do not apply to your template language, and may also change reformatting. For example, in ``handlebars`` there are no spaces inside ``{{#if}}`` tags.

Options:

- django
- jinja
- nunjucks
- handlebars (for handlebars and mustache)
- golang

Usage:

.. code:: ini

   profile="django"

require_pragma
--------------

Only format or lint files that starts with a comment with only the text 'djlint:on'. The comment can be a HTML comment or a comment in the template language defined by the profile setting. If no profile is specified, a comment in any of the template languages is accepted.

Usage:

.. code:: ini

   require_pragma = true

.. code:: html

   <!-- djlint:on -->
   or
   {# djlint:on #}
   or
   {% comment %} djlint:on {% endcomment %}
   or
   {{ /* djlint:on */ }}
   or
   {{!-- djlint:on --}}

max_line_length
---------------

Formatter will attempt to put some html and template tags on a single line instead of wrapping them if the line length will not exceed this value.

Usage:

.. code:: ini

   max_line_length=120

max_attribute_length
--------------------

Formatter will attempt to wrap tag attributes if the attribute length exceeds this value.

Usage:

.. code:: ini

   max_attribute_length=10
