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

   ignore = "W013"

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
- handlebars

Usage:

.. code:: ini

   profile="django"
