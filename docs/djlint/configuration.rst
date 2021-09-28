Configuration
=============

Configuration is done through your projects `pyproject.toml` file. Command line args will always override any settings in `pyproject.toml`.

.. code:: toml

   [tool.djlint]
   <config options>

ignore
------

Ignore linter codes.

Usage:

.. code:: toml

   ignore = "W013"

extension
---------

Use to only find files with a specific extension.

Usage:

.. code:: toml

   extension = "html.dj"

custom_blocks
-------------

Use to indent custom code blocks. For example ``{% toc %}...{% endtoc %}``

Usage:

.. code:: toml

   custom_blocks = "toc,example"

indent
------

Use to change the code indentation. Default is 4 (four spaces).

Usage:

.. code:: toml

   indent = 3 # change indentation level

exclude
-------

Override the default exclude paths.

Usage:

.. code:: toml

   exclude = ".venv,venv,.tox,.eggs,..."


extend_exclude
--------------

Add additional paths to the default exclude.

Usage:

.. code:: toml

   extend_exclude = ".custom"

blank_line_after_tag
--------------------

Add an additional blank line after ``{% <tag> ... %}`` tag groups.

Usage:

.. code:: toml

   blank_line_after_tag = "load,extends,include"
